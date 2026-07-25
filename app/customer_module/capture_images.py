import cv2
import os
import time

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def capture_images(customer_folder):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera.")
        return 0

    count = 0

    print("Look at the camera...")
    time.sleep(2)

    while count < 10:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for (x, y, w, h) in faces:

            # Crop only the face
            face = frame[y:y+h, x:x+w]

            image_path = os.path.join(
                customer_folder,
                f"face_{count+1}.jpg"
            )

            cv2.imwrite(image_path, face)

            count += 1

            print(f"Captured {count}/10")

            # Draw rectangle on live preview
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.imshow("Customer Registration", frame)

            # Wait before capturing next image
            cv2.waitKey(300)

            # Capture only one face per frame
            break

        cv2.imshow("Customer Registration", frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return count