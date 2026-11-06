from app.services.refund_service import submit_refund_request


def handle_refund_request(order_id, customer_unique_id, reason):
    result = submit_refund_request(order_id, customer_unique_id, reason)
    if not result["success"]:
        return {
            "success": False,
            "response": f"Sorry, your refund request cannot proceed. {result['message']}",
            "result": result,
        }
    return {
        "success": True,
        "response": "Your refund request has been submitted successfully.",
        "request": result["request"],
        "result": result,
    }