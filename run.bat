@echo off
REM Food Delivery Route Optimization - Windows Startup Script

echo.
echo ============================================================
echo  Food Delivery Route Optimization System
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python.exe --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python.exe --version

echo.
echo [2/4] Installing dependencies...
python.exe -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!

echo.
echo [3/4] Running tests...
python.exe demo.py
if errorlevel 1 (
    echo ERROR: Tests failed
    pause
    exit /b 1
)

echo.
echo [4/4] Starting Flask server...
echo.
echo ============================================================
echo  Server starting at http://localhost:5000
echo ============================================================
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0\src"
python.exe app.py

pause
