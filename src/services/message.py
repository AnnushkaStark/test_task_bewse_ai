from broker import send_application
from models import Application, User
from schemas.kafka_message import KafkaMessageBase


async def send_message(author: User, application: Application) -> None:
    message_schema = KafkaMessageBase(
        id=application.id,
        username=author.username,
        description=application.description,
        created_at=application.created_at,
    )
    await send_application(application_data=message_schema.model_dump())
