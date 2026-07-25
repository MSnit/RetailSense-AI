import os
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("datasets/sentiment_training.csv")

X = data["review"]
y = data["sentiment"]

# Convert text into numerical features
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X_vectorized = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression(
    max_iter=1000
)

model.fit(X_vectorized, y)

# Create model directory
os.makedirs("models", exist_ok=True)

# Save trained model
joblib.dump(
    model,
    "models/sentiment_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/sentiment_vectorizer.pkl"
)

print("Sentiment model trained successfully.")
print("Training samples:", len(data))
print("Classes:", model.classes_)