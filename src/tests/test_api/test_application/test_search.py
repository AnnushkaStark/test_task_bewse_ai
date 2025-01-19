from typing import Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import Application, User

ROOT_ENDPOINT = "/application_service/api/v1/application/"


class TestSearchApplications:
    async def test_search_in_en_origin(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        application_fixture: Application,
        another_application_fixture: Application,
    ) -> None:
        limit = (20,)
        skip = (0,)
        query = "Tes"
        user_auth_headers = await get_auth_headers(user_fixture)
        params = {"limit": limit, "skip": skip, "query": query}
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers, params=params
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 1
        assert len(response_data["objects"]) == 1
        assert (
            response_data["objects"][0]["author"]["username"]
            == user_fixture.username
        )

    async def test_search_in_en_lower(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        application_fixture: Application,
        another_application_fixture: Application,
    ) -> None:
        limit = (20,)
        skip = (0,)
        query = "tes"
        user_auth_headers = await get_auth_headers(user_fixture)
        params = {"limit": limit, "skip": skip, "query": query}
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers, params=params
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 1
        assert len(response_data["objects"]) == 1
        assert (
            response_data["objects"][0]["author"]["username"]
            == user_fixture.username
        )

    async def test_search_in_en_upper(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        application_fixture: Application,
        another_application_fixture: Application,
    ) -> None:
        limit = (20,)
        skip = (0,)
        query = "TES"
        user_auth_headers = await get_auth_headers(user_fixture)
        params = {"limit": limit, "skip": skip, "query": query}
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers, params=params
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 1
        assert len(response_data["objects"]) == 1
        assert (
            response_data["objects"][0]["author"]["username"]
            == user_fixture.username
        )

    async def test_search_in_ru_origin(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        application_fixture: Application,
        another_application_fixture: Application,
    ) -> None:
        limit = (20,)
        skip = (0,)
        query = "Тэс"
        user_auth_headers = await get_auth_headers(user_fixture)
        params = {"limit": limit, "skip": skip, "query": query}
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers, params=params
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 1
        assert len(response_data["objects"]) == 1
        assert (
            response_data["objects"][0]["author"]["username"]
            == user_fixture.username
        )

    async def test_search_in_ru_lower(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        application_fixture: Application,
        another_application_fixture: Application,
    ) -> None:
        limit = (20,)
        skip = (0,)
        query = "тэс"
        user_auth_headers = await get_auth_headers(user_fixture)
        params = {"limit": limit, "skip": skip, "query": query}
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers, params=params
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 1
        assert len(response_data["objects"]) == 1
        assert (
            response_data["objects"][0]["author"]["username"]
            == user_fixture.username
        )

    async def test_search_in_ru_upper(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        get_auth_headers: Callable,
        user_fixture: User,
        application_fixture: Application,
        another_application_fixture: Application,
    ) -> None:
        limit = (20,)
        skip = (0,)
        query = "ТЭС"
        user_auth_headers = await get_auth_headers(user_fixture)
        params = {"limit": limit, "skip": skip, "query": query}
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers, params=params
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 1
        assert len(response_data["objects"]) == 1
        assert (
            response_data["objects"][0]["author"]["username"]
            == user_fixture.username
        )
