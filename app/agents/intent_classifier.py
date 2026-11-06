import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

ALLOWED_INTENTS = {
    "order_tracking",
    "refund",
    "seller_lookup",
    "faq",
    "product_lookup",
    "unknown",
}

_llm = None


def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model="openrouter/free",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
        )
    return _llm


def classify_intent(user_message):
    prompt = f"""
    You are an intent classification system for an
    e-commerce customer support assistant.

    Classify the customer's message into exactly one category:

    - order_tracking
    - refund
    - seller_lookup
    - product_lookup
    - faq
    - unknown

    Customer message: {user_message}

    Return only the category name.
    """
    try:
        response = get_llm().invoke(prompt)
        intent = (response.content or "").strip().lower()
    except Exception:
        return "unknown"
    return intent if intent in ALLOWED_INTENTS else "unknown"