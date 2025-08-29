#!/bin/bash

# ki-fu Project Manager Script
# Usage: ki [command]
# 
# This script provides quick access to various ki-fu projects
# from the root directory.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to show usage
show_usage() {
    echo "ki-fu Project Manager"
    echo "Usage: ki [command]"
    echo ""
    echo "Available commands:"
    echo "  readaloud         - Start ReadAloud integrated TTS system (browser + service)"
    echo "  readaloud-service - Start only the Higgs Audio persistent service"
    echo "  readaloud-cli     - Start ReadAloud CLI interface"
    echo "  virgility-flask   - Start Virgility Flask dashboard"
    echo "  virgility-fastapi - Start Virgility FastAPI dashboard"
    echo "  help              - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ki readaloud         # Start ReadAloud integrated TTS system"
    echo "  ki readaloud-service # Start only the Higgs Audio service"
    echo "  ki readaloud-cli     # Start ReadAloud CLI"
    echo "  ki virgility-flask   # Start Virgility Flask dashboard"
    echo "  ki virgility-fastapi # Start Virgility FastAPI dashboard"
    echo "  ki help              # Show this help"
}

# Function to start ReadAloud web interface
start_readaloud_web() {
    echo "🚀 Starting ReadAloud - Integrated TTS System"
    echo "========================================"
    echo ""
    echo "This will start:"
    echo "1. Higgs Audio persistent service"
    echo "2. Web interface (browser)"
    echo "3. Both are integrated and managed together"
    echo ""
    echo "Press Ctrl+C in the web interface to stop everything"
    echo ""
    
    cd "$SCRIPT_DIR/readaloud"
    
    # Check if Python is available
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    fi
    
    # Use python3 if available, otherwise python
    PYTHON_CMD="python"
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    fi
    
    # Install required dependencies if not already installed
    echo "🔧 Installing dependencies if needed..."
    $PYTHON_CMD -m pip install flask pyperclip keyboard --quiet
    
    # Check if Higgs Audio is available
    if [ ! -d "H:/AI/higgs/higgs-audio" ] && [ ! -d "/mnt/h/AI/higgs/higgs-audio" ]; then
        echo "⚠️  Warning: Higgs Audio not found at expected location"
        echo "   Expected: H:/AI/higgs/higgs-audio (Windows) or /mnt/h/AI/higgs/higgs-audio (WSL)"
        echo "   The system will use fallback mode (slower TTS generation)"
        echo ""
    else
        echo "✅ Higgs Audio found - fast TTS generation will be available"
        echo ""
    fi
    
    # Start the integrated web interface with service
    echo "🚀 Starting ReadAloud system..."
    $PYTHON_CMD web_interface.py
}

# Function to start only the Higgs Audio persistent service
start_readaloud_service() {
    echo "🔧 Starting Higgs Audio Persistent Service Only"
    echo "============================================="
    echo ""
    echo "This service will:"
    echo "1. Load the AI model once (takes 1-2 minutes)"
    echo "2. Keep it in memory for fast TTS generation"
    echo "3. Process requests much faster"
    echo ""
    echo "Keep this window open while using TTS!"
    echo "Use 'ki readaloud' for the full integrated experience."
    echo ""
    
    cd "$SCRIPT_DIR/readaloud"
    
    # Check if Python is available
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    fi
    
    # Use python3 if available, otherwise python
    PYTHON_CMD="python"
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    fi
    
    # Check if the service script exists
    if [ ! -f "higgs_service.py" ]; then
        echo "❌ Error: higgs_service.py not found"
        echo "Please ensure you're in the correct directory"
        exit 1
    fi
    
    # Start the service
    echo "🚀 Starting Higgs Audio service..."
    $PYTHON_CMD higgs_service.py --service
}

# Function to start ReadAloud CLI
start_readaloud_cli() {
    echo "💻 Starting ReadAloud CLI Interface..."
    echo ""
    
    cd "$SCRIPT_DIR/readaloud"
    
    # Check if Python is available
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    fi
    
    # Use python3 if available, otherwise python
    PYTHON_CMD="python"
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    fi
    
    # Show CLI options
    echo "Available CLI options:"
    echo "  --clipboard    - Read clipboard content"
    echo "  --file <path>  - Read a specific file"
    echo "  --monitor <path> - Monitor a file for changes"
    echo "  --hotkeys      - Enable global hotkeys"
    echo ""
    echo "Example: ki readaloud-cli --clipboard"
    echo ""
    
    # If arguments provided, pass them to the CLI
    if [ $# -gt 0 ]; then
        echo "Running: $PYTHON_CMD main.py $@"
        $PYTHON_CMD main.py "$@"
    else
        echo "Run with --help for more options:"
        $PYTHON_CMD main.py --help
    fi
}

# Function to start Virgility Flask Dashboard
start_virgility_flask() {
    echo "🏠 Starting Virgility Flask Dashboard..."
    echo "🌐 Dashboard will be available at: http://localhost:5000"
    echo "🔌 Connecting to Home Assistant..."
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    cd "$SCRIPT_DIR/virgility/homeassistant-dev"
    
    # Check if Python is available
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    fi
    
    # Use python3 if available, otherwise python
    PYTHON_CMD="python"
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    fi
    
    # Check if virtual environment exists and activate it
    if [ -d "venv" ]; then
        echo "🔧 Activating virtual environment..."
        source venv/bin/activate
    fi
    
    # Install dependencies if needed
    echo "🔧 Installing dependencies if needed..."
    $PYTHON_CMD -m pip install -r requirements.txt --quiet
    
    # Start the Flask dashboard
    echo "🚀 Starting Flask dashboard..."
    cd examples
    $PYTHON_CMD flask_dashboard.py
}

# Function to start Virgility FastAPI Dashboard
start_virgility_fastapi() {
    echo "🏠 Starting Virgility FastAPI Dashboard..."
    echo "🌐 Dashboard will be available at: http://localhost:8000"
    echo "📚 API documentation at: http://localhost:8000/docs"
    echo "🔌 Connecting to Home Assistant..."
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    cd "$SCRIPT_DIR/virgility/homeassistant-dev"
    
    # Check if Python is available
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    fi
    
    # Use python3 if available, otherwise python
    PYTHON_CMD="python"
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    fi
    
    # Check if virtual environment exists and activate it
    if [ -d "venv" ]; then
        echo "🔧 Activating virtual environment..."
        source venv/bin/activate
    fi
    
    # Install dependencies if needed
    echo "🔧 Installing dependencies if needed..."
    $PYTHON_CMD -m pip install -r requirements.txt --quiet
    
    # Start the FastAPI dashboard
    echo "🚀 Starting FastAPI dashboard..."
    cd examples
    $PYTHON_CMD fastapi_dashboard.py
}

# Main script logic
case "${1:-help}" in
    "readaloud")
        start_readaloud_web
        ;;
    "readaloud-service")
        start_readaloud_service
        ;;
    "readaloud-cli")
        shift  # Remove the first argument
        start_readaloud_cli "$@"
        ;;
    "virgility-flask")
        start_virgility_flask
        ;;
    "virgility-fastapi")
        start_virgility_fastapi
        ;;
    "help"|"--help"|"-h")
        show_usage
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac
