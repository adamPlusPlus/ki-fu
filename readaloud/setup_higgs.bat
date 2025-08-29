@echo off
REM Higgs Audio Setup Script for ReadAloud
REM This script sets up Higgs Audio in H:\AI\higgs

echo 🎵 Setting up Higgs Audio for ReadAloud
echo ======================================

REM Check if directory exists
if not exist "H:\AI\higgs" (
    echo Creating directory H:\AI\higgs...
    mkdir "H:\AI\higgs"
)

REM Change to the Higgs directory
cd /d "H:\AI\higgs"

REM Check if Higgs Audio is already cloned
if exist "higgs-audio" (
    echo Higgs Audio already exists. Updating...
    cd higgs-audio
    git pull
    cd ..
) else (
    echo Cloning Higgs Audio repository...
    git clone https://github.com/boson-ai/higgs-audio.git
)

REM Check if clone was successful
if not exist "higgs-audio" (
    echo [ERROR] Failed to clone Higgs Audio repository
    pause
    exit /b 1
)

echo.
echo [INFO] Installing Higgs Audio dependencies...
cd higgs-audio

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo Installing from requirements.txt...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) else (
    echo [WARNING] requirements.txt not found. Installing core dependencies...
    python -m pip install torch torchaudio transformers accelerate
    python -m pip install librosa soundfile pydub
)

REM Go back to ReadAloud directory
cd /d "%~dp0"

echo.
echo [INFO] Updating ReadAloud configuration...
REM Update the config to point to the new Higgs Audio location
python -c "
import json
import os

config_file = 'readaloud_config.json'
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    config = {}

# Update Higgs Audio path
if 'higgs_config' not in config:
    config['higgs_config'] = {}

config['higgs_config']['model_path'] = 'H:/AI/higgs/higgs-audio'
config['higgs_config']['python_path'] = 'python'
config['higgs_config']['higgs_script'] = 'examples/generation.py'

# Set TTS engine to Higgs Audio
config['tts_engine'] = 'higgs_audio'

# Save updated config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print('Configuration updated successfully!')
print(f'Higgs Audio path set to: H:/AI/higgs/higgs-audio')
"

echo.
echo [INFO] Testing Higgs Audio installation...
python -c "
import sys
import os

# Add Higgs Audio to Python path
higgs_path = 'H:/AI/higgs/higgs-audio'
if os.path.exists(higgs_path):
    sys.path.insert(0, higgs_path)
    try:
        # Try to import Higgs Audio modules
        import examples.generation
        print('✓ Higgs Audio modules imported successfully')
    except ImportError as e:
        print(f'⚠ Some Higgs Audio modules not available: {e}')
        print('This is normal for initial setup')
    
    # Check if generation script exists
    gen_script = os.path.join(higgs_path, 'examples', 'generation.py')
    if os.path.exists(gen_script):
        print('✓ Generation script found')
    else:
        print('⚠ Generation script not found')
else:
    print('✗ Higgs Audio directory not found')
"

echo.
echo [INFO] Testing ReadAloud with Higgs Audio...
python main.py --info

echo.
echo 🎉 Higgs Audio setup complete!
echo.
echo Next steps:
echo 1. Test TTS: python main.py --interactive
echo 2. Run StreamDeck integration: python streamdeck/integrate.py
echo.
echo Higgs Audio is now configured at: H:\AI\higgs\higgs-audio
echo.
pause
