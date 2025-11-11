#!/bin/bash

# Sticky Notes App Run Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run ./install.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
echo "Starting Sticky Notes App..."
python src/main.py
