from app.services.conversation_service import update_conversation_context

context = None

context = update_conversation_context(
    context,
    user_message="Where is my order?",
    intent="order_tracking",
    entities={"order_id": None}
)

context = update_conversation_context(
    context,
    clarification_response="My latest order"
)

print(context)