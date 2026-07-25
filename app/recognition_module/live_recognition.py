import cv2
import time

from recognition_module.recognize_customer import recognize_customer
from recognition_module.visit_logger import log_visit
from database.database import get_customer_name


def run_live_recognition():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera.")
        return

    last_customer = None
    last_log_time = 0

    candidate_customer = None
    candidate_frames = 0

    REQUIRED_FRAMES = 3
    COOLDOWN = 30

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Failed to read camera frame.")
            break

        customer_id = recognize_customer(frame)

        # -------------------------
        # CUSTOMER RECOGNIZED
        # -------------------------

        if customer_id:

            customer_name = get_customer_name(customer_id)

            # Check whether same customer appears
            # in consecutive frames
            if customer_id == candidate_customer:
                candidate_frames += 1
            else:
                candidate_customer = customer_id
                candidate_frames = 1

            # Display customer
            cv2.putText(
                frame,
                f"{customer_name} ({customer_id})",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Verification: {candidate_frames}/{REQUIRED_FRAMES}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            current_time = time.time()

            # Customer must appear in 3 consecutive frames
            if candidate_frames >= REQUIRED_FRAMES:

                # Avoid repeated visit logging
                if (
                    customer_id != last_customer
                    or current_time - last_log_time >= COOLDOWN
                ):

                    log_visit(customer_id)

                    print(
                        f"Recognized: {customer_name} "
                        f"({customer_id})"
                    )

                    last_customer = customer_id
                    last_log_time = current_time

        # -------------------------
        # UNKNOWN CUSTOMER
        # -------------------------

        else:

            candidate_customer = None
            candidate_frames = 0

            cv2.putText(
                frame,
                "Unknown Customer",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # -------------------------
        # DISPLAY CAMERA
        # -------------------------

        cv2.imshow(
            "RetailSense AI - Customer Recognition",
            frame
        )

        # Q = return to main menu
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_live_recognition()