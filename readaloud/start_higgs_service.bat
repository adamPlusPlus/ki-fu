@echo off
echo ========================================
echo Starting Higgs Audio Persistent Service
echo ========================================
echo.
echo This service will:
echo 1. Load the AI model once (takes 1-2 minutes)
echo 2. Keep it in memory for fast TTS generation
echo 3. Process requests much faster
echo.
echo Keep this window open while using TTS!
echo.
echo Press Ctrl+C to stop the service
echo.

cd /d "%~dp0"
python higgs_service.py --service

pause
