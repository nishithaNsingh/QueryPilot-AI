from app.services.seller_service import get_seller_order_information


def handle_seller_lookup(seller_id):
    result = get_seller_order_information(seller_id)
    if not result["success"]:
        return {"success": False, "response": result["message"]}

    seller = result["seller"]
    count = result.get("order_count", 0)
    if count == 0:
        msg = "Seller found, but no orders were found."
    else:
        city = seller.get("city") or "unknown city"
        state = seller.get("state") or "unknown state"
        msg = f"Seller located in {city}, {state}. This seller has {count} orders."

    return {
        "success": True,
        "response": msg,
        "seller": seller,
        "orders": result["orders"],
        "order_count": count,
    }