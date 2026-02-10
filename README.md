# ISO 20022 XSD Toolkit - Local Bank Network Deployment

A professional web-based toolkit for analyzing, comparing, and generating test data for ISO 20022 payment message schemas.

## 🚀 Quick Start

### Windows
```batch
# Double-click or run:
start.bat
```

### Linux / macOS
```bash
chmod +x start.sh
./start.sh
```

Then open your browser to: **http://localhost:5000**

---

## 📦 Features

| Feature | Description |
|---------|-------------|
| **Comprehensive Analysis** | Extract ALL metadata from XSD schemas including field classifications, restrictions, and usage rules |
| **Schema Documentation** | Generate detailed Excel documentation of schema structure |
| **Schema Comparison** | Compare 2 or more schemas with Excel, Word, and HTML reports |
| **Test Data Generation** | Generate valid XML test files based on schema constraints |

---

## 🔧 Installation Options

### Option 1: Quick Start (Development)

Best for testing and evaluation:

```bash
# Windows
start.bat

# Linux/macOS
./start.sh
```

### Option 2: Production Installation (Linux)

For permanent deployment on a Linux server:

```bash
sudo bash install_linux.sh
```

This will:
- Install to `/opt/iso20022-toolkit`
- Create a systemd service
- Start automatically on boot
- Use the Waitress production WSGI server

### Option 3: Windows Service

For permanent deployment on Windows Server:

1. Download [NSSM](https://nssm.cc/download)
2. Extract and add to PATH
3. Run as Administrator:
   ```batch
   install_service.bat
   ```

---

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
    "HOST": "0.0.0.0",        // Network interface (0.0.0.0 = all)
    "PORT": 5000,             // HTTP port
    "DEBUG": false,           // Debug mode (false for production)
    "SECRET_KEY": "...",      // IMPORTANT: Change this!
    "TIMEOUT_SECONDS": 300,   // Max processing time
    "CLEANUP_HOURS": 24       // Auto-delete files after X hours
}
```

### Environment Variables (Optional)

Configuration can also be set via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `TOOLKIT_HOST` | `0.0.0.0` | Bind address |
| `TOOLKIT_PORT` | `5000` | HTTP port |
| `TOOLKIT_DEBUG` | `False` | Debug mode |
| `TOOLKIT_SECRET_KEY` | (random) | Flask secret key |
| `TOOLKIT_MAX_UPLOAD_MB` | `100` | Max upload size (MB) |
| `TOOLKIT_TIMEOUT` | `300` | Processing timeout (seconds) |
| `TOOLKIT_CLEANUP_HOURS` | `24` | Auto-cleanup interval |

---

## 🔒 Security Recommendations for Bank Networks

### Network Security

1. **Firewall Rules**: Only allow access from trusted IP ranges
   ```bash
   # Linux example
   sudo ufw allow from 10.0.0.0/8 to any port 5000
   ```

2. **Reverse Proxy**: Use Nginx/Apache for SSL termination
   ```nginx
   server {
       listen 443 ssl;
       server_name toolkit.yourbank.local;
       
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Change Default Secret Key**
   ```json
   {
       "SECRET_KEY": "your-long-random-string-here-minimum-32-chars"
   }
   ```

### File Security

- Uploaded files are stored temporarily in `static/uploads/`
- Output files are stored in `static/outputs/`
- Files are automatically cleaned up after 24 hours (configurable)
- Manual cleanup: POST to `/cleanup`

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/upload` | POST | Upload XSD/XML files |
| `/run_tool` | POST | Execute analysis tool |
| `/download/<file>` | GET | Download generated file |
| `/preview/<file>` | GET | Preview HTML in browser |
| `/health` | GET | Health check (for monitoring) |
| `/status` | GET | Detailed status information |
| `/cleanup` | POST | Trigger file cleanup |

### Health Check Response

```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00",
    "version": "2.0.0-local"
}
```

---

## 📁 Directory Structure

```
iso_toolkit_local/
├── app.py                    # Main Flask application
├── config.json               # Configuration file
├── requirements.txt          # Python dependencies
├── start.bat                 # Windows startup script
├── start.sh                  # Linux/macOS startup script
├── install_service.bat       # Windows service installer
├── install_linux.sh          # Linux production installer
├── tools/                    # Analysis tool scripts
│   ├── iso20022_comprehensive_analyzer.py
│   ├── xsd_to_xml_enhanced.py
│   ├── xsd_comparison_enhanced.py
│   └── test_data_generator.py
├── templates/
│   └── index.html            # Web interface
├── data/
│   └── external_codes.json   # Code set definitions
├── static/
│   ├── uploads/              # Temporary uploaded files
│   └── outputs/              # Generated output files
└── logs/                     # Application logs
```

---

## 🔍 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000

# Linux:
lsof -i :5000
```

Change port in `config.json` if needed.

**Permission denied (Linux):**
```bash
sudo chown -R $USER:$USER .
chmod +x start.sh
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Check Logs

```bash
# Application logs
tail -f logs/toolkit_*.log

# Linux service logs
sudo journalctl -u iso20022-toolkit -f
```

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Memory**: 512MB minimum, 2GB recommended
- **Disk**: 1GB for application + space for uploads
- **OS**: Windows 10/11, Windows Server 2016+, Ubuntu 20.04+, RHEL 8+

---

## 📞 Support

For issues or questions:
1. Check the logs in `/logs` directory
2. Review troubleshooting section above
3. Contact your IT department

---

## 📜 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024 | Local deployment version with production features |
| 1.0.0 | 2024 | Initial Render cloud version |
