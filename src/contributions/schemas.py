import uuid
from pydantic import BaseModel, EmailStr
from decimal import Decimal
from datetime import datetime


class Contribution(BaseModel):
    id: uuid.UUID
    # campaign_id: # foreign key
    amount: Decimal
    currency: str
    donor_name: str | None
    donor_email: EmailStr
    is_anonymous: bool
    payment_status: str
    payment_id: int
    date: datetime
