import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the image
    resized = cv2.resize(gray, (640, 480))

    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)

    # Edge Detection
    edges = cv2.Canny(blurred, 100, 200)

    # Display all outputs
    cv2.imshow("Original", frame)
    cv2.imshow("Gray Scale", gray)
    cv2.imshow("Resized", resized)
    cv2.imshow("Blurred", blurred)
    cv2.imshow("Edges", edges)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()