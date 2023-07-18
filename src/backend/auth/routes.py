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


@auth.route("/login", methods=["POST"])
def login():
    print("we are inside login")
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
    print("we are inside logout")
    response = make_response(
        jsonify({"logout": True, "message": "Logged out successfully"}), 200
    )
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")
    return response


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    print("we are inside refresh")
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
