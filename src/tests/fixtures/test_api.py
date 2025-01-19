from datetime import datetime, timedelta

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models import Application, User
from utilities.security.password_hasher import get_password_hash


@pytest_asyncio.fixture
async def user_fixture(async_session: AsyncSession) -> User:
    user = User(
        username="TestuSER",
        email="psk221219@gmail.com",
        password=get_password_hash("secret"),
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def another_user_fixture(async_session: AsyncSession) -> User:
    user = User(
        username="AnotherUser",
        email="psk221220@gmail.com",
        password=get_password_hash("qwerty"),
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def application_fixture(
    async_session: AsyncSession, user_fixture: User
) -> Application:
    application = Application(
        description="Test description", author_id=user_fixture.id
    )
    async_session.add(application)
    await async_session.commit()
    await async_session.refresh(application)
    return application


@pytest_asyncio.fixture
async def another_application_fixture(
    async_session: AsyncSession, another_user_fixture: User
) -> Application:
    application = Application(
        description="Another test description",
        created_at=(datetime.now() + timedelta(days=1)),
        author_id=another_user_fixture.id,
    )
    async_session.add(application)
    await async_session.commit()
    await async_session.refresh(application)
    return application
