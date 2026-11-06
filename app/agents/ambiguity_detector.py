import json
import re
from app.agents.intent_classifier import get_llm


def _strip_fence(text):
    text = (text or "").strip()
    m = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.S)
    return m.group(1) if m else text


def _fallback():
    return {
        "clarification_required": True,
        "reason": "Unable to determine request clarity",
        "clarification_question": "Could you please clarify your request?",
    }


def detect_ambiguity(user_message, intent, entities):
    prompt = f"""
    You are an ambiguity detection system for an
    e-commerce customer support assistant.

    Customer message: {user_message}
    Detected intent: {intent}
    Extracted entities: {json.dumps(entities)}

    Determine whether clarification is required.

    Rules:
    - If the request is clear, clarification_required = false.
    - If important information is missing, clarification_required = true.
    - Generate one simple clarification question.
    - Never invent customer information.
    - Return valid JSON only.

    Expected format:
    {{
        "clarification_required": true,
        "reason": "Order reference is missing",
        "clarification_question": "Which order would you like to track?"
    }}
    """
    try:
        response = get_llm().invoke(prompt)
        data = json.loads(_strip_fence(response.content))
    except Exception:
        return _fallback()

    if not isinstance(data, dict) or "clarification_required" not in data:
        return _fallback()
    if data["clarification_required"] and not data.get("clarification_question"):
        data["clarification_question"] = "Could you please clarify your request?"
    return data