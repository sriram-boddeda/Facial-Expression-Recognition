from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
import cv2
import numpy as np
import math as mt
import os
from .paths import PROCESSED_DATA_DIR, MODEL_PATH

output_image_path = f"{PROCESSED_DATA_DIR}/output_image.jpg"

# Load Haar Cascade
CASCADE_PATH = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
face_classifier = cv2.CascadeClassifier(CASCADE_PATH)

if face_classifier.empty():
    raise IOError(f"Failed to load Haar Cascade XML from {CASCADE_PATH}")

_classifier = None

def _get_classifier():
    """Lazily load the model (supports .keras or .h5)"""
    global _classifier
    if _classifier is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}.")
        _classifier = load_model(MODEL_PATH, compile=False)
    return _classifier

class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def classify(frame):
    if frame is None or frame.size == 0:
        raise ValueError("Received empty or invalid frame for classification.")

    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except cv2.error as e:
        raise RuntimeError(f"Failed to convert frame to grayscale: {e}")

    if gray is None or gray.size == 0:
        raise ValueError("Grayscale conversion resulted in an empty image.")

    try:
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    except cv2.error as e:
        raise RuntimeError(
            f"detectMultiScale failed on grayscale frame with shape {gray.shape}: {e}"
        )

    c = 1
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        rof_gray = gray[y:y + h, x:x + w]
        rof_gray = cv2.resize(rof_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum(rof_gray) != 0:
            rof = rof_gray.astype('float32') / 255.0
            rof = img_to_array(rof)
            rof = np.expand_dims(rof, axis=0)

            preds = _get_classifier().predict(rof, verbose=0)[0]
            label = class_labels[preds.argmax()]
            label_position = (x, y + h + 8)
            facex = f"face {c}"
            font_scale = w * (2 / 227)
            thickness = mt.ceil(h * (2 / 180))
            cv2.putText(frame, facex, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), thickness)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), thickness)
            c += 1
        else:
            cv2.putText(frame, 'No Face Found', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame

def video_classify():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Webcam could not be opened.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        frame = classify(frame)
        cv2.imshow('Emotion Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def image_classify(filepath):
    frame = cv2.imread(filepath)
    if frame is None:
        raise FileNotFoundError(f"Could not read image from path: {filepath}")
    result = classify(frame)
    cv2.imwrite(output_image_path, result)
