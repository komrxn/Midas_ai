from pydantic import BaseModel
from typing import Optional

class PaymentLinkRequest(BaseModel):
    plan_id: str # 'monthly', 'quarterly', 'annual', 'trial'
    provider: str = "click" # 'click', 'payme'

class PaymentLinkResponse(BaseModel):
    url: str
