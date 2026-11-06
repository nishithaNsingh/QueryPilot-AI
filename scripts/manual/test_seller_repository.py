from app.repositories.seller_repository import get_seller_orders

result = get_seller_orders(
    "3442f8959a84dea7ee197c632cb2df15"
)

print(result)