from datetime import date
from typing import Optional, Sequence

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import Application


class ApplicationsFilter(Filter):
    created_at__gte: Optional[date] = None
    created_at__lte: Optional[date] = None

    class Constants(Filter.Constants):
        model = Application

    async def filter(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> Sequence[Application]:
        statement = (
            select(Application, func.count().over().label("total"))
            .options(selectinload(Application.author))
            .order_by(Application.created_at.desc())
        )
        if self.created_at__gte is not None:
            statement = statement.where(
                func.date(Application.created_at) >= self.created_at__gte
            )
        if self.created_at__lte is not None:
            statement = statement.where(
                func.date(Application.created_at) <= self.created_at__lte
            )
        result = await db.execute(statement)
        rows = result.mappings().unique().all()
        return {
            "limit": limit,
            "offset": skip * limit,
            "total": rows[0]["total"] if rows else 0,
            "objects": [r["Application"] for r in rows],
        }
