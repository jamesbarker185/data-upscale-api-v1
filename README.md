# Image Upscale API v1

A lightweight, local AI-powered image upscaling service using PyTorch and FastAPI. Supports high-fidelity and aesthetic restoration models.

## Features

- **2x / 4x Upscaling**: Choose between varying levels of super-resolution.
- **Dual Modes**: 
  - `Fidelity`: Focuses on preserving realistic details (SwinIR).
  - `Aesthetic`: Focuses on visual appeal and restoration (Real-ESRGAN).
- **Efficient Caching**: Built-in intelligent model caching to optimize memory usage (LRU).
- **Streaming Uploads**: Efficiently handles file uploads to prevent memory overload.

## Limitations

- **Image Dimensions**: Input images must not exceed **2048x2048** pixels.
- **File Size**: Maximum file size is **10MB**.
- **Supported Formats**: JPEG, PNG.
- **Performance**: Upscaling is computationally intensive. First run for a model may be slower due to downloading/loading.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd image-upscale-api-v1
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the server**:
   ```bash
   python main.py
   # OR
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```

2. **Access the Web Interface**:
   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Settings can be customized in `config.py` or via environment variables:

- `MAX_IMAGE_WIDTH`, `MAX_IMAGE_HEIGHT`: Input resolution limits (default 2048).
- `MAX_FILE_SIZE_MB`: Upload size limit (default 10MB).
- `MODEL_CACHE_SIZE`: Number of models to keep in GPU/RAM (default 2).
