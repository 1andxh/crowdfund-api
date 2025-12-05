from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import String
import uuid
from datetime import datetime
from enum import Enum
from pydantic import EmailStr


class Role(str, Enum):
    pass


class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, primary_key=True, unique=True, nullable=False, default=uuid.uuid4
        )
    )
    email: EmailStr = Field(sa_column=Column(String(128), nullable=False, index=True))
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    password_hash: str = Field(
        sa_column=Column(String(128), nullable=False), exclude=True
    )
    is_verified: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self) -> str:
        return f"{self.email}"
