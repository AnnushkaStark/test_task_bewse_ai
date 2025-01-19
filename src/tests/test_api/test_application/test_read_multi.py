from typing import Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import Application, User

ROOT_ENDPOINT = "/application_service/api/v1/application/"


class TestReadApplications:
    async def test_read_all_applications(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        another_user_fixture: User,
        application_fixture: Application,
        another_application_fixture: Application,
    ) -> None:
        endpoint = f"{ROOT_ENDPOINT}all/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 2
        assert len(response_data["objects"]) == 2
        assert (
            response_data["objects"][0]["description"]
            == another_application_fixture.description
        )
        assert (
            response_data["objects"][1]["description"]
            == application_fixture.description
        )

    async def test_read_all_with_filter_by_date(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        another_user_fixture: User,
        application_fixture: Application,
        another_application_fixture: Application,
    ) -> None:
        endpoint = f"{ROOT_ENDPOINT}all/"
        user_auth_headers = await get_auth_headers(user_fixture)
        params = {
            "created_at__lte": another_application_fixture.created_at.date(),
            "created_at__gte": another_application_fixture.created_at.date(),
        }
        response = await http_client.get(
            endpoint, headers=user_auth_headers, params=params
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 1
        assert len(response_data["objects"]) == 1
        assert (
            response_data["objects"][0]["description"]
            == another_application_fixture.description
        )
