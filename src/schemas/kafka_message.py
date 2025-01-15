from datetime import datetime

from pydantic import BaseModel


class KafkaMessageBase(BaseModel):
    username: str
    description: str
    created_at: datetime
