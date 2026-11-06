from app.repositories.order_repository import (
    get_active_orders as _repo_get_active_orders,
    get_customer_all_orders as _repo_get_all_orders,
    get_order_items,
    get_order_delivery_details,
    verify_order_ownership,
)


def _build_order(order_row):
    order_id = order_row[0]
    items = get_order_items(order_id)
    return {
        "order_id": order_row[0],
        "order_status": order_row[1],
        "purchase_timestamp": order_row[2],
        "estimated_delivery_date": order_row[3],
        "products": [
            {
                "product_id": i[0],
                "category": i[1],
                "category_english": i[2],
                "price": i[3],
                "freight_value": i[4],
            }
            for i in items
        ],
    }


def get_customer_active_orders(customer_unique_id):
    return [_build_order(o) for o in _repo_get_active_orders(customer_unique_id)]


def get_customer_all_orders(customer_unique_id):
    return [_build_order(o) for o in _repo_get_all_orders(customer_unique_id)]


def get_selected_order_delivery_details(order_id, customer_unique_id=None):
    if customer_unique_id is not None:
        if not verify_order_ownership(order_id, customer_unique_id):
            return None

    details = get_order_delivery_details(order_id)
    if not details:
        return None

    if details["order_status"] == "delivered":
        when = details["delivered_date"] or "an unknown date"
        details["delivery_message"] = f"Your order was delivered on {when}."
    else:
        eta = details["estimated_delivery_date"] or "an unknown date"
        details["delivery_message"] = (
            f"Your order is currently {details['order_status']}. "
            f"Estimated delivery date: {eta}."
        )
    return details