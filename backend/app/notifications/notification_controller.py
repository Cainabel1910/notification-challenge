from typing import Annotated
from uuid import UUID

from app.auth.auth_dependency import get_current_user
from app.dependencies import get_notification_service
from app.notifications.notification_schema import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)
from app.notifications.notification_service import (
    NotificationService,
)
from app.users.user_model import UserModel
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_notification(
    notification_data: NotificationCreate,
    current_user: Annotated[
        UserModel,
        Depends(get_current_user)
    ],
    service: Annotated[
        NotificationService,
        Depends(get_notification_service)
    ]
) -> NotificationResponse:
    return service.create_notification(
        current_user.id,
        notification_data
    )


@router.get(
    "",
    response_model=list[NotificationResponse]
)
def get_my_notifications(
    current_user: Annotated[
        UserModel,
        Depends(get_current_user)
    ],
    service: Annotated[
        NotificationService,
        Depends(get_notification_service)
    ]
) -> list[NotificationResponse]:
    return service.get_all_notifications(
        current_user.id
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse
)
def get_notification_by_id(
    notification_id: UUID,
    current_user: Annotated[
        UserModel,
        Depends(get_current_user)
    ],
    service: Annotated[
        NotificationService,
        Depends(get_notification_service)
    ]
) -> NotificationResponse:
    return service.get_notification_by_id(
        notification_id,
        current_user.id
    )
    

@router.put(
    "/{notification_id}",
    response_model=NotificationResponse
)
def update_notification(
    notification_id: UUID,
    notification_data: NotificationUpdate,
    current_user: Annotated[
        UserModel,
        Depends(get_current_user)
    ],
    service: Annotated[
        NotificationService,
        Depends(get_notification_service)
    ]
) -> NotificationResponse:
    return service.update_notification(
        notification_id,
        current_user.id,
        notification_data
    )
    
    
@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_notification(
    notification_id: UUID,
    current_user: Annotated[
        UserModel,
        Depends(get_current_user)
    ],
    service: Annotated[
        NotificationService,
        Depends(get_notification_service)
    ]
) -> None:

    service.delete_notification(
        notification_id,
        current_user.id
    )