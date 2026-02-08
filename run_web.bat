@echo off
REM =============================================================================
REM Run React Web Frontend
REM Chemical Equipment Parameter Visualizer - FOSSEE Scientific Analytics
REM Windows Batch Script
REM =============================================================================

title FOSSEE Web Frontend - Vite Dev Server

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  FOSSEE Scientific Analytics - React Web Frontend          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Navigate to web frontend directory
cd /d "%~dp0web-frontend"

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)

REM Check Node version
for /f "tokens=1 delims=v" %%i in ('node --version') do set NODEVER=%%i
echo [INFO] Using Node.js %NODEVER%

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo [INFO] Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Starting Vite dev server at http://localhost:5173         ║
echo ║  Press Ctrl+C to stop                                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Start dev server
call npm run dev
