#!/bin/bash
# =============================================================================
# Run Django Backend Server
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
echo -e "${GREEN}║  FOSSEE Scientific Analytics - Django Backend              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"

# Navigate to backend directory
cd "$(dirname "$0")/backend"

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

# Run migrations
echo -e "${YELLOW}→ Running database migrations...${NC}"
python manage.py migrate --run-syncdb

# Start server
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Starting Django server at http://localhost:8000           ║${NC}"
echo -e "${GREEN}║  API available at http://localhost:8000/api/               ║${NC}"
echo -e "${GREEN}║  Press Ctrl+C to stop                                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

python manage.py runserver 0.0.0.0:8000
