from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ClickRequest(BaseModel):
    """
    Request model for Click.uz callbacks (Prepare/Complete).
    Typically sent as form data, checking validation.
    """
    click_trans_id: int
    service_id: int
    click_paydoc_id: int
    merchant_trans_id: str
    amount: float
    action: int
    error: int
    error_note: str
    sign_time: str
    sign_string: str
    merchant_prepare_id: Optional[str] = None # For Complete requests


class ClickResponse(BaseModel):
    """
    Standard response format for Click.uz
    """
    click_trans_id: int
    merchant_trans_id: str
    merchant_prepare_id: Optional[str] = None
    merchant_confirm_id: Optional[str] = None
    error: int
    error_note: str

class PaymentLinkRequest(BaseModel):
    plan_id: str # 'monthly', 'annual', 'trial'

class PaymentLinkResponse(BaseModel):
    url: str
