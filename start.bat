@echo off
REM ================================================================
REM ISO 20022 XSD Toolkit - Local Bank Network Deployment
REM Windows Startup Script
REM ================================================================

echo.
echo ================================================================
echo     ISO 20022 XSD TOOLKIT - LOCAL DEPLOYMENT
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo [INFO] Checking dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install
    echo [INFO] Attempting to install core dependencies...
    pip install flask openpyxl python-docx lxml rstr jinja2 waitress --quiet
)
echo [OK] Dependencies ready
echo.

REM Create necessary directories
if not exist "static\uploads" mkdir static\uploads
if not exist "static\outputs" mkdir static\outputs
if not exist "logs" mkdir logs

REM Start the application
echo.
echo ================================================================
echo.
echo   Starting ISO 20022 XSD Toolkit...
echo.
echo   Open in browser: http://localhost:5000
echo.
echo   For network access, use your computer's IP address:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do echo     http://%%b:5000
)
echo.
echo   Press Ctrl+C to stop the server
echo.
echo ================================================================
echo.

REM Run with Waitress (production WSGI server) if available
python -c "import waitress" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Running with Flask development server...
    python app.py
) else (
    echo [INFO] Running with Waitress production server...
    python -c "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=5000, threads=4)"
)

pause
