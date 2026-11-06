from app.repositories.seller_repository import get_seller_details, get_seller_orders


def get_seller_information(seller_id):
    seller = get_seller_details(seller_id)
    if not seller:
        return {"success": False, "message": "Seller not found."}
    return {"success": True, "seller": seller}


def get_seller_order_information(seller_id):
    result = get_seller_information(seller_id)
    if not result["success"]:
        return result

    orders = get_seller_orders(seller_id)
    order_list = [
        {"order_id": o[0], "status": o[1], "purchase_date": o[2]}
        for o in orders
    ]
    return {
        "success": True,
        "seller": result["seller"],
        "orders": order_list,
        "order_count": len(order_list),
    }