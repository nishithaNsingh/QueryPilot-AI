CLARIFICATION_LIMIT = 3


def new_context():
    return {
        "messages": [],
        "intent": None,
        "entities": {},
        "clarification_history": [],
        "clarification_attempts": 0,
        "original_message": None,
        "awaiting_clarification": False,
    }


def update_conversation_context(
    context,
    user_message=None,
    intent=None,
    entities=None,
    clarification_response=None,
):
    if context is None:
        context = new_context()

    if user_message:
        context["messages"].append({"role": "user", "content": user_message})
        if context.get("original_message") is None:
            context["original_message"] = user_message

    if intent:
        context["intent"] = intent

    if entities:
        merged = context.get("entities") or {}
        for k, v in entities.items():
            if v is not None:
                merged[k] = v
        context["entities"] = merged

    if clarification_response:
        context["clarification_history"].append(clarification_response)
        context["clarification_attempts"] = context.get("clarification_attempts", 0) + 1
        context["messages"].append({"role": "user", "content": clarification_response})

    return context


def set_awaiting_clarification(context, awaiting=True):
    context["awaiting_clarification"] = awaiting
    return context