from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class DebtBase(BaseModel):
    """Base debt schema."""
    type: str = Field(..., pattern="^(i_owe|owe_me)$")
    person_name: str = Field(..., min_length=1, max_length=200)
    amount: Decimal = Field(..., gt=0)
    currency: str = Field(default="uzs", max_length=3)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[date] = None


class DebtCreate(DebtBase):
    """Schema for creating a debt."""
    pass


class DebtUpdate(BaseModel):
    """Schema for updating a debt."""
    person_name: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[Decimal] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, pattern="^(open|overdue|settled)$")
    due_date: Optional[date] = None
    settled_at: Optional[datetime] = None


class DebtResponse(DebtBase):
    """Schema for debt response."""
    id: UUID
    user_id: UUID
    status: str
    settled_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DebtSummary(BaseModel):
    """Debt summary statistics."""
    i_owe_total: Decimal = Decimal("0")
    owe_me_total: Decimal = Decimal("0")
    i_owe_count: int = 0
    owe_me_count: int = 0
