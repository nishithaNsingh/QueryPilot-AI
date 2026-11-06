import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "olist.sqlite"


def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. "
            "Place the Olist SQLite file at data/olist.sqlite."
        )
    return sqlite3.connect(str(DB_PATH))


def init_db():
    """Create app-managed tables and seed FAQs idempotently."""
    from app.database.schema import (
        create_refund_requests_table,
        create_faqs_table,
        create_faqs_unique_index,
    )
    from app.repositories.faq_repository import insert_faqs

    create_refund_requests_table()
    create_faqs_table()
    create_faqs_unique_index()
    insert_faqs()