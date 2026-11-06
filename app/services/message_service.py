import re
from app.agents.intent_classifier import classify_intent
from app.agents.entity_extractor import extract_entities
from app.agents.ambiguity_detector import detect_ambiguity
from app.agents.clarification_agent import generate_clarification
from app.agents.intent_router import route_intent
from app.services.conversation_service import (
    update_conversation_context,
    set_awaiting_clarification,
    CLARIFICATION_LIMIT,
)
from app.agents.order_tracking_agent import resolve_order_reference, list_orders
from app.services.order_service import get_selected_order_delivery_details
from app.services.seller_service import get_seller_order_information
from app.services.faq_service import find_relevant_faq


def format_order_response(delivery_details):
    status = delivery_details["order_status"]
    order_id = delivery_details["order_id"]
    if status == "delivered":
        when = delivery_details.get("delivered_date") or "an unknown date"
        return f"Good news! Your order {order_id} was delivered on {when}."
    eta = delivery_details.get("estimated_delivery_date") or "an unknown date"
    return (
        f"Your order {order_id} is currently {status}. "
        f"Estimated delivery: {eta}."
    )


def _dispatch(intent, customer_unique_id, entities, user_message, context):
    merged = dict(context.get("entities") or {})
    for k, v in (entities or {}).items():
        if v is not None:
            merged[k] = v

    effective_customer_id = merged.get("customer_unique_id") or customer_unique_id

    if intent == "order_tracking" and not merged.get("order_id"):
        reference = (
            merged.get("date_reference")
            or merged.get("product_name")
            or "my latest"
        )
        if effective_customer_id:
            resolved = resolve_order_reference(effective_customer_id, reference)
            if resolved:
                merged["order_id"] = resolved

    return route_intent(
        intent=intent,
        customer_unique_id=effective_customer_id,
        order_id=merged.get("order_id"),
        reason=merged.get("refund_reason"),
        seller_id=merged.get("seller_id"),
        user_message=user_message,
        context=context,
        entities=merged,
    )


