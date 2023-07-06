from . import auth
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, validate
from werkzeug.security import generate_password_hash
from .models import add_user, is_duplicate_email
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
