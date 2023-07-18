from marshmallow import Schema, fields, validate
from backend.db import execute_query, fetch_query


class UserSchema(Schema):
    name = fields.Str(required=True)
    city = fields.Str(required=True)
    zipcode = fields.Str(required=True)
    interests = fields.List(fields.Int(), required=False)


class RegisterSchema(UserSchema):
    password = fields.Str(required=True, validate=validate.Length(min=6))
    repeatpassword = fields.Str(required=True, validate=validate.Length(min=6))
    email = fields.Email(required=True)


user_schema = UserSchema()
resiter_user_schema = RegisterSchema()


def add_user(name, password, email, city, zipcode, verification_secret):
    sql_insert_query = """INSERT INTO users (name, password, email, city, zipcode, verification_secret)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
    return execute_query(
        sql_insert_query,
        (name, password, email, city, zipcode, verification_secret),
    )


def get_user_by_id(user_id):
    sql_select_query = "SELECT * FROM users WHERE id = %s"
    records = fetch_query(sql_select_query, (user_id,))
    if records:
        return records[0]
    return None


def get_user_id_by_email(email):
    sql_select_query = "SELECT * FROM users WHERE email = %s"
    records = fetch_query(sql_select_query, (email,))
    if records:
        return records[0]["id"]
    return None


def update_user(user_id, name, city, zipcode):
    sql_update_query = (
        "UPDATE users SET name = %s, city = %s, zipcode = %s WHERE id = %s"
    )
    return execute_query(sql_update_query, (name, city, zipcode, user_id))


def update_user_verify_status(email, verified):
    sql_update_query = "UPDATE users SET verified = %s WHERE email = %s"
    return execute_query(sql_update_query, (verified, email))


def delete_user(user_id):
    sql_delete_query = "DELETE FROM users WHERE id = %s"
    return execute_query(sql_delete_query, (user_id,))


def is_duplicate_email(email):
    sql_select_query = "SELECT * FROM users WHERE email = %s"
    records = fetch_query(sql_select_query, (email,))
    if records:
        return True


def add_user_interests(user_id, interests):
    for category_id in interests:
        sql_insert_query = (
            "INSERT INTO user_interests (user_id, category_id) VALUES (%s, %s)"
        )
        if not execute_query(sql_insert_query, (user_id, category_id)):
            return False
    return True


def delete_user_interests(user_id):
    sql_delete_query = "DELETE FROM user_interests WHERE user_id = %s"
    return execute_query(sql_delete_query, (user_id,))


def get_email_from_verification_token(token):
    sql_select_query = "SELECT email FROM users WHERE verification_secret = %s"
    print(token)
    records = fetch_query(sql_select_query, (token,))
    print(records)
    if records:
        return records[0]
    return None