def process_message(user_message, customer_unique_id, context=None):
    msg = user_message.strip()
    lower_msg = msg.lower()
    if not msg:
        return {
            "status": "error",
            "intent": None,
            "response": "Please type a message.",
            "result": None,
            "context": context,
        }

    # =========================================================
    # 1. RULE-BASED FAST PATH (Bypasses LLM entirely)
    # =========================================================
    
    # A. Product Name Query
    if "product name" in lower_msg:
        return {
            "status": "completed",
            "intent": "product_lookup",
            "response": "The Olist database does not contain product names. It only has product IDs and translated categories. Try asking for 'products in the electronics category' or 'details for product ID [ID]'.",
            "result": None,
            "context": context,
        }

    # B. FAQ Query
    if lower_msg.startswith("faq:") or lower_msg.startswith("faq "):
        question = msg[4:].strip()
        faqs = find_relevant_faq(question)
        if faqs:
            return {"status": "completed", "intent": "faq", "response": faqs[0][2], "context": context}
        return {"status": "completed", "intent": "faq", "response": "No FAQ found.", "context": context}

    # C. Find Customer / Orders (32 char hex IDs)
    match = re.search(r'\b([a-f0-9]{32})\b', lower_msg)
    if match:
        extracted_id = match.group(1)
        if "customer" in lower_msg or "order" in lower_msg:
            seller_info = get_seller_order_information(extracted_id)
            if seller_info["success"]:
                return {
                    "status": "completed",
                    "intent": "seller_lookup",
                    "response": f"Seller located in {seller_info['seller']['city']}, {seller_info['seller']['state']}. Has {seller_info['order_count']} orders.",
                    "result": seller_info,
                    "context": context,
                }
            
            res = list_orders(extracted_id, active_only=False)
            if res["success"]:
                return {
                    "status": "completed",
                    "intent": "order_tracking",
                    "response": f"Found {len(res['orders'])} orders for customer {extracted_id}.",
                    "result": res,
                    "context": context,
                }
            return {"status": "completed", "intent": "order_tracking", "response": f"No orders found for ID {extracted_id}.", "result": res, "context": context}

    # D. Order Tracking (Using Sidebar Customer ID)
    if customer_unique_id:
        if any(k in lower_msg for k in ["latest order", "recent order", "last order"]):
            resolved = resolve_order_reference(customer_unique_id, "my latest")
            if resolved:
                delivery = get_selected_order_delivery_details(resolved, customer_unique_id)
                if delivery:
                    return {
                        "status": "completed",
                        "intent": "order_tracking",
                        "response": format_order_response(delivery),
                        "result": delivery,
                        "context": context,
                    }
        elif any(k in lower_msg for k in ["oldest order", "first order"]):
            resolved = resolve_order_reference(customer_unique_id, "my oldest")
            if resolved:
                delivery = get_selected_order_delivery_details(resolved, customer_unique_id)
                if delivery:
                    return {
                        "status": "completed",
                        "intent": "order_tracking",
                        "response": format_order_response(delivery),
                        "result": delivery,
                        "context": context,
                    }
        elif "track order" in lower_msg:
            # Try to extract a specific 32-char order ID from the text
            order_match = re.search(r'\b([a-f0-9]{32})\b', lower_msg)
            if order_match:
                order_id = order_match.group(1)
                delivery = get_selected_order_delivery_details(order_id, customer_unique_id)
                if delivery:
                    return {
                        "status": "completed",
                        "intent": "order_tracking",
                        "response": format_order_response(delivery),
                        "result": delivery,
                        "context": context,
                    }
                else:
                    return {"status": "completed", "intent": "order_tracking", "response": "Order not found or not owned by this customer.", "context": context}

    # =========================================================
    # 2. LLM FALLBACK (For complex conversational queries)
    # =========================================================
    try:
        intent = classify_intent(msg)
        entities = extract_entities(msg)
    except Exception as exc:
        return {
            "status": "error",
            "intent": None,
            "response": "Assistant temporarily unavailable (LLM error).",
            "result": {"error": str(exc)},
            "context": context,
        }

    context = update_conversation_context(
        context, user_message=msg, intent=intent, entities=entities
    )

    if intent in ("order_tracking", "refund"):
        try:
            ambiguity = detect_ambiguity(msg, intent, entities)
        except Exception:
            ambiguity = {"clarification_required": False}

        if ambiguity.get("clarification_required") and not entities.get("customer_unique_id"):
            question = generate_clarification(ambiguity)
            set_awaiting_clarification(context, True)
            return {
                "status": "clarification_required",
                "intent": intent,
                "response": question,
                "result": ambiguity,
                "context": context,
            }

    result = _dispatch(intent, customer_unique_id, entities, msg, context)
    response = result.get("response") if isinstance(result, dict) else None

    return {
        "status": "completed",
        "intent": intent,
        "result": result,
        "response": response,
        "context": context,
    }


def continue_conversation(context, customer_unique_id, clarification_response):
    if context is None or not clarification_response:
        return {"status": "error", "response": "I didn't catch that. Could you please clarify?", "context": context}

    if context.get("clarification_attempts", 0) >= CLARIFICATION_LIMIT:
        set_awaiting_clarification(context, False)
        return {"status": "error", "response": "I couldn't determine what you're asking. Please start a new message.", "context": context}

    intent = context.get("intent") or "order_tracking"

    try:
        new_entities = extract_entities(clarification_response)
    except Exception:
        new_entities = {}

    context = update_conversation_context(
        context, intent=intent, entities=new_entities, clarification_response=clarification_response
    )

    if intent == "order_tracking":
        merged = context.get("entities") or {}
        if not merged.get("order_id"):
            resolved = resolve_order_reference(customer_unique_id, clarification_response)
            if resolved:
                merged["order_id"] = resolved
                context["entities"] = merged

        order_id = (context.get("entities") or {}).get("order_id")
        if order_id:
            delivery = get_selected_order_delivery_details(order_id, customer_unique_id)
            if delivery:
                set_awaiting_clarification(context, False)
                return {
                    "status": "completed",
                    "intent": intent,
                    "result": delivery,
                    "response": format_order_response(delivery),
                    "context": context,
                }

    result = _dispatch(intent, customer_unique_id, new_entities, clarification_response, context)

    if result.get("success") is False:
        set_awaiting_clarification(context, True)
        return {
            "status": "clarification_required",
            "intent": intent,
            "result": result,
            "response": result.get("response") or "Could you provide more detail?",
            "context": context,
        }

    set_awaiting_clarification(context, False)
    return {
        "status": "completed",
        "intent": intent,
        "result": result,
        "response": result.get("response"),
        "context": context,
    }