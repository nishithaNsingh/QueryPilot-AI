from app.agents.order_tracking_agent import track_customer_order


def main():
    customer_unique_id = "001ae44fa04911a9e9577356dce6c63c"

    result = track_customer_order(customer_unique_id)
    print(result)


if __name__ == "__main__":
    main()