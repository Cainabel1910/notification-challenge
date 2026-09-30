from app.notifications.delivery_model import (
    NotificationDeliveryModel,
)
from sqlalchemy.orm import Session


class NotificationDeliveryRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        delivery: NotificationDeliveryModel
    ) -> NotificationDeliveryModel:
        self.db.add(delivery)
        self.db.commit()
        self.db.refresh(delivery)

        return delivery