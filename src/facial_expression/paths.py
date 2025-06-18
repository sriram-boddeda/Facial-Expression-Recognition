# paths.py
# This file centralizes important project paths to avoid hardcoding them in different modules.
# This makes it easier to manage and update paths as the project evolves.

import os

# Get the absolute path of the project's root directory.
# We assume this file is located within a subdirectory of the project root
# (e.g., src/facial_expression/paths.py).
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Construct paths relative to the project root
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')

MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'Trained_Model.h5')

DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs')
ARCHITECTURE_IMAGE_PATH = os.path.join(DOCS_DIR, 'architecture', 'threecnnmode.jpg')

# Add variables for other paths here as needed