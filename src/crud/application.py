from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from models import Application, User
from schemas.application import ApplicationBase, ApplicationCreateDB

from .async_crud import BaseAsyncCRUD


class ApplicationCRUD(
    BaseAsyncCRUD[Application, ApplicationBase, ApplicationCreateDB]
):
    async def get_by_uid(
        self, db: AsyncSession, uid: UUID
    ) -> Optional[Application]:
        statement = (
            select(self.model)
            .options(joinedload(self.model.author))
            .where(self.model.uid == uid)
        )
        result = await db.execute(statement)
        return result.scalars().unique().first()

    async def get_by_author_username(
        self, db: AsyncSession, author_username: str
    ) -> List[Application]:
        statement = (
            select(self.model)
            .options(joinedload(self.model.author))
            .where(User.username == author_username)
        )
        result = await db.execute(statement)
        return result.scalars().unique().all()


application_crud = ApplicationCRUD(Application)
