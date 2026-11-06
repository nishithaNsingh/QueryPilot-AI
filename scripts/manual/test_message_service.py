from app.services import message_service
from app.services.conversation_service import new_context


def _stub_agents(monkeypatch, intent="order_tracking", entities=None, ambiguity=None):
    monkeypatch.setattr(message_service, "classify_intent", lambda _m: intent)
    monkeypatch.setattr(
        message_service, "extract_entities",
        lambda _m: entities if entities is not None else {
            "order_id": None, "seller_id": None, "product_name": None,
            "product_id": None, "category": None,
            "date_reference": None, "customer_reference": None,
            "refund_reason": None,
        },
    )
    monkeypatch.setattr(
        message_service, "detect_ambiguity",
        lambda *_a, **_k: ambiguity or {"clarification_required": False},
    )


def test_process_message_completes(monkeypatch, temp_db):
    _stub_agents(monkeypatch, entities={"order_id": "O1"})
    out = message_service.process_message("track O1", "u1", new_context())
    assert out["status"] == "completed"
    assert out["intent"] == "order_tracking"
    assert out["result"]["success"] is True


def test_clarification_flow(monkeypatch, temp_db):
    _stub_agents(
        monkeypatch,
        ambiguity={
            "clarification_required": True,
            "clarification_question": "Which order?",
        },
    )
    first = message_service.process_message("track my order", "u1", new_context())
    assert first["status"] == "clarification_required"
    assert first["response"] == "Which order?"

    second = message_service.continue_conversation(
        first["context"], "u1", "my latest"
    )
    assert second["status"] == "completed"
    assert second["result"]["success"] is True


def test_message_service_survives_llm_failure(monkeypatch, temp_db):
    def boom(_):
        raise RuntimeError("openrouter 429")

    monkeypatch.setattr(message_service, "classify_intent", boom)
    out = message_service.process_message("hi", "u1", new_context())
    assert out["status"] == "error"
    assert "unavailable" in out["response"].lower()