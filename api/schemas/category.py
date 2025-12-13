from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern="^(expense|income|debt)$")
    icon: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=20)


class CategoryCreate(CategoryBase):
    """Schema for creating a custom category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    icon: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=20)


class CategoryResponse(CategoryBase):
    """Schema for category response."""
    id: UUID
    user_id: Optional[UUID]
    is_default: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CategoryWithStats(CategoryResponse):
    """Category with transaction statistics."""
    transaction_count: int = 0
    total_amount: float = 0.0
