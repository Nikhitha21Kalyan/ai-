@echo off
REM Healthcare Fraud Detection - Windows Startup Script
REM This script starts both MongoDB and Flask backend

echo.
echo ========================================
echo Healthcare Fraud Detection System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

REM Check if MongoDB is installed
where mongod >nul 2>&1
if errorlevel 1 (
    echo WARNING: MongoDB is not found in PATH
    echo Please ensure MongoDB is installed and running
    echo Visit: https://www.mongodb.com/try/download/community
    echo.
)

REM Start MongoDB in a new window
echo Starting MongoDB...
start cmd /k mongod

REM Wait a moment for MongoDB to start
timeout /t 3 /nobreak

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist venv (
    echo.
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing/updating dependencies...
pip install -q -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo.
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please edit .env with your configuration before running again.
    pause
    exit /b 1
)

REM Start Flask app
echo.
echo ========================================
echo Starting Healthcare Fraud Detection API
echo ========================================
echo.
echo API Server: http://localhost:5000
echo Frontend: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
