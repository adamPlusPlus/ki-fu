@echo off
echo ========================================
echo ReadAloud - Integrated TTS System
echo ========================================
echo.
echo This will start:
echo 1. Higgs Audio persistent service
echo 2. Web interface (browser)
echo 3. Both are integrated and managed together
echo.
echo Press Ctrl+C in the web interface to stop everything
echo.

cd /d "%~dp0"

echo 🚀 Starting ReadAloud system...
python web_interface.py

echo.
echo 🛑 ReadAloud system stopped
pause
