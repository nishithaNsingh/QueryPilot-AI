from app.repositories.order_repository import get_order_delivery_details

order_id = "a59ef0abffbef8ddaae23600b6ee6604"

result = get_order_delivery_details(order_id)

if result:
    print("Order Delivery Details")
    print("----------------------")

    for key, value in result.items():
        print(f"{key}: {value}")
else:
    print("Order not found.")