from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
import math as mt
import os
from .paths import PROCESSED_DATA_DIR
output_image_path = f"{PROCESSED_DATA_DIR}/output_image.jpg"
from .paths import MODEL_PATH


# Load the Haar cascade for face detection. The XML file lives alongside this
# module, so construct the path relative to this file to avoid issues when the
# current working directory differs.
CASCADE_PATH = os.path.join(os.path.dirname(__file__),
                            'haarcascade_frontalface_default.xml')
face_classifier = cv2.CascadeClassifier(CASCADE_PATH)

_classifier = None


def _get_classifier():
    """Load the trained CNN model on first use.

    ``load_model`` in Keras 3 can raise cryptic errors when the file is missing
    or saved with an older version. By checking the path and disabling compile
    and safe mode, we improve compatibility with legacy ``.h5`` models.
    """

    global _classifier
    if _classifier is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Please download or train it."
            )

        _classifier = load_model(MODEL_PATH, compile=False, safe_mode=False)
    return _classifier

class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


def classify(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    c = 1
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        rof_gray = gray[y:y + h, x:x + w]
        rof_gray = cv2.resize(rof_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([rof_gray]) != 0:
            rof = rof_gray.astype('float') / 255.0
            rof = img_to_array(rof)  # shape: (48, 48, 1)
            rof = np.expand_dims(rof, axis=0)  # shape: (1, 48, 48, 1)

            # ✅ Ensure input shape is correct
            if rof.ndim == 5 and rof.shape[1] == 1:
                rof = np.squeeze(rof, axis=1)

            # Make a prediction on the ROF, then lookup the class
            preds = _get_classifier().predict(rof)[0]
            label = class_labels[preds.argmax()]
            label_position = (x, y + h + 8)
            facex = "face " + str(c)
            cv2.putText(frame, facex, (x, y), cv2.FONT_HERSHEY_SIMPLEX, w * (2 / 227), (0, 255, 0),
                        mt.ceil(h * (2 / 180)))
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, w * (2 / 227), (0, 255, 0),
                        mt.ceil(h * (2 / 180)))
            c += 1
        else:
            cv2.putText(frame, 'No Face Found', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame


def video_classify():
    cap = cv2.VideoCapture(0)
    while True:
        # Grab a single frame of video
        ret, frame = cap.read()
        frame = classify(frame)
        cv2.imshow('Emotion Detector',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def image_classify(frame):
    frame = cv2.imread(frame)
    frame1 = classify(frame)
    cv2.imwrite(output_image_path, frame1)
