
from app.services.order_service import get_customer_active_orders


def test_customer_active_orders():

    customer_unique_id = "001ae44fa04911a9e9577356dce6c63c"

    result = get_customer_active_orders(customer_unique_id)

    print("Customer Orders:")

    for order in result:
        print(order)


if __name__ == "__main__":
    test_customer_active_orders()
