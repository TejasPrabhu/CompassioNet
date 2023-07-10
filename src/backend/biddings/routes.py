from flask import Blueprint, request, jsonify
from .models import (
    schema,
    add_bid,
    get_bid_by_id,
    update_bid_by_id,
    delete_bid_by_id,
    get_all_bids_for_item_model,
)

bidding = Blueprint("bidding", __name__)


@bidding.route("/", methods=["POST"])
def create_bid():
    data = request.json
    errors = schema.validate(data)
    if errors:
        return (
            jsonify({"status": 400, "message": "Invalid input data", "errors": errors}),
            400,
        )
    # Add the bid to the database
    check = add_bid(data)
    if check:
        return (
            jsonify(
                {
                    "status": 201,
                    "message": "Bid created",
                    "data": data,
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


@bidding.route("/<int:bid_id>", methods=["GET"])
def get_bid(bid_id):
    bid = get_bid_by_id(bid_id)
    if bid:
        return (
            jsonify(
                {
                    "status": 200,
                    "message": "Bid retrieved",
                    "bid": bid,
                }
            ),
            200,
        )
    return jsonify({"status": 404, "message": "Bid not found"}), 404


@bidding.route("/<int:bid_id>", methods=["PUT"])
def update_bid(bid_id):
    # Extract data from the request
    data = request.json
    # Validate the data
    errors = schema.validate(data)
    if errors:
        return (
            jsonify({"status": 400, "message": "Invalid input data", "errors": errors}),
            400,
        )
    # Update the bid in the database
    success = update_bid_by_id(bid_id, data)
    if success:
        return jsonify({"status": 200, "message": "Bid updated"}), 200
    return jsonify({"status": 404, "message": "Bid not found"}), 404


@bidding.route("/<int:bid_id>", methods=["DELETE"])
def delete_bid(bid_id):
    success = delete_bid_by_id(bid_id)
    if success:
        return jsonify({"status": 200, "message": "Bid deleted"}), 200
    return jsonify({"status": 404, "message": "Bid not found"}), 404


@bidding.route("/item/<int:item_id>", methods=["GET"])
def get_all_bids_for_item(item_id):
    bids = get_all_bids_for_item_model(item_id)
    if bids:
        return (
            jsonify(
                {
                    "status": 200,
                    "message": "Retrieved a list of bids for the item",
                    "bids": bids,
                }
            ),
            200,
        )
    else:
        return jsonify({"status": 404, "message": "No bids found for the item"}), 404
