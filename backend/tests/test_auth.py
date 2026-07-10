import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_flow_success(client: AsyncClient):
    """Verifies a full successful user lifecycle: register, login, profile retrieval, and logout."""
    user_payload = {
        "email": "test@example.com",
        "username": "testdeveloper",
        "password": "strongpassword123",
    }

    # 1. Register User
    reg_response = await client.post("/api/auth/register", json=user_payload)
    assert reg_response.status_code == 201
    reg_data = reg_response.json()
    assert reg_data["email"] == user_payload["email"]
    assert reg_data["username"] == user_payload["username"]
    assert "id" in reg_data

    # 2. Login User
    login_payload = {
        "username_or_email": user_payload["username"],
        "password": user_payload["password"],
    }
    login_response = await client.post("/api/auth/login", json=login_payload)
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"
    
    # 3. Access Protected Route (/users/me) using Header auth
    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me_response = await client.get("/api/users/me", headers=headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == user_payload["email"]
    assert me_data["username"] == user_payload["username"]

    # 4. Access Protected Route using Cookie auth
    # We pass the cookies parameter to simulate browser session storage
    cookies = {"access_token": token}
    me_cookie_response = await client.get("/api/users/me", cookies=cookies)
    assert me_cookie_response.status_code == 200
    assert me_cookie_response.json()["username"] == user_payload["username"]

    # 5. Logout User
    logout_response = await client.post("/api/auth/logout")
    assert logout_response.status_code == 200
    assert "Logged out successfully" in logout_response.json()["message"]


@pytest.mark.asyncio
async def test_register_duplicate_credentials(client: AsyncClient):
    """Verifies that registration fails when duplicate usernames or email credentials are submitted."""
    user_payload = {
        "email": "dup@example.com",
        "username": "duplevel",
        "password": "password123",
    }

    # Register first user
    res1 = await client.post("/api/auth/register", json=user_payload)
    assert res1.status_code == 201

    # Register duplicate email
    dup_email_payload = {
        "email": "dup@example.com",
        "username": "duplevel2",
        "password": "password123",
    }
    res2 = await client.post("/api/auth/register", json=dup_email_payload)
    assert res2.status_code == 400
    assert "email already exists" in res2.json()["detail"]

    # Register duplicate username
    dup_user_payload = {
        "email": "dup2@example.com",
        "username": "duplevel",
        "password": "password123",
    }
    res3 = await client.post("/api/auth/register", json=dup_user_payload)
    assert res3.status_code == 400
    assert "username already exists" in res3.json()["detail"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Verifies that login fails when invalid credentials are provided."""
    # Attempt login on non-existent account
    login_payload = {
        "username_or_email": "nonexistent",
        "password": "wrongpassword",
    }
    response = await client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401
    assert "Incorrect username" in response.json()["detail"]


@pytest.mark.asyncio
async def test_users_me_unauthorized(client: AsyncClient):
    """Verifies that requesting /users/me fails when no authentication is provided."""
    response = await client.get("/api/users/me")
    assert response.status_code == 401
    assert "Authentication credentials not found." in response.json()["detail"]
