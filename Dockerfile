# Use an official Python runtime as a parent image
# 3.10-slim is a good balance of size and compatibility
FROM python:3.10-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# libgl1-mesa-glx and libglib2.0-0 are often required for OpenCV/image libraries even if headless
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create models directory to ensure it exists for volume mounting
RUN mkdir -p models

# Expose port 8080
EXPOSE 8080

# Command to run the application
# We use uvicorn directly. Host 0.0.0.0 is crucial for Docker networking.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
