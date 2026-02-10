#!/bin/bash

# ================================================================
# ISO 20022 XSD Toolkit - Local Bank Network Deployment
# Linux/macOS Startup Script
# ================================================================

set -e

echo ""
echo "================================================================"
echo "    ISO 20022 XSD TOOLKIT - LOCAL DEPLOYMENT"
echo "================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed${NC}"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  macOS: brew install python3"
    echo "  RHEL/CentOS: sudo yum install python3"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[INFO]${NC} Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}[OK]${NC} Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo -e "${YELLOW}[INFO]${NC} Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo -e "${YELLOW}[INFO]${NC} Checking dependencies..."
pip install -r requirements.txt --quiet 2>/dev/null || {
    echo -e "${YELLOW}[WARNING]${NC} Some dependencies may have failed"
    echo -e "${YELLOW}[INFO]${NC} Installing core dependencies..."
    pip install flask openpyxl python-docx lxml rstr jinja2 waitress --quiet
}
echo -e "${GREEN}[OK]${NC} Dependencies ready"
echo ""

# Create necessary directories
mkdir -p static/uploads static/outputs logs

# Get local IP addresses
get_local_ips() {
    if command -v ip &> /dev/null; then
        ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v '127.0.0.1'
    elif command -v ifconfig &> /dev/null; then
        ifconfig | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v '127.0.0.1'
    fi
}

echo ""
echo "================================================================"
echo ""
echo "   Starting ISO 20022 XSD Toolkit..."
echo ""
echo "   Open in browser: http://localhost:5000"
echo ""
echo "   For network access, use your computer's IP address:"
for ip in $(get_local_ips); do
    echo "     http://${ip}:5000"
done
echo ""
echo "   Health check: http://localhost:5000/health"
echo "   Status page:  http://localhost:5000/status"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""
echo "================================================================"
echo ""

# Run with Waitress (production server) if available
if python3 -c "import waitress" 2>/dev/null; then
    echo -e "${GREEN}[INFO]${NC} Running with Waitress production server..."
    python3 -c "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=5000, threads=4)"
else
    echo -e "${YELLOW}[INFO]${NC} Running with Flask development server..."
    python3 app.py
fi
