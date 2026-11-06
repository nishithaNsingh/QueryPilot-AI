from app.agents.ambiguity_detector import detect_ambiguity
from app.agents.intent_classifier import classify_intent
from app.agents.entity_extractor import extract_entities

message = "Where is my order?"

intent = classify_intent(message)
entities = extract_entities(message)

result = detect_ambiguity(
    message,
    intent,
    entities
)

print("\nAmbiguity Result:")
print(result)