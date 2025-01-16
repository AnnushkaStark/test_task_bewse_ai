from typing import Sequence

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from models import Application, User
from schemas.application import ApplicationPaginatedResponse
from utilities.search import get_transliterated_value


class SearchApplicationCRUD:
    async def get_search_applications_results(
        self, db: AsyncSession, query: str, skip: int = 0, limit: int = 10
    ) -> ApplicationPaginatedResponse:
        result = {}
        kwargs = {
            "db": db,
            "query": await get_transliterated_value(query=query),
            "skip": skip,
            "limit": limit,
        }
        result = await self.get_applications_result(**kwargs)
        return result

    async def get_applications_result(
        self,
        db: AsyncSession,
        query: list[str],
        skip: int = 0,
        limit: int = 10,
    ) -> Sequence[Application]:
        statement = (
            select(Application, func.count().over().label("total"))
            .join(User)
            .options(joinedload(Application.author))
            .filter(*(User.username.ilike(f"%{q}%") for q in query))
            .order_by(User.username)
        )
        result = await db.execute(statement)
        rows = result.mappings().unique().all()
        return {
            "limit": limit,
            "offset": skip * limit,
            "total": rows[0]["total"] if rows else 0,
            "objects": [r["Application"] for r in rows],
        }


search_application_crud = SearchApplicationCRUD()
