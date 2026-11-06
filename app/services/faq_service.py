import re
from app.repositories.faq_repository import get_faqs

STOP_WORDS = {
    "how", "can", "you", "the", "a", "an", "is",
    "my", "i", "do", "does", "to", "for", "me",
    "what", "where", "when", "who", "why", "please",
}


def find_relevant_faq(user_question):
    faqs = get_faqs()
    query_words = {
        w for w in re.findall(r"\w+", user_question.lower())
        if len(w) > 2 and w not in STOP_WORDS
    }
    if not query_words:
        return []

    scored = []
    normalized = user_question.lower().strip().rstrip("?")
    for faq in faqs:
        faq_words = set(re.findall(r"\w+", faq[1].lower()))
        score = len(query_words & faq_words)
        if normalized and normalized in faq[1].lower():
            score += 5
        if score > 0:
            scored.append((score, faq))

    if not scored:
        return []
    scored.sort(key=lambda x: x[0], reverse=True)
    return [scored[0][1]]