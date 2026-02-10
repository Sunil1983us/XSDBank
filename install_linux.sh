#!/bin/bash

# ================================================================
# ISO 20022 XSD Toolkit - Linux Production Installation Script
# Run with sudo: sudo bash install_linux.sh
# ================================================================

set -e

# Configuration
INSTALL_DIR="/opt/iso20022-toolkit"
SERVICE_USER="www-data"
SERVICE_GROUP="www-data"
LOG_DIR="/var/log/iso20022-toolkit"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "================================================================"
echo "  ISO 20022 XSD Toolkit - Production Installation"
echo "================================================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[ERROR] Please run as root (sudo bash install_linux.sh)${NC}"
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed${NC}"
    echo "Install with: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Python 3 found: $(python3 --version)"

# Create installation directory
echo -e "${YELLOW}[INFO]${NC} Creating installation directory..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$LOG_DIR"

# Copy files
echo -e "${YELLOW}[INFO]${NC} Copying application files..."
cp -r ./* "$INSTALL_DIR/"
rm -f "$INSTALL_DIR/install_linux.sh"
rm -f "$INSTALL_DIR/install_service.bat"
rm -f "$INSTALL_DIR/*.service"

# Create virtual environment
echo -e "${YELLOW}[INFO]${NC} Creating virtual environment..."
cd "$INSTALL_DIR"
python3 -m venv venv

# Install dependencies
echo -e "${YELLOW}[INFO]${NC} Installing Python dependencies..."
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install -r requirements.txt

# Create directories
mkdir -p "$INSTALL_DIR/static/uploads"
mkdir -p "$INSTALL_DIR/static/outputs"
mkdir -p "$INSTALL_DIR/logs"

# Set permissions
echo -e "${YELLOW}[INFO]${NC} Setting permissions..."
chown -R "$SERVICE_USER:$SERVICE_GROUP" "$INSTALL_DIR"
chown -R "$SERVICE_USER:$SERVICE_GROUP" "$LOG_DIR"
chmod -R 755 "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/start.sh"

# Install systemd service
echo -e "${YELLOW}[INFO]${NC} Installing systemd service..."
cat > /etc/systemd/system/iso20022-toolkit.service << EOF
[Unit]
Description=ISO 20022 XSD Toolkit Web Application
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_GROUP
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/venv/bin:/usr/bin
ExecStart=$INSTALL_DIR/venv/bin/python -c "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=5000, threads=4)"
Restart=always
RestartSec=5
StandardOutput=append:$LOG_DIR/app.log
StandardError=append:$LOG_DIR/error.log

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable iso20022-toolkit.service

# Start the service
echo -e "${YELLOW}[INFO]${NC} Starting service..."
systemctl start iso20022-toolkit.service

# Wait and check status
sleep 2
if systemctl is-active --quiet iso20022-toolkit.service; then
    echo -e "${GREEN}[OK]${NC} Service is running"
else
    echo -e "${RED}[ERROR]${NC} Service failed to start"
    echo "Check logs with: journalctl -u iso20022-toolkit.service"
    exit 1
fi

echo ""
echo "================================================================"
echo -e "  ${GREEN}Installation Complete!${NC}"
echo "================================================================"
echo ""
echo "  Installation Directory: $INSTALL_DIR"
echo "  Log Directory: $LOG_DIR"
echo ""
echo "  Access the application at:"
echo "    http://localhost:5000"
echo "    http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "  Service commands:"
echo "    Start:   sudo systemctl start iso20022-toolkit"
echo "    Stop:    sudo systemctl stop iso20022-toolkit"
echo "    Restart: sudo systemctl restart iso20022-toolkit"
echo "    Status:  sudo systemctl status iso20022-toolkit"
echo "    Logs:    sudo journalctl -u iso20022-toolkit -f"
echo ""
echo "  Configuration file: $INSTALL_DIR/config.json"
echo ""
