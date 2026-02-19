from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session

from .dependencies import RefreshTokenBearer, get_current_user
from ..schemas.user_schemas import UserCreateModel, UserLoginModel, UserResponseModel
from .service import UserService
from .utils import create_access_token, verify_password


auth_router = APIRouter()
user_service = UserService()
Session = Annotated[AsyncSession, Depends(get_session)]
refresh_token_bearer = RefreshTokenBearer()
REFRESH_TOKEN_EXPIRY = 2


@auth_router.post(
    "/signup", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(user_data: UserCreateModel, session: Session):
    email = user_data.email

    user_exists = await user_service.check_user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    try:
        new_user = await user_service.create_user(user_data, session)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    return new_user


@auth_router.post("/login")
async def login(login_data: UserLoginModel, session: Session):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    if user is not None and verify_password(password, user.password_hash):
        access_token = create_access_token(
            user_data={
                "email": user.email,
                "user_id": str(user.id),
            }
        )
        refresh_token = create_access_token(
            user_data={
                "email": user.email,
                "user_id": str(user.id),
            },
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            refresh=True,
        )
        return JSONResponse(
            content={
                "message": "login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid login. Wrong Email or Password",
    )


@auth_router.get("/logout")
async def revoke_token():
    pass


@auth_router.post("/refresh")
async def refresh_token(token_data: dict[str, Any] = Depends(refresh_token_bearer)):
    new_access_token = create_access_token(user_data=token_data["user"])
    return JSONResponse(content={"access_token": new_access_token})


@auth_router.get("/me", response_model=UserResponseModel)
async def get_user(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Credentials",
        )
    return user
