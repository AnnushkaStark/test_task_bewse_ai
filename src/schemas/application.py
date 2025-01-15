from typing import List

from pydantic import BaseModel, Field

from constants.application import (
    MAX_DESCRIPTION_LENGTH,
    MIN_DESCRIPTION_LENGTH,
)
from schemas.paginate import PaginatedResponseBase
from schemas.user import UserResponse


class ApplicationBase(BaseModel):
    class Config:
        from_attributes = True


class ApplicationCreate(ApplicationBase):
    description: str = Field(
        min_length=MIN_DESCRIPTION_LENGTH, max_length=MAX_DESCRIPTION_LENGTH
    )


class ApplicationCreateDB(ApplicationCreate):
    author_id: int


class ApplicationResponse(ApplicationCreate):
    author: UserResponse


class ApplicationPaginatedResponse(PaginatedResponseBase):
    objects: List[ApplicationResponse] = []

    class Config:
        arbitrary_types_allowed = True
