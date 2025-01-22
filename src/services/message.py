from broker import send_application
from models import Application, User


async def send_message(author: User, application: Application) -> None:
    message_schema = {
        "id": application.id,
        "username": author.username,
        "description": application.description,
        "created_at": application.created_at.isoformat(),
    }
    try:
        await send_application(application_data=message_schema)
    except Exception as e:
        raise Exception(str(e))
