from app.agents.intent_router import route_intent


def main():
    customer_unique_id = "001ae44fa04911a9e9577356dce6c63c"

    result = route_intent(
        intent="order_tracking",
        customer_unique_id=customer_unique_id
    )

    print(result)


if __name__ == "__main__":
    main()