from dataclasses import dataclass
from datetime import datetime


@dataclass
class DeliveryResult:
    status: str
    sent_at: datetime