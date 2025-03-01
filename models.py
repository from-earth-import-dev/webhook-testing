from datetime import datetime

from pydantic import BaseModel, field_serializer


class WebhookPayload(BaseModel):
    event_id: int
    timestamp: datetime
    event_type: str
    description: str

    @field_serializer("timestamp", mode="plain")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.isoformat()
