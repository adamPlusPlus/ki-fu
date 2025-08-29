@echo off
REM ki-fu Project Manager Script (Windows)
REM Usage: ki [command]
REM 
REM This script provides quick access to various ki-fu projects
REM from the root directory.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

REM Function to show usage
:show_usage
echo ki-fu Project Manager
echo Usage: ki [command]
echo.
echo Available commands:
echo   readaloud         - Start ReadAloud integrated TTS system (browser + service)
echo   readaloud-service - Start only the Higgs Audio persistent service
echo   readaloud-cli     - Start ReadAloud CLI interface
echo   virgility-flask   - Start Virgility Flask dashboard
echo   virgility-fastapi - Start Virgility FastAPI dashboard
echo   help              - Show this help message
echo.
echo Examples:
echo   ki readaloud         # Start ReadAloud integrated TTS system
echo   ki readaloud-service # Start only the Higgs Audio service
echo   ki readaloud-cli     # Start ReadAloud CLI
echo   ki virgility-flask   # Start Virgility Flask dashboard
echo   ki virgility-fastapi # Start Virgility FastAPI dashboard
echo   ki help              # Show this help
goto :eof

REM Function to start ReadAloud web interface
:start_readaloud_web
echo 🚀 Starting ReadAloud - Integrated TTS System
echo ========================================
echo.
echo This will start:
echo 1. Higgs Audio persistent service
echo 2. Web interface (browser)
echo 3. Both are integrated and managed together
echo.
echo Press Ctrl+C in the web interface to stop everything
echo.

cd /d "%SCRIPT_DIR%readaloud"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python and try again
    exit /b 1
)

REM Install required dependencies if not already installed
echo 🔧 Installing dependencies if needed...
python -m pip install flask pyperclip keyboard --quiet

REM Check if Higgs Audio is available
if not exist "H:\AI\higgs\higgs-audio" (
    echo ⚠️  Warning: Higgs Audio not found at expected location
    echo    Expected: H:\AI\higgs\higgs-audio
    echo    The system will use fallback mode (slower TTS generation)
    echo.
) else (
    echo ✅ Higgs Audio found - fast TTS generation will be available
    echo.
)

REM Start the integrated web interface with service
echo 🚀 Starting ReadAloud system...
python web_interface.py
goto :eof

REM Function to start only the Higgs Audio persistent service
:start_readaloud_service
echo 🔧 Starting Higgs Audio Persistent Service Only
echo =============================================
echo.
echo This service will:
echo 1. Load the AI model once (takes 1-2 minutes)
echo 2. Keep it in memory for fast TTS generation
echo 3. Process requests much faster
echo.
echo Keep this window open while using TTS!
echo Use 'ki readaloud' for the full integrated experience.
echo.

cd /d "%SCRIPT_DIR%readaloud"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python and try again
    exit /b 1
)

REM Check if the service script exists
if not exist "higgs_service.py" (
    echo ❌ Error: higgs_service.py not found
    echo Please ensure you're in the correct directory
    exit /b 1
)

REM Start the service
echo 🚀 Starting Higgs Audio service...
python higgs_service.py --service
goto :eof

REM Function to start ReadAloud CLI
:start_readaloud_cli
echo 💻 Starting ReadAloud CLI Interface...
echo.

cd /d "%SCRIPT_DIR%readaloud"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python and try again
    exit /b 1
)

REM Show CLI options
echo Available CLI options:
echo   --clipboard    - Read clipboard content
echo   --file ^<path^>  - Read a specific file
echo   --monitor ^<path^> - Monitor a file for changes
echo   --hotkeys      - Enable global hotkeys
echo.
echo Example: ki readaloud-cli --clipboard
echo.

REM If arguments provided, pass them to the CLI
if not "%1"=="" (
    echo Running: python main.py %*
    python main.py %*
) else (
    echo Run with --help for more options:
    python main.py --help
)
goto :eof

REM Function to start Virgility Flask Dashboard
:start_virgility_flask
echo 🏠 Starting Virgility Flask Dashboard...
echo 🌐 Dashboard will be available at: http://localhost:5000
echo 🔌 Connecting to Home Assistant...
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%SCRIPT_DIR%virgility\homeassistant-dev"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python and try again
    exit /b 1
)

REM Install dependencies if needed
echo 🔧 Installing dependencies if needed...
python -m pip install -r requirements.txt --quiet

REM Start the Flask dashboard
echo 🚀 Starting Flask dashboard...
cd examples
python flask_dashboard.py
goto :eof

REM Function to start Virgility FastAPI Dashboard
:start_virgility_fastapi
echo 🏠 Starting Virgility FastAPI Dashboard...
echo 🌐 Dashboard will be available at: http://localhost:8000
echo 📚 API documentation at: http://localhost:8000/docs
echo 🔌 Connecting to Home Assistant...
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%SCRIPT_DIR%virgility\homeassistant-dev"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python and try again
    exit /b 1
)

REM Install dependencies if needed
echo 🔧 Installing dependencies if needed...
python -m pip install -r requirements.txt --quiet

REM Start the FastAPI dashboard
echo 🚀 Starting FastAPI dashboard...
cd examples
python fastapi_dashboard.py
goto :eof

REM Main script logic
if "%1"=="" goto show_usage
if "%1"=="help" goto show_usage
if "%1"=="--help" goto show_usage
if "%1"=="-h" goto show_usage

if "%1"=="readaloud" goto start_readaloud_web
if "%1"=="readaloud-service" goto start_readaloud_service
if "%1"=="readaloud-cli" (
    shift
    goto start_readaloud_cli
)
if "%1"=="virgility-flask" goto start_virgility_flask
if "%1"=="virgility-fastapi" goto start_virgility_fastapi

echo ❌ Unknown command: %1
echo.
goto show_usage
