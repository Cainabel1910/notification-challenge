from abc import ABC, abstractmethod

from app.notifications.delivery_result import DeliveryResult


class NotificationStrategy(ABC):

    @abstractmethod
    def validate(self, recipient: str, content: str) -> None:
        pass

    @abstractmethod
    def send(
        self,
        recipient: str,
        title: str,
        content: str
    ) -> DeliveryResult:
        pass