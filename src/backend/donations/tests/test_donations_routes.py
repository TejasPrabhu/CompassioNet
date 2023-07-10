import pytest
from flask import jsonify
from backend import create_app
from backend.config import TestingConfig
from backend.products.models import get_current_id_value
from backend.donations.models import (
    add_donation,
    get_donation_by_id,
    update_donation_by_id,
    delete_donation_by_id,
    get_all_donations_received_by_user_model,
)

create_data = {
    "item_id": 1,
    "recipient_id": 1,
}

update_data = {
    "item_id": 2,
    "recipient_id": 2,
}


@pytest.fixture
def created_donation_id(client):
    add_donation(create_data)
    donation_id = get_current_id_value()[0]
    yield donation_id
    delete_donation_by_id(donation_id)


@pytest.fixture
def delete_donation_id(client):
    yield
    donation_id = get_current_id_value()[0]
    delete_donation_by_id(donation_id)


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    return app.test_client()


def test_create_donation(client, delete_donation_id):
    response = client.post("/donations/", json=create_data)
    assert response.status_code == 201
    assert response.json["status"] == 201
    assert response.json["message"] == "Donation created"


def test_get_donation(client, created_donation_id):
    response = client.get(f"/donations/{created_donation_id}")
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "Donation retrieved"
    assert "donation" in response.json


def test_update_donation(client, created_donation_id):
    response = client.put(f"/donations/{created_donation_id}", json=update_data)
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "Donation updated"


def test_delete_donation(client, created_donation_id):
    response = client.delete(f"/donations/{created_donation_id}")
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "Donation deleted"


def test_get_all_donations_received_by_user(client, created_donation_id):
    recipient_id = create_data["recipient_id"]
    response = client.get(f"/donations/received/{recipient_id}")
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "Retrieved a list of received items"
    assert "received" in response.json
