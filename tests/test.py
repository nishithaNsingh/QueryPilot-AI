import sqlite3

conn = sqlite3.connect("data/olist.sqlite")

cursor = conn.cursor()

cursor.execute("""
SELECT 
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status;
""")

tables = cursor.fetchall()

print(tables)