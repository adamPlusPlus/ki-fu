# 🌐 ReadAloud Web Interface

A beautiful, modern web interface for controlling ReadAloud's text-to-speech functionality with a Visual Studio dark theme.

## ✨ Features

- **🎨 Visual Studio Dark Theme** - Familiar, professional appearance
- **🎛️ Volume Control** - Adjust audio output level (0-100%)
- **🎭 Voice Settings** - Choose from multiple voice types
- **🌡️ Temperature Control** - Fine-tune voice variation (0.0-1.0)
- **⚡ Speed Control** - Adjust speech playback speed (0.5x-2.0x)
- **🔧 TTS Engine Selection** - Choose between Higgs Audio, Coqui TTS, or System TTS
- **📋 Quick Actions** - Read clipboard, selection, or test text
- **💾 Configuration Management** - Save and reset settings
- **📱 Responsive Design** - Works on desktop and mobile devices

## 🚀 Quick Start

### Windows
```batch
# Double-click the batch file
start_web.bat

# Or run from command line
python web_interface.py
```

### Unix/Linux/macOS
```bash
# Install Flask first
pip install flask

# Start the interface
python web_interface.py
```

The web interface will automatically:
1. Start on `http://localhost:5000`
2. Open your default browser
3. Load your current configuration

## 🎯 Interface Layout

### Left Panel - Settings
- **TTS Engine**: Choose your preferred TTS engine
- **Voice Settings**: Configure voice type, temperature, volume, and speed
- **Configuration**: Save settings or reset to defaults

### Right Panel - Controls
- **Quick Actions**: Read clipboard, selection, or stop audio
- **Test TTS**: Enter custom text to test the system
- **System Info**: View current engine status and Higgs Audio availability

## ⌨️ Keyboard Shortcuts

- **Ctrl+Enter**: Test TTS with current text
- **Ctrl+S**: Save configuration
- **Escape**: Stop current audio playback

## 🔧 Configuration

The web interface automatically:
- Loads your existing `readaloud_config.json`
- Saves changes back to the configuration file
- Updates settings in real-time
- Provides visual feedback for all operations

## 🎨 Theme Details

The interface uses a **Visual Studio Dark Theme** with:
- **Primary Background**: `#1e1e1e` (VS Code dark)
- **Secondary Background**: `#252526` (VS Code panel)
- **Accent Blue**: `#007acc` (VS Code blue)
- **Accent Green**: `#4ec9b0` (VS Code green)
- **Text Colors**: Carefully chosen for optimal readability

## 🔌 API Endpoints

The web interface provides REST API endpoints:

- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `POST /api/tts` - Perform TTS operations
- `GET /api/status` - Get system status

## 🚨 Troubleshooting

### Interface Won't Start
- Ensure Python is installed and in PATH
- Install Flask: `pip install flask`
- Check if port 5000 is available

### No Audio Output
- Verify Higgs Audio is properly configured
- Check system audio settings
- Run `python test_simple.py` to test TTS

### Configuration Not Saving
- Check file permissions for `readaloud_config.json`
- Ensure the file is not read-only
- Verify the configuration file path

## 🔄 Integration with StreamDeck

The web interface works alongside your StreamDeck setup:
- **Web Interface**: Fine-tune settings and test TTS
- **StreamDeck**: Quick actions and daily use
- **Shared Configuration**: Both use the same `readaloud_config.json`

## 📱 Mobile Support

The interface is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Edge, Safari)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Tablet devices

## 🎯 Use Cases

- **Initial Setup**: Configure TTS engine and voice settings
- **Testing**: Verify TTS functionality with custom text
- **Fine-tuning**: Adjust volume, speed, and voice parameters
- **Monitoring**: Check system status and Higgs Audio availability
- **Configuration**: Save and manage different voice profiles

## 🔮 Future Enhancements

- **Voice Profiles**: Save and switch between different configurations
- **Audio Preview**: Hear voice samples before applying settings
- **Batch Processing**: Process multiple text files
- **History**: Track and replay previous TTS requests
- **Advanced Controls**: Pitch, emphasis, and pronunciation settings

## 📞 Support

If you encounter issues:
1. Check the browser console for error messages
2. Verify all dependencies are installed
3. Test the basic TTS functionality first
4. Check the configuration file format

---

**Enjoy your new ReadAloud web interface! 🎉**
