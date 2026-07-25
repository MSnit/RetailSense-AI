import streamlit as st
import pandas as pd
import sqlite3
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RetailSense AI",
    page_icon="🛒",
    layout="wide"
)

st.markdown("""
<style>

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(128, 128, 128, 0.08);
    border: 1px solid rgba(128, 128, 128, 0.20);
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    font-size: 14px;
}

[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: 700;
}

/* Sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128, 128, 128, 0.15);
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Headings */
h1 {
    letter-spacing: -1px;
}

h2, h3 {
    letter-spacing: -0.4px;
}

/* Remove Streamlit footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

DATABASE_FILE = os.path.join(
    BASE_DIR,
    "datasets",
    "retailsense.db"
)


def load_table(table_name):

    if not os.path.exists(DATABASE_FILE):
        return pd.DataFrame()

    allowed_tables = {
        "customers",
        "visits",
        "reviews",
        "chat_logs",
        "product_logs"
    }

    if table_name not in allowed_tables:
        return pd.DataFrame()

    try:

        conn = sqlite3.connect(DATABASE_FILE)

        df = pd.read_sql_query(
            f"SELECT * FROM {table_name}",
            conn
        )

        conn.close()

        return df

    except Exception as error:

        st.error(
            f"Database error ({table_name}): {error}"
        )

        return pd.DataFrame()


# =========================================================
# LOAD DATA
# =========================================================

customers_df = load_table("customers")
visits_df = load_table("visits")
sentiment_df = load_table("reviews")
chat_df = load_table("chat_logs")
products_df = load_table("product_logs")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🛒 RetailSense")
    st.caption("AI Retail Intelligence")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Customers",
            "Product Intelligence",
            "Sentiment Analytics",
            "Chatbot Analytics"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("RetailSense AI • v1.0")


# =========================================================
# HEADER
# =========================================================

st.title("🛒 RetailSense AI")

st.caption(
    "Smart Retail & Customer Intelligence Platform"
)

st.divider()


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.header("Dashboard Overview")

    # -------------------------
    # UNIQUE VISITORS
    # -------------------------

    if (
        not visits_df.empty
        and "customer_id" in visits_df.columns
    ):

        unique_visitors = (
            visits_df["customer_id"]
            .dropna()
            .nunique()
        )

    else:

        unique_visitors = 0

    # -------------------------
    # PRODUCT DETECTIONS
    # -------------------------

    if (
        not products_df.empty
        and "count" in products_df.columns
    ):

        total_products = int(
            products_df["count"].sum()
        )

    else:

        total_products = 0

    # -------------------------
    # METRICS
    # -------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Registered Customers",
        len(customers_df)
    )

    col2.metric(
        "Total Visits",
        len(visits_df)
    )

    col3.metric(
        "Unique Visitors",
        unique_visitors
    )

    col4.metric(
        "Customer Reviews",
        len(sentiment_df)
    )

    col5.metric(
        "Product Detections",
        total_products
    )

    st.divider()

    # -------------------------
    # CUSTOMER DATABASE
    # -------------------------

    st.subheader("👥 Customer Database")

    if not customers_df.empty:

        st.dataframe(
            customers_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No customers registered yet."
        )

    st.divider()

    # -------------------------
    # RECENT VISITS
    # -------------------------

    st.subheader("🕒 Recent Visits")

    if not visits_df.empty:

        recent_visits = visits_df.copy()

        if "id" in recent_visits.columns:

            recent_visits = (
                recent_visits
                .sort_values(
                    "id",
                    ascending=False
                )
            )

        st.dataframe(
            recent_visits.head(10),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No visits recorded yet."
        )

    st.divider()

    # -------------------------
    # CUSTOMER VISIT ANALYTICS
    # -------------------------

    st.subheader(
        "📊 Customer Visit Analytics"
    )

    if (
        not visits_df.empty
        and "customer_id" in visits_df.columns
    ):

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

    else:

        st.info(
            "No visit analytics available."
        )

    # -------------------------
    # VISITS OVER TIME
    # -------------------------

    if (
        not visits_df.empty
        and "timestamp" in visits_df.columns
    ):

        st.subheader(
            "Visits Over Time"
        )

        visit_timeline = visits_df.copy()

        visit_timeline["timestamp"] = pd.to_datetime(
            visit_timeline["timestamp"],
            errors="coerce"
        )

        visit_timeline = (
            visit_timeline
            .dropna(
                subset=["timestamp"]
            )
        )

        if not visit_timeline.empty:

            daily_visits = (
                visit_timeline
                .set_index("timestamp")
                .resample("D")
                .size()
            )

            st.line_chart(
                daily_visits
            )


# =========================================================
# CUSTOMERS
# =========================================================

elif page == "Customers":

    st.header(
        "👥 Customer Intelligence"
    )

    # -------------------------
    # METRICS
    # -------------------------

    if (
        not visits_df.empty
        and "customer_id" in visits_df.columns
    ):

        customers_with_visits = (
            visits_df["customer_id"]
            .dropna()
            .nunique()
        )

    else:

        customers_with_visits = 0

    col1, col2 = st.columns(2)

    col1.metric(
        "Registered Customers",
        len(customers_df)
    )

    col2.metric(
        "Customers With Visits",
        customers_with_visits
    )

    st.divider()

    # -------------------------
    # CUSTOMER TABLE
    # -------------------------

    st.subheader(
        "Registered Customers"
    )

    if not customers_df.empty:

        st.dataframe(
            customers_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No customers registered."
        )

    st.divider()

    # -------------------------
    # VISITS BY CUSTOMER
    # -------------------------

    st.subheader(
        "Visits by Customer"
    )

    if (
        not visits_df.empty
        and "customer_id" in visits_df.columns
    ):

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

    else:

        st.info(
            "No customer visit data available."
        )


# =========================================================
# PRODUCT INTELLIGENCE
# =========================================================

elif page == "Product Intelligence":

    st.header(
        "📦 Product Intelligence"
    )

    if not products_df.empty:

        # -------------------------
        # PRODUCT TOTALS
        # -------------------------

        product_totals = (
            products_df
            .groupby("product")["count"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        total_detections = int(
            products_df["count"].sum()
        )

        unique_products = (
            products_df["product"]
            .nunique()
        )

        if not product_totals.empty:

            top_product = (
                product_totals.index[0]
            )

        else:

            top_product = "None"

        # -------------------------
        # METRICS
        # -------------------------

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        col1.metric(
            "Detection Records",
            len(products_df)
        )

        col2.metric(
            "Total Detections",
            total_detections
        )

        col3.metric(
            "Unique Products",
            unique_products
        )

        col4.metric(
            "Most Detected",
            top_product
        )

        st.divider()

        # -------------------------
        # PRODUCT DISTRIBUTION
        # -------------------------

        st.subheader(
            "📊 Product Distribution"
        )

        product_chart = (
            product_totals
            .reset_index()
        )

        product_chart.columns = [
            "Product",
            "Detections"
        ]

        st.bar_chart(
            product_chart,
            x="Product",
            y="Detections"
        )

        st.divider()

        # -------------------------
        # DETECTION HISTORY
        # -------------------------

        st.subheader(
            "Product Detection History"
        )

        if "timestamp" in products_df.columns:

            history_df = (
                products_df.copy()
            )

            history_df["timestamp"] = (
                pd.to_datetime(
                    history_df["timestamp"],
                    errors="coerce"
                )
            )

            history_df = (
                history_df
                .dropna(
                    subset=["timestamp"]
                )
            )

            if not history_df.empty:

                daily_products = (
                    history_df
                    .set_index("timestamp")
                    .resample("D")["count"]
                    .sum()
                )

                st.line_chart(
                    daily_products
                )

        # -------------------------
        # RECENT DETECTIONS
        # -------------------------

        st.subheader(
            "Recent Detection Records"
        )

        recent_products = (
            products_df.copy()
        )

        if "id" in recent_products.columns:

            recent_products = (
                recent_products
                .sort_values(
                    "id",
                    ascending=False
                )
            )

        st.dataframe(
            recent_products.head(20),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No product detections recorded yet."
        )


# =========================================================
# SENTIMENT ANALYTICS
# =========================================================

elif page == "Sentiment Analytics":

    st.header(
        "💬 Sentiment Analytics"
    )

    if not sentiment_df.empty:

        # -------------------------
        # COUNTS
        # -------------------------

        total_reviews = len(
            sentiment_df
        )

        if "sentiment" in sentiment_df.columns:

            positive = int(
                (
                    sentiment_df["sentiment"]
                    == "Positive"
                ).sum()
            )

            neutral = int(
                (
                    sentiment_df["sentiment"]
                    == "Neutral"
                ).sum()
            )

            negative = int(
                (
                    sentiment_df["sentiment"]
                    == "Negative"
                ).sum()
            )

        else:

            positive = 0
            neutral = 0
            negative = 0

        # -------------------------
        # METRICS
        # -------------------------

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        col1.metric(
            "Total Reviews",
            total_reviews
        )

        col2.metric(
            "Positive",
            positive
        )

        col3.metric(
            "Neutral",
            neutral
        )

        col4.metric(
            "Negative",
            negative
        )

        st.divider()

        # -------------------------
        # SENTIMENT DISTRIBUTION
        # -------------------------

        if "sentiment" in sentiment_df.columns:

            st.subheader(
                "Sentiment Distribution"
            )

            sentiment_counts = (
                sentiment_df["sentiment"]
                .value_counts()
                .reset_index()
            )

            sentiment_counts.columns = [
                "Sentiment",
                "Reviews"
            ]

            st.bar_chart(
                sentiment_counts,
                x="Sentiment",
                y="Reviews"
            )

        # -------------------------
        # CONFIDENCE
        # -------------------------

        if "confidence" in sentiment_df.columns:

            confidence_values = (
                pd.to_numeric(
                    sentiment_df["confidence"],
                    errors="coerce"
                )
                .dropna()
            )

            if not confidence_values.empty:

                avg_confidence = (
                    confidence_values.mean()
                )

                # Handle either 0-1 or 0-100
                if avg_confidence <= 1:
                    avg_confidence *= 100

                st.metric(
                    "Average Confidence",
                    f"{avg_confidence:.1f}%"
                )

        st.divider()

        # -------------------------
        # RECENT REVIEWS
        # -------------------------

        st.subheader(
            "Recent Customer Reviews"
        )

        recent_reviews = (
            sentiment_df.copy()
        )

        if "id" in recent_reviews.columns:

            recent_reviews = (
                recent_reviews
                .sort_values(
                    "id",
                    ascending=False
                )
            )

        st.dataframe(
            recent_reviews.head(20),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No sentiment data available yet."
        )


# =========================================================
# CHATBOT ANALYTICS
# =========================================================

elif page == "Chatbot Analytics":

    st.header(
        "🤖 Chatbot Analytics"
    )

    if not chat_df.empty:

        # -------------------------
        # CONFIDENCE
        # -------------------------

        if "confidence" in chat_df.columns:

            confidence_values = pd.to_numeric(
                chat_df["confidence"],
                errors="coerce"
            )

            valid_confidence = (
                confidence_values
                .dropna()
            )

            if not valid_confidence.empty:

                avg_raw = (
                    valid_confidence.mean()
                )

                # Support 0-1 and 0-100
                if avg_raw <= 1:

                    average_confidence = (
                        avg_raw * 100
                    )

                    low_confidence = int(
                        (
                            valid_confidence
                            < 0.40
                        ).sum()
                    )

                else:

                    average_confidence = avg_raw

                    low_confidence = int(
                        (
                            valid_confidence
                            < 40
                        ).sum()
                    )

            else:

                average_confidence = 0
                low_confidence = 0

        else:

            average_confidence = 0
            low_confidence = 0

        # -------------------------
        # METRICS
        # -------------------------

        col1, col2, col3 = (
            st.columns(3)
        )

        col1.metric(
            "Total Queries",
            len(chat_df)
        )

        col2.metric(
            "Average Confidence",
            f"{average_confidence:.1f}%"
        )

        col3.metric(
            "Low Confidence",
            low_confidence
        )

        st.divider()

        # -------------------------
        # CONFIDENCE HISTORY
        # -------------------------

        if (
            "timestamp" in chat_df.columns
            and
            "confidence" in chat_df.columns
        ):

            st.subheader(
                "Confidence History"
            )

            chart_df = chat_df.copy()

            chart_df["timestamp"] = (
                pd.to_datetime(
                    chart_df["timestamp"],
                    errors="coerce"
                )
            )

            chart_df["confidence"] = (
                pd.to_numeric(
                    chart_df["confidence"],
                    errors="coerce"
                )
            )

            chart_df = (
                chart_df
                .dropna(
                    subset=[
                        "timestamp",
                        "confidence"
                    ]
                )
            )

            if not chart_df.empty:

                if (
                    chart_df["confidence"]
                    .mean()
                    <= 1
                ):

                    chart_df[
                        "confidence_percent"
                    ] = (
                        chart_df["confidence"]
                        * 100
                    )

                else:

                    chart_df[
                        "confidence_percent"
                    ] = (
                        chart_df["confidence"]
                    )

                st.line_chart(
                    chart_df,
                    x="timestamp",
                    y="confidence_percent"
                )

        st.divider()

        # -------------------------
        # RECENT CONVERSATIONS
        # -------------------------

        st.subheader(
            "Recent Conversations"
        )

        recent_chats = (
            chat_df.copy()
        )

        if "id" in recent_chats.columns:

            recent_chats = (
                recent_chats
                .sort_values(
                    "id",
                    ascending=False
                )
            )

        st.dataframe(
            recent_chats.head(20),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No chatbot conversations recorded yet."
        )