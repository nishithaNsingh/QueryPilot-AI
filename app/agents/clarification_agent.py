def generate_clarification(ambiguity_result):
    """Return the clarification question as a string (never blocks on input)."""
    if not ambiguity_result or not ambiguity_result.get("clarification_required"):
        return None
    return (
        ambiguity_result.get("clarification_question")
        or "Could you please clarify your request?"
    )