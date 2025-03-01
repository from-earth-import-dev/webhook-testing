from datetime import datetime

from pydantic import BaseModel


class WebhookPayload(BaseModel):
    event_id: int
    timestamp: datetime
    event_type: str
    description: str

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
