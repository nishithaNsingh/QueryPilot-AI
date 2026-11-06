import json
import re
from app.agents.intent_classifier import get_llm


def _strip_fence(text):
    text = (text or "").strip()
    m = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.S)
    return m.group(1) if m else text


# Added customer_unique_id
EMPTY = {
    "order_id": None,
    "seller_id": None,
    "product_name": None,
    "product_id": None,
    "category": None,
    "date_reference": None,
    "customer_reference": None,
    "customer_unique_id": None, 
    "refund_reason": None,
}


def extract_entities(user_message):
    prompt = f"""
You are an entity extraction system.

Extract information from the customer message.

Fields:
- order_id
- seller_id
- product_name
- product_id
- category
- date_reference
- customer_reference
- customer_unique_id (this is a 32-character hex string)
- refund_reason

Rules:
1. Extract dates exactly as mentioned (e.g., "yesterday", "last week").
2. Never convert relative dates into actual dates.
3. Return null only when the information is absent.
4. Do not invent information.
5. Return valid JSON only (use null, not None).

Customer message: {user_message}

Return:
{{
    "order_id": null,
    "seller_id": null,
    "product_name": null,
    "product_id": null,
    "category": null,
    "date_reference": null,
    "customer_reference": null,
    "customer_unique_id": null,
    "refund_reason": null
}}
"""
    try:
        response = get_llm().invoke(prompt)
        data = json.loads(_strip_fence(response.content))
    except Exception:
        return dict(EMPTY)

    if not isinstance(data, dict):
        return dict(EMPTY)
    return {**EMPTY, **data}