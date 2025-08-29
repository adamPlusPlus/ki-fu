# ReadAloud - Local Text-to-Speech Tool

A powerful, local text-to-speech tool that can read text from various sources using advanced TTS engines like Higgs Audio.

## Features

- **Multiple TTS Engines**: Support for Higgs Audio, Coqui TTS, and more
- **Text Sources**:
  - Highlighted text (via hotkeys)
  - Clipboard content
  - File monitoring (auto-read on changes)
  - Direct text input
- **Trigger Methods**:
  - Global hotkeys
  - File system monitoring
  - Command line interface
  - GUI interface
- **Audio Output**: High-quality audio generation with customizable settings

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. For Higgs Audio, follow the [official installation guide](https://github.com/boson-ai/higgs-audio)

## Usage

### Command Line Interface

```bash
# Read clipboard content
python readaloud.py --clipboard

# Read a specific file
python readaloud.py --file path/to/file.txt

# Monitor a file for changes
python readaloud.py --monitor path/to/file.txt

# Read highlighted text (requires hotkey setup)
python readaloud.py --hotkeys
```

### Hotkeys

- `Ctrl+Shift+R`: Read highlighted text
- `Ctrl+Shift+C`: Read clipboard content
- `Ctrl+Shift+S`: Stop current audio

### Configuration

Create a `.env` file to customize settings:

```env
TTS_ENGINE=higgs_audio
AUDIO_OUTPUT_PATH=./audio_output
DEFAULT_VOICE=default
SPEECH_RATE=1.0
```

## Architecture

- `tts_engine.py`: Abstract TTS engine interface
- `engines/`: TTS engine implementations
- `triggers/`: Various trigger mechanisms
- `audio_manager.py`: Audio playback and management
- `main.py`: Main application entry point

## Supported TTS Engines

1. **Higgs Audio**: High-quality, expressive speech synthesis
2. **Coqui TTS**: Fast, lightweight TTS
3. **Festival**: Classic Unix TTS system
4. **eSpeak**: Compact TTS engine

## Contributing

Feel free to submit issues and enhancement requests!
