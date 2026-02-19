from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Enum as SAEnum,
    Numeric,
    Text,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from src.db.base import Base
import enum
from .user_model import User


class CampaignStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    creator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    story: Mapped[str | None] = mapped_column(Text, nullable=True)
    goal_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    current_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[CampaignStatus] = mapped_column(
        SAEnum(CampaignStatus, name="campaign_status_enum", create_type=True),
        default=CampaignStatus.ACTIVE,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    creator: Mapped["User"] = relationship("User", back_populates="campaigns")
