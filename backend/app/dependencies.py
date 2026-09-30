from typing import Annotated

from database.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.auth_service import AuthService
from app.notifications.delivery_repository import (
    NotificationDeliveryRepository,
)
from app.notifications.notification_repository import (
    NotificationRepository,
)
from app.notifications.notification_service import NotificationService
from app.users.user_repository import UserRepository
from app.users.user_service import UserService


def get_user_service(
    db: Annotated[Session, Depends(get_db)],
) -> UserService:
    return UserService(UserRepository(db))


def get_auth_service(
    db: Annotated[Session, Depends(get_db)],
) -> AuthService:
    return AuthService(UserRepository(db))


def get_notification_service(
    db: Annotated[Session, Depends(get_db)],
) -> NotificationService:
    repository = NotificationRepository(db)
    delivery_repository = NotificationDeliveryRepository(db)
    return NotificationService(repository, delivery_repository)