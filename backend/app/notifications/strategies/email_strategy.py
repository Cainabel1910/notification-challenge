import re
from datetime import UTC, datetime

from app.notifications.delivery_result import DeliveryResult
from app.notifications.strategies.notification_strategy import (
    NotificationStrategy,
)
from core.exceptions import InvalidRecipientException
from core.messages import NotificationMessages


class EmailNotificationStrategy(NotificationStrategy):

    def validate(
        self,
        recipient: str,
        content: str,
    ) -> None:
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(email_pattern, recipient):
            raise InvalidRecipientException(
                NotificationMessages.INVALID_EMAIL_RECIPIENT
            )

    def send(
        self,
        recipient: str,
        title: str,
        content: str
    ) -> DeliveryResult:

        template = (
            f"Subject: {title}\n\n"
            f"{content}"
        )

        print(
            f"Sending EMAIL to {recipient}\n"
            f"{template}"
        )

        return DeliveryResult(
            status="SENT",
            sent_at=datetime.now(UTC)
        )