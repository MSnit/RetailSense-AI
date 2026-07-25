import streamlit as st
import json
import os
import pandas as pd


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RetailSense AI",
    page_icon="🛒",
    layout="wide"
)


# =========================================================
# DATA PATHS
# =========================================================

CUSTOMERS_FILE = "datasets/customers.json"
VISITS_FILE = "datasets/visit_logs.json"
SENTIMENT_FILE = "datasets/sentiment_logs.json"
CHATBOT_FILE = "datasets/chatbot_logs.json"


# =========================================================
# DATA LOADER
# =========================================================

def load_json(path):

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


# =========================================================
# LOAD DATA
# =========================================================

customers = load_json(CUSTOMERS_FILE)
visits = load_json(VISITS_FILE)
sentiments = load_json(SENTIMENT_FILE)
chat_logs = load_json(CHATBOT_FILE)


# =========================================================
# SIDEBAR
# =========================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Customers",
        "Product Intelligence",
        "Sentiment Analytics",
        "Chatbot Analytics"
    ]
)


# =========================================================
# HEADER
# =========================================================

st.title("🛒 RetailSense AI")
st.caption("Smart Retail & Customer Intelligence Platform")

st.divider()


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.header("Dashboard Overview")

    # -------------------------
    # METRICS
    # -------------------------

    unique_visitors = len(
        {
            visit.get("customer_id")
            for visit in visits
            if visit.get("customer_id")
        }
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Registered Customers",
        len(customers)
    )

    col2.metric(
        "Total Visits",
        len(visits)
    )

    col3.metric(
        "Unique Visitors",
        unique_visitors
    )

    col4.metric(
        "Customer Reviews",
        len(sentiments)
    )

    st.divider()

    # -------------------------
    # CUSTOMER DATABASE
    # -------------------------

    st.subheader("👥 Customer Database")

    if customers:

        customer_df = pd.DataFrame(customers)

        st.dataframe(
            customer_df,
            use_container_width=True
        )

    else:

        st.info("No customers registered yet.")

    st.divider()

    # -------------------------
    # RECENT VISITS
    # -------------------------

    st.subheader("🕒 Recent Visits")

    if visits:

        visits_df = pd.DataFrame(visits)

        st.dataframe(
            visits_df.tail(10),
            use_container_width=True
        )

    else:

        st.info("No visits recorded yet.")

    st.divider()

    # -------------------------
    # CUSTOMER VISIT ANALYTICS
    # -------------------------

    st.subheader("📊 Customer Visit Analytics")

    if visits:

        visits_df = pd.DataFrame(visits)

        if "customer_id" in visits_df.columns:

            visit_counts = (
                visits_df["customer_id"]
                .value_counts()
                .reset_index()
            )

            visit_counts.columns = [
                "Customer ID",
                "Visits"
            ]

            st.bar_chart(
                visit_counts,
                x="Customer ID",
                y="Visits"
            )

        # -------------------------
        # VISITS OVER TIME
        # -------------------------

        if "timestamp" in visits_df.columns:

            st.subheader("Visits Over Time")

            timeline_df = visits_df.copy()

            timeline_df["timestamp"] = pd.to_datetime(
                timeline_df["timestamp"],
                errors="coerce"
            )

            timeline_df = timeline_df.dropna(
                subset=["timestamp"]
            )

            if not timeline_df.empty:

                daily_visits = (
                    timeline_df
                    .set_index("timestamp")
                    .resample("D")
                    .size()
                )

                st.line_chart(daily_visits)

    else:

        st.info("No visit analytics available.")


# =========================================================
# CUSTOMERS
# =========================================================

elif page == "Customers":

    st.header("👥 Customer Intelligence")

    col1, col2 = st.columns(2)

    col1.metric(
        "Registered Customers",
        len(customers)
    )

    unique_visitors = len(
        {
            visit.get("customer_id")
            for visit in visits
            if visit.get("customer_id")
        }
    )

    col2.metric(
        "Customers With Visits",
        unique_visitors
    )

    st.divider()

    if customers:

        customer_df = pd.DataFrame(customers)

        st.subheader("Registered Customers")

        st.dataframe(
            customer_df,
            use_container_width=True
        )

    else:

        st.info("No customers registered.")

    st.divider()

    # -------------------------
    # VISITS BY CUSTOMER
    # -------------------------

    if visits:

        visits_df = pd.DataFrame(visits)

        if "customer_id" in visits_df.columns:

            st.subheader("Visits by Customer")

            visit_counts = (
                visits_df["customer_id"]
                .value_counts()
                .reset_index()
            )

            visit_counts.columns = [
                "Customer ID",
                "Visits"
            ]

            st.bar_chart(
                visit_counts,
                x="Customer ID",
                y="Visits"
            )


