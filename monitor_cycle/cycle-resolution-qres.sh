#!/usr/bin/env bash

# cycle-resolution-qres.sh
# Shell script that downloads and uses QRes utility to change resolutions
# This approach often works when Windows API calls fail

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/tools"
QRES_PATH="$TOOLS_DIR/qres.exe"

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if QRes is available
check_qres() {
    if [[ -f "$QRES_PATH" ]]; then
        return 0
    else
        return 1
    fi
}

# Function to download QRes utility
download_qres() {
    print_status $BLUE "QRes utility not found. Attempting to download..."
    
    # Create tools directory if it doesn't exist
    mkdir -p "$TOOLS_DIR"
    
    # Try to download QRes from a reliable source
    print_status $YELLOW "Downloading QRes utility..."
    
    # Note: In a real scenario, you'd want to download from the official source
    # For now, we'll provide instructions
    print_status $CYAN "Please download QRes manually:"
    print_status $WHITE "1. Go to: https://www.majorgeeks.com/files/details/qres.html"
    print_status $WHITE "2. Download qres.exe"
    print_status $WHITE "3. Place it in: $TOOLS_DIR"
    print_status $WHITE "4. Run this script again"
    echo ""
    
    return 1
}

# Function to list available displays using QRes
list_displays_qres() {
    if check_qres; then
        print_status $BLUE "Detecting displays with QRes..."
        "$QRES_PATH" /l
    else
        print_status $RED "QRes not available. Cannot list displays."
        return 1
    fi
}

# Function to change resolution using QRes
change_resolution_qres() {
    local width=$1
    local height=$2
    local refresh=$3
    
    if check_qres; then
        print_status $YELLOW "Changing resolution to ${width}x${height} @ ${refresh}Hz using QRes..."
        
        # QRes command format: qres.exe /x:WIDTH /y:HEIGHT /f:REFRESH
        local result
        if "$QRES_PATH" "/x:$width" "/y:$height" "/f:$refresh"; then
            print_status $GREEN "Resolution change successful!"
            return 0
        else
            print_status $RED "Resolution change failed."
            return 1
        fi
    else
        print_status $RED "QRes utility not available."
        return 1
    fi
}

# Function to show help
show_help() {
    cat << EOF
Usage: $0 [OPTION] [WIDTH] [HEIGHT] [REFRESH]

Options:
    -h, --help          Show this help message
    -l, --list          List available displays using QRes
    -d, --download      Download QRes utility
    -c, --cycle         Cycle through predefined resolutions
    
Examples:
    $0 -l                    # List displays
    $0 -d                    # Download QRes
    $0 -c                    # Cycle resolutions
    $0 1920 1080 60         # Set specific resolution

Predefined resolution cycle:
    1280x960 @ 144Hz
    1920x1080 @ 120Hz
    4096x2160 @ 60Hz

Note: This script requires QRes utility to be downloaded first.
EOF
}

# Function to cycle through predefined resolutions
cycle_resolutions() {
    local resolutions=(
        "1280:960:144"
        "1920:1080:120"
        "4096:2160:60"
    )
    
    print_status $CYAN "=== RESOLUTION CYCLE MODE ==="
    print_status $YELLOW "Available resolutions:"
    
    for i in "${!resolutions[@]}"; do
        IFS=':' read -r w h f <<< "${resolutions[$i]}"
        print_status $WHITE "  Mode $((i+1)): ${w}x${h} @ ${f}Hz"
    done
    
    echo ""
    print_status $BLUE "Select resolution to apply (1-${#resolutions[@]}):"
    read -r selection
    
    if [[ "$selection" =~ ^[1-3]$ ]]; then
        local index=$((selection-1))
        IFS=':' read -r w h f <<< "${resolutions[$index]}"
        change_resolution_qres "$w" "$h" "$f"
    else
        print_status $RED "Invalid selection. Please choose 1, 2, or 3."
    fi
}

# Main script logic
main() {
    # Check if QRes is available
    if ! check_qres; then
        print_status $YELLOW "QRes utility not found."
        download_qres
        exit 1
    fi
    
    # Parse command line arguments
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
        -l|--list)
            list_displays_qres
            exit 0
            ;;
        -d|--download)
            download_qres
            exit 0
            ;;
        -c|--cycle)
            cycle_resolutions
            exit 0
            ;;
        "")
            # No arguments, show help
            show_help
            exit 0
            ;;
        *)
            # Assume it's a resolution specification
            if [[ $# -eq 3 ]]; then
                local width=$1
                local height=$2
                local refresh=$3
                
                if [[ "$width" =~ ^[0-9]+$ && "$height" =~ ^[0-9]+$ && "$refresh" =~ ^[0-9]+$ ]]; then
                    change_resolution_qres "$width" "$height" "$refresh"
                else
                    print_status $RED "Invalid resolution format. Use: WIDTH HEIGHT REFRESH"
                    exit 1
                fi
            else
                print_status $RED "Invalid arguments. Use: $0 WIDTH HEIGHT REFRESH"
                print_status $YELLOW "Or use: $0 -h for help"
                exit 1
            fi
            ;;
    esac
}

# Run main function with all arguments
main "$@"
