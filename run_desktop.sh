#!/bin/bash
# =============================================================================
# Run PyQt5 Desktop Application
# Chemical Equipment Parameter Visualizer
# FOSSEE Scientific Analytics
# =============================================================================

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  FOSSEE Scientific Analytics - PyQt5 Desktop App           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"

# Navigate to desktop-app directory
cd "$(dirname "$0")/desktop-app"

# Python 3.12 paths (macOS)
PYTHON_PATHS=(
    "/opt/homebrew/bin/python3.12"
    "/usr/local/bin/python3.12"
    "/usr/bin/python3.12"
    "python3.12"
    "python3"
)

# Find Python 3.12
PYTHON=""
for path in "${PYTHON_PATHS[@]}"; do
    if command -v "$path" &> /dev/null; then
        version=$("$path" --version 2>&1)
        if [[ "$version" == *"3.12"* ]] || [[ "$version" == *"3.1"* ]]; then
            PYTHON="$path"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "${YELLOW}⚠ Python 3.12 not found, using default python3${NC}"
    PYTHON="python3"
fi

echo -e "${GREEN}→ Using Python: $($PYTHON --version)${NC}"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}→ Creating virtual environment...${NC}"
    $PYTHON -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}→ Activated virtual environment${NC}"

# Install dependencies
echo -e "${YELLOW}→ Installing dependencies...${NC}"
pip install -q -r requirements.txt

# Check if backend is running
echo -e "${YELLOW}→ Checking backend connection...${NC}"
if curl -s http://localhost:8000/api/datasets/ > /dev/null 2>&1; then
    echo -e "${GREEN}→ Backend is running at http://localhost:8000${NC}"
else
    echo -e "${YELLOW}⚠ Backend not detected at http://localhost:8000${NC}"
    echo -e "${YELLOW}  Run ./run_backend.sh in another terminal first${NC}"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start desktop application
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Launching PyQt5 Desktop Application                       ║${NC}"
echo -e "${GREEN}║  Close window or press Ctrl+C to stop                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

python main.py
