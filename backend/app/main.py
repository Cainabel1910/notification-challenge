from core.exception_handlers import (
    email_already_registered_handler,
    invalid_credentials_handler,
    invalid_notification_content_handler,
    invalid_recipient_handler,
    invalid_token_handler,
    notification_not_found_handler,
    user_not_found_handler,
)
from core.exceptions import (
    EmailAlreadyRegisteredException,
    InvalidCredentialsException,
    InvalidNotificationContentException,
    InvalidRecipientException,
    InvalidTokenException,
    NotificationNotFoundException,
    UserNotFoundException,
)
from fastapi import FastAPI

from app.auth.auth_controller import router as auth_router
from app.notifications.notification_controller import router as notification_router
from app.users.user_controller import router as user_router

app = FastAPI()


app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler
)

app.add_exception_handler(
    EmailAlreadyRegisteredException,
    email_already_registered_handler
)

app.add_exception_handler(
    InvalidCredentialsException,
    invalid_credentials_handler,
)

app.add_exception_handler(
    InvalidTokenException,
    invalid_token_handler,
)

app.add_exception_handler(
    NotificationNotFoundException,
    notification_not_found_handler,
)

app.add_exception_handler(
    InvalidRecipientException,
    invalid_recipient_handler,
)

app.add_exception_handler(
    InvalidNotificationContentException,
    invalid_notification_content_handler,
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(notification_router)