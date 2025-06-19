# Facial-Expression-Recognition

This project provides a small PyQt6 based interface for performing facial expression classification on both images and live video. It relies on a pre-trained convolutional neural network and OpenCV for face detection.

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/your-user/Facial-Expression-Recognition.git
   cd Facial-Expression-Recognition
   ```
2. Install the required Python packages. TensorFlow 2.12 requires Python 3.8–3.10.
   ```bash
   pip install -r requirements.txt
   ```

## Obtaining `Trained_Model.h5`

A trained model is required to run the classifiers:

- **Download**: Grab `Trained_Model.h5` from [Google Drive](https://drive.google.com/file/d/1RaSSzdPUyg-C6nV9Ztr7x6nlFf4xTCld) and place it in the `models/` directory at the project root.
- **Train it yourself**: Use `Model_Training.ipynb` together with the [FER-2013 dataset](https://www.kaggle.com/datasets/msambare/fer2013) to train a model and save it to `models/Trained_Model.h5`.

## Usage

Run the main application:

```bash
python main.py
```

The interface contains two tabs:

1. **Image Classifier** – choose an image and the model will annotate the detected faces.
2. **Video Classifier** – start the webcam feed and view the predicted expressions in real time.

### Settings

You can provide a `settings.json` file in the project root to configure the model path and video source. The default file looks like:

```json
{
  "model_path": "models/Trained_Model.keras",
  "video_source": 0
}
```

Command-line options override the file:

```bash
python main.py --model-path path/to/model --video-source 1
```

### Example: Image Classification

![Example image classification](images/image_classification_example.jpg)

### Example: Video Classification

![Video classification example](images/video_classification_example.gif)

### Web Interface

A simple Streamlit application is also available. Launch it with:

```bash
streamlit run src/fer_app/web_app.py
```

