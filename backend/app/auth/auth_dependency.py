from typing import Annotated

from app.security.jwt import decode_access_token
from app.users.user_model import UserModel
from app.users.user_repository import UserRepository
from core.exceptions import InvalidTokenException
from core.messages import AuthMessages
from database.database import get_db
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

security = HTTPBearer()


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security)
    ],
    db: Annotated[Session, Depends(get_db)]
) -> UserModel:


    user_id = decode_access_token(
        credentials.credentials
    )

    repository = UserRepository(db)
    user = repository.find_by_id(user_id)

    if user is None:
        raise InvalidTokenException(
            AuthMessages.INVALID_TOKEN
        )

    return user