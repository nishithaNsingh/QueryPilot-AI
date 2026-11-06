from app.services.faq_service import find_relevant_faq


def handle_faq_request(user_question):
    faqs = find_relevant_faq(user_question)
    if not faqs:
        return {
            "success": False,
            "response": (
                "Sorry, I couldn't find an answer. "
                "Please contact customer support."
            ),
        }
    faq = faqs[0]
    return {
        "success": True,
        "response": faq[2],
        "faq_id": faq[0],
        "question": faq[1],
    }