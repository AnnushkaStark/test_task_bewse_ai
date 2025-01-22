from typing import Callable

from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from crud.application import application_crud
from models import User
from schemas.application import ApplicationCreate

ROOT_ENDPOINT = "/application_service/api/v1/application/"


class TestApplicationCreate:
    async def test_create_success(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        mocker: MockerFixture,
        get_auth_headers: Callable,
        user_fixture: User,
    ) -> None:
        mocker_method = mocker.patch("services.message.send_message")
        mocker_method.return_value = None
        mocker_method.side_effect = None
        user_auth_headers = await get_auth_headers(user_fixture)
        data = ApplicationCreate(description="My Test Application")
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump(), headers=user_auth_headers
        )
        assert response.status_code == 201
        await async_session.close()
        created_applications = await application_crud.get_by_author_username(
            db=async_session, author_username=user_fixture.username
        )
        assert created_applications != []
        assert len(created_applications) == 1
        assert created_applications[0].description == data.description
        assert mocker_method.call_count == 1
