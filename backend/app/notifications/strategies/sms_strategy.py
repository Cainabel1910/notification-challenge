import re
from datetime import UTC, datetime

from app.notifications.delivery_result import DeliveryResult
from app.notifications.strategies.notification_strategy import (
    NotificationStrategy,
)
from core.config import settings
from core.exceptions import (
    InvalidNotificationContentException,
    InvalidRecipientException,
)
from core.messages import NotificationMessages


class SmsNotificationStrategy(NotificationStrategy):

    def validate(
        self,
        recipient: str,
        content: str,
    ) -> None:
        phone_pattern = r"^\+?[1-9]\d{7,14}$"

        if not re.match(phone_pattern, recipient):
            raise InvalidRecipientException(
                NotificationMessages.INVALID_SMS_RECIPIENT
            )

        if len(content) > settings.sms_max_length:
            raise InvalidNotificationContentException(
                NotificationMessages.SMS_CONTENT_TOO_LONG.format(
                    max_length=settings.sms_max_length
                )
            )

    def send(
        self,
        recipient: str,
        title: str,
        content: str
    ) -> DeliveryResult:

        print(
            f"Sending SMS to {recipient}: "
            f"{content}"
        )

        return DeliveryResult(
            status="SENT",
            sent_at=datetime.now(UTC)
        )