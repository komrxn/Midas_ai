from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, UUID
from uuid import uuid4
from ..database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False)
