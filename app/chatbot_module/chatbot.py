import json
import random
import joblib
import os
from datetime import datetime

MODEL_PATH = "models/chatbot_model.pkl"
VECTORIZER_PATH = "models/chatbot_vectorizer.pkl"
INTENTS_PATH = "datasets/intents.json"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

with open(INTENTS_PATH, "r") as file:
    data = json.load(file)


def get_response(message):
    vector = vectorizer.transform([message])

    probabilities = model.predict_proba(vector)[0]

    confidence = max(probabilities)
    predicted_tag = model.classes_[probabilities.argmax()]

    if confidence < 0.40:
        return "Sorry, I didn't understand that. Could you rephrase?", confidence

    for intent in data["intents"]:
        if intent["tag"] == predicted_tag:
            return random.choice(intent["responses"]), confidence

    return "Sorry, I couldn't find an answer.", confidence


if __name__ == "__main__":

    print("RetailSense AI Chatbot")
    print("Type 'exit' to stop.\n")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            print("Bot: Goodbye!")
            break

        response, confidence = get_response(message)

        save_chat_log(message, response, confidence)

        print("Bot:", response)
        print(f"Confidence: {confidence * 100:.2f}%\n")


def run_chatbot():

    print("\n=== RetailSense AI Chatbot ===")
    print("Type 'exit' to return to main menu.\n")

    while True:

        message = input("You: ")

        if message.lower().strip() == "exit":
            print("Returning to main menu...")
            break

        response, confidence = get_response(message)

        print(f"Bot: {response}")
        print(f"Confidence: {confidence * 100:.2f}%\n")

def save_chat_log(message, response, confidence):

    path = "datasets/chatbot_logs.json"

    if os.path.exists(path):
        with open(path, "r") as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append({
        "message": message,
        "response": response,
        "confidence": round(float(confidence), 4),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(path, "w") as file:
        json.dump(logs, file, indent=4)

if __name__ == "__main__":
    run_chatbot()