
from app.services.order_service import get_customer_active_orders
from app.agents.order_tracking_agent import (
    display_active_orders,
    select_order
)


def test_order_tracking():

    customer_unique_id = "001ae44fa04911a9e9577356dce6c63c"

    orders = get_customer_active_orders(customer_unique_id)

    order_options = display_active_orders(orders)

    if order_options:
        selected_order = select_order(order_options, 1)
        print("Final selection:", selected_order)


if __name__ == "__main__":
    test_order_tracking()
