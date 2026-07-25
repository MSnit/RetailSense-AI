import json
import random
import joblib

from database.database import add_chat_log


# =========================================================
# PATHS
# =========================================================

MODEL_PATH = "models/chatbot_model.pkl"
VECTORIZER_PATH = "models/chatbot_vectorizer.pkl"
INTENTS_PATH = "datasets/intents.json"


# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load(MODEL_PATH)

vectorizer = joblib.load(
    VECTORIZER_PATH
)

with open(
    INTENTS_PATH,
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)


# =========================================================
# GET RESPONSE
# =========================================================

def get_response(message):

    vector = vectorizer.transform(
        [message]
    )

    probabilities = model.predict_proba(
        vector
    )[0]

    confidence = float(
        max(probabilities)
    )

    predicted_tag = model.classes_[
        probabilities.argmax()
    ]

    # Low confidence fallback
    if confidence < 0.40:

        return (
            "Sorry, I didn't understand that. "
            "Could you rephrase?",
            confidence
        )

    # Find response
    for intent in data["intents"]:

        if intent["tag"] == predicted_tag:

            response = random.choice(
                intent["responses"]
            )

            return response, confidence

    return (
        "Sorry, I couldn't find an answer.",
        confidence
    )


# =========================================================
# RUN CHATBOT
# =========================================================

def run_chatbot():

    print(
        "\n=== RetailSense AI Chatbot ==="
    )

    print(
        "Type 'exit' to return to main menu.\n"
    )

    while True:

        message = input(
            "You: "
        ).strip()

        if message.lower() == "exit":

            print(
                "Returning to main menu..."
            )

            break

        if not message:
            continue

        # Get chatbot response
        response, confidence = get_response(
            message
        )

        # Save conversation to SQLite
        try:

            add_chat_log(
                message,
                response,
                confidence
            )

            print(
                "Chat logged successfully."
            )

        except Exception as error:

            print(
                f"Chat logging failed: {error}"
            )

        # Display response
        print(
            f"Bot: {response}"
        )

        print(
            f"Confidence: "
            f"{confidence * 100:.2f}%\n"
        )


# =========================================================
# DIRECT RUN
# =========================================================

if __name__ == "__main__":

    run_chatbot()