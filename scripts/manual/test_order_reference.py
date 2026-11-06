from app.agents.order_tracking_agent import resolve_order_reference

customer_unique_id = "001ae44fa04911a9e9577356dce6c63c"

reference = "my latest"

result = resolve_order_reference(
    customer_unique_id,
    reference
)

print("Resolved Order ID:", result)