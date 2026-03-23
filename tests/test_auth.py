import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_success(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "email": "newuser@test.com",
        "password": "password123",
        "full_name": "New User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data


async def test_register_duplicate_email(client: AsyncClient):
    await client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "password": "password123"
    })
    response = await client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "password": "password456"
    })
    assert response.status_code == 400


async def test_register_invalid_email(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "email": "notanemail",
        "password": "password123"
    })
    assert response.status_code == 422


async def test_login_success(client: AsyncClient, registered_user):
    response = await client.post(
        "/auth/login",
        data={
            "username": "test@smartdocs.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient, registered_user):
    response = await client.post(
        "/auth/login",
        data={
            "username": "test@smartdocs.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        data={
            "username": "nobody@test.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401


async def test_get_me_success(client: AsyncClient, auth_headers):
    response = await client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@smartdocs.com"
    assert "hashed_password" not in data


async def test_get_me_no_token(client: AsyncClient):
    response = await client.get("/auth/me")
    assert response.status_code == 401


async def test_get_me_invalid_token(client: AsyncClient):
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401