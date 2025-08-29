@echo off
REM ReadAloud Web Interface Startup Script
echo 🌐 Starting ReadAloud Web Interface...
echo 📱 Opening browser automatically...
echo 🔧 Interface will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Install dependencies if not already installed
python -m pip install flask pyperclip keyboard --quiet

REM Start the web interface
python web_interface.py
