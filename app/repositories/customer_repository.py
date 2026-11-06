from app.database.connection import get_connection


def get_customer_id(customer_unique_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT customer_id FROM customers WHERE customer_unique_id = ?",
            (customer_unique_id,),
        )
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def customer_exists(customer_unique_id):
    return get_customer_id(customer_unique_id) is not None