import tkinter as tk
from tkinter import ttk
from video_classifier_tab import VideoClassifierTab
from image_classifier_tab import ImageClassifierTab


class MainApplication:
    def __init__(self, root):
        self.root = root
        root.title("Facial Expression Recognition Client")

        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set the window size to half of the screen resolution
        window_width = int(screen_width / 2)
        window_height = int(screen_height / 2)

        # Calculate the window position to center it on the screen
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        # Set the window size and position
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both")

        self.video_classifier = VideoClassifierTab(self.tab_control)
        self.image_classifier = ImageClassifierTab(self.tab_control)

        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        selected_tab = event.widget.tab(event.widget.select(), "text")
        if selected_tab != "Video Classifier":
            self.video_classifier.stop_video_stream()
        else:
            self.image_classifier.update_images()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
