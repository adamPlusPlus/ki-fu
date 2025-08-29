#!/bin/bash
# ReadAloud Setup Script
# This script helps set up the ReadAloud TTS tool

set -e

echo "🎵 ReadAloud TTS Tool Setup"
echo "============================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_header "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        print_status "Python 3 found: $(python3 --version)"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        print_status "Python found: $(python --version)"
    else
        print_error "Python not found. Please install Python 3.7+ and try again."
        exit 1
    fi
}

# Install Python dependencies
install_dependencies() {
    print_header "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        print_status "Installing from requirements.txt..."
        $PYTHON_CMD -m pip install --upgrade pip
        $PYTHON_CMD -m pip install -r requirements.txt
    else
        print_warning "requirements.txt not found. Installing core dependencies..."
        $PYTHON_CMD -m pip install torch torchaudio transformers accelerate
        $PYTHON_CMD -m pip install pyperclip watchdog keyboard pynput
        $PYTHON_CMD -m pip install librosa soundfile pydub click rich
    fi
}

# Setup Higgs Audio
setup_higgs_audio() {
    print_header "Setting up Higgs Audio TTS engine..."
    
    read -p "Do you want to set up Higgs Audio? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cloning Higgs Audio repository..."
        
        if [ ! -d "higgs-audio" ]; then
            git clone https://github.com/boson-ai/higgs-audio.git
        else
            print_status "Higgs Audio directory already exists. Updating..."
            cd higgs-audio
            git pull
            cd ..
        fi
        
        print_status "Installing Higgs Audio dependencies..."
        cd higgs-audio
        $PYTHON_CMD -m pip install -r requirements.txt
        cd ..
        
        print_status "Higgs Audio setup complete!"
    else
        print_warning "Skipping Higgs Audio setup. You can set it up later manually."
    fi
}

# Create configuration
create_config() {
    print_header "Creating configuration..."
    
    if [ ! -f "readaloud_config.json" ]; then
        print_status "Creating default configuration..."
        $PYTHON_CMD -c "
from config import Config
config = Config()
config.create_sample_config()
print('Configuration created successfully!')
"
    else
        print_status "Configuration file already exists."
    fi
}

# Create audio output directory
create_directories() {
    print_header "Creating necessary directories..."
    
    mkdir -p audio_output
    mkdir -p logs
    
    print_status "Directories created: audio_output/, logs/"
}

# Test installation
test_installation() {
    print_header "Testing installation..."
    
    print_status "Checking TTS engines..."
    $PYTHON_CMD main.py --info
    
    print_status "Checking available voices..."
    $PYTHON_CMD main.py --voices
    
    print_status "Installation test complete!"
}

# Main setup function
main() {
    print_header "Starting ReadAloud setup..."
    
    check_python
    install_dependencies
    setup_higgs_audio
    create_config
    create_directories
    test_installation
    
    echo
    echo "🎉 Setup complete! ReadAloud is ready to use."
    echo
    echo "Quick start:"
    echo "  python main.py --interactive    # Start interactive mode"
    echo "  python main.py --hotkeys        # Enable global hotkeys"
    echo "  python main.py --clipboard      # Monitor clipboard"
    echo "  python main.py --monitor file.txt # Monitor file changes"
    echo
    echo "For more options: python main.py --help"
    echo
    echo "Configuration file: readaloud_config.json"
    echo "Edit this file to customize settings."
}

# Run setup
main "$@"
