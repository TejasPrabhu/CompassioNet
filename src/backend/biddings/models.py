from marshmallow import Schema, fields, validate
from backend.db import execute_query, fetch_query


class BiddingSchema(Schema):
    item_id = fields.Int(required=True)
    bidder_id = fields.Int(required=True)


schema = BiddingSchema()


def add_bidding(data):
    sql_insert_query = """INSERT INTO biddings (item_id, bidder_id)
                          VALUES (%s, %s)
                          RETURNING id"""
    params = (
        data["item_id"],
        data["bidder_id"],
    )
    return execute_query(sql_insert_query, params)


def get_bidding_by_id(bidding_id):
    sql_select_query = "SELECT * FROM biddings WHERE id = %s"
    records = fetch_query(sql_select_query, (bidding_id,))
    if records:
        return records[0]
    return None


def update_bidding_by_id(bidding_id, data):
    sql_update_query = """UPDATE biddings SET item_id = %s, bidder_id = %s
                          WHERE id = %s"""
    params = (
        data["item_id"],
        data["bidder_id"],
        bidding_id,
    )
    return execute_query(sql_update_query, params)


def delete_bidding_by_id(bidding_id):
    sql_delete_query = "DELETE FROM biddings WHERE id = %s"
    return execute_query(sql_delete_query, (bidding_id,))


def get_current_bidding_id_value():
    sql_get_id_query = """SELECT LASTVAL()"""
    return execute_query(sql_get_id_query, (), return_value=True)


def get_all_biddings_for_item_model(item_id):
    sql_select_query = "SELECT bidder_id FROM biddings WHERE item_id = %s"
    records = fetch_query(sql_select_query, (item_id,))
    if records:
        return [item[0] for item in records]
    return None
