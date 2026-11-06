from app.agents.intent_classifier import classify_intent

message = "Where is my order?"

print(classify_intent(message))