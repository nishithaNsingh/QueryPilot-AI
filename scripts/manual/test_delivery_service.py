from app.services.order_service import (
    get_selected_order_delivery_details
)

order_id = "a59ef0abffbef8ddaae23600b6ee6604"

result = get_selected_order_delivery_details(order_id)

if result:
    print("\nDelivery Information")
    print("--------------------")
    print(result["delivery_message"])
else:
    print("Order not found.")