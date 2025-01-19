from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from api.filters.application import ApplicationsFilter
from crud.application import application_crud
from crud.search import search_application_crud
from models import User
from schemas.application import (
    ApplicationCreate,
    ApplicationPaginatedResponse,
    ApplicationResponse,
)
from services import application as application_service

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_application(
    application: ApplicationCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await application_service.create(
            db=db, author=current_user, create_schema=application
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/", response_model=ApplicationPaginatedResponse)
async def search_applications(
    skip: int = 0,
    limit: int = 20,
    query: str = Query(min_length=2),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await search_application_crud.get_search_applications_result(
        db=db, skip=skip, limit=limit, query=query
    )


@router.get("/all/", response_model=ApplicationPaginatedResponse)
async def read_applications(
    skip: int = 0,
    limit: int = 20,
    filter: ApplicationsFilter = FilterDepends(ApplicationsFilter),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await filter.filter(db=db, skip=skip, limit=limit)


@router.get("/{application_uid}/", response_model=ApplicationResponse)
async def read_application(
    application_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    if found_application := await application_crud.get_by_uid(
        db=db, uid=application_uid
    ):
        return found_application
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )
