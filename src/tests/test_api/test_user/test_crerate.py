from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models import User
from schemas.user import UserCreate

ROOT_ENDPOINT = "/application_service/api/v1/user/"


class TestUserCreate:
    async def test_create_success(
        self, async_session: AsyncSession, http_client: AsyncClient
    ) -> None:
        data = UserCreate(
            username="MyUser",
            email="myusermail@gmail.com",
            password="12345678",
            password_confirm="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 201
        await async_session.close()
        created_user = await user_crud.get_by_username(
            db=async_session, username=data.username
        )
        assert created_user is not None
        assert data.email == created_user.email

    async def test_create_with_duplicate_username(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        user_fixture: User,
    ) -> None:
        data = UserCreate(
            username=user_fixture.username,
            email="myusermail@gmail.com",
            password="12345678",
            password_confirm="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert (
            response_data["detail"]
            == f"Username {user_fixture.username} alredy exsists!"
        )
        not_created_user = await user_crud.get_by_email(
            db=async_session, email=data.email
        )
        assert not_created_user is None

    async def test_create_with_duplicate_email(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        user_fixture: User,
    ) -> None:
        data = UserCreate(
            username="MyUser",
            email=user_fixture.email,
            password="12345678",
            password_confirm="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert (
            response_data["detail"]
            == f"Email {user_fixture.email}  alredy exsists!"
        )
        not_created_user = await user_crud.get_by_username(
            db=async_session, username=data.username
        )
        assert not_created_user is None

    async def test_create_with_invalid_password(
        self, async_session: AsyncSession, http_client: AsyncClient
    ) -> None:
        data = UserCreate(
            username="MyUser",
            email="myusermail@gmail.com",
            password="12345678",
            password_confirm="123456789",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert response_data["detail"] == "Passwords don't match!"
        not_created_user = await user_crud.get_by_username(
            db=async_session, username=data.username
        )
        assert not_created_user is None
