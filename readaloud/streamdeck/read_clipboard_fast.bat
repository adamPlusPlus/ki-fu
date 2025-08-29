@echo off
echo ========================================
echo ReadAloud Fast TTS (Service Mode)
echo ========================================

REM Change to readaloud directory
cd /d "C:\Project\ki-fu\readaloud"

REM Get clipboard content using PowerShell
for /f "delims=" %%i in ('powershell -command "Get-Clipboard"') do set "clipboard_text=%%i"

REM Check if clipboard has content
if "%clipboard_text%"=="" (
    echo Clipboard is empty!
    echo.
    pause
    exit /b 1
)

echo Clipboard content: %clipboard_text:~0,100%...
echo.

REM Create output directory
if not exist "audio_output" mkdir "audio_output"

REM Generate unique filename using timestamp
set "timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "timestamp=%timestamp: =0%"
set "output_file=audio_output\output_%timestamp%.wav"

echo Generating audio to: %output_file%
echo Using persistent service (should be fast!)...
echo.

REM Call the service
python higgs_service.py --text "%clipboard_text%" --output "%output_file%"

REM Check if successful
if exist "%output_file%" (
    echo.
    echo Audio generated successfully!
    echo File: %output_file%
    
    REM Play the audio
    start "" "%output_file%"
    echo Audio is now playing...
) else (
    echo.
    echo Failed to generate audio!
    echo Make sure the Higgs Audio service is running!
    echo Run: start_higgs_service.bat
)

echo.
echo Press any key to continue...
pause >nul
