import json
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


with open("datasets/intents.json", "r") as file:
    data = json.load(file)


texts = []
labels = []

for intent in data["intents"]:

    for pattern in intent["patterns"]:
        texts.append(pattern)
        labels.append(intent["tag"])


vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(texts)


model = LogisticRegression(
    max_iter=1000
)

model.fit(X, labels)


os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/chatbot_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/chatbot_vectorizer.pkl"
)


print("Chatbot model trained successfully.")
print("Training samples:", len(texts))
print("Intents:", model.classes_)