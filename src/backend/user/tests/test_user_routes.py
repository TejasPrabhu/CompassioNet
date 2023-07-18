import pytest
from flask import jsonify
from backend import create_app
from backend.config import TestingConfig
from backend.auth.models import get_user_by_email


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    return app.test_client()


def test_register(client):
    data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testuser",
        "repeatpassword": "testuser",
        "city": "Test City",
        "zipcode": "12345",
        "interests": [1, 2, 3],
    }
    response = client.post("/user/register", json=data)
    assert response.status_code == 201
    assert response.json["status"] == 201
    assert (
        response.json["message"]
        == "Your registration request has been received. Please check your email for further instructions."
    )


def test_get_profile(client):
    user_id = get_user_by_email("testuser@example.com")["id"]
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "User profile retrieved successfully"


def test_update_profile(client):
    user_id = get_user_by_email("testuser@example.com")["id"]
    data = {
        "name": "John Smith",
        "city": "San Francisco",
        "zipcode": "54321",
        "interests": [4, 5],
    }
    response = client.put(f"/user/{user_id}", json=data)
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "User profile updated successfully"


def test_delete_profile(client):
    user_id = get_user_by_email("testuser@example.com")["id"]
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "User profile deleted successfully"
