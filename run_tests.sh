#!/bin/bash

# Run tests for the webMethods.io Integration Asset Puller

# Make sure the script is executable
chmod +x modified_webmethods_asset_puller.py
chmod +x test_asset_puller.py

# Create a simple test environment
echo "Setting up test environment..."
mkdir -p test_env
cd test_env

# Copy necessary files
cp ../modified_webmethods_asset_puller.py .
cp ../test_asset_puller.py .
cp ../config.json .

# Run the tests
echo "Running tests..."
python3 test_asset_puller.py

# Clean up
echo "Cleaning up..."
cd ..
rm -rf test_env

echo "Test completed."

# Made with Bob
