import sys
import argparse
import json
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from video_classifier_tab import VideoClassifierTab
from image_classifier_tab import ImageClassifierTab
from Classifier import set_model_path
from paths import MODEL_PATH as DEFAULT_MODEL_PATH


def parse_args():
    parser = argparse.ArgumentParser(description="Facial Expression Recognition GUI")
    parser.add_argument("--settings", default="settings.json", help="Path to JSON settings file")
    parser.add_argument("--model-path", help="Path to trained model")
    parser.add_argument("--video-source", help="Video source index or file path")
    return parser.parse_args()


class MainApplication(QMainWindow):
    def __init__(self, video_source=0):
        super().__init__()
        self.setWindowTitle("Facial Expression Recognition Client")

        # Set the window size to half of the screen resolution
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen.width() // 4, screen.height() // 4,
                         screen.width() // 2, screen.height() // 2)

        self.tab_control = QTabWidget(self)
        self.setCentralWidget(self.tab_control)

        self.video_classifier = VideoClassifierTab(video_source=video_source)
        self.image_classifier = ImageClassifierTab()

        self.tab_control.addTab(self.video_classifier, "Video Classifier")
        self.tab_control.addTab(self.image_classifier, "Image Classifier")

        self.tab_control.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        if self.tab_control.tabText(index) != "Video Classifier":
            self.video_classifier.stop_video_stream()
        else:
            self.image_classifier.update_images()


if __name__ == "__main__":
    args = parse_args()
    settings = {}
    if os.path.exists(args.settings):
        try:
            with open(args.settings, "r") as f:
                settings = json.load(f)
        except Exception as e:
            print(f"Failed to read settings file: {e}")

    model_path = args.model_path or settings.get("model_path", DEFAULT_MODEL_PATH)
    video_source = args.video_source if args.video_source is not None else settings.get("video_source", 0)

    try:
        video_source = int(video_source)
    except (TypeError, ValueError):
        pass

    set_model_path(model_path)

    app = QApplication(sys.argv)
    main_window = MainApplication(video_source=video_source)
    main_window.show()
    sys.exit(app.exec())
