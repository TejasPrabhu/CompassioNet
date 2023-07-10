import pytest
from flask import jsonify
from backend import create_app
from backend.config import TestingConfig
from backend.products.models import (
    add_product,
    get_product_by_id,
    update_product_by_id,
    delete_product_by_id,
    get_current_id_value,
)

create_data = {
    "item_name": "Test Product",
    "quantity": 10,
    "description": "This is a test product.",
    "category_id": 1,
    "donor_id": 1,
    "img_url": "https://example.com/image.jpg",
}

update_data = {
    "item_name": "Updated Product",
    "quantity": 5,
    "description": "This is a updated test product.",
    "category_id": 2,
    "donor_id": 2,
    "img_url": "https://example.com/updated-image.jpg",
}


@pytest.fixture
def created_product_id(client):
    add_product(create_data)
    product_id = get_current_id_value()[0]
    yield product_id
    delete_product_by_id(product_id)


@pytest.fixture
def delete_product_id(client):
    yield
    product_id = get_current_id_value()[0]
    delete_product_by_id(product_id)


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    return app.test_client()


def test_create_product(client, delete_product_id):
    response = client.post("/products/", json=create_data)
    assert response.status_code == 201
    assert response.json["status"] == 201
    assert response.json["message"] == "Product created"


def test_get_product(client, created_product_id):
    response = client.get(f"/products/{created_product_id}")
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "Product retrieved"
    assert "product" in response.json


def test_update_product(client, created_product_id):
    response = client.put(f"/products/{created_product_id}", json=update_data)
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "Product updated"


def test_delete_product(client, created_product_id):
    response = client.delete(f"/products/{created_product_id}")
    assert response.status_code == 200
    assert response.json["status"] == 200
    assert response.json["message"] == "Product deleted"
