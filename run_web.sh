#!/bin/bash
# =============================================================================
# Run React Web Frontend (Vite)
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
echo -e "${GREEN}║  FOSSEE Scientific Analytics - React Web Frontend          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"

# Navigate to web-frontend directory
cd "$(dirname "$0")/web-frontend"

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18+${NC}"
    echo "  Install via: brew install node"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}→ Using Node.js: $NODE_VERSION${NC}"

# Check for npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}✗ npm not found. Please install npm${NC}"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}→ Installing npm dependencies...${NC}"
    npm install
else
    echo -e "${GREEN}→ Dependencies already installed${NC}"
fi

# Check if backend is running
echo -e "${YELLOW}→ Checking backend connection...${NC}"
if curl -s http://localhost:8000/api/datasets/ > /dev/null 2>&1; then
    echo -e "${GREEN}→ Backend is running at http://localhost:8000${NC}"
else
    echo -e "${YELLOW}⚠ Backend not detected. Run ./run_backend.sh first${NC}"
fi

# Start Vite dev server
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Starting Vite dev server at http://localhost:5173         ║${NC}"
echo -e "${GREEN}║  Press Ctrl+C to stop                                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

npm run dev
