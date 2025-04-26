# Use a stable Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /code

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /code/requirements.txt

# Copy application code
COPY ./app /code/app

# Expose the port your app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

