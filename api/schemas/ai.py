from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from uuid import UUID


class AIParseRequest(BaseModel):
    """Request for AI transaction parsing."""
    text: Optional[str] = Field(None, description="Text message to parse")
    # File handling will be done via multipart/form-data for voice/images


class AIParseResponse(BaseModel):
    """Response from AI transaction parsing."""
    type: str  # income or expense
    amount: Decimal
    currency: str
    description: str
    suggested_category_id: Optional[UUID] = None
    suggested_category_name: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    ai_parsed_data: dict
    auto_created: bool = False  # True if transaction was auto-created


class CategorySuggestion(BaseModel):
    """Category suggestion for a description."""
    category_id: UUID
    category_name: str
    category_slug: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class CategorySuggestRequest(BaseModel):
    """Request for category suggestion."""
    description: str = Field(..., min_length=1)
    transaction_type: str = Field(..., pattern="^(income|expense)$")


class CategorySuggestResponse(BaseModel):
    """Response with category suggestions."""
    suggestions: list[CategorySuggestion]
    best_match: Optional[CategorySuggestion] = None
