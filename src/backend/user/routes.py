import os
import secrets
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash
from . import user
from backend.db import fetch_query
from .models import (
    add_user,
    is_duplicate_email,
    user_schema,
    resiter_user_schema,
    get_user_by_id,
    update_user,
    delete_user,
    delete_user_interests,
    add_user_interests,
    get_email_from_verification_token,
    get_user_id_by_email,
    update_user_verify_status,
)
from .utils import (
    send_verification_email,
)

DOMAIN_URL = os.environ.get("DOMAIN_URL")


@user.route("/register", methods=["POST"])
def register():
    data = request.json
    errors = resiter_user_schema.validate(data)
    if errors:
        return (
            jsonify(
                {
                    "status": 400,
                    "data": {},
                    "message": "Invalid input data. Please check and try again.",
                    "errors": errors,
                }
            ),
            400,
        )

    password = data.get("password")
    repeat_password = data.get("repeatpassword")

    if repeat_password != password:
        return (
            jsonify(
                {
                    "status": 400,
                    "data": {},
                    "message": "Invalid input data. Please check and try again.",
                }
            ),
            400,
        )

    hashed_password = generate_password_hash(password)
    email = data.get("email")
    check = is_duplicate_email(email)
    if check:
        return (
            jsonify(
                {
                    "status": 500,
                    "data": {},
                    "message": "Email already exists. Please try to login with the same email",
                }
            ),
            500,
        )

    name = data.get("name")
    city = data.get("city")
    zipcode = data.get("zipcode")
    interests = data.get("interests", [])

    token = str(secrets.token_urlsafe(32))
    check = add_user(name, hashed_password, email, city, zipcode, token)
    user_id = get_user_id_by_email(email)
    interests_check = add_user_interests(user_id, interests)

    if check and interests_check:
        # Send verification email
        verification_link = f"http://{DOMAIN_URL}/user/verify-email/{token}"
        send_verification_email(email, verification_link)

        return (
            jsonify(
                {
                    "status": 201,
                    "data": data,
                    "message": "Your registration request has been received. Please check your email for further instructions.",
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


@user.route("/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return jsonify(
            {
                "status": 200,
                "data": user_data,
                "message": "User profile retrieved successfully",
            }
        )
    return jsonify({"status": 404, "data": {}, "message": "User not found"})


@user.route("/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    data = request.json
    errors = user_schema.validate(data)
    if errors:
        return (
            jsonify(
                {
                    "status": 400,
                    "data": {},
                    "message": "Invalid input data",
                    "errors": errors,
                }
            ),
            400,
        )

    if not get_user_by_id(user_id):
        return jsonify({"status": 404, "data": {}, "message": "User not found"})

    name = data.get("name")
    city = data.get("city")
    zipcode = data.get("zipcode")
    interests = data.get("interests", [])

    updated = update_user(user_id, name, city, zipcode)
    delete_check = delete_user_interests(user_id)
    interests_check = add_user_interests(user_id, interests)

    if updated and delete_check and interests_check:
        return (
            jsonify(
                {
                    "status": 200,
                    "data": data,
                    "message": "User profile updated successfully",
                }
            ),
            200,
        )
    return jsonify({"status": 500, "data": {}, "message": "Internal Server Error"}), 500


@user.route("/<int:user_id>", methods=["DELETE"])
def delete_profile(user_id):
    if not get_user_by_id(user_id):
        return jsonify({"status": 404, "data": {}, "message": "User not found"}), 404

    deleted = delete_user(user_id)
    if deleted:
        return (
            jsonify(
                {
                    "status": 200,
                    "data": {},
                    "message": "User profile deleted successfully",
                },
            ),
            200,
        )
    return jsonify({"status": 500, "data": {}, "message": "Internal Server Error"}), 500


@user.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    email = get_email_from_verification_token(token)
    if email and update_user_verify_status(email, True):
        return (
            jsonify(
                {
                    "status": 200,
                    "data": {},
                    "message": "Email verified successfully.",
                }
            ),
            200,
        )
    return (
        jsonify(
            {
                "status": 200,
                "data": {},
                "message": "Invalid Verification token",
            }
        ),
        200,
    )
