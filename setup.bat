@echo off
REM =============================================================================
REM Full Setup Script for Windows
REM Chemical Equipment Parameter Visualizer - FOSSEE Scientific Analytics
REM Sets up all components: backend, web frontend, and desktop app
REM =============================================================================

title FOSSEE Full Setup

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  FOSSEE Scientific Analytics - Full Setup                  ║
echo ║  This will set up backend, web frontend, and desktop app   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Store root directory
set ROOT_DIR=%~dp0

REM =============================================================================
REM Backend Setup
REM =============================================================================
echo.
echo [1/3] Setting up Django Backend...
echo ════════════════════════════════════════════════════════════
cd /d "%ROOT_DIR%backend"

if not exist "venv" (
    echo [INFO] Creating virtual environment for backend...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo [INFO] Installing backend dependencies...
pip install -q -r requirements.txt
echo [INFO] Running database migrations...
python manage.py migrate --run-syncdb
call deactivate

echo [SUCCESS] Backend setup complete!

REM =============================================================================
REM Web Frontend Setup
REM =============================================================================
echo.
echo [2/3] Setting up React Web Frontend...
echo ════════════════════════════════════════════════════════════
cd /d "%ROOT_DIR%web-frontend"

echo [INFO] Installing npm dependencies...
call npm install

echo [SUCCESS] Web frontend setup complete!

REM =============================================================================
REM Desktop App Setup
REM =============================================================================
echo.
echo [3/3] Setting up PyQt5 Desktop App...
echo ════════════════════════════════════════════════════════════
cd /d "%ROOT_DIR%desktop-app"

if not exist "venv" (
    echo [INFO] Creating virtual environment for desktop app...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo [INFO] Installing desktop app dependencies...
pip install -q -r requirements.txt
call deactivate

echo [SUCCESS] Desktop app setup complete!

REM =============================================================================
REM Done
REM =============================================================================
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Setup Complete!                                           ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║  To start the application:                                 ║
echo ║                                                            ║
echo ║  1. Run backend:     run_backend.bat                       ║
echo ║  2. Run web app:     run_web.bat                           ║
echo ║  3. Run desktop:     run_desktop.bat                       ║
echo ║                                                            ║
echo ║  URLs:                                                     ║
echo ║  - Backend API: http://localhost:8000/api/                 ║
echo ║  - Web App:     http://localhost:5173                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

cd /d "%ROOT_DIR%"
pause
