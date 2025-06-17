import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
#from Test import classify
from . import classifier

class VideoClassifierTab:
    def __init__(self, tab_control):
        self.tab1 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text="Video Classifier")

        self.video_stream_active = False
        self.cap = None
        self.resized_frame = None
        self.min_width = 200
        self.min_height = 200

        self.start_video_classifier_button = ttk.Button(self.tab1, text="Start Video Classifier", command=self.toggle_video_stream)
        self.start_video_classifier_button.pack(padx=10, pady=10)

        self.video_label = ttk.Label(self.tab1)
        self.video_label.pack()

    def process_frame(self, frame):
        # Your custom function to process the video frame
        # Example: Convert the frame to grayscale
        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return classifier.classify(frame)

    def show_frame(self):
        if self.video_stream_active and self.cap is not None:
            _, frame = self.cap.read()
            if frame is not None:
                processed_frame = self.process_frame(frame)
                self.display_frame(processed_frame)
                self.tab1.after(10, self.show_frame)
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
            window_width = self.tab1.winfo_width()
            window_height = self.tab1.winfo_height() - self.start_video_classifier_button.winfo_height() - 20

            resized_width = max(self.min_width, window_width)
            resized_height = max(self.min_height, window_height)

            resized_frame = self.resize_frame(frame, resized_width, resized_height)

            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(rgb_frame)
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=img_tk)
            self.video_label.img = img_tk

    def toggle_video_stream(self):
        if not self.video_stream_active:
            self.start_video_classifier_button.config(text="Stop Video Classifier")
            self.video_stream_active = True
            self.cap = cv2.VideoCapture(0)  # Replace '0' with the video file path if you want to load a video file
            self.show_frame()
        else:
            self.stop_video_stream()

    def stop_video_stream(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.start_video_classifier_button.config(text="Start Video Classifier")
        self.video_stream_active = False
        self.video_label.config(image=None)
        self.video_label.img = None
