from typing import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import Application, User
from utilities.search import get_transliterated_value


class SearchApplicationCRUD:
    async def get_search_applications_result(
        self,
        db: AsyncSession,
        query: str,
        skip: int = 0,
        limit: int = 10,
    ) -> Sequence[Application]:
        lst_query = await get_transliterated_value(query=query)
        statement = (
            select(Application, func.count().over().label("total"))
            .join(User)
            .options(joinedload(Application.author))
            .filter(or_(*[User.username.ilike(f"%{q}%") for q in lst_query]))
            .offset(skip)
            .limit(limit)
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
