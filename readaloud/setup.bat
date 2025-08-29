@echo off
REM ReadAloud Setup Script for Windows
REM This script helps set up the ReadAloud TTS tool

echo 🎵 ReadAloud TTS Tool Setup
echo ============================

REM Check if Python is installed
echo [SETUP] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

echo [INFO] Python found: 
python --version

REM Install Python dependencies
echo [SETUP] Installing Python dependencies...
if exist requirements.txt (
    echo [INFO] Installing from requirements.txt...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) else (
    echo [WARNING] requirements.txt not found. Installing core dependencies...
    python -m pip install torch torchaudio transformers accelerate
    python -m pip install pyperclip watchdog keyboard pynput
    python -m pip install librosa soundfile pydub click rich
)

REM Setup Higgs Audio
echo [SETUP] Setting up Higgs Audio TTS engine...
set /p setup_higgs="Do you want to set up Higgs Audio? (y/n): "

if /i "%setup_higgs%"=="y" (
    echo [INFO] Cloning Higgs Audio repository...
    
    if not exist "higgs-audio" (
        git clone https://github.com/boson-ai/higgs-audio.git
    ) else (
        echo [INFO] Higgs Audio directory already exists. Updating...
        cd higgs-audio
        git pull
        cd ..
    )
    
    echo [INFO] Installing Higgs Audio dependencies...
    cd higgs-audio
    python -m pip install -r requirements.txt
    cd ..
    
    echo [INFO] Higgs Audio setup complete!
) else (
    echo [WARNING] Skipping Higgs Audio setup. You can set it up later manually.
)

REM Create configuration
echo [SETUP] Creating configuration...
if not exist "readaloud_config.json" (
    echo [INFO] Creating default configuration...
    python -c "from config import Config; config = Config(); config.create_sample_config(); print('Configuration created successfully!')"
) else (
    echo [INFO] Configuration file already exists.
)

REM Create audio output directory
echo [SETUP] Creating necessary directories...
if not exist "audio_output" mkdir audio_output
if not exist "logs" mkdir logs

echo [INFO] Directories created: audio_output/, logs/

REM Test installation
echo [SETUP] Testing installation...
echo [INFO] Checking TTS engines...
python main.py --info

echo [INFO] Checking available voices...
python main.py --voices

echo [INFO] Installation test complete!

echo.
echo 🎉 Setup complete! ReadAloud is ready to use.
echo.
echo Quick start:
echo   python main.py --interactive    # Start interactive mode
echo   python main.py --hotkeys        # Enable global hotkeys
echo   python main.py --clipboard      # Monitor clipboard
echo   python main.py --monitor file.txt # Monitor file changes
echo.
echo For more options: python main.py --help
echo.
echo Configuration file: readaloud_config.json
echo Edit this file to customize settings.
echo.
pause
