"""
Telegram authentication schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class TelegramUser(BaseModel):
    """User data from Telegram Web App."""
    
    id: int = Field(..., description="Telegram user ID")
    first_name: str = Field(..., description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    username: Optional[str] = Field(None, description="Telegram username")
    language_code: Optional[str] = Field("en", description="User's language code")


class TelegramAuthRequest(BaseModel):
    """Request payload for Telegram authentication."""
    
    init_data: str = Field(
        ...,
        description="Raw initData string from Telegram.WebApp.initData",
        min_length=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "init_data": "user=%7B%22id%22%3A123456%7D&auth_date=1234567890&hash=abc123..."
            }
        }
