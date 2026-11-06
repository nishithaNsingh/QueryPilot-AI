from app.database.connection import get_connection

PRODUCT_COLUMNS = """
    p.product_id,
    p.product_category_name,
    t.product_category_name_english,
    p.product_name_lenght,
    p.product_description_lenght,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
"""


def _row_to_product(row):
    return {
        "product_id": row[0],
        "category": row[1],
        "category_english": row[2],
        "name_length": row[3],
        "description_length": row[4],
        "photos_qty": row[5],
        "weight_g": row[6],
        "length_cm": row[7],
        "height_cm": row[8],
        "width_cm": row[9],
    }


def search_products(query, limit=10):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        like = f"%{query.lower()}%"
        cursor.execute(
            f"""
            SELECT {PRODUCT_COLUMNS}
            FROM products p
            LEFT JOIN product_category_name_translation t
                   ON p.product_category_name = t.product_category_name
            WHERE LOWER(p.product_id) LIKE ?
               OR LOWER(p.product_category_name) LIKE ?
               OR LOWER(t.product_category_name_english) LIKE ?
            ORDER BY p.product_id
            LIMIT ?
            """,
            (like, like, like, limit),
        )
        return [_row_to_product(r) for r in cursor.fetchall()]
    finally:
        conn.close()


def get_product_details(product_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT {PRODUCT_COLUMNS}
            FROM products p
            LEFT JOIN product_category_name_translation t
                   ON p.product_category_name = t.product_category_name
            WHERE p.product_id = ?
            """,
            (product_id,),
        )
        row = cursor.fetchone()
        return _row_to_product(row) if row else None
    finally:
        conn.close()


def get_products_by_category(category, limit=10):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        like = f"%{category.lower()}%"
        cursor.execute(
            f"""
            SELECT {PRODUCT_COLUMNS}
            FROM products p
            LEFT JOIN product_category_name_translation t
                   ON p.product_category_name = t.product_category_name
            WHERE LOWER(t.product_category_name_english) LIKE ?
               OR LOWER(p.product_category_name) LIKE ?
            ORDER BY p.product_id
            LIMIT ?
            """,
            (like, like, limit),
        )
        return [_row_to_product(r) for r in cursor.fetchall()]
    finally:
        conn.close()


def get_product_categories():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT product_category_name_english
            FROM product_category_name_translation
            WHERE product_category_name_english IS NOT NULL
            ORDER BY product_category_name_english
            """
        )
        return [r[0] for r in cursor.fetchall()]
    finally:
        conn.close()