from app.services.message_service import process_message

result = process_message(
    "How long does delivery take?",
    None
)

print("\nFAQ E2E RESULT:")
print(result)