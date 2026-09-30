from typing import Annotated
from uuid import UUID

from app.auth.auth_dependency import get_current_user
from app.dependencies import get_user_service
from app.users.user_model import UserModel
from app.users.user_schema import UserCreate, UserResponse
from app.users.user_service import UserService
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_all_users(
    service: Annotated[UserService, Depends(get_user_service)]
):
    return service.get_all_users()


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: Annotated[
        UserModel,
        Depends(get_current_user)
    ]
) -> UserModel:
    return current_user


@router.get(
    "/by-email/{email}",
    response_model=UserResponse
)
def get_user_by_email(
    email: str,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return service.get_user_by_email(email)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user_by_id(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return service.get_user_by_id(user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return service.register_user(user_data)
