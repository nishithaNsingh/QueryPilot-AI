from app.repositories.order_repository import (
    get_order_refund_details,
    verify_order_ownership,
)
from app.repositories.refund_repository import (
    create_refund_request,
    has_existing_refund_request,
)


def check_refund_eligibility(order_id, customer_unique_id):
    if not verify_order_ownership(order_id, customer_unique_id):
        return {"eligible": False, "reason": "Order not found for this customer."}

    details = get_order_refund_details(order_id)
    if not details:
        return {"eligible": False, "reason": "Order details not found."}

    status = details[0][1]
    if status == "canceled":
        return {"eligible": True, "reason": "Order was canceled."}
    if status == "delivered":
        return {"eligible": True, "reason": "Order was delivered. Return/refund review required."}
    return {"eligible": False, "reason": f"Order is currently {status}."}


def submit_refund_request(order_id, customer_unique_id, reason):
    if not reason or not reason.strip():
        return {"success": False, "message": "A refund reason is required."}

    if not verify_order_ownership(order_id, customer_unique_id):
        return {"success": False, "message": "Order not found for this customer."}

    if has_existing_refund_request(order_id):
        return {"success": False, "message": "A refund request already exists for this order."}

    eligibility = check_refund_eligibility(order_id, customer_unique_id)
    if not eligibility["eligible"]:
        return {"success": False, "message": eligibility["reason"]}

    request = create_refund_request(order_id, reason.strip())
    return {"success": True, "message": "Refund request submitted successfully.", "request": request}