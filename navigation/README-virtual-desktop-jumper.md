# Virtual Desktop Jumper - AutoHotkey Script

This AutoHotkey script allows you to jump directly to specific virtual desktops using keyboard shortcuts, providing functionality that Windows doesn't have built-in.

## Features

- **Direct Desktop Jumping**: Jump to any virtual desktop using `Ctrl + Win + Numpad` keys
- **Alternative Shortcuts**: Also supports `Ctrl + Win + 1-9` for non-numpad users
- **Smart Navigation**: Automatically calculates the fastest route to your target desktop
- **Desktop Counting**: Automatically detects and counts your virtual desktops
- **Visual Feedback**: Shows tooltips to confirm actions and current status
- **System Tray Integration**: Easy access to functions via system tray menu

## Requirements

- **AutoHotkey v1.1** (Classic version) - Download from [autohotkey.com](https://www.autohotkey.com/)
- Windows 10 or 11
- Administrator privileges (recommended for best compatibility)

## Installation

1. **Install AutoHotkey v1.1** (Classic version, not v2)
2. **Download** the `virtual-desktop-jumper.ahk` file
3. **Right-click** the `.ahk` file and select "Run as administrator"
4. **Keep the script running** in the background

## Usage

### Primary Shortcuts (Numpad)
- `Ctrl + Win + Numpad1` → Jump to Desktop 1
- `Ctrl + Win + Numpad2` → Jump to Desktop 2
- `Ctrl + Win + Numpad3` → Jump to Desktop 3
- `Ctrl + Win + Numpad4` → Jump to Desktop 4
- `Ctrl + Win + Numpad5` → Jump to Desktop 5
- `Ctrl + Win + Numpad6` → Jump to Desktop 6
- `Ctrl + Win + Numpad7` → Jump to Desktop 7
- `Ctrl + Win + Numpad8` → Jump to Desktop 8
- `Ctrl + Win + Numpad9` → Jump to Desktop 9

### Alternative Shortcuts (Regular Numbers)
- `Ctrl + Win + 1` → Jump to Desktop 1
- `Ctrl + Win + 2` → Jump to Desktop 2
- `Ctrl + Win + 3` → Jump to Desktop 3
- `Ctrl + Win + 4` → Jump to Desktop 4
- `Ctrl + Win + 5` → Jump to Desktop 5
- `Ctrl + Win + 6` → Jump to Desktop 6
- `Ctrl + Win + 7` → Jump to Desktop 7
- `Ctrl + Win + 8` → Jump to Desktop 8
- `Ctrl + Win + 9` → Jump to Desktop 9

### Utility Shortcuts
- `Ctrl + Win + R` → Refresh desktop count
- `Ctrl + Win + I` → Show current desktop information

## How It Works

1. **Desktop Detection**: The script automatically counts your virtual desktops
2. **Smart Navigation**: Calculates the shortest path to your target desktop
3. **Windows Integration**: Uses Windows' built-in `Win + Ctrl + Left/Right` shortcuts
4. **Position Tracking**: Keeps track of which desktop you're currently on

## System Tray Menu

Right-click the AutoHotkey icon in your system tray to access:
- **Refresh Desktop Count**: Re-count your virtual desktops
- **Show Desktop Info**: Display current desktop and total count
- **Exit**: Close the script

## Troubleshooting

### Script Not Working
- **Run as Administrator**: Right-click the script and select "Run as administrator"
- **Check AutoHotkey Version**: Ensure you're using AutoHotkey v1.1 (Classic), not v2
- **Restart Script**: Close and re-run the script if it stops responding

### Desktop Count Issues
- **Use Ctrl + Win + R**: Refresh the desktop count if you add/remove desktops
- **Manual Count**: The script may need help detecting desktops if you have many

### Performance Issues
- **Reduce Delays**: Edit the script to reduce `Sleep` values if navigation feels slow
- **Close Other Scripts**: Ensure no other AutoHotkey scripts are conflicting

## Customization

You can edit the script to:
- **Change Hotkeys**: Modify the key combinations to your preference
- **Adjust Delays**: Change `Sleep` values for faster/slower navigation
- **Add Features**: Extend functionality as needed

## Limitations

- **Desktop Detection**: Relies on Windows' navigation behavior, not direct API access
- **Maximum Desktops**: Limited to 9 desktops (can be extended in the script)
- **Windows Version**: Designed for Windows 10/11, may not work on older versions

## Auto-Start

To run the script automatically on startup:
1. Press `Win + R`, type `shell:startup`, press Enter
2. Copy the `.ahk` file to the startup folder
3. Or create a shortcut to the script in the startup folder

## Support

If you encounter issues:
1. Check that AutoHotkey v1.1 is installed
2. Ensure the script is running as administrator
3. Try refreshing the desktop count with `Ctrl + Win + R`
4. Restart the script if needed

## License

This script is provided as-is for personal use. Feel free to modify and distribute as needed.
