from uuid import UUID

from app.notifications.delivery_model import (
    NotificationDeliveryModel,
)
from app.notifications.delivery_repository import (
    NotificationDeliveryRepository,
)
from app.notifications.notification_model import NotificationModel
from app.notifications.notification_repository import (
    NotificationRepository,
)
from app.notifications.notification_schema import NotificationCreate, NotificationUpdate
from app.notifications.strategies.strategy_factory import (
    NotificationStrategyFactory,
)
from core.exceptions import (
    NotificationNotFoundException,
)
from core.messages import NotificationMessages


class NotificationService:

    def __init__(
        self,
        repository: NotificationRepository,
        delivery_repository: NotificationDeliveryRepository
    ):
        self.repository = repository
        self.delivery_repository = delivery_repository


    def create_notification(
        self,
        user_id: UUID,
        notification_data: NotificationCreate
    ) -> NotificationModel:

        strategy = NotificationStrategyFactory.get_strategy(
            notification_data.channel
        )

        strategy.validate(
            notification_data.recipient,
            notification_data.content,
        )

        notification = NotificationModel(
            user_id=user_id,
            title=notification_data.title,
            content=notification_data.content,
            channel=notification_data.channel.value,
            recipient=notification_data.recipient
        )

        saved_notification = self.repository.save(
            notification
        )

        delivery_result = strategy.send(
            saved_notification.recipient,
            saved_notification.title,
            saved_notification.content
        )

        delivery = NotificationDeliveryModel(
            notification_id=saved_notification.id,
            title=saved_notification.title,
            content=saved_notification.content,
            channel=saved_notification.channel,
            recipient=saved_notification.recipient,
            status=delivery_result.status,
            sent_at=delivery_result.sent_at
        )

        self.delivery_repository.save(delivery)

        return saved_notification


    def get_notification_by_id(
        self,
        notification_id: UUID,
        user_id: UUID
    ) -> NotificationModel:

        notification = (
            self.repository.find_by_id_and_user_id(
                notification_id,
                user_id
            )
        )

        if notification is None:
            raise NotificationNotFoundException(
                NotificationMessages.NOT_FOUND
            )

        return notification


    def get_all_notifications(
        self,
        user_id: UUID
    ) -> list[NotificationModel]:

        return self.repository.find_all_by_user_id(
            user_id
        )
        
    
    def update_notification(
        self,
        notification_id: UUID,
        user_id: UUID,
        notification_data: NotificationUpdate
    ) -> NotificationModel:

        notification = (
            self.repository.find_by_id_and_user_id(
                notification_id,
                user_id
            )
        )

        if notification is None:
            raise NotificationNotFoundException(
                NotificationMessages.NOT_FOUND
            )

        strategy = NotificationStrategyFactory.get_strategy(
            notification_data.channel
        )

        strategy.validate(
            notification_data.recipient,
            notification_data.content,
        )

        notification.title = notification_data.title
        notification.content = notification_data.content
        notification.channel = notification_data.channel.value
        notification.recipient = notification_data.recipient

        updated_notification = self.repository.update(
            notification
        )

        delivery_result = strategy.send(
            updated_notification.recipient,
            updated_notification.title,
            updated_notification.content
        )

        delivery = NotificationDeliveryModel(
            notification_id=updated_notification.id,
            title=updated_notification.title,
            content=updated_notification.content,
            channel=updated_notification.channel,
            recipient=updated_notification.recipient,
            status=delivery_result.status,
            sent_at=delivery_result.sent_at
        )

        self.delivery_repository.save(delivery)

        return updated_notification
    
    
    def delete_notification(
        self,
        notification_id: UUID,
        user_id: UUID
    ) -> None:

        notification = (
            self.repository.find_by_id_and_user_id(
                notification_id,
                user_id
            )
        )

        if notification is None:
            raise NotificationNotFoundException(
                NotificationMessages.NOT_FOUND
            )

        self.repository.delete(notification)