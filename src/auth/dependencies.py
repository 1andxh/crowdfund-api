from typing_extensions import Annotated
from annotated_doc import Doc
from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_token
from .service import UserService
from .models import User
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated, Any, override, List

user_service = UserService()


class Tokenbearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict[str, Any] | None:

        credentials: HTTPAuthorizationCredentials | None = await super().__call__(
            request
        )
        assert credentials is not None

        token = credentials.credentials

        token_data = decode_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        self.verify_token_data(token_data)

        return token_data

    def verify_token_data(self, token_data: dict[str, Any]):
        raise NotImplementedError("please override this method in child class")


class AccessTokenBearer(Tokenbearer):
    @override
    def verify_token_data(self, token_data: dict[str, Any]):
        # check token type
        if token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Provide an access token"
            )


class RefreshTokenBearer(Tokenbearer):
    @override
    def verify_token_data(self, token_data: dict[str, Any]):
        # check token type
        if not token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Provide refresh token"
            )


TokenData = Annotated[dict[str, Any], Depends(AccessTokenBearer())]
Session = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(token_data: TokenData, session: Session):
    user_email = token_data["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)

    return user
