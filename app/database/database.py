import os
import sqlite3


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "retailsense.db"
)


# =========================================================
# CONNECTION
# =========================================================

def get_connection():

    return sqlite3.connect(DATABASE_PATH)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            images INTEGER DEFAULT 0,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Visits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # Reviews
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review TEXT NOT NULL,
            sentiment TEXT,
            confidence REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Chat logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            response TEXT,
            confidence REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

     # Product detections
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            count INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

    conn.commit()
    conn.close()


# =========================================================
# VISIT
# =========================================================

def add_visit(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO visits (customer_id)
        VALUES (?)
        """,
        (customer_id,)
    )

    conn.commit()
    conn.close()


# =========================================================
# SENTIMENT REVIEW
# =========================================================

def add_review(review, sentiment, confidence):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reviews
        (review, sentiment, confidence)
        VALUES (?, ?, ?)
        """,
        (
            review,
            sentiment,
            float(confidence)
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# CHATBOT LOG
# =========================================================

def add_chat_log(message, response, confidence):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_logs
        (message, response, confidence)
        VALUES (?, ?, ?)
        """,
        (
            message,
            response,
            float(confidence)
        )
    )

    conn.commit()
    conn.close()

def add_customer(customer_id, name, images):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO customers
        (customer_id, name, images)
        VALUES (?, ?, ?)
        """,
        (
            customer_id,
            name,
            int(images)
        )
    )

    conn.commit()
    conn.close()

def get_all_customers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, name, images
        FROM customers
        ORDER BY customer_id
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "customer_id": row[0],
            "name": row[1],
            "images": row[2]
        }
        for row in rows
    ]


def get_customer_name(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM customers
        WHERE customer_id = ?
        """,
        (customer_id,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]

    return "Unknown"


def generate_next_customer_id():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id
        FROM customers
    """)

    rows = cursor.fetchall()
    conn.close()

    numbers = []

    for row in rows:

        customer_id = row[0]

        try:
            numbers.append(
                int(customer_id.split("-")[1])
            )
        except (IndexError, ValueError):
            continue

    next_number = max(numbers, default=0) + 1

    return f"RS-{next_number:03d}"

def add_product_log(product, count):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO product_logs
        (product, count)
        VALUES (?, ?)
        """,
        (
            product,
            int(count)
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# DIRECT RUN
# =========================================================

if __name__ == "__main__":

    initialize_database()

    print(
        "RetailSense database initialized successfully."
    )