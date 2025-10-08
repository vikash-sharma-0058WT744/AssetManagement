#!/bin/bash

# Script to run the webMethods.io Integration Asset Puller

echo "Starting webMethods.io Integration Asset Puller..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if requests library is installed
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required Python packages..."
    pip install requests
fi

# Check if config.json exists
if [ ! -f "config.json" ]; then
    echo "Error: config.json not found. Please create it based on the README instructions."
    exit 1
fi

# Run the asset puller
python3 webmethods_asset_puller.py

echo "Asset puller execution completed."

# Made with Bob
