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
from datetime import datetime
from src.db.base import Base
from src.auth import User
from src.campaigns import Campaign


class Contribution(Base):
    __tablename__ = "contributions"
