from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image
import os
import numpy as np
from Classifier import classify


class ImageClassifierTab(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_image_path = None
        self.input_image = None
        self.output_image = None

        layout = QVBoxLayout()

        self.choose_button = QPushButton("Choose Image")
        self.choose_button.clicked.connect(self.choose_image)
        layout.addWidget(self.choose_button)

        image_layout = QHBoxLayout()

        self.input_image_widget = QLabel("Input Image")
        self.input_image_widget.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.input_image_widget)

        self.output_image_widget = QLabel("Output Image")
        self.output_image_widget.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.output_image_widget)

        layout.addLayout(image_layout)

        self.setLayout(layout)

    def choose_image(self):
        initial_dir = os.path.join(os.path.dirname(__file__), "img")
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", initial_dir,
                                                   "Image Files (*.jpg *.jpeg *.png);;All Files (*)")
        if file_path:
            self.selected_image_path = file_path
            self.input_image = Image.open(self.selected_image_path)
            self.output_image = Image.fromarray(classify(np.array(self.input_image)))
            self.update_images()

    def update_images(self):
        if self.input_image is not None:
            window_width = self.width() // 2
            window_height = max(200, self.height() - self.choose_button.height() - 20)
            aspect_ratio = self.input_image.width / self.input_image.height

            input_width = min(window_width, self.input_image.width)
            input_height = min(window_height, int(input_width / aspect_ratio))

            if input_height > window_height:
                input_height = window_height
                input_width = int(input_height * aspect_ratio)

            input_image_resized = self.input_image.resize((input_width, input_height))
            input_qimage = QImage(input_image_resized.tobytes(), input_width, input_height, QImage.Format_RGB888)
            input_pixmap = QPixmap.fromImage(input_qimage)
            self.input_image_widget.setPixmap(input_pixmap)

            if self.output_image is not None:
                output_width = min(window_width, self.output_image.width)
                output_height = min(window_height, int(output_width / aspect_ratio))

                if output_height > window_height:
                    output_height = window_height
                    output_width = int(output_height * aspect_ratio)

                output_image_resized = self.output_image.resize((output_width, output_height))
                output_qimage = QImage(output_image_resized.tobytes(), output_width, output_height, QImage.Format_RGB888)
                output_pixmap = QPixmap.fromImage(output_qimage)
                self.output_image_widget.setPixmap(output_pixmap)

    def reset_images(self):
        self.input_image_widget.clear()
        self.output_image_widget.clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_images()
