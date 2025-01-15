from typing import Optional

from email_validator import validate_email
from pydantic import BaseModel, EmailStr, Field, validator

from constants.user import (
    MAX_NICKNAME_LENGTH,
    MIN_NICKNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
)


class UserBase(BaseModel):
    username: str = Field(
        min_length=MIN_NICKNAME_LENGTH, max_length=MAX_NICKNAME_LENGTH
    )
    email: EmailStr
    password: str = Field(min_length=MIN_PASSWORD_LENGTH)

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password_confirm: Optional[str] = None

    @validator("email")
    def email_check(cls, v: EmailStr) -> EmailStr:
        email_info = validate_email(v, check_deliverability=True)
        email = email_info.normalized
        return email


class UserCreateDB(UserBase):
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
