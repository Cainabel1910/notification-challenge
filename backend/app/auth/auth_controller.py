from typing import Annotated

from app.auth.auth_schema import LoginRequest, TokenResponse
from app.auth.auth_service import AuthService
from app.dependencies import get_auth_service
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    login_data: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> TokenResponse:
    return service.login(login_data)
