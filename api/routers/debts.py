from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from ..database import get_db
from ..models.debt import Debt
from ..models.user import User
from ..schemas.debt import DebtCreate, DebtUpdate, DebtResponse, DebtSummary
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/debts", tags=["debts"])


@router.post("", response_model=DebtResponse, status_code=201)
async def create_debt(
    debt_data: DebtCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new debt."""
    debt = Debt(
        user_id=current_user.id,
        **debt_data.model_dump()
    )
    
    db.add(debt)
    await db.commit()
    await db.refresh(debt)
    
    return debt


@router.get("", response_model=list[DebtResponse])
async def list_debts(
    type: Optional[str] = Query(None, pattern="^(i_owe|owe_me)$"),
    status: Optional[str] = Query(None, pattern="^(open|overdue|settled)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all debts for current user with optional filters."""
    query = select(Debt).where(Debt.user_id == current_user.id)
    
    if type:
        query = query.where(Debt.type == type)
    
    if status:
        query = query.where(Debt.status == status)
    
    # Check for overdue debts
    today = date.today()
    
    query = query.order_by(Debt.created_at.desc())
    
    result = await db.execute(query)
    debts = result.scalars().all()
    
    # Update overdue status
    for debt in debts:
        if debt.status == "open" and debt.due_date and debt.due_date < today:
            debt.status = "overdue"
    
    await db.commit()
    
    return debts


@router.get("/balance", response_model=DebtSummary)
async def get_debt_balance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get debt balance summary."""
    # I owe
    i_owe_query = select(
        func.coalesce(func.sum(Debt.amount), 0).label("total"),
        func.count(Debt.id).label("count")
    ).where(
        and_(
            Debt.user_id == current_user.id,
            Debt.type == "i_owe",
            Debt.status != "settled"
        )
    )
    
    i_owe_result = await db.execute(i_owe_query)
    i_owe_row = i_owe_result.first()
    
    # Owe me
    owe_me_query = select(
        func.coalesce(func.sum(Debt.amount), 0).label("total"),
        func.count(Debt.id).label("count")
    ).where(
        and_(
            Debt.user_id == current_user.id,
            Debt.type == "owe_me",
            Debt.status != "settled"
        )
    )
    
    owe_me_result = await db.execute(owe_me_query)
    owe_me_row = owe_me_result.first()
    
    return DebtSummary(
        i_owe_total=Decimal(str(i_owe_row.total)) if i_owe_row else Decimal("0"),
        owe_me_total=Decimal(str(owe_me_row.total)) if owe_me_row else Decimal("0"),
        i_owe_count=i_owe_row.count if i_owe_row else 0,
        owe_me_count=owe_me_row.count if owe_me_row else 0
    )


@router.get("/{debt_id}", response_model=DebtResponse)
async def get_debt(
    debt_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific debt by ID."""
    result = await db.execute(
        select(Debt).where(
            and_(
                Debt.id == debt_id,
                Debt.user_id == current_user.id
            )
        )
    )
    debt = result.scalar_one_or_none()
    
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    return debt


@router.put("/{debt_id}", response_model=DebtResponse)
async def update_debt(
    debt_id: UUID,
    debt_data: DebtUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a debt."""
    result = await db.execute(
        select(Debt).where(
            and_(
                Debt.id == debt_id,
                Debt.user_id == current_user.id
            )
        )
    )
    debt = result.scalar_one_or_none()
    
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    # Update fields
    update_data = debt_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(debt, field, value)
    
    await db.commit()
    await db.refresh(debt)
    
    return debt


@router.post("/{debt_id}/mark-paid", response_model=DebtResponse)
async def mark_debt_as_paid(
    debt_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark a debt as settled/paid."""
    result = await db.execute(
        select(Debt).where(
            and_(
                Debt.id == debt_id,
                Debt.user_id == current_user.id
            )
        )
    )
    debt = result.scalar_one_or_none()
    
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    debt.status = "settled"
    debt.settled_at = datetime.now()
    
    await db.commit()
    await db.refresh(debt)
    
    return debt


@router.delete("/{debt_id}", status_code=204)
async def delete_debt(
    debt_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a debt."""
    result = await db.execute(
        select(Debt).where(
            and_(
                Debt.id == debt_id,
                Debt.user_id == current_user.id
            )
        )
    )
    debt = result.scalar_one_or_none()
    
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    await db.delete(debt)
    await db.commit()
    
    return None
