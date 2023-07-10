from marshmallow import Schema, fields, validate
from backend.db import execute_query, fetch_query
from backend.products.models import get_product_by_id, update_product_by_id


class DonationSchema(Schema):
    item_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)


schema = DonationSchema()


def add_donation(data):
    sql_insert_query = """INSERT INTO donations (item_id, recipient_id)
                          VALUES (%s, %s)
                          RETURNING id"""
    params = (
        data["item_id"],
        data["recipient_id"],
    )
    product_data = get_product_by_id(data["item_id"])
    if product_data["quantity"] == 0:
        return False
    product_data["quantity"] = int(product_data["quantity"]) - 1
    update_product_by_id(data["item_id"], product_data)
    return execute_query(sql_insert_query, params)


def get_donation_by_id(donation_id):
    sql_select_query = "SELECT * FROM donations WHERE id = %s"
    records = fetch_query(sql_select_query, (donation_id,))
    if records:
        return records[0]
    return None


def update_donation_by_id(donation_id, data):
    sql_update_query = """UPDATE donations SET item_id = %s, recipient_id = %s
                          WHERE id = %s"""
    params = (
        data["item_id"],
        data["recipient_id"],
        donation_id,
    )
    return execute_query(sql_update_query, params)


def delete_donation_by_id(donation_id):
    sql_delete_query = "DELETE FROM donations WHERE id = %s"
    return execute_query(sql_delete_query, (donation_id,))


def get_current_donation_id_value():
    sql_get_id_query = """SELECT LASTVAL()"""
    return execute_query(sql_get_id_query, (), return_value=True)


def get_all_donations_received_by_user_model(recipient_id):
    sql_select_query = "SELECT item_id FROM donations WHERE recipient_id = %s"
    records = fetch_query(sql_select_query, (recipient_id,))
    if records:
        product_list = []
        for k in records:
            product_list.append(k["item_id"])
        return product_list
    return None
