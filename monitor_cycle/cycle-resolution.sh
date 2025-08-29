#!/usr/bin/env bash

# cycle-resolution.sh
# Shell script wrapper for cycling monitor resolutions
# This script calls the PowerShell script with proper error handling

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PS_SCRIPT="$SCRIPT_DIR/Cycle-Monitor-Resolution-Working.ps1"

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if PowerShell is available
check_powershell() {
    if command -v powershell.exe >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to check if the PowerShell script exists
check_script() {
    if [[ -f "$PS_SCRIPT" ]]; then
        return 0
    else
        return 1
    fi
}

# Function to display available displays
list_displays() {
    print_status $BLUE "Detecting available displays..."
    powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "
        Add-Type -AssemblyName System.Windows.Forms
        \$screens = [System.Windows.Forms.Screen]::AllScreens
        Write-Host 'Available displays:'
        for (\$i = 0; \$i -lt \$screens.Length; \$i++) {
            \$screen = \$screens[\$i]
            Write-Host \"  Display \$(\$i + 1): \$(\$screen.Bounds.Width)x\$(\$screen.Bounds.Height) at (\$(\$screen.Bounds.X),\$(\$screen.Bounds.Y))\"
        }
    "
}

# Function to show current resolution
show_current() {
    print_status $BLUE "Current display settings:"
    powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "
        Add-Type -AssemblyName System.Windows.Forms
        \$screens = [System.Windows.Forms.Screen]::AllScreens
        for (\$i = 0; \$i -lt \$screens.Length; \$i++) {
            \$screen = \$screens[\$i]
            Write-Host \"Display \$(\$i + 1): \$(\$screen.Bounds.Width)x\$(\$screen.Bounds.Height) at (\$(\$screen.Bounds.X),\$(\$screen.Bounds.Y))\"
        }
    "
}

# Function to cycle resolution
cycle_resolution() {
    local display_name=${1:-""}
    
    print_status $YELLOW "Cycling monitor resolution..."
    
    if [[ -n "$display_name" ]]; then
        print_status $BLUE "Targeting display: $display_name"
        powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$PS_SCRIPT" -DisplayName "$display_name"
    else
        print_status $BLUE "Auto-detecting display..."
        powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$PS_SCRIPT"
    fi
    
    if [[ $? -eq 0 ]]; then
        print_status $GREEN "Resolution changed successfully!"
    else
        print_status $RED "Failed to change resolution."
        return 1
    fi
}

# Function to show help
show_help() {
    cat << EOF
Usage: $0 [OPTION] [DISPLAY_NAME]

Options:
    -h, --help          Show this help message
    -l, --list          List available displays
    -c, --current       Show current display settings
    -d, --display       Specify display name (e.g., '\\\\.\\DISPLAY1')
    
Examples:
    $0                    # Auto-detect and cycle resolution
    $0 -l                # List available displays
    $0 -c                # Show current settings
    $0 -d "\\\\.\\DISPLAY2"  # Cycle resolution on specific display

The script cycles through these predefined resolutions:
    1280x960 @ 144Hz
    1920x1080 @ 120Hz
    4096x2160 @ 60Hz

EOF
}

# Main script logic
main() {
    # Check if PowerShell is available
    if ! check_powershell; then
        print_status $RED "Error: PowerShell is not available on this system."
        exit 1
    fi
    
    # Check if the PowerShell script exists
    if ! check_script; then
        print_status $RED "Error: PowerShell script not found at: $PS_SCRIPT"
        exit 1
    fi
    
    # Parse command line arguments
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
        -l|--list)
            list_displays
            exit 0
            ;;
        -c|--current)
            show_current
            exit 0
            ;;
        -d|--display)
            if [[ -z "$2" ]]; then
                print_status $RED "Error: Display name required after -d option"
                exit 1
            fi
            cycle_resolution "$2"
            ;;
        "")
            # No arguments, cycle resolution with auto-detection
            cycle_resolution
            ;;
        *)
            # Assume it's a display name
            cycle_resolution "$1"
            ;;
    esac
}

# Run main function with all arguments
main "$@"
