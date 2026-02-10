@echo off
REM ================================================================
REM ISO 20022 XSD Toolkit - Windows Service Installation
REM Run this script as Administrator to install as a Windows Service
REM ================================================================

echo.
echo ================================================================
echo   ISO 20022 XSD Toolkit - Windows Service Installer
echo ================================================================
echo.
echo This script will install the toolkit as a Windows Service
echo so it starts automatically when Windows boots.
echo.
echo Prerequisites:
echo   1. Python 3.8+ installed
echo   2. Run this script as Administrator
echo   3. NSSM (Non-Sucking Service Manager) installed
echo.

REM Check for admin rights
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Please run this script as Administrator
    pause
    exit /b 1
)

REM Check if NSSM is available
where nssm >nul 2>&1
if errorlevel 1 (
    echo [INFO] NSSM not found. Downloading...
    echo.
    echo Please download NSSM from: https://nssm.cc/download
    echo Extract and add to PATH, then run this script again.
    echo.
    echo Alternative: You can run the toolkit manually using start.bat
    pause
    exit /b 1
)

set SERVICE_NAME=ISO20022Toolkit
set CURRENT_DIR=%~dp0
set PYTHON_PATH=
set APP_PATH=%CURRENT_DIR%app.py

REM Find Python path
for /f "tokens=*" %%i in ('where python') do (
    set PYTHON_PATH=%%i
    goto :found_python
)
:found_python

if "%PYTHON_PATH%"=="" (
    echo [ERROR] Python not found in PATH
    pause
    exit /b 1
)

echo [INFO] Using Python: %PYTHON_PATH%
echo [INFO] Application: %APP_PATH%
echo [INFO] Service Name: %SERVICE_NAME%
echo.

REM Check if service already exists
sc query %SERVICE_NAME% >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Service already exists. Stopping and removing...
    nssm stop %SERVICE_NAME%
    nssm remove %SERVICE_NAME% confirm
    timeout /t 2 /nobreak >nul
)

REM Install the service
echo [INFO] Installing service...
nssm install %SERVICE_NAME% "%PYTHON_PATH%" "%APP_PATH%"
nssm set %SERVICE_NAME% AppDirectory "%CURRENT_DIR%"
nssm set %SERVICE_NAME% DisplayName "ISO 20022 XSD Toolkit"
nssm set %SERVICE_NAME% Description "ISO 20022 Payment Message Schema Analysis Toolkit"
nssm set %SERVICE_NAME% Start SERVICE_AUTO_START
nssm set %SERVICE_NAME% AppStdout "%CURRENT_DIR%logs\service_stdout.log"
nssm set %SERVICE_NAME% AppStderr "%CURRENT_DIR%logs\service_stderr.log"
nssm set %SERVICE_NAME% AppRotateFiles 1
nssm set %SERVICE_NAME% AppRotateBytes 10485760

echo.
echo [INFO] Starting service...
nssm start %SERVICE_NAME%

echo.
echo ================================================================
echo   Installation Complete!
echo ================================================================
echo.
echo The service is now installed and running.
echo.
echo   Service Name: %SERVICE_NAME%
echo   URL: http://localhost:5000
echo.
echo   To manage the service:
echo     Start:   nssm start %SERVICE_NAME%
echo     Stop:    nssm stop %SERVICE_NAME%
echo     Restart: nssm restart %SERVICE_NAME%
echo     Remove:  nssm remove %SERVICE_NAME%
echo.
echo   Or use Windows Services Manager (services.msc)
echo.
pause
