from marshmallow import Schema, fields, validate
from backend.db import execute_query, fetch_query


class ProductSchema(Schema):
    item_name = fields.Str(required=True, validate=validate.Length(max=1000))
    quantity = fields.Int(required=True, validate=validate.Range(min=0))
    description = fields.Str(required=True, validate=validate.Length(max=1000))
    category_id = fields.Int(required=True)
    donor_id = fields.Int(required=True)
    img_url = fields.Str(validate=validate.Length(max=1000))


schema = ProductSchema()


def add_product(data):
    sql_insert_query = """INSERT INTO items (item_name, quantity, description, category_id, donor_id, img_url)
                          VALUES (%s, %s, %s, %s, %s, %s)
                          RETURNING id"""
    params = (
        data["item_name"],
        data["quantity"],
        data["description"],
        data["category_id"],
        data["donor_id"],
        data["img_url"],
    )
    return execute_query(sql_insert_query, params)


def get_product_by_id(product_id):
    sql_select_query = "SELECT * FROM items WHERE id = %s"
    records = fetch_query(sql_select_query, (product_id,))
    if records:
        return records[0]
    return None


def update_product_by_id(product_id, data):
    sql_update_query = """UPDATE items SET item_name = %s, quantity = %s, description = %s, category_id = %s, donor_id = %s, img_url = %s
                          WHERE id = %s"""
    params = (
        data["item_name"],
        data["quantity"],
        data["description"],
        data["category_id"],
        data["donor_id"],
        data["img_url"],
        product_id,
    )
    return execute_query(sql_update_query, params)


def delete_product_by_id(product_id):
    sql_delete_query = "DELETE FROM items WHERE id = %s"
    return execute_query(sql_delete_query, (product_id,))


def get_current_id_value():
    sql_get_id_query = """SELECT LASTVAL()"""
    return execute_query(sql_get_id_query, (), return_value=True)
