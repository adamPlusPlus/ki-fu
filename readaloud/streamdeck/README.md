# ReadAloud StreamDeck Integration

This module provides seamless integration between ReadAloud TTS and Elgato StreamDeck, allowing you to trigger text-to-speech functionality with physical button presses while the app runs in the background.

## 🎯 Features

- **Background Operation**: ReadAloud runs as a background service
- **StreamDeck Integration**: Direct button mapping to TTS actions
- **Multiple Actions**: Clipboard reading, text selection, file monitoring
- **Auto-start**: Configured to start automatically with your system
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install additional StreamDeck dependencies
pip install websocket-client psutil python-daemon
```

### 2. Run Integration Script

```bash
# Windows
python streamdeck/integrate.py

# Unix/Linux/macOS
python streamdeck/integrate.py
```

### 3. Configure StreamDeck

The integration script will automatically:
- Detect StreamDeck software
- Configure button mappings
- Start background services
- Setup auto-start

## 📋 StreamDeck Button Layout

### Default Profile

| Button | Action | Description |
|--------|--------|-------------|
| 1 | 📋 Read Clipboard | Read current clipboard content |
| 2 | 📝 Read Selection | Read currently selected text |
| 3 | ⏹️ Stop Audio | Stop current audio playback |
| 4 | 📄 Read File | Read a specific file |
| 5 | 👁️ Toggle Monitor | Toggle file monitoring |
| 6 | ⚡ Quick Actions | Access to common actions |

### Minimal Profile

| Button | Action | Description |
|--------|--------|-------------|
| 1 | 📋 Read Clipboard | Read current clipboard content |
| 2 | 📝 Read Selection | Read currently selected text |
| 3 | ⏹️ Stop Audio | Stop current audio playback |

## 🔧 Configuration

### StreamDeck Settings

Edit `streamdeck_config.json` to customize:

```json
{
  "streamdeck": {
    "host": "localhost",
    "port": 8000,
    "token": "your_token_here",
    "auto_reconnect": true
  }
}
```

### Button Customization

Each button can be customized with:

- **Action**: The TTS action to perform
- **Parameters**: Action-specific parameters
- **Icon**: Emoji or text icon
- **Color**: Button color theme
- **Description**: Tooltip description

## 🖥️ Background Service

The background service provides:

- **File Monitoring**: Watch files for changes
- **Clipboard Monitoring**: Detect clipboard updates
- **System Health**: Monitor disk space, memory usage
- **Auto-cleanup**: Remove old audio files
- **Logging**: Comprehensive logging to `logs/` directory

### Service Management

```bash
# Start background service
python background_service.py --daemon

# Check service status
python background_service.py --status

# Stop service
# Use the PID files in logs/ directory
```

## 🔌 StreamDeck Plugin

The StreamDeck plugin:

- **Connects via WebSocket** to StreamDeck software
- **Registers Actions** for button mapping
- **Handles Messages** from StreamDeck
- **Provides Status Updates** back to StreamDeck
- **Auto-reconnects** on connection loss

### Plugin Actions

- `read_clipboard`: Read clipboard content
- `read_selection`: Read selected text
- `stop_audio`: Stop audio playback
- `read_file`: Read specific file
- `toggle_monitoring`: Toggle file monitoring

## 🚀 Auto-start Configuration

### Windows

- Creates startup script in registry
- Runs automatically on login
- Background service starts minimized

### Linux/macOS

- Creates systemd user service
- Enables service for auto-start
- Runs in background on boot

## 📁 File Structure

```
streamdeck/
├── plugin.py              # StreamDeck plugin
├── integrate.py           # Integration script
├── startup.bat            # Windows startup
├── startup.sh             # Unix startup
├── streamdeck_config.json # Button configuration
└── README.md              # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **StreamDeck Not Detected**
   - Ensure StreamDeck software is running
   - Check if StreamDeck process is active
   - Restart StreamDeck software

2. **Connection Failed**
   - Verify WebSocket port (default: 8000)
   - Check firewall settings
   - Ensure no other service uses the port

3. **Background Service Won't Start**
   - Check Python dependencies
   - Verify file permissions
   - Check log files in `logs/` directory

4. **Buttons Not Responding**
   - Verify plugin is running
   - Check StreamDeck button configuration
   - Restart StreamDeck integration

### Debug Mode

```bash
# Enable verbose logging
export READALOUD_LOG_LEVEL=DEBUG

# Run integration with debug output
python streamdeck/integrate.py --debug
```

### Log Files

- `logs/readaloud_background.log`: Background service logs
- `logs/streamdeck.log`: StreamDeck plugin logs
- `logs/background.pid`: Background service PID
- `logs/streamdeck.pid`: StreamDeck plugin PID

## 🔒 Security Considerations

- **Local Only**: No network access required
- **Token Authentication**: Optional token-based authentication
- **File Permissions**: Only reads specified files
- **Process Isolation**: Runs in separate processes

## 📈 Performance

- **Memory Usage**: ~50-100MB for background service
- **CPU Usage**: Minimal when idle
- **Disk Usage**: Temporary audio files (auto-cleaned)
- **Startup Time**: ~5-10 seconds

## 🔄 Updates

To update the StreamDeck integration:

1. Stop current services
2. Update code files
3. Restart integration script
4. Services will auto-restart with new configuration

## 🤝 Contributing

To add new StreamDeck actions:

1. Add action to `plugin.py` actions dictionary
2. Update `streamdeck_config.json` with button mapping
3. Test the new action
4. Update documentation

## 📞 Support

For issues with StreamDeck integration:

1. Check log files first
2. Verify StreamDeck software is running
3. Ensure all dependencies are installed
4. Check system requirements

## 🎯 Use Cases

- **Content Creators**: Quick TTS for scripts and content
- **Developers**: Code review with audio feedback
- **Accessibility**: Screen reading for documents
- **Productivity**: Multi-tasking with audio output
- **Streaming**: Live TTS for audience interaction

## 🚀 Future Enhancements

- **Custom Button Icons**: Upload custom images
- **Dynamic Profiles**: Context-aware button layouts
- **Voice Selection**: Quick voice switching
- **Audio Effects**: Real-time audio processing
- **Cloud Integration**: Remote TTS capabilities
