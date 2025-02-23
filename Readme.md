# Diabetic Retinopathy Detection System

## Overview

The Diabetic Retinopathy Detection System is a web application that enables users to upload retinal images for classification of diabetic retinopathy levels. Using a trained machine learning model, the application provides real-time predictions, categorizing images into five levels of diabetic retinopathy (DR):

1. **No DR**
2. **Mild DR**
3. **Moderate DR**
4. **Severe DR**
5. **Proliferative DR**

Each prediction includes a detailed description of the detected level.

## Features

- User authentication (registration and login)
- Image upload with drag-and-drop functionality
- Real-time prediction results with progress indication
- Responsive and professional user interface built with Tailwind CSS

## Technologies Used

- **Backend**: Flask
- **Machine Learning**: Keras
- **Database**: SQLite
- **Frontend**: HTML, CSS (Tailwind CSS)
- **Image Processing**: PIL (Pillow)

## Installation Guide

Follow the steps below to set up and run the application locally.

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)


### Step 1: Create a Virtual Environment (Optional)

It’s recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:

    ```bash
    venv\Scripts\activate
    ```

- On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

### Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

Start the Flask application:

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000` by default.

### Step 4: Access the Application

Open your web browser and navigate to `http://127.0.0.1:5000`. You can create a new account or log in with an existing account to begin using the application.

## Usage Instructions

1. **Login/Register**: Create an account or log in.
2. **Upload Image**: Drag and drop your retinal image or use the "Choose File" button.
3. **View Results**: After submitting the image, a progress bar will indicate processing. The prediction level and description will be displayed upon completion.

## Model Description

The application utilizes a Keras model (loaded from a `.h5` file) to analyze uploaded retinal images and classify them according to the severity of diabetic retinopathy.


## Acknowledgments

- Flask framework for web development
- Keras for building and training the neural network
- TensorFlow as the backend for Keras
- Tailwind CSS for styling the user interface
```

