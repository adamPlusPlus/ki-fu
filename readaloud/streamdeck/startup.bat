@echo off
REM ReadAloud StreamDeck Integration Startup Script
REM This script starts ReadAloud in background mode for StreamDeck integration

echo Starting ReadAloud StreamDeck Integration...

REM Change to the ReadAloud directory
cd /d "%~dp0.."

REM Start background service
echo Starting background service...
start /min python background_service.py --daemon

REM Wait a moment for service to start
timeout /t 3 /nobreak >nul

REM Start StreamDeck plugin
echo Starting StreamDeck plugin...
start /min python streamdeck/plugin.py

echo ReadAloud StreamDeck integration started successfully!
echo The service is now running in the background.
echo Press any key to close this window...
pause >nul
