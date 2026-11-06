from app.services.message_service import process_message

customer_unique_id = "001ae44fa04911a9e9577356dce6c63c"

result = process_message(
    "I want a refund for order a59ef0abffbef8ddaae23600b6ee6604 because I don't want it anymore.",
    customer_unique_id
)

print("\nQueryPilot Result:")
print(result)