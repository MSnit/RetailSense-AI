import os
from deepface import DeepFace

CUSTOMER_DB = "datasets/customers"

# Lower = stricter matching
MAX_DISTANCE = 0.30


def recognize_customer(frame):

    try:
        results = DeepFace.find(
            img_path=frame,
            db_path=CUSTOMER_DB,
            model_name="Facenet512",
            distance_metric="cosine",
            enforce_detection=True,
            silent=True
        )

        if not results or results[0].empty:
            return None

        matches = results[0]

        # Best match = smallest distance
        best_match = matches.sort_values("distance").iloc[0]

        distance = float(best_match["distance"])

        # Reject weak matches
        if distance > MAX_DISTANCE:
            return None

        identity = best_match["identity"]

        customer_id = os.path.basename(
            os.path.dirname(identity)
        )

        return customer_id

    except Exception:
        return None