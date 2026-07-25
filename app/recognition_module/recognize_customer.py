import os
from deepface import DeepFace


CUSTOMER_DB = "datasets/customers"

# Start slightly relaxed; we'll tune after testing
MAX_DISTANCE = 0.45


def recognize_customer(frame):

    try:

        results = DeepFace.find(
            img_path=frame,
            db_path=CUSTOMER_DB,
            model_name="Facenet512",
            distance_metric="cosine",
            detector_backend="opencv",
            enforce_detection=False,
            silent=True
        )

        if not results:
            return None

        matches = results[0]

        if matches.empty:
            return None

        best_match = matches.sort_values(
            "distance"
        ).iloc[0]

        distance = float(
            best_match["distance"]
        )

        print(
            f"Best match distance: {distance:.3f}"
        )

        if distance > MAX_DISTANCE:
            return None

        identity = best_match["identity"]

        customer_id = os.path.basename(
            os.path.dirname(identity)
        )

        return customer_id

    except Exception as error:

        print(
            f"Recognition error: {error}"
        )

        return None