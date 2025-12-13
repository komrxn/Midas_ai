from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case

from ..database import get_db
from ..models.user import User
from ..models.transaction import Transaction
from ..models.category import Category
from ..schemas.analytics import (
    BalanceResponse,
    CategoryBreakdownResponse,
    CategoryBreakdownItem,
    TimeSeriesResponse,
    TimeSeriesDataPoint,
    AnalyticsSummaryResponse,
    TrendMetric
)
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/balance", response_model=BalanceResponse)
async def get_balance(
    period: str = Query("month", pattern="^(day|week|month|year|all)$"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get balance (income - expense) for a period.
    
    - **period**: Preset period (day/week/month/year/all)
    - **start_date**: Custom start date (overrides period)
    - **end_date**: Custom end date (overrides period)
    """
    
    # Determine date range
    if start_date and end_date:
        pass  # Use custom range
    else:
        end_date = datetime.now()
        if period == "day":
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            start_date = end_date - timedelta(days=7)
        elif period == "month":
            start_date = end_date - timedelta(days=30)
        elif period == "year":
            start_date = end_date - timedelta(days=365)
        else:  # all
            start_date = datetime(2020, 1, 1)
    
    # Get income and expense totals
    result = await db.execute(
        select(
            func.sum(case((Transaction.type == 'income', Transaction.amount), else_=0)).label('income'),
            func.sum(case((Transaction.type == 'expense', Transaction.amount), else_=0)).label('expense')
        ).where(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )
        )
    )
    row = result.one()
    
    total_income = Decimal(row.income or 0)
    total_expense = Decimal(row.expense or 0)
    balance = total_income - total_expense
    
    period_label = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    
    return BalanceResponse(
        balance=balance,
        total_income=total_income,
        total_expense=total_expense,
        currency=current_user.default_currency,
        period_label=period_label
    )


@router.get("/categories", response_model=CategoryBreakdownResponse)
async def get_category_breakdown(
    period: str = Query("month", pattern="^(day|week|month|year|all)$"),
    type: str = Query("expense", pattern="^(income|expense)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get category breakdown for pie chart.
    
    - **period**: Time period
    - **type**: Transaction type (income/expense)
    """
    
    # Determine date range
    end_date = datetime.now()
    if period == "day":
        start_date = end_date - timedelta(days=1)
    elif period == "week":
        start_date = end_date - timedelta(days=7)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    elif period == "year":
        start_date = end_date - timedelta(days=365)
    else:
        start_date = datetime(2020, 1, 1)
    
    # Aggregate by category
    result = await db.execute(
        select(
            Category.id,
            Category.name,
            Category.slug,
            Category.color,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        ).select_from(Transaction).join(
            Category, Transaction.category_id == Category.id, isouter=True
        ).where(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.type == type,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )
        ).group_by(Category.id, Category.name, Category.slug, Category.color)
    )
    
    rows = result.all()
    total_amount = sum(Decimal(row.total or 0) for row in rows)
    
    categories = []
    for row in rows:
        amount = Decimal(row.total or 0)
        percentage = float(amount / total_amount * 100) if total_amount > 0 else 0.0
        
        categories.append(CategoryBreakdownItem(
            category_id=str(row.id) if row.id else None,
            category_name=row.name or "Без категории",
            category_slug=row.slug or "uncategorized",
            amount=amount,
            percentage=round(percentage, 1),
            transaction_count=row.count,
            color=row.color
        ))
    
    # Sort by amount descending
    categories.sort(key=lambda x: x.amount, reverse=True)
    
    return CategoryBreakdownResponse(
        categories=categories,
        total=total_amount,
        currency=current_user.default_currency
    )


@router.get("/trends", response_model=TimeSeriesResponse)
async def get_trends(
    period: str = Query("month", pattern="^(month|year)$"),
    granularity: str = Query("day", pattern="^(day|week|month)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get time-series data for trend charts.
    
    - **period**: Data range (month/year)
    - **granularity**: Data point interval (day/week/month)
    """
    
    # Determine date range
    end_date = datetime.now()
    if period == "month":
        start_date = end_date - timedelta(days=30)
    else:  # year
        start_date = end_date - timedelta(days=365)
    
    # Get all transactions in range
    result = await db.execute(
        select(Transaction).where(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )
        ).order_by(Transaction.transaction_date)
    )
    transactions = result.scalars().all()
    
    # Group by time period
    data_points = {}
    current = start_date
    
    while current <= end_date:
        if granularity == "day":
            key = current.strftime("%Y-%m-%d")
            next_period = current + timedelta(days=1)
        elif granularity == "week":
            key = current.strftime("%Y-W%W")
            next_period = current + timedelta(days=7)
        else:  # month
            key = current.strftime("%Y-%m")
            next_period = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        data_points[key] = {"income": Decimal("0"), "expense": Decimal("0")}
        current = next_period
    
    # Aggregate transactions
    for tx in transactions:
        if granularity == "day":
            key = tx.transaction_date.strftime("%Y-%m-%d")
        elif granularity == "week":
            key = tx.transaction_date.strftime("%Y-W%W")
        else:
            key = tx.transaction_date.strftime("%Y-%m")
        
        if key in data_points:
            if tx.type == "income":
                data_points[key]["income"] += tx.amount
            else:
                data_points[key]["expense"] += tx.amount
    
    # Build response
    series_data = []
    running_balance = Decimal("0")
    
    for date_key in sorted(data_points.keys()):
        income = data_points[date_key]["income"]
        expense = data_points[date_key]["expense"]
        running_balance += (income - expense)
        
        series_data.append(TimeSeriesDataPoint(
            date=date_key,
            income=income,
            expense=expense,
            balance=running_balance
        ))
    
    return TimeSeriesResponse(
        data=series_data,
        granularity=granularity,
        currency=current_user.default_currency
    )


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get combined analytics summary (balance + category breakdown + trends).
    
    This is a convenience endpoint for dashboard views.
    """
    
    # Get balance for current month
    balance = await get_balance("month", None, None, current_user, db)
    
    # Get category breakdown
    categories = await get_category_breakdown("month", "expense", current_user, db)
    
    # Get trends
    trends = await get_trends("month", "day", current_user, db)
    
    return AnalyticsSummaryResponse(
        balance=balance,
        category_breakdown=categories,
        trends=trends
    )
