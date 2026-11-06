from app.database.connection import get_connection

OPEN_STATUSES = ("pending", "approved")


def create_refund_request(order_id, reason):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO refund_requests (order_id, reason) VALUES (?, ?)",
            (order_id, reason),
        )
        request_id = cursor.lastrowid
        conn.commit()
        cursor.execute(
            "SELECT request_id, order_id, reason, status, created_at "
            "FROM refund_requests WHERE request_id = ?",
            (request_id,),
        )
        row = cursor.fetchone()
        return {
            "request_id": row[0],
            "order_id": row[1],
            "reason": row[2],
            "status": row[3],
            "created_at": row[4],
        }
    finally:
        conn.close()


def has_existing_refund_request(order_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        placeholders = ", ".join("?" * len(OPEN_STATUSES))
        cursor.execute(
            f"SELECT 1 FROM refund_requests "
            f"WHERE order_id = ? AND status IN ({placeholders}) LIMIT 1",
            (order_id, *OPEN_STATUSES),
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def get_refund_requests_for_order(order_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT request_id, order_id, reason, status, created_at "
            "FROM refund_requests WHERE order_id = ? "
            "ORDER BY created_at DESC, request_id DESC",
            (order_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()