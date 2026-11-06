from app.database.connection import get_connection


def get_seller_details(seller_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT seller_id, seller_zip_code_prefix,
                   seller_city, seller_state
            FROM sellers WHERE seller_id = ?
            """,
            (seller_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "seller_id": row[0],
            "zip_code": row[1],
            "city": row[2],
            "state": row[3],
        }
    finally:
        conn.close()


def get_seller_orders(seller_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT o.order_id, o.order_status,
                   o.order_purchase_timestamp
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE oi.seller_id = ?
            ORDER BY o.order_purchase_timestamp DESC, o.order_id
            """,
            (seller_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()