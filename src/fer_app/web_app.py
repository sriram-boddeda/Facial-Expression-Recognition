import cv2
import numpy as np
import streamlit as st
from PIL import Image
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from pathlib import Path
import sys

# Ensure the "facial_expression" package can be imported when running via
# ``streamlit run`` by adding the project root to ``sys.path``.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from facial_expression.Classifier import classify


st.set_page_config(page_title="Facial Expression Recognition")

st.title("Facial Expression Recognition")

image_tab, webcam_tab = st.tabs(["Image Upload", "Webcam"])

with image_tab:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        input_image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(input_image)
        output_image = classify(image_np.copy())
        st.image([input_image, output_image], caption=["Input", "Prediction"])

with webcam_tab:
    st.write("Webcam feed with real-time expression recognition.")

    class EmotionProcessor(VideoProcessorBase):
        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            img = classify(img)
            return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(key="emotion", video_processor_factory=EmotionProcessor)
