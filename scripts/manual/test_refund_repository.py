from app.services.refund_service import submit_refund_request

result = submit_refund_request(
    "a59ef0abffbef8ddaae23600b6ee6604",
    "Customer requested a refund"
)

print(result)