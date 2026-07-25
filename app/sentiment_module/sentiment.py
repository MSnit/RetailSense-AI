from textblob import TextBlob


def analyze_sentiment(text):
    score = TextBlob(text).sentiment.polarity

    if score > 0.1:
        sentiment = "Positive"
    elif score < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, score


review = input("Enter customer review: ")

sentiment, score = analyze_sentiment(review)

print("Sentiment:", sentiment)
print("Score:", round(score, 2))