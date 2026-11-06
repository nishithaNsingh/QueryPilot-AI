from app.repositories.customer_repository import get_customer_id


def get_unique_customer_id():
    customer_id = '06b8999e2fba1a1fbc88172c00ba8bc7'
    unique_id = get_customer_id(customer_id)
    print(unique_id)


if __name__ == "__main__":
    get_unique_customer_id()
