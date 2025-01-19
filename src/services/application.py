from sqlalchemy.ext.asyncio import AsyncSession

from crud.application import application_crud
from models import Application, User
from schemas.application import ApplicationCreate, ApplicationCreateDB
from services import message as message_service


async def create(
    db: AsyncSession, create_schema: ApplicationCreate, author: User
) -> Application:
    create_data = ApplicationCreateDB(
        author_id=author.id, **create_schema.model_dump(exclude_unset=True)
    )
    application = await application_crud.create(
        db=db, create_schema=create_data
    )
    # await message_service.send_message(author=author, application=application)
    return application
