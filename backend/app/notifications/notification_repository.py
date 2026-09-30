from datetime import UTC, datetime
from uuid import UUID

from app.notifications.notification_model import NotificationModel
from sqlalchemy import select
from sqlalchemy.orm import Session


class NotificationRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        notification: NotificationModel
    ) -> NotificationModel:
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    

    def find_by_id(
        self,
        notification_id: UUID
    ) -> NotificationModel | None:
        return self.db.get(
            NotificationModel,
            notification_id
        )
        
        
    def find_by_id_and_user_id(
        self,
        notification_id: UUID,
        user_id: UUID
    ) -> NotificationModel | None:
        statement = (
            select(NotificationModel)
            .where(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id,
                NotificationModel.deleted_at.is_(None)
            )
        )

        return self.db.scalar(statement)
    

    def find_all_by_user_id(
        self,
        user_id: UUID
    ) -> list[NotificationModel]:
        statement = (
            select(NotificationModel)
            .where(NotificationModel.user_id == user_id,
                   NotificationModel.deleted_at.is_(None))
        )

        return list(
            self.db.scalars(statement).all()
        )
        
    
    def update(
        self,
        notification: NotificationModel
    ) -> NotificationModel:
        self.db.commit()
        self.db.refresh(notification)

        return notification
    
    
    def delete(
        self,
        notification: NotificationModel
    ) -> None:
        notification.deleted_at = datetime.now(UTC)

        self.db.commit()