from typing import ClassVar

from app.notifications.notification_channel import NotificationChannel
from app.notifications.strategies.email_strategy import (
    EmailNotificationStrategy,
)
from app.notifications.strategies.notification_strategy import (
    NotificationStrategy,
)
from app.notifications.strategies.push_strategy import (
    PushNotificationStrategy,
)
from app.notifications.strategies.sms_strategy import (
    SmsNotificationStrategy,
)


class NotificationStrategyFactory:

    _strategies: ClassVar[dict[NotificationChannel, NotificationStrategy]] = {
        NotificationChannel.EMAIL: EmailNotificationStrategy(),
        NotificationChannel.SMS: SmsNotificationStrategy(),
        NotificationChannel.PUSH: PushNotificationStrategy(),
    }

    @classmethod
    def get_strategy(
        cls,
        channel: NotificationChannel
    ) -> NotificationStrategy:
        return cls._strategies[channel]