import sqlite3
from pathlib import Path

import pytest


@pytest.fixture()
def temp_db(tmp_path, monkeypatch):
    db = tmp_path / "test.sqlite"
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            customer_unique_id TEXT
        );
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_status TEXT,
            order_purchase_timestamp TEXT,
            order_estimated_delivery_date TEXT,
            order_delivered_customer_date TEXT
        );
        CREATE TABLE order_items (
            order_id TEXT,
            product_id TEXT,
            seller_id TEXT,
            price REAL,
            freight_value REAL
        );
        CREATE TABLE order_payments (
            order_id TEXT,
            payment_type TEXT,
            payment_value REAL
        );
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_category_name TEXT,
            product_name_lenght INTEGER,
            product_description_lenght INTEGER,
            product_photos_qty INTEGER,
            product_weight_g INTEGER,
            product_length_cm INTEGER,
            product_height_cm INTEGER,
            product_width_cm INTEGER
        );
        CREATE TABLE product_category_name_translation (
            product_category_name TEXT,
            product_category_name_english TEXT
        );
        CREATE TABLE sellers (
            seller_id TEXT PRIMARY KEY,
            seller_zip_code_prefix TEXT,
            seller_city TEXT,
            seller_state TEXT
        );
        CREATE TABLE refund_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE faqs (
            faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        );
        """
    )

    cur.executemany(
        "INSERT INTO customers VALUES (?, ?)",
        [("c1", "u1"), ("c2", "u2")],
    )
    cur.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
        [
            ("O1", "c1", "delivered", "2024-01-01", "2024-01-10", "2024-01-08"),
            ("O2", "c1", "shipped", "2024-02-01", "2024-02-10", None),
            ("O3", "c2", "delivered", "2024-03-01", "2024-03-10", "2024-03-08"),
        ],
    )
    cur.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("P1", "eletronicos", 40, 100, 2, 500, 20, 10, 15),
            ("P2", "moveis", 30, 80, 1, 1000, 50, 30, 40),
        ],
    )
    cur.executemany(
        "INSERT INTO product_category_name_translation VALUES (?, ?)",
        [("eletronicos", "electronics"), ("moveis", "furniture")],
    )
    cur.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?, ?, ?)",
        [("O1", "P1", "S1", 100.0, 10.0), ("O2", "P2", "S1", 200.0, 20.0)],
    )
    cur.execute("INSERT INTO order_payments VALUES ('O1', 'credit_card', 110.0)")
    cur.execute(
        "INSERT INTO sellers VALUES ('S1', '01000', 'Sao Paulo', 'SP')"
    )
    conn.commit()
    conn.close()

    monkeypatch.setattr(
        "app.database.connection.DB_PATH", db, raising=True
    )
    yield db