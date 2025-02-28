from datetime import datetime

from pydantic import BaseModel


class WebhookPayload(BaseModel):
    event_id: int
    timestamp: datetime  # expects an ISO formatted string
    event_type: str
    description: str
