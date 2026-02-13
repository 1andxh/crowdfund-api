from sqlalchemy import String, NUMERIC
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from enum import Enum
from decimal import Decimal


class Beneficiary(str, Enum):
    CHARITY = "charity"
    INDIVIDUAL = "individual"


class Status(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"


class Currency(str, Enum):
    GHS = "GHS"
    NGN = "NGN"
    USD = "USD"


class Campaign(SQLModel, table=True):
    __tablename__: str = "campaign"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, primary_key=True, unique=True, nullable=False, default=uuid.uuid4
        ),
    )
    # creator_id: str  # this part will reference the user field
    title: str = Field(sa_column=Column(String(50), nullable=False))
    description: str = Field(sa_column=Column(String(255), nullable=False))
    beneficiary_name: str
    beneficiary_type: str = Field(
        sa_column=Column(
            pg.VARCHAR, nullable=True, server_default=Beneficiary.INDIVIDUAL.value
        )
    )
    target_amount: Decimal = Field(sa_column=Column(NUMERIC(10, 2), nullable=False))
    current_amount: Decimal = Field(
        sa_column=Column(NUMERIC(10, 2), server_default="0.00")
    )
    # donation_count: int
    currency: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default=Currency.GHS.value)
    )
    status: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default=Status.ACTIVE.value)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    deadline: str = Field(
        sa_column=Column(String(50), nullable=True, server_default="xxxx-xx-xx")
    )

    def __repr__(self) -> str:
        return f"-> {self.title}  added!"


# - id
# - creator_id (who created it? links to USERS)
# - title
# - description
# - goal_amount (in GHS)
# - current_amount (total contributed so far)
# - deadline (when does campaign end?)
# - status (ACTIVE, SUCCESSFUL, FAILED, EXTENDED?)
# - created_at
# - updated_at
