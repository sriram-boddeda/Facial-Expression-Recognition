import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import numpy as np
from Classifier import classify


class ImageClassifierTab:
    def __init__(self, tab_control):
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab2, text="Image Classifier")

        self.selected_image_path = None
        self.input_image = None
        self.output_image = None

        self.choose_button = ttk.Button(self.tab2, text="Choose Image", command=self.choose_image)
        self.choose_button.pack(pady=10)

        self.image_frame = ttk.Frame(self.tab2)
        self.image_frame.pack(padx=10, pady=10)

        self.input_label = ttk.Label(self.image_frame, text="Input Image")
        self.output_label = ttk.Label(self.image_frame, text="Output Image")
        self.input_label.grid(row=0, column=0, padx=5, pady=5)
        self.output_label.grid(row=0, column=1, padx=5, pady=5)

        self.input_image_label = ttk.Label(self.image_frame)
        self.output_image_label = ttk.Label(self.image_frame)
        self.input_image_label.grid(row=1, column=0, padx=5, pady=5)
        self.output_image_label.grid(row=1, column=1, padx=5, pady=5)

        self.tab2.bind("<Configure>", self.resize_images)

    def choose_image(self):
        initial_dir = os.path.join(os.path.dirname(__file__), "img")
        file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Select Image",
                                               filetypes=[("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg"),
                                                          ("PNG Files", "*.png"), ("All Files", "*.*")])
        if file_path:
            self.selected_image_path = file_path
            self.input_image = Image.open(self.selected_image_path)
            self.output_image = Image.fromarray(classify(np.array(self.input_image)))
            self.update_images()

    def resize_images(self, event):
        self.update_images()

    def update_images(self):
        if self.input_image is not None:
            self.input_image_label.config(image=None)
            self.output_image_label.config(image=None)

            window_width = self.tab2.winfo_width() // 2
            window_height = max(200, self.tab2.winfo_height() - self.choose_button.winfo_height() - 20)
            aspect_ratio = self.input_image.width / self.input_image.height

            input_width = min(window_width, self.input_image.width)
            input_height = min(window_height, int(input_width / aspect_ratio))

            if input_height > window_height:
                input_height = window_height
                input_width = int(input_height * aspect_ratio)

            input_image_resized = self.input_image.resize((input_width, input_height))
            input_photo = ImageTk.PhotoImage(image=input_image_resized)
            self.input_image_label.config(image=input_photo)
            self.input_image_label.image = input_photo

            if self.output_image is not None:
                output_width = min(window_width, self.output_image.width)
                output_height = min(window_height, int(output_width / aspect_ratio))

                if output_height > window_height:
                    output_height = window_height
                    output_width = int(output_height * aspect_ratio)

                output_image_resized = self.output_image.resize((output_width, output_height))
                output_photo = ImageTk.PhotoImage(image=output_image_resized)
                self.output_image_label.config(image=output_photo)
                self.output_image_label.image = output_photo
    def reset_images(self):
        self.Input_image_label.config(image=None)
        self.output_image_label.config(image=None)
