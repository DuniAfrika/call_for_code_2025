FROM python:3.11-slim

# for cache efficiency
RUN pip install --upgrade pip

# Set the working directory
WORKDIR /code

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
