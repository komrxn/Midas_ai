"""
Test authentication endpoints.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration."""
    response = await client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "new@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient):
    """Test registration with duplicate username."""
    # First registration
    await client.post(
        "/auth/register",
        json={"username": "duplicate", "email": "dup1@example.com", "password": "pass123"}
    )
    
    # Second registration with same username
    response = await client.post(
        "/auth/register",
        json={"username": "duplicate", "email": "dup2@example.com", "password": "pass123"}
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """Test user login."""
    # Register first
    await client.post(
        "/auth/register",
        json={"username": "logintest", "email": "login@example.com", "password": "pass123"}
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={"username": "logintest", "password": "pass123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "logintest"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with wrong password."""
    # Register
    await client.post(
        "/auth/register",
        json={"username": "wrongpass", "email": "wrong@example.com", "password": "correct123"}
    )
    
    # Login with wrong password
    response = await client.post(
        "/auth/login",
        json={"username": "wrongpass", "password": "wrong456"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, auth_headers: dict):
    """Test getting current user info."""
    response = await client.get("/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "authuser"
    assert data["email"] == "auth@example.com"


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing protected endpoint without token."""
    response = await client.get("/auth/me")
    
    assert response.status_code == 403  # No credentials provided
