@echo off
echo ========================================
echo ReadAloud Clipboard TTS
echo ========================================

REM Change to Higgs Audio directory
cd /d "H:\AI\higgs\higgs-audio"

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
if not exist "C:\Project\ki-fu\readaloud\audio_output" mkdir "C:\Project\ki-fu\readaloud\audio_output"

REM Generate unique filename using timestamp
set "timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "timestamp=%timestamp: =0%"
set "output_file=C:\Project\ki-fu\readaloud\audio_output\output_%timestamp%.wav"

echo Generating audio to: %output_file%
echo This may take 1-2 minutes on first run...
echo.

REM Call Higgs Audio directly
python examples/generation.py --transcript "%clipboard_text%" --out_path "%output_file%" --temperature 0.3

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
)

echo.
echo Press any key to continue...
pause >nul
