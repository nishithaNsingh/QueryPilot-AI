from app.services.order_service import (
    get_customer_active_orders,
    get_customer_all_orders,
    get_selected_order_delivery_details,
)


LATEST_TOKENS = {"my latest", "latest", "latest order", "my latest order", "most recent"}
OLDEST_TOKENS = {"my oldest", "oldest", "oldest order", "my oldest order", "first order"}


def resolve_order_reference(customer_unique_id, reference):
    if not reference:
        return None

    reference = reference.lower().strip()

    # 1) Explicit order ID (any status)
    explicit = reference.upper()
    all_orders = get_customer_all_orders(customer_unique_id)
    for order in all_orders:
        if order["order_id"].lower() == reference:
            return order["order_id"]

    if not all_orders:
        return None

    # 2) Latest / oldest (all orders)
    if reference in LATEST_TOKENS:
        return all_orders[0]["order_id"]
    if reference in OLDEST_TOKENS:
        return all_orders[-1]["order_id"]

    # 3) Product / category match (active orders first, then all)
    for pool in (get_customer_active_orders(customer_unique_id), all_orders):
        matches = []
        for order in pool:
            for product in order.get("products", []):
                cat = (product.get("category_english") or "").lower()
                pid = (product.get("product_id") or "").lower()
                if reference and (reference in cat or reference == pid):
                    matches.append(order["order_id"])
                    break
        if len(matches) == 1:
            return matches[0]

    return None


def track_order(customer_unique_id, order_id):
    delivery = get_selected_order_delivery_details(order_id, customer_unique_id)
    if not delivery:
        return {"success": False, "response": "Order not found for this customer."}
    return {"success": True, "response": delivery["delivery_message"], "order": delivery}


def list_orders(customer_unique_id, active_only=True):
    orders = (
        get_customer_active_orders(customer_unique_id)
        if active_only
        else get_customer_all_orders(customer_unique_id)
    )
    return {"success": True, "orders": orders}