from flask import Blueprint, request, jsonify
from .models import (
    add_donation,
    get_donation_by_id,
    update_donation_by_id,
    delete_donation_by_id,
    schema,
    get_all_donations_received_by_user_model,
)
from . import donations


@donations.route("/", methods=["POST"])
def create_donation():
    data = request.json
    errors = schema.validate(data)
    if errors:
        return (
            jsonify({"status": 400, "message": "Invalid input data", "errors": errors}),
            400,
        )
    # Add the donation to the database
    donation_id = add_donation(data)
    if donation_id:
        return (
            jsonify(
                {
                    "status": 201,
                    "message": "Donation created",
                    "donation_id": donation_id,
                }
            ),
            201,
        )
    return (
        jsonify(
            {
                "status": 500,
                "data": {},
                "message": "Internal Server Error. Please try again later.",
            }
        ),
        500,
    )


@donations.route("/<int:donation_id>", methods=["GET"])
def get_donation(donation_id):
    donation = get_donation_by_id(donation_id)
    if donation:
        return (
            jsonify(
                {
                    "status": 200,
                    "message": "Donation retrieved",
                    "donation": donation,
                }
            ),
            200,
        )
    return jsonify({"status": 404, "message": "Donation not found"}), 404


@donations.route("/<int:donation_id>", methods=["PUT"])
def update_donation(donation_id):
    # Extract data from the request
    data = request.json
    # Validate the data
    errors = schema.validate(data)
    if errors:
        return (
            jsonify({"status": 400, "message": "Invalid input data", "errors": errors}),
            400,
        )
    # Update the donation in the database
    success = update_donation_by_id(donation_id, data)
    if success:
        return jsonify({"status": 200, "message": "Donation updated"}), 200
    return jsonify({"status": 404, "message": "Donation not found"}), 404


@donations.route("/<int:donation_id>", methods=["DELETE"])
def delete_donation(donation_id):
    success = delete_donation_by_id(donation_id)
    if success:
        return jsonify({"status": 200, "message": "Donation deleted"}), 200
    return jsonify({"status": 404, "message": "Donation not found"}), 404


@donations.route("/received/<int:recipient_id>", methods=["GET"])
def get_all_donations_received_by_user(recipient_id):
    received = get_all_donations_received_by_user_model(recipient_id)
    if received:
        return (
            jsonify(
                {
                    "status": 200,
                    "message": "Retrieved a list of received items",
                    "received": received,
                }
            ),
            200,
        )
    return jsonify({"status": 404, "message": "No items received"}), 404
