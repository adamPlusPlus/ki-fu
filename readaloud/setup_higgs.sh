#!/bin/bash
# Higgs Audio Setup Script for ReadAloud
# This script sets up Higgs Audio in H:/AI/higgs (or specified path)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default path (can be overridden)
HIGGS_PATH="${1:-H:/AI/higgs}"

echo "🎵 Setting up Higgs Audio for ReadAloud"
echo "======================================"

# Convert Windows path to Unix path if needed
if [[ "$HIGGS_PATH" == *":"* ]]; then
    # Convert H:/AI/higgs to /mnt/h/AI/higgs (for WSL) or similar
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        HIGGS_PATH=$(echo "$HIGGS_PATH" | sed 's|^\([A-Z]\):/|/\1/|' | sed 's|\\|/|g')
    else
        # For WSL, convert to /mnt/h/AI/higgs
        HIGGS_PATH=$(echo "$HIGGS_PATH" | sed 's|^\([A-Z]\):/|/mnt/\L\1/|' | sed 's|\\|/|g')
    fi
fi

print_status "Setting up Higgs Audio in: $HIGGS_PATH"

# Check if directory exists
if [[ ! -d "$HIGGS_PATH" ]]; then
    print_status "Creating directory $HIGGS_PATH..."
    mkdir -p "$HIGGS_PATH"
fi

# Change to the Higgs directory
cd "$HIGGS_PATH"

# Check if Higgs Audio is already cloned
if [[ -d "higgs-audio" ]]; then
    print_status "Higgs Audio already exists. Updating..."
    cd higgs-audio
    git pull
    cd ..
else
    print_status "Cloning Higgs Audio repository..."
    git clone https://github.com/boson-ai/higgs-audio.git
fi

# Check if clone was successful
if [[ ! -d "higgs-audio" ]]; then
    print_error "Failed to clone Higgs Audio repository"
    exit 1
fi

echo
print_status "Installing Higgs Audio dependencies..."
cd higgs-audio

# Check if requirements.txt exists
if [[ -f "requirements.txt" ]]; then
    print_status "Installing from requirements.txt..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
else
    print_warning "requirements.txt not found. Installing core dependencies..."
    python -m pip install torch torchaudio transformers accelerate
    python -m pip install librosa soundfile pydub
fi

# Go back to ReadAloud directory
cd - > /dev/null

echo
print_status "Updating ReadAloud configuration..."

# Update the config to point to the new Higgs Audio location
python3 -c "
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

config['higgs_config']['model_path'] = '$HIGGS_PATH/higgs-audio'
config['higgs_config']['python_path'] = 'python'
config['higgs_config']['higgs_script'] = 'examples/generation.py'

# Set TTS engine to Higgs Audio
config['tts_engine'] = 'higgs_audio'

# Save updated config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print('Configuration updated successfully!')
print(f'Higgs Audio path set to: $HIGGS_PATH/higgs-audio')
"

echo
print_status "Testing Higgs Audio installation..."
python3 -c "
import sys
import os

# Add Higgs Audio to Python path
higgs_path = '$HIGGS_PATH/higgs-audio'
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

echo
print_status "Testing ReadAloud with Higgs Audio..."
python3 main.py --info

echo
print_success "Higgs Audio setup complete!"
echo
echo "Next steps:"
echo "1. Test TTS: python3 main.py --interactive"
echo "2. Run StreamDeck integration: python3 streamdeck/integrate.py"
echo
echo "Higgs Audio is now configured at: $HIGGS_PATH/higgs-audio"
echo
