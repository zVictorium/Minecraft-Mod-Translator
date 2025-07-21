#!/bin/bash

# Change to project root directory
cd "$(dirname "$0")/.."

# Check if virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run setup.sh first to initialize the environment."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment!"
    exit 1
fi

# Run the CLI app in app mode
mod-translator app "$@"

# Add a pause at the end so the terminal doesn't close immediately
echo
echo Press any key to exit...
read