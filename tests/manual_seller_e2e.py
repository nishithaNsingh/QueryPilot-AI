from app.services.message_service import process_message

result = process_message(
    "Show me details for seller 3442f8959a84dea7ee197c632cb2df15",
    None
)

print("\nSELLER E2E RESULT:")
print(result)