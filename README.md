# GreenGuard

An AI-powered waste classification web application designed to reduce recycling contamination and eliminate "wish-cycling" by instantly identifying waste materials from uploaded images.


## Features
- **AI Image Classification:** Instantly detects 7 types of waste: Battery, Biological, Glass, Metal, Paper, Plastic, and Trash.
- **Actionable Insights:** Provides disposal instructions, recommended recycling bin colors, and confidence scores.
- **Interactive UI:** Smooth drag-and-drop file upload with real-time image previews without page reloads.


## Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
- **Backend:** Python, FastAPI, Uvicorn, Jinja2
- **Machine Learning:** TensorFlow, Keras, Pillow (PIL)
- **Architecture:** Convolutional Neural Network (CNN) utilizing Conv2D and MaxPooling2D layers for spatial feature extraction.


# Quick Start Guide

### Step 1: Install Git LFS
Git Large File Storage (LFS) is required to download the .keras model files correctly.

- Mac: brew install git-lfs
- Windows: Download from git-lfs.com

### Step 2: Clone and Pull the Repository

```
git clone https://github.com/Kathoollllll/garbage-classification.git
cd garbage-classification
git lfs install
git lfs pull
```

### Step 3: Set Up the Dataset (Choose One)
Generate the dataset structure using the raw images in the repo:

```
python split_data.py
```

### Step 4: Run Standalone Verification
Test the standalone model environment before launching the web app:

```
python classify.py
```

**Note:** Skipping Step 1 causes this to fail with an OSError because the model files will download as empty 1KB pointers.

### Step 5: Launch the Application
1. Install the required Python dependencies:

```
pip install -r requirements.txt
```

2. Start the FastAPI backend server:

```
uvicorn app:app --reload
```

3. Open your browser and navigate to the local address displayed in your terminal (typically ```http://127.0.0.1:8000```).
