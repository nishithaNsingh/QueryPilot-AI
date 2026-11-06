import os
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database.connection import init_db  # noqa: E402
from app.services.message_service import (  # noqa: E402
    process_message,
    continue_conversation,
)
from app.services.conversation_service import new_context  # noqa: E402
from app.repositories.customer_repository import customer_exists  # noqa: E402


st.set_page_config(page_title="QueryPilot-AI Admin", page_icon="🛫", layout="wide")

if "initialized" not in st.session_state:
    try:
        init_db()
        st.session_state.initialized = True
    except Exception as exc:
        st.error(f"Database initialization failed: {exc}")
        st.stop()


def reset_conversation():
    st.session_state.context = new_context()
    st.session_state.messages = []
    st.session_state.pending_clarification = False


if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = new_context()
if "pending_clarification" not in st.session_state:
    st.session_state.pending_clarification = False
if "customer_unique_id" not in st.session_state:
    st.session_state.customer_unique_id = ""


with st.sidebar:
    st.markdown("## 🛫 QueryPilot-AI")
    st.caption("AI-powered e-commerce support (Admin Console)")

    st.text_input(
        "Customer Unique ID (Optional)",
        key="customer_unique_id",
        placeholder="Enter a customer_unique_id...",
        help="Leave blank and type the ID directly in the chat to search for a specific customer.",
    )

    if st.session_state.customer_unique_id:
        if customer_exists(st.session_state.customer_unique_id):
            st.success("Customer verified.")
        else:
            st.warning("Customer ID not found in the database.")

    st.divider()
    if st.button("🆕 New conversation", use_container_width=True):
        reset_conversation()
        st.rerun()
    if st.button("🧹 Clear conversation", use_container_width=True):
        reset_conversation()
        st.rerun()

    st.divider()
    st.markdown(
        """
**What I can do**
- 📦 Track orders ("where is my latest order?")
- 🔍 Admin Search ("find this customer <id> active orders")
- 💸 Process refunds (delivered / canceled orders)
- 🏷️ Look up sellers by ID
- 🛍️ Search products by category or product ID
- ❓ Answer FAQs (payment, delivery, cancellation)
"""
    )
    if not os.getenv("OPENROUTER_API_KEY"):
        st.warning("OPENROUTER_API_KEY is not set. LLM features will fall back gracefully.")


st.title("QueryPilot-AI Chat")
st.caption("Ask about orders, refunds, sellers, products, or paste a Customer ID to search directly.")


def render_result(result):
    if not isinstance(result, dict):
        return
    
    # 1. Render Orders Table
    if result.get("orders"):
        rows = []
        for o in result["orders"]:
            rows.append({
                "Order ID": o.get("order_id", "Unknown"),
                "Status": o.get("order_status") or o.get("status", "Unknown"),
                "Purchase Date": o.get("purchase_timestamp") or o.get("purchase_date", "Unknown"),
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
        
    # 2. Render Products
    if result.get("products"):
        for p in result["products"]:
            with st.container(border=True):
                st.markdown(f"**Product ID:** `{p['product_id']}`")
                st.caption(
                    f"Category: {p.get('category_english') or p.get('category') or '—'}  ·  "
                    f"Weight: {p.get('weight_g') or '—'} g"
                )
                
    # 3. Render Seller
    if result.get("seller"):
        s = result["seller"]
        st.markdown(
            f"**Seller:** `{s['seller_id']}`  \n"
            f"**Location:** {s.get('city') or '—'}, {s.get('state') or '—'}  \n"
            f"**Orders:** {result.get('order_count', 0)}"
        )
        
    # 4. Render Refund Request
    if result.get("request"):
        st.success(
            f"Refund request #{result['request']['request_id']} "
            f"is **{result['request']['status']}**."
        )

# Replay chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("result"):
            render_result(msg["result"])

placeholder = (
    "Answer the clarification…"
    if st.session_state.pending_clarification
    else "Ask about an order, refund, seller, product, or FAQ…"
)

user_input = st.chat_input(placeholder)
if user_input:
    # No blocking check here — admin can search via chat freely.

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                if st.session_state.pending_clarification:
                    out = continue_conversation(
                        st.session_state.context,
                        st.session_state.customer_unique_id,
                        user_input,
                    )
                else:
                    out = process_message(
                        user_input,
                        st.session_state.customer_unique_id,
                        st.session_state.context,
                    )
            except Exception as exc:  # noqa: BLE001
                out = {
                    "status": "error",
                    "response": f"Unexpected error: {exc}",
                    "context": st.session_state.context,
                    "result": None,
                }

        st.session_state.context = out.get("context") or st.session_state.context
        st.session_state.pending_clarification = (
            out.get("status") == "clarification_required"
        )

        response_text = out.get("response") or "(no response)"
        st.markdown(response_text)
        render_result(out.get("result"))

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text,
            "result": out.get("result"),
        }
    )