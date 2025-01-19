import uuid
from typing import Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import Application, User

ROOT_ENDPOINT = "/application_service/api/v1/application/"


class TestReadApplication:
    async def test_read_success(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        application_fixture: Application,
    ) -> None:
        endpoint = f"{ROOT_ENDPOINT}{application_fixture.uid}/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["description"] == application_fixture.description

    async def test_read_by_invalid_uid(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        application_fixture: Application,
    ) -> None:
        endpoint = f"{ROOT_ENDPOINT}{uuid.uuid4()}/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Not found"
