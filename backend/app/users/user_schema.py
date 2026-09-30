import re
from datetime import datetime
from uuid import UUID

from core.config import settings
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:

        if len(password) < settings.password_min_length:
            raise ValueError(
                f"Password must contain at least "
                f"{settings.password_min_length} characters"
            )

        if settings.password_require_uppercase and not re.search(r"[A-Z]", password):
                raise ValueError(
                    "Password must contain at least one uppercase letter"
                )

        if settings.password_require_number and not re.search(r"\d", password):
                raise ValueError(
                    "Password must contain at least one number"
                )

        if settings.password_require_symbol and not re.search(r"[^A-Za-z0-9]", password):
                raise ValueError(
                    "Password must contain at least one symbol"
                )

        return password


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime