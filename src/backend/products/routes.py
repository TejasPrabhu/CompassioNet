from flask import Blueprint, request, jsonify
from .models import (
    add_product,
    get_product_by_id,
    update_product_by_id,
    delete_product_by_id,
    schema,
)
from . import products


@products.route("/", methods=["POST"])
def create_product():
    data = request.json
    errors = schema.validate(data)
    if errors:
        return (
            jsonify({"status": 400, "message": "Invalid input data", "errors": errors}),
            400,
        )
    # Add the product to the database
    product_id = add_product(data)
    return (
        jsonify(
            {
                "status": 201,
                "message": "Product created",
                "product_id": product_id,
            }
        ),
        201,
    )


@products.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    # Retrieve the product from the database
    product = get_product_by_id(product_id)
    if product:
        return (
            jsonify(
                {
                    "status": 200,
                    "message": "Product retrieved",
                    "product": product,
                }
            ),
            200,
        )
    else:
        return jsonify({"status": 404, "message": "Product not found"}), 404


@products.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    # Extract data from the request
    data = request.json
    # Validate the data
    errors = schema.validate(data)
    if errors:
        return (
            jsonify({"status": 400, "message": "Invalid input data", "errors": errors}),
            400,
        )
    # Update the product in the database
    success = update_product_by_id(product_id, data)
    if success:
        return jsonify({"status": 200, "message": "Product updated"}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404


@products.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    success = delete_product_by_id(product_id)
    if success:
        return jsonify({"status": 200, "message": "Product deleted"}), 200
    return jsonify({"status": 404, "message": "Product not found"}), 404
