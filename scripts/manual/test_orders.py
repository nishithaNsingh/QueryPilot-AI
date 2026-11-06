
from app.repositories.order_repository import get_active_orders
from app.repositories.order_repository import get_order_items

def test_get_order_items():
    order_id = "ad21c59c0840e6cb83a9ceb5573f8159"

    items = get_order_items(order_id)

    print("Products found:", len(items))
    print(items)

def test_get_active_orders():
    customer_unique_id = "001ae44fa04911a9e9577356dce6c63c"

    orders = get_active_orders(customer_unique_id)

    print("Orders found:", len(orders))
    print("Result:", orders)



if __name__ == "__main__":
    test_get_active_orders()
    test_get_order_items()