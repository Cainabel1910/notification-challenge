from datetime import datetime
from uuid import UUID, uuid4

from database.base import Base
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class NotificationDeliveryModel(Base):
    __tablename__ = "notification_deliveries"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    notification_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("notifications.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    sent_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )