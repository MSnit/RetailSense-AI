import joblib
import json
import os
from datetime import datetime
from database.database import add_review

MODEL_PATH = "models/sentiment_model.pkl"
VECTORIZER_PATH = "models/sentiment_vectorizer.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def analyze_sentiment(text):
    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]
    confidence = max(probabilities)

    return prediction, confidence


def run_sentiment_analysis():
    print("\n=== Customer Sentiment Analysis ===")

    review = input("Enter customer review: ")

    sentiment, confidence = analyze_sentiment(review)

    add_review(
    review,
    sentiment,
    confidence
)

    

    print(f"\nSentiment  : {sentiment}")
    print(f"Confidence : {confidence * 100:.2f}%")


if __name__ == "__main__":
    run_sentiment_analysis()

def save_sentiment(review, sentiment, confidence):

    path = "datasets/sentiment_logs.json"

    if os.path.exists(path):
        with open(path, "r") as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append({
        "review": review,
        "sentiment": sentiment,
        "confidence": round(float(confidence), 4),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(path, "w") as file:
        json.dump(logs, file, indent=4)