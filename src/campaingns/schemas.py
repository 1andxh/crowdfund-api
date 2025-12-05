import uuid
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class Campaign(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    beneficiary_name: str
    beneficiary_type: str
    target_amount: Decimal
    current_amount: Decimal
    currency: str
    status: str
    created_at: datetime
    updated_at: datetime
    deadline: str


class CampaignCreateModel(BaseModel):
    title: str
    description: str
    beneficiary_name: str
    beneficiary_type: str
    target_amount: Decimal
    current_amount: Decimal | None
    currency: str
    deadline: str | None


class CampaignUpdateModel(BaseModel):
    title: str | None
    description: str | None
    beneficiary_name: str | None
    beneficiary_type: str | None
    target_amount: Decimal
    current_amount: Decimal
    currency: str | None
    deadline: str | None
