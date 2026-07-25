import cv2
from ultralytics import YOLO
from collections import Counter

model = YOLO("yolov8n.pt")

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

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, verbose=False)

    result = results[0]

    # Get detected class names
    detected_objects = []

    for box in result.boxes:

        class_id = int(box.cls[0])

        class_name = model.names[class_id]

        if class_name in RETAIL_CLASSES:
         detected_objects.append(class_name)
    # Count objects
    object_counts = Counter(detected_objects)

    # YOLO bounding boxes
    annotated_frame = result.plot()

    # Display counts
    y = 30

    for object_name, count in object_counts.items():

        text = f"{object_name}: {count}"

        cv2.putText(
            annotated_frame,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        y += 35

    cv2.imshow(
        "RetailSense AI - Product Intelligence",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()