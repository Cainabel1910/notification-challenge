from core.exceptions import (
    EmailAlreadyRegisteredException,
    InvalidCredentialsException,
    InvalidNotificationContentException,
    InvalidRecipientException,
    InvalidTokenException,
    NotificationNotFoundException,
    UserNotFoundException,
)
from fastapi import Request
from fastapi.responses import JSONResponse


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )


async def email_already_registered_handler(
    request: Request,
    exc: EmailAlreadyRegisteredException
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        }
    )
    


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsException
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": str(exc)
        }
    )
    

async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenException
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": str(exc)
        }
    )


async def notification_not_found_handler(
    request: Request,
    exc: NotificationNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )
    

async def invalid_recipient_handler(
    request: Request,
    exc: InvalidRecipientException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )


async def invalid_notification_content_handler(
    request: Request,
    exc: InvalidNotificationContentException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )
    
    