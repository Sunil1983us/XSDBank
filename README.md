# ISO 20022 XSD Toolkit

A professional web-based toolkit for analyzing, comparing, and generating test data for ISO 20022 payment message schemas.

## 🚀 Quick Start

### Windows
```batch
start.bat
```

### Linux / macOS
```bash
chmod +x start.sh
./start.sh
```

Then open: **http://localhost:5000**

---

## 📦 Features

| Feature | Description | Output |
|---------|-------------|--------|
| **Comprehensive Analysis** | Extract ALL metadata including Yellow/White field classifications from XSD annotations | Excel (.xlsx) |
| **Schema Documentation** | Generate detailed documentation of schema structure | Excel (.xlsx) |
| **Schema Comparison** | Compare 2 schemas with detailed difference reporting | Excel + Word + HTML |
| **Test Data Generator** | Generate valid XML test files from schema | ZIP of XML files |

---

## 📁 Project Structure

```
iso_toolkit/
├── app.py                 # Flask web application
├── config.json            # Configuration (create from template)
├── config.json.template   # Configuration template
├── requirements.txt       # Python dependencies
├── start.bat              # Windows startup script
├── start.sh               # Linux/macOS startup script
├── install_linux.sh       # Linux production installer
├── install_service.bat    # Windows service installer
├── tools/
│   ├── schema_analyzer.py     # Comprehensive XSD analysis
│   ├── schema_documenter.py   # Schema documentation generator
│   ├── schema_comparator.py   # Schema comparison tool
│   ├── xml_generator.py       # Test XML file generator
│   ├── html_report_generator.py # Interactive HTML reports
│   └── code_set_loader.py     # ISO 20022 code set loader
├── templates/
│   └── index.html         # Web interface
├── data/
│   └── external_codes.json # ISO 20022 code definitions
├── static/
│   ├── uploads/           # Temporary uploaded files
│   └── outputs/           # Generated output files
└── logs/                  # Application logs
```

---

## ⚙️ Configuration

Copy the template and customize:
```bash
cp config.json.template config.json
```

Key settings in `config.json`:
```json
{
    "HOST": "0.0.0.0",
    "PORT": 5000,
    "DEBUG": false,
    "SECRET_KEY": "CHANGE-THIS-TO-SECURE-RANDOM-STRING",
    "TIMEOUT_SECONDS": 300,
    "CLEANUP_HOURS": 24
}
```

**Important:** Change `SECRET_KEY` before production deployment.

---

## 🔧 Installation Options

### Option 1: Development Mode
```bash
# Windows
start.bat

# Linux/macOS
./start.sh
```

### Option 2: Linux Production
```bash
sudo bash install_linux.sh
```
Installs as a systemd service at `/opt/iso20022-toolkit`.

### Option 3: Windows Service
Requires [NSSM](https://nssm.cc/download):
```batch
install_service.bat
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/upload` | POST | Upload XSD/XML files |
| `/run_tool` | POST | Execute analysis tool |
| `/download/<file>` | GET | Download generated file |
| `/preview/<file>` | GET | Preview HTML in browser |
| `/health` | GET | Health check |
| `/status` | GET | Detailed status |
| `/cleanup` | POST | Trigger file cleanup |

---

## 🔒 Security Notes

For bank network deployment:
1. Change `SECRET_KEY` in config.json
2. Use a reverse proxy (nginx) for SSL
3. Restrict network access via firewall
4. Files auto-cleanup after 24 hours (configurable)

---

## 📋 Requirements

- Python 3.8+
- 512MB RAM minimum
- 1GB disk space

---

## 🐛 Troubleshooting

**Port in use:**
```bash
# Change port in config.json or find process:
# Windows: netstat -ano | findstr :5000
# Linux: lsof -i :5000
```

**Check logs:**
```bash
# Application logs
tail -f logs/toolkit_*.log

# Linux service logs  
sudo journalctl -u iso20022-toolkit -f
```

---

## 📜 License

Internal use only. Contact your organization for licensing terms.
