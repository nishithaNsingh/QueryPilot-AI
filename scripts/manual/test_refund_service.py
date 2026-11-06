from app.services.refund_service import submit_refund_request

order_id = "a59ef0abffbef8ddaae23600b6ee6604"

result = submit_refund_request(
    order_id,
    "Customer requested a refund"
)

print(result)