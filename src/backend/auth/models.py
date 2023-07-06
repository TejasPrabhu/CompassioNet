from backend.db import execute_query, fetch_query


def add_user(name, password, email, city, zipcode):
    sql_insert_query = """INSERT INTO users (name, password, email, city, zipcode)
                        VALUES (%s, %s, %s, %s, %s)"""
    return execute_query(sql_insert_query, (name, password, email, city, zipcode))


def is_duplicate_email(email):
    sql_select_query = "SELECT * FROM users WHERE email = %s"
    records = fetch_query(sql_select_query, (email,))
    if records:
        return True
