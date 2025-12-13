from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import uuid4
from sqlalchemy import String, Numeric, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base


class Debt(Base):
    """Debt model for tracking loans (I owe / owe me)."""
    
    __tablename__ = "debts"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Debt details
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # i_owe, owe_me
    person_name: Mapped[str] = mapped_column(String(200), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="uzs")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Status tracking
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")  # open, overdue, settled
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    settled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="debts")
    
    def __repr__(self) -> str:
        return f"<Debt(id={self.id}, type={self.type}, person={self.person_name}, amount={self.amount})>"
