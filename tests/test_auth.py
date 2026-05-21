def register_user(client, email="test@example.com", username="tester", password="password123"):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )


def login_user(client, email="test@example.com", password="password123"):
    # OAuth2PasswordRequestForm w FastAPI oczekuje formularza:
    # username + password, a nie JSON.
    return client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )


def test_register_returns_200_and_user_data(client):
    response = register_user(client)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "tester"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email_returns_400(client):
    register_user(client)
    response = register_user(client)

    assert response.status_code == 400


def test_register_invalid_email_returns_validation_error(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "tester",
            "email": "wrong-email",
            "password": "password123",
        },
    )

    assert response.status_code in [400, 422]


def test_login_returns_token(client):
    register_user(client)
    response = login_user(client)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password_returns_401(client):
    register_user(client)
    response = login_user(client, password="wrong-password")

    assert response.status_code == 401


def test_me_without_token_returns_401(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_with_token_returns_200(client):
    register_user(client)
    login_response = login_user(client)
    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
