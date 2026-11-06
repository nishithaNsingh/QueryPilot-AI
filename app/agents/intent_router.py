from app.agents.order_tracking_agent import track_order
from app.agents.refund_agent import handle_refund_request
from app.agents.faq_agent import handle_faq_request
from app.agents.seller_lookup_agent import handle_seller_lookup
from app.agents.product_lookup_agent import handle_product_lookup


def route_intent(
    intent,
    customer_unique_id=None,
    order_id=None,
    reason=None,
    seller_id=None,
    user_message=None,
    context=None,
    entities=None,
):
    if intent == "order_tracking":
        if not customer_unique_id:
            return {"success": False, "response": "Customer authentication required."}
        if not order_id:
            return {
                "success": False,
                "response": (
                    "I couldn't identify which order you mean. "
                    "You can tell me the order ID, say 'my latest order', "
                    "or describe the product."
                ),
            }
        return track_order(customer_unique_id, order_id)

    if intent == "refund":
        if not customer_unique_id:
            return {"success": False, "response": "Customer authentication required."}
        if not order_id or not reason:
            return {
                "success": False,
                "response": "Please provide the order ID and a refund reason.",
            }
        return handle_refund_request(order_id, customer_unique_id, reason)

    if intent == "faq":
        if not user_message:
            return {"success": False, "response": "Please provide your question."}
        return handle_faq_request(user_message)

    if intent == "seller_lookup":
        if not seller_id:
            return {"success": False, "response": "Please provide a seller ID."}
        return handle_seller_lookup(seller_id)

    if intent == "product_lookup":
        return handle_product_lookup(entities or {})

    return {
        "success": False,
        "response": f"I'm not sure how to help with '{user_message}'.",
    }