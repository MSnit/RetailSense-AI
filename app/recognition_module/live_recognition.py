import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    result = DeepFace.find(
        img_path=frame,
        db_path="datasets/customers",
        model_name="Facenet512",
        enforce_detection=False,
        silent=True
    )

    print(result)

    cv2.imshow("RetailSense AI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()