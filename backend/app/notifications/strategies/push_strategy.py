from datetime import UTC, datetime

from app.notifications.delivery_result import DeliveryResult
from app.notifications.strategies.notification_strategy import (
    NotificationStrategy,
)
from core.exceptions import InvalidRecipientException
from core.messages import NotificationMessages


class PushNotificationStrategy(NotificationStrategy):

    def validate(
        self,
        recipient: str,
        content: str,
    ) -> None:
        if not recipient.strip():
            raise InvalidRecipientException(
                NotificationMessages.INVALID_PUSH_RECIPIENT
            )

    def send(
        self,
        recipient: str,
        title: str,
        content: str
    ) -> DeliveryResult:

        payload = {
            "device_token": recipient,
            "notification": {
                "title": title,
                "body": content
            }
        }

        print(
            f"Sending PUSH: {payload}"
        )

        return DeliveryResult(
            status="SENT",
            sent_at=datetime.now(UTC)
        )