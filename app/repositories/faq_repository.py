from app.database.connection import get_connection


def get_faqs():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT faq_id, question, answer FROM faqs")
        return cursor.fetchall()
    finally:
        conn.close()


def insert_faqs():
    """Idempotent seed. Returns number of NEW rows inserted."""
    faqs = [
        ("How can I track my order?",
         "You can track your order using your order ID."),
        ("How long does delivery take?",
         "Delivery time depends on the seller and shipping location."),
        ("Can I cancel my order?",
         "Order cancellation depends on the current order status."),
        ("How do I request a refund?",
         "You can request a refund through customer support."),
        ("How can I contact the seller?",
         "You can find seller details through your order information."),
    ]

    conn = get_connection()
    try:
        cursor = conn.cursor()
        before = cursor.execute("SELECT COUNT(*) FROM faqs").fetchone()[0]
        cursor.executemany(
            "INSERT OR IGNORE INTO faqs (question, answer) VALUES (?, ?)",
            faqs,
        )
        conn.commit()
        after = cursor.execute("SELECT COUNT(*) FROM faqs").fetchone()[0]
        return after - before
    finally:
        conn.close()


def search_faq(search_term):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        words = search_term.lower().split()
        if not words:
            return []
        conditions = " AND ".join(["LOWER(question) LIKE ?" for _ in words])
        cursor.execute(
            f"SELECT faq_id, question, answer FROM faqs WHERE {conditions}",
            tuple(f"%{w}%" for w in words),
        )
        return cursor.fetchall()
    finally:
        conn.close()