from pydantic import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import exists, select

from ..models.user_model import User
from ..schemas.user_schemas import UserCreateModel
from .utils import hash_password


class UserService:
    async def get_user_by_email(self, email: EmailStr, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def check_user_exists(self, email: EmailStr, session: AsyncSession) -> bool:
        statement = select(exists(select(User.id).where(User.email == email)))
        result = await session.execute(statement)
        return result.scalar() or False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(
            email=user_data_dict["email"],
            full_name=user_data_dict["full_name"],
            password_hash=hash_password(user_data_dict["password"]),
        )

        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)
        return new_user
