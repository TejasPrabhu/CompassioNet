import json
import pytest
import jwt
from backend import create_app
from backend.config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    return app.test_client()


def extract_cookie_value(cookies, cookie_name):
    for cookie in cookies:
        if cookie.startswith(cookie_name):
            cookie_parts = cookie.split(";")
            cookie_value = cookie_parts[0].split("=")[1]
            return cookie_value
    return None


def test_login(client):
    data = {"email": "john@example.com", "password": "password1"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == 200
    assert response.json["login"] is True
    assert response.json["message"] == "Logged in successfully"

    # Assert the presence of access token in the response cookies
    assert response.headers.get("Set-Cookie") is not None
    cookies = response.headers.getlist("Set-Cookie")

    # Assert the presence of access token in the response cookies
    access_token_cookie = extract_cookie_value(cookies, "access_token_cookie")
    assert access_token_cookie is not None
    access_token = access_token_cookie

    refresh_token_cookie = extract_cookie_value(cookies, "refresh_token_cookie")
    assert refresh_token_cookie is not None
    refresh_token = refresh_token_cookie

    decoded_refresh_token = jwt.decode(
        refresh_token, options={"verify_signature": False}
    )
    assert decoded_refresh_token["sub"] == data["email"]

    decoded_access_token = jwt.decode(access_token, options={"verify_signature": False})
    assert decoded_access_token["sub"] == data["email"]


def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json["logout"] is True
    assert response.json["message"] == "Logged out successfully"

    assert response.headers.get("Set-Cookie") is not None
    cookies = response.headers.getlist("Set-Cookie")

    access_token_cookie = extract_cookie_value(cookies, "access_token_cookie")
    assert access_token_cookie is ""

    refresh_token_cookie = extract_cookie_value(cookies, "refresh_token_cookie")
    assert refresh_token_cookie is ""


def test_refresh(client):
    data = {"email": "john@example.com", "password": "password1"}
    login_response = client.post("/auth/login", json=data)
    cookies = login_response.headers.getlist("Set-Cookie")
    access_token_cookie = extract_cookie_value(cookies, "access_token_cookie")

    headers = {
        "Authorization": f"Bearer {access_token_cookie}",
        "X-CSRF-TOKEN": "csrf_refresh_token",
    }

    response = client.post("/auth/refresh", headers=headers)
    assert response.status_code == 200
    assert response.json["refresh"] is True
    assert response.json["message"] == "Access token refreshed"

    cookies = response.headers.getlist("Set-Cookie")
    refreshed_access_token_cookie = extract_cookie_value(cookies, "access_token_cookie")

    assert refreshed_access_token_cookie != access_token_cookie
