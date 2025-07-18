# Facial-Expression-Recognition

This project provides a small PyQt6 based interface for performing facial expression classification on both images and live video. It relies on a pre-trained convolutional neural network and OpenCV for face detection.

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/your-user/Facial-Expression-Recognition.git
   cd Facial-Expression-Recognition
   ```
2. Install the required Python packages(Install python version from .python-version using pyenv and use that as local to create virtual environment(venv) for the project).
   ```bash
   pip install -r requirements.txt
   ```

## Obtaining `models/Trained_Model.keras`

A trained model is required to run the classifiers:

- **Download**: Grab `models/Trained_Model.keras` from [Google Drive](https://drive.google.com/file/d/16yW_2m_IRVToAXQqWF8o6oomhAcbgKq8/view?usp=sharing) and place it in the `models/` directory at the project root.
- **Train it yourself**: Use `notebooks/Model_Training.ipynb` together with the [FER-2013 dataset](https://www.kaggle.com/datasets/msambare/fer2013) to train a model and save it to `models/models/Trained_Model.keras`.

## Usage

Run the main application:

```bash
python main.py
```

The interface contains two tabs:

1. **Image Classifier** – choose an image and the model will annotate the detected faces.
2. **Video Classifier** – start the webcam feed and view the predicted expressions in real time.

### Example: Image Classification

![Example image classification](images/image_classification_example.jpg)

### Example: Video Classification

![Video classification example](images/video_classification_example.gif)

### Web Interface

A simple Streamlit application is also available. Launch it with:

```bash
streamlit run src/fer_app/web_app.py
```
