import json
from unittest.mock import MagicMock

from app.agents import intent_classifier, entity_extractor, ambiguity_detector


def _fake_llm(content):
    m = MagicMock()
    m.invoke.return_value = MagicMock(content=content)
    return m


def test_classify_intent_mocked(monkeypatch):
    monkeypatch.setattr(
        intent_classifier, "get_llm", lambda: _fake_llm("order_tracking")
    )
    assert intent_classifier.classify_intent("where is my order") == "order_tracking"


def test_classify_intent_unknown_on_error(monkeypatch):
    def boom():
        raise RuntimeError("rate limited")

    monkeypatch.setattr(intent_classifier, "get_llm", boom)
    assert intent_classifier.classify_intent("hello") == "unknown"


def test_extract_entities_strips_code_fence(monkeypatch):
    payload = {"order_id": "O1", "seller_id": None}
    content = "```json\n" + json.dumps(payload) + "\n```"
    monkeypatch.setattr(entity_extractor, "get_llm", lambda: _fake_llm(content))
    out = entity_extractor.extract_entities("track O1")
    assert out["order_id"] == "O1"
    assert out["refund_reason"] is None


def test_ambiguity_detector_parses_json(monkeypatch):
    payload = {
        "clarification_required": True,
        "reason": "missing order",
        "clarification_question": "Which order?",
    }
    monkeypatch.setattr(ambiguity_detector, "get_llm", lambda: _fake_llm(json.dumps(payload)))
    out = ambiguity_detector.detect_ambiguity("track", "order_tracking", {})
    assert out["clarification_required"] is True
    assert out["clarification_question"] == "Which order?"