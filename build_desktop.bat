@echo off
REM =============================================================================
REM Build Desktop Executable with PyInstaller
REM Chemical Equipment Parameter Visualizer - FOSSEE Scientific Analytics
REM Windows Batch Script
REM =============================================================================

title FOSSEE Desktop - Build Executable

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  FOSSEE Scientific Analytics - Build Desktop Executable    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Navigate to desktop app directory
cd /d "%~dp0desktop-app"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Activate virtual environment
if not exist "venv" (
    echo [ERROR] Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Install PyInstaller if not present
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

echo [INFO] Building executable...

REM Build with PyInstaller
pyinstaller ^
    --name "FOSSEE-ChemViz" ^
    --windowed ^
    --onefile ^
    --icon "styles/icon.ico" ^
    --add-data "styles;styles" ^
    --hidden-import "PyQt5.sip" ^
    --hidden-import "matplotlib.backends.backend_qt5agg" ^
    main.py

if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Build Complete!                                           ║
echo ║                                                            ║
echo ║  Executable location:                                      ║
echo ║  desktop-app\dist\FOSSEE-ChemViz.exe                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

call deactivate
pause
