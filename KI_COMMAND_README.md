# 🚀 ki-fu Project Manager

A quick command-line interface to access your ki-fu projects from anywhere in your system.

## ✨ Features

- **Quick Access**: Run `ki [command]` from anywhere to access ki-fu projects
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Easy Setup**: Simple alias configuration
- **Extensible**: Easy to add new project commands

## 🚀 Quick Start

### 1. Setup the Alias

Run the setup script to automatically configure the `ki` command:

```bash
./setup_ki_alias.sh
```

This will add an alias to your shell configuration file (`.bashrc`, `.zshrc`, etc.).

### 2. Restart Your Terminal

Or reload your shell configuration:

```bash
source ~/.bashrc  # for bash
source ~/.zshrc   # for zsh
```

### 3. Start Using the ki Command

```bash
ki readaloud     # Start ReadAloud web interface
ki help          # Show available commands
```

## 📋 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `readaloud` | Start ReadAloud web interface | `ki readaloud` |
| `readaloud-cli` | Start ReadAloud CLI interface | `ki readaloud-cli --clipboard` |
| `virgility-flask` | Start Virgility Flask dashboard | `ki virgility-flask` |
| `virgility-fastapi` | Start Virgility FastAPI dashboard | `ki virgility-fastapi` |
| `help` | Show help message | `ki help` |

## 🔧 Manual Setup

If you prefer to set up the alias manually:

### Bash/Zsh
Add this line to your `~/.bashrc` or `~/.zshrc`:

```bash
alias ki='/path/to/your/ki-fu/ki.sh'
```

### Windows Command Prompt
Create a batch file in a directory that's in your PATH, or add the ki-fu directory to your PATH.

## 🌐 ReadAloud Web Interface

The `ki readaloud` command will:

1. Navigate to the readaloud project directory
2. Install Flask if needed
3. Start the web interface on `http://localhost:5000`
4. Automatically open your browser

## 💻 ReadAloud CLI

The `ki readaloud-cli` command provides access to the command-line interface:

```bash
ki readaloud-cli --clipboard    # Read clipboard content
ki readaloud-cli --file text.txt # Read a specific file
ki readaloud-cli --monitor log.txt # Monitor a file for changes
ki readaloud-cli --hotkeys       # Enable global hotkeys
```

## 🏠 Virgility Dashboards

The Virgility project provides two different dashboard implementations for Home Assistant:

### Flask Dashboard
```bash
ki virgility-flask   # Start Flask dashboard at http://localhost:5000
```

The Flask dashboard provides:
- Traditional web interface with templates
- Entity control and monitoring
- Service calling capabilities
- Simple, lightweight implementation

### FastAPI Dashboard
```bash
ki virgility-fastapi # Start FastAPI dashboard at http://localhost:8000
```

The FastAPI dashboard provides:
- Modern API-first architecture
- Interactive API documentation at `/docs`
- Better performance and async support
- RESTful API endpoints
- Built-in validation and error handling

Both dashboards will:
1. Navigate to the virgility project directory
2. Activate virtual environment if available
3. Install dependencies if needed
4. Start the respective dashboard server

## 🛠️ Adding New Commands

To add new project commands, edit the `ki.sh` file and add new case statements:

```bash
case "${1:-help}" in
    "readaloud")
        start_readaloud_web
        ;;
    "newproject")           # Add this
        start_new_project    # Add this
        ;;                   # Add this
    # ... existing cases
esac
```

## 📁 File Structure

```
ki-fu/
├── ki.sh                   # Main shell script (Unix/Linux/macOS)
├── ki.bat                  # Windows batch file
├── setup_ki_alias.sh      # Setup script for alias
├── KI_COMMAND_README.md    # This file
└── readaloud/             # ReadAloud project
    ├── web_interface.py   # Web interface
    └── main.py            # CLI interface
```

## 🔍 Troubleshooting

### Command Not Found
- Make sure you've run `./setup_ki_alias.sh`
- Restart your terminal or reload shell config
- Check that the alias was added to your shell config file

### Python Not Found
- Ensure Python is installed and in your PATH
- Try running `python --version` or `python3 --version`

### Permission Denied
- Make sure the script is executable: `chmod +x ki.sh`

## 🎯 Future Enhancements

Potential commands to add:
- `ki monitor` - Access monitor cycle scripts
- `ki navigation` - Access virtual desktop tools
- `ki myrient` - Access ROM downloader
- `ki virgility` - Access Home Assistant tools

## 📝 License

This project is part of your ki-fu workspace. Feel free to modify and extend as needed!
