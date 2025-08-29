# Monitor Resolution Cycle Scripts

This directory contains scripts to cycle through predefined monitor resolutions on Windows systems.

## Files

- **`Cycle-Resolution.bat`** - Fixed batch file that calls the PowerShell script from the local directory
- **`Cycle-Resolution-Admin.bat`** - Batch file that runs with administrator privileges
- **`cycle-resolution.sh`** - Shell script wrapper with additional features (recommended for Git Bash users)
- **`cycle-resolution-qres.sh`** - Shell script that uses QRes utility to bypass Windows restrictions
- **`Cycle-Monitor-Resolution-Working.ps1`** - Main PowerShell script that cycles resolutions
- **`Cycle-Monitor-Resolution-Registry.ps1`** - PowerShell script that attempts registry modifications
- **`Cycle-Monitor-Resolution-Improved.ps1`** - Enhanced version with display detection (experimental)
- **`Cycle-Monitor-Resolution-Fixed.ps1`** - Fixed version of the original script (experimental)
- **`Cycle-Monitor-Resolution-Simple.ps1`** - Simplified version using Windows Forms

## Usage

### Shell Script (Recommended)

```bash
# List available displays
./cycle-resolution.sh -l

# Show current display settings
./cycle-resolution.sh -c

# Cycle resolution on auto-detected display
./cycle-resolution.sh

# Cycle resolution on specific display
./cycle-resolution.sh -d "\\\\.\\DISPLAY1"

# Show help
./cycle-resolution.sh -h
```

### PowerShell Script Directly

```powershell
# Cycle resolution on auto-detected display
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "Cycle-Monitor-Resolution-Working.ps1"

# Cycle resolution on specific display
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "Cycle-Monitor-Resolution-Working.ps1" -DisplayName "\\.\DISPLAY1"
```

### Batch File

```cmd
# Run the batch file (double-click or run from command prompt)
Cycle-Resolution.bat
```

## Predefined Resolutions

The scripts cycle through these resolutions:

1. **1280x960 @ 144Hz** - Low resolution, high refresh rate
2. **1920x1080 @ 120Hz** - Full HD, high refresh rate  
3. **4096x2160 @ 60Hz** - 4K, standard refresh rate

## How It Works

1. **Display Detection**: Automatically detects available displays using Windows Forms
2. **Current Mode**: Identifies the current resolution and finds its position in the cycle
3. **Next Mode**: Calculates the next resolution in the sequence
4. **User Guidance**: Provides step-by-step instructions for manual resolution changes
5. **Settings Integration**: Optionally opens Windows Display Settings

## Features

- ✅ **Auto-display detection** - No need to specify display names
- ✅ **Multi-monitor support** - Works with any number of displays
- ✅ **User-friendly output** - Clear instructions and visual indicators
- ✅ **Error handling** - Graceful fallback when automatic changes aren't possible
- ✅ **Cross-platform shell** - Works in Git Bash, WSL, and other Unix-like environments
- ✅ **PowerShell integration** - Leverages Windows native capabilities

## Requirements

- **Windows 10/11** with PowerShell 5.1 or later
- **Git Bash** or similar shell environment (for .sh script)
- **Administrator privileges** may be required for some operations

## Troubleshooting

### "PowerShell execution policy" error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "No displays detected" error
- Ensure you're running on a Windows system
- Check that Windows Forms assembly is available
- Try specifying a display name manually: `-DisplayName "\\.\DISPLAY1"`

### Resolution changes not applying
- The script provides manual instructions when automatic changes fail
- Some displays may not support all resolutions
- Check your graphics driver settings

## Customization

To modify the resolution modes, edit the `$Modes` array in the PowerShell script:

```powershell
$Modes = @(
    @{W=1920; H=1080; F=60},   # Full HD @ 60Hz
    @{W=2560; H=1440; F=75},   # 2K @ 75Hz
    @{W=3840; H=2160; F=60}    # 4K @ 60Hz
)
```

## Notes

- The script cannot automatically change resolutions due to Windows security restrictions
- It provides a user-friendly interface to guide manual resolution changes
- Run the script multiple times to cycle through all available modes
- The cycle order is: Mode 1 → Mode 2 → Mode 3 → Mode 1 (repeat)

## Bypassing Windows Restrictions

If the standard scripts fail due to Windows security restrictions, try these alternatives:

### 1. **Administrator Mode** (Most Effective)
```cmd
# Run as administrator - this often bypasses restrictions
Cycle-Resolution-Admin.bat
```

### 2. **QRes Utility** (External Tool)
```bash
# Download QRes and use the dedicated script
./cycle-resolution-qres.sh -d
./cycle-resolution-qres.sh -c
```

### 3. **Registry Modifications**
```powershell
# Try registry-based approach
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "Cycle-Monitor-Resolution-Registry.ps1"
```

### 4. **Graphics Driver Control Panel**
- **NVIDIA**: Right-click desktop > NVIDIA Control Panel > Change Resolution
- **AMD**: Right-click desktop > AMD Radeon Settings > Display > Custom Resolution
- **Intel**: Right-click desktop > Intel Graphics Settings > Display > Custom Resolution

### 5. **Third-Party Tools**
- **Custom Resolution Utility (CRU)** - Advanced users
- **Display Driver Uninstaller (DDU)** - Clean driver reinstall
- **nircmd** - Command-line utilities

### Why Windows Blocks Resolution Changes

Windows has become increasingly restrictive due to:
- **DRM protection** for streaming content
- **Security concerns** about display manipulation
- **Driver compatibility** issues
- **UWP app restrictions** in newer Windows versions

The most reliable workaround is using your graphics driver's control panel, as it operates at a lower level than Windows APIs.
