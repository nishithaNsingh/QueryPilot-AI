from app.agents.clarification_agent import generate_clarification


def main():
    ambiguity_result = {
        "clarification_required": True,
        "reason": "Multiple active orders found",
        "clarification_question": "Which order would you like to track?"
    }

    response = generate_clarification(ambiguity_result)
    print("Clarification response:", response)


if __name__ == "__main__":
    main()