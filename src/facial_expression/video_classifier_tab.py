from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np
import Classifier


class VideoClassifierTab(QWidget):
    """Tab displaying webcam video with real-time emotion classification."""

    def __init__(self):
        super().__init__()

        self.video_stream_active = False
        self.cap = None
        self.min_width = 200
        self.min_height = 200

        layout = QVBoxLayout()
        self.start_video_classifier_button = QPushButton("Start Video Classifier")
        self.start_video_classifier_button.clicked.connect(self.toggle_video_stream)
        layout.addWidget(self.start_video_classifier_button)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.show_frame)

    def process_frame(self, frame):
        return Classifier.classify(frame)

    def show_frame(self):
        if self.video_stream_active and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                processed_frame = self.process_frame(frame)
                self.display_frame(processed_frame)
            else:
                self.stop_video_stream()
        else:
            self.stop_video_stream()

    def resize_frame(self, frame, target_width, target_height):
        aspect_ratio = frame.shape[1] / frame.shape[0]
        if frame.shape[1] > target_width or frame.shape[0] > target_height:
            if frame.shape[1] / target_width > frame.shape[0] / target_height:
                resized_frame = cv2.resize(frame, (target_width, int(target_width / aspect_ratio)))
            else:
                resized_frame = cv2.resize(frame, (int(target_height * aspect_ratio), target_height))
        else:
            x_offset = (target_width - frame.shape[1]) // 2
            y_offset = (target_height - frame.shape[0]) // 2
            resized_frame = np.zeros((target_height, target_width, frame.shape[2]), dtype=np.uint8)
            resized_frame[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
        return resized_frame

    def display_frame(self, frame):
        if frame is not None:
            window_width = max(self.min_width, self.width())
            window_height = max(self.min_height, self.height() - self.start_video_classifier_button.height() - 20)
            resized_frame = self.resize_frame(frame, window_width, window_height)
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.video_label.setPixmap(pixmap)

    def toggle_video_stream(self):
        if not self.video_stream_active:
            self.start_video_classifier_button.setText("Stop Video Classifier")
            self.video_stream_active = True
            self.cap = cv2.VideoCapture(0)
            self.timer.start(10)
        else:
            self.stop_video_stream()

    def stop_video_stream(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.timer.stop()
        self.start_video_classifier_button.setText("Start Video Classifier")
        self.video_stream_active = False
        self.video_label.clear()
