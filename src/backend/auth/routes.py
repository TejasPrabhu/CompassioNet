from datetime import timedelta
from flask import Blueprint, request, jsonify, make_response
from marshmallow import Schema, fields, validate
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from . import auth
from .models import add_user, is_duplicate_email, get_user_by_email
from .utils import check_invalid_credentials
from backend.db import fetch_query


class UserSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    repeatpassword = fields.Str(required=True, validate=validate.Length(min=6))
    email = fields.Email(required=True)
    city = fields.Str(required=True)
    zipcode = fields.Str(required=True)


user_schema = UserSchema()


@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    errors = user_schema.validate(data)
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

    # Hash password
    hashed_password = generate_password_hash(password)

    # if generate_password_hash(repeat_password) != hashed_password:
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

    email = data.get("email")
    check = is_duplicate_email(email)
    if check:
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

    name = data.get("name")
    city = data.get("city")
    zipcode = data.get("zipcode")

    check = add_user(name, hashed_password, email, city, zipcode)
    if check:
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


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if check_invalid_credentials(email, password):
        return (
            jsonify(
                {"status": 400, "message": "Invalid credentials. Please try again."}
            ),
            400,
        )

    # additional_claims = {"email": email}

    access_token = create_access_token(
        identity=email,
        # additional_claims=additional_claims,
        expires_delta=timedelta(minutes=15),
    )
    refresh_token = create_refresh_token(
        identity=email,
        # additional_claims=additional_claims,
        expires_delta=timedelta(days=1),
    )

    response = make_response(
        jsonify({"login": True, "message": "Logged in successfully"}), 200
    )
    response.set_cookie(
        "access_token_cookie", access_token, httponly=True, samesite="Strict"
    )
    response.set_cookie(
        "refresh_token_cookie", refresh_token, httponly=True, samesite="Strict"
    )

    return response


@auth.route("/logout", methods=["POST"])
def logout():
    response = make_response(
        jsonify({"logout": True, "message": "Logged out successfully"}), 200
    )
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")
    return response


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(
        identity=current_user, expires_delta=timedelta(minutes=15)
    )
    response = make_response(
        jsonify({"refresh": True, "message": "Access token refreshed"}), 200
    )
    response.set_cookie(
        "access_token_cookie", access_token, httponly=True, samesite="Strict"
    )
    return response
