#!/bin/bash

# Run script for Transport OCR Agent Streamlit App
# This script starts the Streamlit application

echo "Starting Transport OCR Agent..."
echo "Make sure you have set up your .env file with API keys!"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env file and add your API keys before running the app."
    exit 1
fi

# Run Streamlit app
streamlit run app.py
