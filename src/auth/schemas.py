import uuid
from datetime import datetime
from pydantic import EmailStr, BaseModel, Field


class UserBaseModel(BaseModel):
    email: EmailStr
    # phone_number: str
    full_name: str


class UserCreateModel(UserBaseModel):
    password: str


class UserLoginModel(BaseModel):
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=8, max_length=128)


class UserResponseModel(UserBaseModel):
    id: uuid.UUID
    is_verified: bool
    created_at: datetime
