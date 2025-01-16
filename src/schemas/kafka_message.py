from datetime import datetime

from pydantic import BaseModel


class KafkaMessageBase(BaseModel):
    id: int
    username: str
    description: str
    created_at: datetime
