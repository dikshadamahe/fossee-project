@echo off
REM =============================================================================
REM Run Django Backend Server
REM Chemical Equipment Parameter Visualizer - FOSSEE Scientific Analytics
REM Windows Batch Script
REM =============================================================================

title FOSSEE Backend - Django Server

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  FOSSEE Scientific Analytics - Django Backend              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.12 from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2 delims= " %%i in ('python --version') do set PYVER=%%i
echo [INFO] Using Python %PYVER%

REM Create virtual environment if not exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -q -r requirements.txt

REM Run database migrations
echo [INFO] Running database migrations...
python manage.py migrate --run-syncdb

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Starting Django server at http://localhost:8000           ║
echo ║  API available at http://localhost:8000/api/               ║
echo ║  Press Ctrl+C to stop                                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Start server
python manage.py runserver 0.0.0.0:8000
