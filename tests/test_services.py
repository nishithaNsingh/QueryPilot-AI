from app.services import refund_service, order_service, faq_service
from app.repositories import faq_repository


def test_refund_rejects_cross_customer(temp_db):
    r = refund_service.submit_refund_request("O3", "u1", "no longer needed")
    assert r["success"] is False
    assert "not found" in r["message"].lower()


def test_refund_rejects_duplicate(temp_db):
    ok = refund_service.submit_refund_request("O1", "u1", "test")
    assert ok["success"] is True
    dup = refund_service.submit_refund_request("O1", "u1", "test")
    assert dup["success"] is False
    assert "already exists" in dup["message"].lower()


def test_refund_rejects_ineligible_status(temp_db):
    r = refund_service.submit_refund_request("O2", "u1", "test")
    assert r["success"] is False


def test_delivery_details_ownership(temp_db):
    assert order_service.get_selected_order_delivery_details("O3", "u1") is None
    d = order_service.get_selected_order_delivery_details("O1", "u1")
    assert d and d["order_status"] == "delivered"


def test_faq_idempotent_and_search(temp_db):
    assert faq_repository.insert_faqs() == 5
    assert faq_repository.insert_faqs() == 0
    hits = faq_service.find_relevant_faq("how long does delivery take")
    assert hits and "delivery" in hits[0][1].lower()