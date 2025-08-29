# ReadAloud Project Structure

This document provides an overview of the ReadAloud project structure and architecture.

## Directory Structure

```
readaloud/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── setup.sh                  # Unix/Linux setup script
├── setup.bat                 # Windows setup script
├── main.py                   # Main application entry point
├── config.py                 # Configuration management
├── tts_engine.py             # Abstract TTS engine interface
├── gui.py                    # Graphical user interface
├── engines/                  # TTS engine implementations
│   ├── __init__.py
│   ├── higgs_audio.py        # Higgs Audio TTS engine
│   └── coqui_tts.py          # Coqui TTS engine
├── triggers/                 # Trigger mechanisms
│   ├── __init__.py
│   ├── clipboard_trigger.py  # Clipboard monitoring
│   ├── file_monitor_trigger.py # File change monitoring
│   ├── hotkey_trigger.py     # Global hotkeys
│   └── text_input_trigger.py # Direct text input
├── examples/                  # Example usage scripts
│   ├── read_clipboard.sh     # Clipboard reading example
│   ├── read_file.sh          # File reading example
│   └── monitor_file.sh       # File monitoring example
├── audio_output/             # Generated audio files (created by setup)
├── logs/                     # Application logs (created by setup)
└── PROJECT_STRUCTURE.md      # This file
```

## Core Components

### 1. TTS Engine Interface (`tts_engine.py`)
- Abstract base class `TTSEngine` that all TTS engines must implement
- Cross-platform `AudioPlayer` class for audio playback
- Defines the contract for TTS engine implementations

### 2. TTS Engine Implementations (`engines/`)
- **Higgs Audio**: High-quality, expressive speech synthesis using [Boson AI's Higgs Audio](https://github.com/boson-ai/higgs-audio)
- **Coqui TTS**: Fast, lightweight TTS as a fallback option
- Each engine implements the `TTSEngine` interface

### 3. Trigger Mechanisms (`triggers/`)
- **Clipboard Trigger**: Monitors clipboard for changes
- **File Monitor Trigger**: Watches files for modifications
- **Hotkey Trigger**: Global keyboard shortcuts
- **Text Input Trigger**: Direct text input and file reading

### 4. Configuration Management (`config.py`)
- JSON-based configuration system
- Automatic configuration file creation
- Environment-specific settings
- TTS engine-specific configurations

### 5. Main Application (`main.py`)
- Command-line interface with multiple modes
- Integration of all components
- Threading for non-blocking operations
- Error handling and logging

### 6. Graphical Interface (`gui.py`)
- Tkinter-based GUI
- Real-time status updates
- File operations
- Hotkey management

## Key Features

### Text-to-Speech Capabilities
- Multiple TTS engines (Higgs Audio, Coqui TTS)
- Voice customization
- Audio quality control (temperature, seed)
- Cross-platform audio playback

### Trigger Methods
- **Highlighted Text**: `Ctrl+Shift+R` to read selected text
- **Clipboard**: `Ctrl+Shift+C` to read clipboard content
- **File Monitoring**: Auto-read files when they change
- **Direct Input**: Interactive text input mode
- **Global Hotkeys**: System-wide keyboard shortcuts

### File Support
- Text files (`.txt`, `.md`)
- Code files (`.py`, `.js`, `.html`)
- Automatic encoding detection
- Real-time file change monitoring

## Usage Modes

### 1. Interactive Mode
```bash
python main.py --interactive
```
- Direct text input
- File loading
- Real-time TTS

### 2. Hotkey Mode
```bash
python main.py --hotkeys
```
- Global keyboard shortcuts
- Background operation
- System-wide accessibility

### 3. Clipboard Monitoring
```bash
python main.py --clipboard
```
- Automatic clipboard detection
- Continuous monitoring
- Instant TTS response

### 4. File Monitoring
```bash
python main.py --monitor file.txt
```
- Real-time file change detection
- Automatic content reading
- Development workflow integration

### 5. Single File Reading
```bash
python main.py --file file.txt
```
- One-time file reading
- Batch processing
- Script integration

## Configuration

### Configuration File (`readaloud_config.json`)
```json
{
  "tts_engine": "auto",
  "voice": "default",
  "temperature": 0.3,
  "seed": null,
  "audio_output_path": "./audio_output",
  "higgs_config": {
    "model_path": "/path/to/higgs-audio",
    "python_path": "python",
    "higgs_script": "examples/generation.py"
  },
  "coqui_config": {
    "model_name": "tts_models/en/ljspeech/tacotron2-DDC"
  },
  "hotkeys": {
    "read_selection": "ctrl+shift+r",
    "read_clipboard": "ctrl+shift+c",
    "stop_audio": "ctrl+shift+s"
  }
}
```

### Environment Variables
- `TTS_ENGINE`: Preferred TTS engine
- `AUDIO_OUTPUT_PATH`: Audio file output directory
- `DEFAULT_VOICE`: Default voice selection
- `SPEECH_RATE`: Speech rate multiplier

## Installation

### Quick Setup
```bash
# Unix/Linux/macOS
./setup.sh

# Windows
setup.bat
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Clone Higgs Audio (optional)
git clone https://github.com/boson-ai/higgs-audio.git

# Create configuration
python -c "from config import Config; Config().create_sample_config()"
```

## Development

### Adding New TTS Engines
1. Create new engine class in `engines/`
2. Implement `TTSEngine` interface
3. Add to engine selection logic in `main.py`
4. Update configuration schema

### Adding New Triggers
1. Create new trigger class in `triggers/`
2. Implement trigger interface
3. Add to trigger registry in `main.py`
4. Update GUI if applicable

### Testing
```bash
# Test TTS engine
python main.py --info

# Test voices
python main.py --voices

# Test file reading
python main.py --file README.md
```

## Troubleshooting

### Common Issues
1. **TTS Engine Not Available**: Check dependencies and model paths
2. **Audio Playback Issues**: Verify system audio drivers
3. **Hotkey Conflicts**: Check for conflicting applications
4. **File Permission Errors**: Ensure read access to monitored files

### Debug Mode
```bash
# Enable verbose logging
python main.py --debug

# Check configuration
python -c "from config import Config; print(Config().config)"
```

## Performance Considerations

### Memory Usage
- TTS models loaded on-demand
- Audio files cleaned up after playback
- Efficient file monitoring with watchdog

### CPU Usage
- TTS synthesis in background threads
- Non-blocking UI operations
- Configurable monitoring intervals

### Storage
- Temporary audio files in system temp directory
- Configurable output directory
- Automatic cleanup of old files

## Security

### File Access
- Only reads specified files
- No network access by default
- Local-only operation

### Hotkey Safety
- User-defined key combinations
- No system-level permissions required
- Graceful error handling

## Future Enhancements

### Planned Features
- Web interface
- Mobile app support
- Cloud TTS integration
- Advanced voice cloning
- Multi-language support
- Audio format conversion
- Speech-to-text integration

### Extensibility
- Plugin system for TTS engines
- Custom trigger mechanisms
- Audio processing pipelines
- Integration APIs
