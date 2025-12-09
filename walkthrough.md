# AI Image Upscaler POC - Walkthrough

## Overview
This is a local web application that allows users to upscale images using two different AI models:
- **Fidelity Mode** (SwinIR): Focuses on preserving details, lines, and text.
- **Aesthetic Mode** (Real-ESRGAN): Focuses on hallucinating details and texture for better looking photos.

## Setup Instructions

### Prerequisites
- Python 3.10+
- Internet connection (for initial model download)

### Installation
1.  **Clone/Open** the project folder.
2.  **Create venv**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

### Running the App
1.  **Start the Server**:
    ```powershell
    uvicorn main:app --reload
    ```
    *Note: On the first run, it will automatically download the AI models (~200MB). Check the terminal for progress.*

2.  **Access the UI**:
    Open [http://localhost:8080](http://localhost:8080) in your browser.

## Usage
1.  **Upload**: specific an image (JPG/PNG).
2.  **Select Mode**:
    *   *Fidelity*: For drawings, anime, or documents.
    *   *Aesthetic*: For real-world photos.
3.  **Upscale**: Click the button and wait (10-30s on CPU).
4.  **Compare**: Use the slider to see the difference.

## Troubleshooting
- **Slow Inference**: If you don't have an NVIDIA GPU, inference runs on CPU. This is normal.
- **Out of Memory**: Large images might crash the process on limited RAM. Resize images to <1000px if this happens.
