# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads static/cropped_images static/outputs static/page_images static/segmentated_images

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Expose port (Render sets PORT dynamically)
EXPOSE ${PORT:-5002}

# Run the application (use shell form so $PORT is expanded)
CMD gunicorn --bind 0.0.0.0:${PORT:-5002} --workers 2 --timeout 600 app:app

