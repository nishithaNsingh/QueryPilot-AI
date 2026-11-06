from app.database.connection import get_connection


def create_refund_requests_table():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS refund_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


def create_faqs_table():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faqs (
                faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def create_faqs_unique_index():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_faqs_question
            ON faqs(question)
        """)
        conn.commit()
    finally:
        conn.close()