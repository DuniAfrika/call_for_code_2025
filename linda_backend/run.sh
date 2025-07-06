#!/bin/env bash

if pip freeze | grep -q -f requirements.txt; then
    echo "All dependencies are already installed."
else
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "Starting the application..."
uvicorn main:app --host 0.0.0.0 --port 8000
