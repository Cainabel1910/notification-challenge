from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from core.config import settings
from core.exceptions import InvalidTokenException
from core.messages import AuthMessages


def create_access_token(user_id: UUID) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expiration_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expiration
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> UUID:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidTokenException(
                AuthMessages.INVALID_TOKEN
            )

        return UUID(user_id)

    except (jwt.InvalidTokenError, ValueError) as error:
        raise InvalidTokenException(
            AuthMessages.INVALID_TOKEN
        ) from error