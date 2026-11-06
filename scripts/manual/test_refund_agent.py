from app.agents.refund_agent import handle_refund_request

result = handle_refund_request(
    "a59ef0abffbef8ddaae23600b6ee6604",
    "Customer requested a refund"
)

print(result)