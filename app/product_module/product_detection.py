import cv2
import json
import os
from datetime import datetime
from collections import Counter
from ultralytics import YOLO


model = YOLO("yolov8n.pt")

PRODUCT_LOG_FILE = "datasets/product_logs.json"

RETAIL_CLASSES = {
    "bottle",
    "cup",
    "banana",
    "apple",
    "orange",
    "sandwich",
    "cell phone",
    "book",
    "toothbrush"
}


def save_product_log(object_counts):

    if not object_counts:
        return

    if os.path.exists(PRODUCT_LOG_FILE):
        try:
            with open(PRODUCT_LOG_FILE, "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (json.JSONDecodeError, OSError):
            logs = []
    else:
        logs = []

    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "products": dict(object_counts),
        "total_products": sum(object_counts.values())
    })

    with open(PRODUCT_LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)


def run_product_detection():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera.")
        return

    last_counts = Counter()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model(
            frame,
            verbose=False,
            conf=0.40
        )

        result = results[0]

        detected_objects = []

        for box in result.boxes:

            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            if class_name in RETAIL_CLASSES:
                detected_objects.append(class_name)

        object_counts = Counter(detected_objects)

        annotated_frame = result.plot()

        y = 30

        for object_name, count in object_counts.items():

            cv2.putText(
                annotated_frame,
                f"{object_name}: {count}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            y += 35

        cv2.putText(
            annotated_frame,
            "Press Q to finish session",
            (20, annotated_frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Remember latest non-empty detection
        if object_counts:
            last_counts = object_counts.copy()

        cv2.imshow(
            "RetailSense AI - Product Intelligence",
            annotated_frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save once per detection session
    if last_counts:

        save_product_log(last_counts)

        print("\nProduct session saved.")

        for product, count in last_counts.items():
            print(f"{product}: {count}")

    else:
        print("\nNo retail products detected.")


if __name__ == "__main__":
    run_product_detection()