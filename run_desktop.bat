@echo off
REM =============================================================================
REM Run PyQt5 Desktop Application
REM Chemical Equipment Parameter Visualizer - FOSSEE Scientific Analytics
REM Windows Batch Script
REM =============================================================================

title FOSSEE Desktop App - PyQt5

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  FOSSEE Scientific Analytics - PyQt5 Desktop App           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Navigate to desktop app directory
cd /d "%~dp0desktop-app"

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

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Starting PyQt5 Desktop Application...                     ║
echo ║  Close the window to exit                                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Start desktop app
python main.py
