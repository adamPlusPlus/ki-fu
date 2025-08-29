# 🚀 ki-fu Project Manager Script

The `ki.sh` (Linux/macOS) and `ki.bat` (Windows) scripts provide quick access to various ki-fu projects from the root directory.

## 📋 Available Commands

### 🎵 ReadAloud TTS System
- **`ki readaloud`** - Start the **integrated TTS system** (browser + service)
- **`ki readaloud-service`** - Start only the Higgs Audio persistent service
- **`ki readaloud-cli`** - Start ReadAloud CLI interface

### 🏠 Virgility Dashboard
- **`ki virgility-flask`** - Start Virgility Flask dashboard
- **`ki virgility-fastapi`** - Start Virgility FastAPI dashboard

### 📖 Help
- **`ki help`** - Show help message

## 🎯 ReadAloud Integrated System

The **`ki readaloud`** command launches the complete ReadAloud experience:

### ✨ What It Does
1. **🚀 Starts Higgs Audio persistent service** - Loads AI model once, keeps it in memory
2. **🌐 Opens web interface** - Beautiful Visual Studio dark theme control panel
3. **🔗 Integrates everything** - Browser controls service, unified experience
4. **🧹 Auto-cleanup** - Closing browser stops service automatically

### 🎮 Features
- **Service Status Panel** - See if service is running/ready/loading
- **Start/Stop Controls** - Manage service from browser
- **Fast TTS Generation** - Once model is loaded, TTS is much faster
- **Fallback Mode** - Works even if service fails
- **Real-time Updates** - Live service status monitoring

### 🚀 Performance
- **First run**: 1-2 minutes (model loading)
- **Subsequent runs**: 10-30 seconds (model stays in memory)
- **StreamDeck integration**: Use `read_clipboard_fast.bat` for instant TTS

## 🔧 Service-Only Mode

Use **`ki readaloud-service`** if you want to:
- Run the service separately from browser
- Use it with other tools/scripts
- Debug service issues
- Run in background for other applications

## 💻 CLI Mode

Use **`ki readaloud-cli`** for:
- Command-line TTS operations
- Scripting and automation
- Server environments
- Quick testing

## 🌍 Cross-Platform Support

- **Linux/macOS**: Use `./ki.sh` or `bash ki.sh`
- **Windows**: Use `ki.bat` or `cmd /c ki.bat`
- **WSL**: Use `./ki.sh` (bash script)

## 📁 File Structure

```
ki-fu/
├── ki.sh              # Linux/macOS script
├── ki.bat             # Windows script
├── KI_README.md       # This file
└── readaloud/
    ├── web_interface.py      # Integrated web + service
    ├── higgs_service.py      # Persistent service
    ├── start_readaloud.bat   # Windows launcher
    └── streamdeck/
        └── read_clipboard_fast.bat  # Fast StreamDeck TTS
```

## 🎮 StreamDeck Integration

1. **Start the service**: `ki readaloud-service`
2. **Assign button to**: `readaloud/streamdeck/read_clipboard_fast.bat`
3. **Copy text** → **Press button** → **Instant TTS!**

## 🚨 Troubleshooting

### Service Won't Start
- Check Python installation: `python --version`
- Verify Higgs Audio path: `H:\AI\higgs\higgs-audio`
- Install dependencies: `pip install flask pyperclip keyboard`

### Browser Issues
- Check if port 5000 is available
- Try `ki readaloud-service` first, then open browser manually
- Check console for error messages

### Performance Issues
- First TTS generation always takes 1-2 minutes
- Subsequent generations should be much faster
- Ensure service is running and ready

## 🔄 Quick Start

```bash
# Start everything (recommended)
ki readaloud

# Start only service
ki readaloud-service

# Start CLI
ki readaloud-cli --clipboard

# Get help
ki help
```

## 📝 Examples

```bash
# Linux/macOS
./ki.sh readaloud
./ki.sh readaloud-service
./ki.sh readaloud-cli --clipboard

# Windows
ki.bat readaloud
ki.bat readaloud-service
ki.bat readaloud-cli --clipboard

# WSL
bash ki.sh readaloud
```

---

**🎉 Enjoy your integrated TTS experience!** The browser and service work together seamlessly, giving you the best of both worlds: fast performance and easy control.
