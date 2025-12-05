from .models import User
from .schemas import UserCreateModel
from .utils import hash_password
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists
from pydantic import EmailStr
from typing import Any
import logging

# logger = logging.getLogger(__name__)


class UserService:
    async def get_user_by_email(self, email: EmailStr, session: AsyncSession):
        # statement = select(exists(select(User).where(User.email == email)))
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        # logger.info(f"{(type(user))}")
        return user

    # async def check_user_exists(self, email: EmailStr, session: AsyncSession) -> bool:
    #     user = await self.get_user_by_email(email, session)
    #     # if not user:
    #     #     return False
    #     # return True
    #     return bool(user)

    # check user without fetching data
    async def check_user_exists(self, email: EmailStr, session: AsyncSession) -> bool:
        statement = select(exists(select(User.id).where(User.email == email)))
        result = await session.execute(statement)
        return result.scalar() or False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = hash_password(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        return new_user
