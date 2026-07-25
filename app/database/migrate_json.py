import json
import os

from database import get_connection, initialize_database


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATASET_DIR = os.path.join(BASE_DIR, "datasets")


def load_json(filename):

    path = os.path.join(DATASET_DIR, filename)

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def migrate():

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # CUSTOMERS
    # -------------------------

    customers = load_json("customers.json")

    for customer in customers:

        cursor.execute(
            """
            INSERT OR REPLACE INTO customers
            (customer_id, name, images)
            VALUES (?, ?, ?)
            """,
            (
                customer["customer_id"],
                customer["name"],
                customer.get("images", 0)
            )
        )

    # -------------------------
    # VISITS
    # -------------------------

    visits = load_json("visit_logs.json")

    for visit in visits:

        cursor.execute(
            """
            INSERT INTO visits
            (customer_id, timestamp)
            VALUES (?, ?)
            """,
            (
                visit["customer_id"],
                visit["timestamp"]
            )
        )

    # -------------------------
    # SENTIMENT REVIEWS
    # -------------------------

    reviews = load_json("sentiment_logs.json")

    for review in reviews:

        cursor.execute(
            """
            INSERT INTO reviews
            (review, sentiment, confidence, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (
                review["review"],
                review["sentiment"],
                review["confidence"],
                review["timestamp"]
            )
        )

    # -------------------------
    # CHATBOT LOGS
    # -------------------------

    chats = load_json("chatbot_logs.json")

    for chat in chats:

        cursor.execute(
            """
            INSERT INTO chat_logs
            (message, response, confidence, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (
                chat["message"],
                chat["response"],
                chat["confidence"],
                chat["timestamp"]
            )
        )

    conn.commit()
    conn.close()

    print("\nMigration completed successfully.")
    print(f"Customers : {len(customers)}")
    print(f"Visits    : {len(visits)}")
    print(f"Reviews   : {len(reviews)}")
    print(f"Chat Logs : {len(chats)}")


if __name__ == "__main__":
    migrate()