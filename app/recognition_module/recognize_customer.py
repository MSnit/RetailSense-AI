from deepface import DeepFace

result = DeepFace.find(
    img_path="datasets/customers/RS-010/face_1.jpg",
    db_path="datasets/customers",
    model_name="Facenet512",
    enforce_detection=False
)

print(result)