#!/bin/bash

echo "===================================="
echo "  Minecraft Mod Translator Setup"
echo "===================================="
echo

# Change to project root directory
cd "$(dirname "$0")/.."

# Upgrade pip to latest version
echo "Upgrading pip to latest version..."
python3 -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Error: Failed to upgrade pip!"
    exit 1
fi
echo "Pip upgraded successfully."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment!"
    exit 1
fi
echo "Virtual environment created successfully."

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment!"
    exit 1
fi
echo "Virtual environment activated successfully."

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies!"
    exit 1
fi
echo "Dependencies installed successfully."

# Install package in development mode
echo "Installing package in development mode..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "Error: Failed to install package in development mode!"
    exit 1
fi
echo "Package installed successfully."

echo
echo "===================================="
echo "      Setup Complete!"
echo "===================================="
echo

# Show help for the CLI tool
echo "Displaying help for mod-translator..."
mod-translator --help

read -p "Press Enter to continue..."