import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .video_classifier_tab import VideoClassifierTab
from .image_classifier_tab import ImageClassifierTab


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facial Expression Recognition Client")

        # Set the window size to half of the screen resolution
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen.width() // 4, screen.height() // 4,
                         screen.width() // 2, screen.height() // 2)

        self.tab_control = QTabWidget(self)
        self.setCentralWidget(self.tab_control)

        self.video_classifier = VideoClassifierTab()
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
    app = QApplication(sys.argv)
    main_window = MainApplication()
    main_window.show()
    sys.exit(app.exec_())
