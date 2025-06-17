# Facial-Expression-Recognition

This project provides a small PyQt5 based interface for performing facial expression classification on both images and live video. It relies on a pre-trained convolutional neural network and OpenCV for face detection.

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/your-user/Facial-Expression-Recognition.git
   cd Facial-Expression-Recognition
   ```
2. Install the required Python packages. The repository provides a
   `.python-version` file for [pyenv](https://github.com/pyenv/pyenv). Run the
   setup script to create a virtual environment and install the package from
   `pyproject.toml`.
   ```bash
   ./scripts/setup.sh            # or ./scripts/setup.sh cpu/macos
   ```
   Pass `cpu` or `macos` to install TensorFlow for your platform.

## Obtaining `Trained_Model.h5`

A trained model is required to run the classifiers:

- **Download**: Grab `Trained_Model.h5` from [Google Drive](https://drive.google.com/file/d/1RaSSzdPUyg-C6nV9Ztr7x6nlFf4xTCld) and place it in the repository root.
- **Train it yourself**: Use `Model_Training.ipynb` together with the [FER-2013 dataset](https://www.kaggle.com/datasets/msambare/fer2013) to train a model and save it as `Trained_Model.h5`.

## Usage

Run the main application:

```bash
python -m facial_expression_recognition
```

The interface contains two tabs:

1. **Image Classifier** – choose an image and the model will annotate the detected faces.
2. **Video Classifier** – start the webcam feed and view the predicted expressions in real time.

### Example: Image Classification

![Example image classification](images/image_classification_example.jpg)

### Example: Video Classification

![Video classification example](images/video_classification_example.gif)
