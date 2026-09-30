from datetime import datetime
from uuid import UUID

from app.notifications.notification_channel import NotificationChannel
from pydantic import BaseModel


class NotificationCreate(BaseModel):
    title: str
    content: str
    channel: NotificationChannel
    recipient: str


class NotificationResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    content: str
    channel: NotificationChannel
    recipient: str
    created_at: datetime
    updated_at: datetime


class NotificationUpdate(BaseModel):
    title: str
    content: str
    channel: NotificationChannel
    recipient: str