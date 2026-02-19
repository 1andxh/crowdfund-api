from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from src.db.base import Base
from .campaign_model import Campaign


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String)

    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)

    password_hash: Mapped[str] = mapped_column(String)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # relationship
    campaigns: Mapped[list["Campaign"]] = relationship(
        "Campaign", back_populates="creator"
    )
