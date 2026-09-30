from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.notifications.notification_channel import NotificationChannel


@dataclass
class Notification:
    id: UUID
    user_id: UUID
    title: str
    content: str
    channel: NotificationChannel
    recipient: str
    created_at: datetime
    updated_at: datetime