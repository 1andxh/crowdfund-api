from datetime import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.db.base import Base

if TYPE_CHECKING:
    from src.campaigns.models import Campaign
    from src.contributions.models import Contribution


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
    contributions: Mapped[list["Contribution"]] = relationship(
        "Contribution", back_populates="user"
    )
