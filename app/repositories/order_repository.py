from app.database.connection import get_connection

ACTIVE_STATUSES = ("approved", "created", "invoiced", "processing", "shipped")


def get_active_orders(customer_unique_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        placeholders = ", ".join("?" * len(ACTIVE_STATUSES))
        cursor.execute(
            f"""
            SELECT o.order_id, o.order_status,
                   o.order_purchase_timestamp,
                   o.order_estimated_delivery_date
            FROM customers AS c
            JOIN orders AS o ON c.customer_id = o.customer_id
            WHERE c.customer_unique_id = ?
              AND o.order_status IN ({placeholders})
            ORDER BY o.order_purchase_timestamp DESC, o.order_id
            """,
            (customer_unique_id, *ACTIVE_STATUSES),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_customer_all_orders(customer_unique_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT o.order_id, o.order_status,
                   o.order_purchase_timestamp,
                   o.order_estimated_delivery_date
            FROM customers AS c
            JOIN orders AS o ON c.customer_id = o.customer_id
            WHERE c.customer_unique_id = ?
            ORDER BY o.order_purchase_timestamp DESC, o.order_id
            """,
            (customer_unique_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_order_items(order_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.product_id,
                   p.product_category_name,
                   pd.product_category_name_english,
                   oi.price,
                   oi.freight_value
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            LEFT JOIN product_category_name_translation pd
                   ON p.product_category_name = pd.product_category_name
            WHERE oi.order_id = ?
            """,
            (order_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_order_delivery_details(order_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT order_id, order_status,
                   order_purchase_timestamp,
                   order_estimated_delivery_date,
                   order_delivered_customer_date
            FROM orders WHERE order_id = ?
            """,
            (order_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "order_id": row[0],
            "order_status": row[1],
            "purchase_timestamp": row[2],
            "estimated_delivery_date": row[3],
            "delivered_date": row[4],
        }
    finally:
        conn.close()


def get_order_refund_details(order_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT o.order_id, o.order_status,
                   p.payment_type, p.payment_value
            FROM orders o
            LEFT JOIN order_payments p ON o.order_id = p.order_id
            WHERE o.order_id = ?
            """,
            (order_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def verify_order_ownership(order_id, customer_unique_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 1
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_id = ? AND c.customer_unique_id = ?
            LIMIT 1
            """,
            (order_id, customer_unique_id),
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def get_order_by_id(order_id):
    return get_order_delivery_details(order_id)