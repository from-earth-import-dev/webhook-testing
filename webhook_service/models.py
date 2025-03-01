from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class WebhookPayload(BaseModel):
    event_id: int
    timestamp: datetime
    event_type: str
    description: str

    model_config = ConfigDict(extra="forbid")

    @field_serializer("timestamp", mode="plain")
    def serialize_timestamp(self: "WebhookPayload", value: datetime) -> str:
        return value.isoformat()
