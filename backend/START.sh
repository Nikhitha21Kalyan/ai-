#!/bin/bash
# Healthcare Fraud Detection - Linux/Mac Startup Script
# This script starts MongoDB and Flask backend

echo ""
echo "========================================"
echo "Healthcare Fraud Detection System"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

# Check if MongoDB is installed and running
if command -v mongod &> /dev/null; then
    echo "Checking MongoDB..."
    if ! pgrep -x "mongod" > /dev/null; then
        echo "Starting MongoDB..."
        mongod --dbpath /data/db &
        sleep 3
    else
        echo "MongoDB is already running"
    fi
else
    echo "WARNING: MongoDB is not found"
    echo "Please install MongoDB from https://www.mongodb.com/try/download/community"
    echo "Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas"
fi

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing/updating dependencies..."
pip install -q -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your configuration before running again."
    exit 1
fi

# Start Flask app
echo ""
echo "========================================"
echo "Starting Healthcare Fraud Detection API"
echo "========================================"
echo ""
echo "API Server: http://localhost:5000"
echo "Frontend: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
