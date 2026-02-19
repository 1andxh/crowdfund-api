from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Enum as SAEnum,
    Numeric,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from datetime import datetime
from src.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.campaigns.models import Campaign
    from src.auth.models import User
    from src.contributions.models import Contribution


class PayoutStatus(str, enum.Enum):
    PENDING = "PENDING"  # Payout created, email not sent yet
    NOTIFIED = "NOTIFIED"


class Payout(Base):
    __tablename__ = "payouts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    campaign_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("campaigns.id"), nullable=False, unique=True
    )
    amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    status: Mapped[PayoutStatus] = mapped_column(
        SAEnum(PayoutStatus, name="payout_status_enum", native_enum=False),
        default=PayoutStatus.PENDING,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    notified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # relationship
    campaign: Mapped["Campaign"] = relationship(
        "Campaign", back_populates="payout", uselist=False
    )
