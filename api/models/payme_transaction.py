from datetime import datetime
from uuid import uuid4
from sqlalchemy import String, Integer, BigInteger, JSON, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base

class PaymeTransaction(Base):
    """
    Model to track Payme.uz payment transactions (Merchant API).
    """
    __tablename__ = "payme_transactions"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Payme External ID
    paycom_transaction_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    
    # Timestamps (BigInt as per Payme spec)
    paycom_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
    paycom_time_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    create_time: Mapped[int] = mapped_column(BigInteger, default=lambda: int(datetime.now().timestamp() * 1000), nullable=False)
    perform_time: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    cancel_time: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    
    # Amount in TIYINS
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    
    # User linkage (account[order_id] maps to this)
    # Using String to store UUID because Payme passes params as strings/numbers
    order_id: Mapped[str] = mapped_column(String, index=True, nullable=False) 
    
    # State: 1=Created, 2=Completed, -1=Cancelled, -2=Revoked
    state: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Cancellation reason
    reason: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Receivers (for split payments, optional)
    receivers: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # We can add a relationship if order_id is strictly a user_id
    # but to be flexible (maybe order_id is plan_id:user_id), we keep it loose or add property
