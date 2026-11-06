from app.repositories import order_repository, refund_repository, customer_repository


def test_verify_order_ownership(temp_db):
    assert order_repository.verify_order_ownership("O1", "u1") is True
    assert order_repository.verify_order_ownership("O1", "u2") is False
    assert order_repository.verify_order_ownership("NOPE", "u1") is False


def test_get_customer_all_orders_order(temp_db):
    rows = order_repository.get_customer_all_orders("u1")
    assert [r[0] for r in rows] == ["O2", "O1"]


def test_order_refund_details_left_join(temp_db):
    details = order_repository.get_order_refund_details("O2")
    assert details and details[0][1] == "shipped"


def test_refund_duplicate_and_history(temp_db):
    assert refund_repository.has_existing_refund_request("O1") is False
    refund_repository.create_refund_request("O1", "test")
    assert refund_repository.has_existing_refund_request("O1") is True
    assert len(refund_repository.get_refund_requests_for_order("O1")) == 1


def test_customer_exists(temp_db):
    assert customer_repository.customer_exists("u1") is True
    assert customer_repository.customer_exists("nope") is False