# =========================================================
# PRODUCT INTELLIGENCE
# =========================================================

elif page == "Product Intelligence":

    st.header("📦 Product Intelligence")

    st.info(
        "Product detection is working. "
        "Product analytics logging will be connected next."
    )

    st.subheader("Current Capabilities")

    st.write("• YOLOv8 object detection")
    st.write("• Retail object filtering")
    st.write("• Real-time product counting")
    st.write("• Webcam-based detection")


# =========================================================
# SENTIMENT ANALYTICS
# =========================================================

elif page == "Sentiment Analytics":

    st.header("💬 Sentiment Analytics")

    if sentiments:

        sentiment_df = pd.DataFrame(sentiments)

        # -------------------------
        # METRICS
        # -------------------------

        total = len(sentiment_df)

        if "sentiment" in sentiment_df.columns:

            positive = (
                sentiment_df["sentiment"] == "Positive"
            ).sum()

            neutral = (
                sentiment_df["sentiment"] == "Neutral"
            ).sum()

            negative = (
                sentiment_df["sentiment"] == "Negative"
            ).sum()

        else:

            positive = 0
            neutral = 0
            negative = 0

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Reviews",
            total
        )

        col2.metric(
            "Positive",
            int(positive)
        )

        col3.metric(
            "Neutral",
            int(neutral)
        )

        col4.metric(
            "Negative",
            int(negative)
        )

        st.divider()

        # -------------------------
        # DISTRIBUTION
        # -------------------------

        if "sentiment" in sentiment_df.columns:

            st.subheader("Sentiment Distribution")

            sentiment_counts = (
                sentiment_df["sentiment"]
                .value_counts()
            )

            st.bar_chart(
                sentiment_counts
            )

        # -------------------------
        # CONFIDENCE
        # -------------------------

        if "confidence" in sentiment_df.columns:

            average_confidence = (
                sentiment_df["confidence"].mean()
                * 100
            )

            st.metric(
                "Average Model Confidence",
                f"{average_confidence:.1f}%"
            )

        # -------------------------
        # REVIEWS
        # -------------------------

        st.subheader("Recent Customer Reviews")

        st.dataframe(
            sentiment_df.tail(20),
            use_container_width=True
        )

    else:

        st.info(
            "No sentiment data available yet."
        )


# =========================================================
# CHATBOT ANALYTICS
# =========================================================

elif page == "Chatbot Analytics":

    st.header("🤖 Chatbot Analytics")

    if chat_logs:

        chat_df = pd.DataFrame(chat_logs)

        # -------------------------
        # METRICS
        # -------------------------

        total_queries = len(chat_df)

        if "confidence" in chat_df.columns:

            average_confidence = (
                chat_df["confidence"].mean()
                * 100
            )

            low_confidence = (
                chat_df["confidence"] < 0.40
            ).sum()

        else:

            average_confidence = 0
            low_confidence = 0

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Queries",
            total_queries
        )

        col2.metric(
            "Average Confidence",
            f"{average_confidence:.1f}%"
        )

        col3.metric(
            "Fallback / Low Confidence",
            int(low_confidence)
        )

        st.divider()

        # -------------------------
        # CONFIDENCE HISTORY
        # -------------------------

        if (
            "timestamp" in chat_df.columns
            and "confidence" in chat_df.columns
        ):

            st.subheader("Confidence History")

            chart_df = chat_df.copy()

            chart_df["timestamp"] = pd.to_datetime(
                chart_df["timestamp"],
                errors="coerce"
            )

            chart_df["confidence_percent"] = (
                chart_df["confidence"] * 100
            )

            chart_df = chart_df.dropna(
                subset=["timestamp"]
            )

            if not chart_df.empty:

                st.line_chart(
                    chart_df,
                    x="timestamp",
                    y="confidence_percent"
                )

        # -------------------------
        # RECENT CONVERSATIONS
        # -------------------------

        st.subheader("Recent Conversations")

        st.dataframe(
            chat_df.tail(20),
            use_container_width=True
        )

    else:

        st.info(
            "No chatbot conversations recorded yet."
        )