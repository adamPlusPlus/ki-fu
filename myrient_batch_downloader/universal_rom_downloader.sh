#!/bin/bash

# Universal ROM Batch Downloader
# Downloads ROMs from Myrient archives based on platform selection and download queue
# Usage: ./universal_rom_downloader.sh [platform] [subtype]

# Configuration
MYRIENT_BASE_URL="https://myrient.erista.me/files/Redump/"
DOWNLOAD_DIR="./downloads"
QUEUE_FILE="./download_queue"
LOG_FILE="./download_log.txt"
TEMP_DIR="./temp"

# Available platforms and their subtypes
declare -A PLATFORMS
PLATFORMS["Nintendo - Nintendo Entertainment System"]="NES"
PLATFORMS["Nintendo - Super Nintendo Entertainment System"]="SNES"
PLATFORMS["Nintendo - Nintendo 64"]="N64"
PLATFORMS["Nintendo - Nintendo GameCube"]="NGC"
PLATFORMS["Nintendo - Nintendo Wii"]="WII"
PLATFORMS["Nintendo - Nintendo Wii U"]="WIIU"
PLATFORMS["Nintendo - Nintendo Switch"]="NSW"
PLATFORMS["Sony - PlayStation"]="PS1"
PLATFORMS["Sony - PlayStation 2"]="PS2"
PLATFORMS["Sony - PlayStation 3"]="PS3"
PLATFORMS["Sony - PlayStation 4"]="PS4"
PLATFORMS["Sony - PlayStation 5"]="PS5"
PLATFORMS["Sony - PlayStation Portable"]="PSP"
PLATFORMS["Sony - PlayStation Vita"]="PSV"
PLATFORMS["Microsoft - Xbox"]="XBOX"
PLATFORMS["Microsoft - Xbox 360"]="X360"
PLATFORMS["Microsoft - Xbox One"]="XONE"
PLATFORMS["Microsoft - Xbox Series X|S"]="XSX"
PLATFORMS["Sega - Master System"]="SMS"
PLATFORMS["Sega - Mega Drive - Genesis"]="MD"
PLATFORMS["Sega - Sega CD"]="SCD"
PLATFORMS["Sega - Sega 32X"]="32X"
PLATFORMS["Sega - Sega Saturn"]="SAT"
PLATFORMS["Sega - Dreamcast"]="DC"
PLATFORMS["Atari - 2600"]="A2600"
PLATFORMS["Atari - 5200"]="A5200"
PLATFORMS["Atari - 7800"]="A7800"
PLATFORMS["Atari - Jaguar"]="JAG"
PLATFORMS["Atari - Lynx"]="LYNX"
PLATFORMS["NEC - PC Engine - TurboGrafx-16"]="PCE"
PLATFORMS["NEC - PC Engine CD - TurboGrafx-CD"]="PCE-CD"
PLATFORMS["NEC - PC Engine SuperGrafx"]="SGX"
PLATFORMS["NEC - PC-FX"]="PCFX"
PLATFORMS["SNK - Neo Geo"]="NEO"
PLATFORMS["SNK - Neo Geo CD"]="NGCD"
PLATFORMS["SNK - Neo Geo Pocket"]="NGP"
PLATFORMS["SNK - Neo Geo Pocket Color"]="NGPC"
PLATFORMS["Bandai - WonderSwan"]="WS"
PLATFORMS["Bandai - WonderSwan Color"]="WSC"
PLATFORMS["Commodore - Amiga"]="AMIGA"
PLATFORMS["Commodore - Commodore 64"]="C64"
PLATFORMS["Commodore - Amiga CD32"]="CD32"
PLATFORMS["Apple - Apple II"]="APPLE2"
PLATFORMS["Apple - Macintosh"]="MAC"
PLATFORMS["IBM - PC"]="PC"
PLATFORMS["IBM - PC DOS"]="DOS"
PLATFORMS["IBM - PC Windows"]="WIN"
PLATFORMS["IBM - PC Linux"]="LINUX"
PLATFORMS["IBM - PC macOS"]="MACOS"
PLATFORMS["IBM - PC Android"]="ANDROID"
PLATFORMS["IBM - PC iOS"]="IOS"
PLATFORMS["IBM - PC Web"]="WEB"
PLATFORMS["IBM - PC VR"]="VR"
PLATFORMS["IBM - PC AR"]="AR"
PLATFORMS["IBM - PC Cloud"]="CLOUD"
PLATFORMS["IBM - PC Mobile"]="MOBILE"
PLATFORMS["IBM - PC Handheld"]="HANDHELD"
PLATFORMS["IBM - PC Console"]="CONSOLE"
PLATFORMS["IBM - PC Arcade"]="ARCADE"
PLATFORMS["IBM - PC Pinball"]="PINBALL"
PLATFORMS["IBM - PC Casino"]="CASINO"
PLATFORMS["IBM - PC Educational"]="EDU"
PLATFORMS["IBM - PC Sports"]="SPORTS"
PLATFORMS["IBM - PC Racing"]="RACING"
PLATFORMS["IBM - PC Fighting"]="FIGHTING"
PLATFORMS["IBM - PC Shooter"]="SHOOTER"
PLATFORMS["IBM - PC Adventure"]="ADV"
PLATFORMS["IBM - PC RPG"]="RPG"
PLATFORMS["IBM - PC Strategy"]="STRAT"
PLATFORMS["IBM - PC Simulation"]="SIM"
PLATFORMS["IBM - PC Puzzle"]="PUZZLE"
PLATFORMS["IBM - PC Platformer"]="PLAT"
PLATFORMS["IBM - PC Action"]="ACTION"
PLATFORMS["IBM - PC Horror"]="HORROR"
PLATFORMS["IBM - PC Comedy"]="COMEDY"
PLATFORMS["IBM - PC Drama"]="DRAMA"
PLATFORMS["IBM - PC Sci-Fi"]="SCIFI"
PLATFORMS["IBM - PC Fantasy"]="FANTASY"
PLATFORMS["IBM - PC Historical"]="HIST"
PLATFORMS["IBM - PC Military"]="MIL"
PLATFORMS["IBM - PC Western"]="WESTERN"
PLATFORMS["IBM - PC Crime"]="CRIME"
PLATFORMS["IBM - PC Mystery"]="MYSTERY"
PLATFORMS["IBM - PC Thriller"]="THRILLER"
PLATFORMS["IBM - PC Romance"]="ROMANCE"
PLATFORMS["IBM - PC Musical"]="MUSICAL"
PLATFORMS["IBM - PC Documentary"]="DOC"
PLATFORMS["IBM - PC Animation"]="ANIM"
PLATFORMS["IBM - PC Family"]="FAMILY"
PLATFORMS["IBM - PC Children"]="CHILDREN"
PLATFORMS["IBM - PC Teen"]="TEEN"
PLATFORMS["IBM - PC Adult"]="ADULT"
PLATFORMS["IBM - PC Mature"]="MATURE"
PLATFORMS["IBM - PC Everyone"]="EVERYONE"
PLATFORMS["IBM - PC Everyone 10+"]="E10+"
PLATFORMS["IBM - PC Teen 13+"]="T13+"
PLATFORMS["IBM - PC Mature 17+"]="M17+"
PLATFORMS["IBM - PC Adults Only 18+"]="AO18+"
PLATFORMS["IBM - PC Rating Pending"]="RP"
PLATFORMS["IBM - PC Not Rated"]="NR"
PLATFORMS["IBM - PC Unrated"]="UR"
PLATFORMS["IBM - PC Unknown"]="UNK"
PLATFORMS["IBM - PC Other"]="OTHER"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Create directories
mkdir -p "$DOWNLOAD_DIR"
mkdir -p "$TEMP_DIR"

# Initialize log file
echo "Universal ROM Download Session Started: $(date)" > "$LOG_FILE"

# Function to log messages
log_message() {
    local message="$1"
    echo -e "$message"
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $message" >> "$LOG_FILE"
}

# Function to display platform selection menu
show_platform_menu() {
    log_message "${CYAN}Available Platforms:${NC}"
    log_message "${YELLOW}Enter platform name or number:${NC}"
    echo ""
    
    local count=1
    for platform in "${!PLATFORMS[@]}"; do
        printf "${BLUE}%2d.${NC} %s\n" "$count" "$platform"
        count=$((count + 1))
    done
    echo ""
}

# Function to get platform by number or name
get_platform() {
    local input="$1"
    local count=1
    
    # Check if input is a number
    if [[ "$input" =~ ^[0-9]+$ ]]; then
        for platform in "${!PLATFORMS[@]}"; do
            if [ $count -eq $input ]; then
                echo "$platform"
                return 0
            fi
            count=$((count + 1))
        done
        return 1
    else
        # Check if input matches a platform name (case-insensitive)
        for platform in "${!PLATFORMS[@]}"; do
            if [[ "${platform,,}" == *"${input,,}"* ]]; then
                echo "$platform"
                return 0
            fi
        done
        return 1
    fi
}

# Function to get platform URL
get_platform_url() {
    local platform="$1"
    # URL encode spaces and special characters
    local encoded_platform=$(echo "$platform" | sed 's/ /%20/g' | sed 's/(/%28/g' | sed 's/)/%29/g')
    echo "${MYRIENT_BASE_URL}${encoded_platform}/"
}

# Function to clean game title for search
clean_title() {
    local title="$1"
    # Remove common suffixes and clean up
    title=$(echo "$title" | sed 's/ - Missing.*$//')
    title=$(echo "$title" | sed 's/ (Note:.*$//')
    title=$(echo "$title" | sed 's/ - Missing$//')
    # Remove extra whitespace
    title=$(echo "$title" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    echo "$title"
}

# Function to download and parse archive index
download_archive_index() {
    local platform="$1"
    local index_file="$TEMP_DIR/archive_index.html"
    
    log_message "${BLUE}Downloading archive index for: $platform${NC}"
    
    if curl -s -o "$index_file" "$(get_platform_url "$platform")"; then
        log_message "${GREEN}Archive index downloaded successfully${NC}"
        return 0
    else
        log_message "${RED}Failed to download archive index${NC}"
        return 1
    fi
}

# Function to search for game in archive
search_game() {
    local game_title="$1"
    local index_file="$TEMP_DIR/archive_index.html"
    
    log_message "${BLUE}Searching for: $game_title${NC}"
    
    # Create multiple search patterns for better matching
    local search_patterns=(
        "$(echo "$game_title" | sed 's/[[:space:]]\+/.*/g')"
        "$(echo "$game_title" | sed 's/[[:space:]]\+/.*/g' | sed 's/[^a-zA-Z0-9]/.*/g')"
        "$(echo "$game_title" | tr '[:upper:]' '[:lower:]' | sed 's/[[:space:]]\+/.*/g')"
        "$(echo "$game_title" | sed 's/[[:space:]]\+/.*/g' | sed 's/[^a-zA-Z0-9]/.*/g' | sed 's/.*/.*&.*/')"
    )
    
    # Try each search pattern
    for pattern in "${search_patterns[@]}"; do
        local matches=$(grep -i "$pattern" "$index_file" | grep -E 'href="[^"]*\.zip"' | head -10)
        
        if [ -n "$matches" ]; then
            log_message "${GREEN}Found $(echo "$matches" | wc -l) potential matches for: $game_title${NC}"
            echo "$matches"
            return 0
        fi
    done
    
    log_message "${YELLOW}No matches found for: $game_title${NC}"
    return 1
}

# Function to select best match
select_best_match() {
    local game_title="$1"
    local matches="$2"
    
    # Score each match based on similarity
    local best_match=""
    local best_score=0
    
    while IFS= read -r match; do
        if [ -n "$match" ]; then
            # Extract filename from href attribute, handling different HTML formats
            local filename=""
            if echo "$match" | grep -q 'href="[^"]*\.zip"'; then
                filename=$(echo "$match" | sed 's/.*href="\([^"]*\.zip\)".*/\1/')
            elif echo "$match" | grep -q 'href="[^"]*"'; then
                filename=$(echo "$match" | sed 's/.*href="\([^"]*\)".*/\1/')
            fi
            
            # Validate that we got a proper filename
            if [ -n "$filename" ] && [ "$filename" != "$match" ] && [[ "$filename" != *"Searching for:"* ]]; then
                local clean_filename=$(echo "$filename" | sed 's/\.zip$//' | sed 's/%20/ /g' | sed 's/%28/(/g' | sed 's/%29/)/g')
                
                # Simple scoring based on word overlap
                local score=0
                local game_words=$(echo "$game_title" | tr '[:upper:]' '[:lower:]' | tr '[:space:]' '\n' | grep -v '^$')
                local filename_words=$(echo "$clean_filename" | tr '[:upper:]' '[:lower:]' | tr '[:space:]' '\n' | grep -v '^$')
                
                while IFS= read -r word; do
                    if echo "$filename_words" | grep -q "^$word$"; then
                        score=$((score + 1))
                    fi
                done <<< "$game_words"
                
                if [ $score -gt $best_score ]; then
                    best_score=$score
                    best_match="$filename"
                fi
            fi
        fi
    done <<< "$matches"
    
    echo "$best_match"
}

# Function to download game
download_game() {
    local game_title="$1"
    local filename="$2"
    local platform="$3"
    local download_url="$(get_platform_url "$platform")${filename}"
    
    log_message "${BLUE}Downloading: $game_title${NC}"
    log_message "Filename: $filename"
    log_message "URL: $download_url"
    
    # Check if file already exists
    if [ -f "$DOWNLOAD_DIR/$filename" ]; then
        log_message "${YELLOW}File already exists, skipping download: $filename${NC}"
        return 0
    fi
    
    # Download with progress bar and resume support
    if curl -L -C - -o "$DOWNLOAD_DIR/$filename" "$download_url" --progress-bar --retry 3 --retry-delay 5; then
        log_message "${GREEN}Successfully downloaded: $game_title${NC}"
        return 0
    else
        log_message "${RED}Failed to download: $game_title${NC}"
        # Remove partial download if it exists
        rm -f "$DOWNLOAD_DIR/$filename"
        return 1
    fi
}

# Function to extract game titles from queue file
extract_games() {
    local temp_file=$(mktemp)
    
    # Extract game titles from clean format (no suffixes)
    grep -E '^[A-Za-z0-9]' "$QUEUE_FILE" | \
    sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
    grep -v '^$' > "$temp_file"
    
    echo "$temp_file"
}

# Function to remove completed game from queue
remove_from_queue() {
    local game_title="$1"
    local temp_file=$(mktemp)
    
    # Remove the line containing this game title
    grep -v "$game_title" "$QUEUE_FILE" > "$temp_file"
    mv "$temp_file" "$QUEUE_FILE"
    
    log_message "${GREEN}Removed '$game_title' from download queue${NC}"
}

# Function to cleanup temporary files
cleanup() {
    log_message "${BLUE}Cleaning up temporary files...${NC}"
    rm -rf "$TEMP_DIR"
}

# Function to display help
show_help() {
    echo "Usage: $0 [platform] [subtype]"
    echo ""
    echo "Examples:"
    echo "  $0                           # Interactive platform selection"
    echo "  $0 PS2                       # Download PS2 games"
    echo "  $0 \"Sony - PlayStation 2\"   # Download PS2 games (full name)"
    echo "  $0 9                         # Download PS2 games (by number)"
    echo ""
    echo "Available platforms:"
    echo "  PS2, SNES, N64, PS1, XBOX, DC, etc."
    echo ""
}

# Main execution
main() {
    local platform=""
    local platform_name=""
    
    # Parse command line arguments
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_help
        exit 0
    fi
    
    # If platform specified, use it
    if [ -n "$1" ]; then
        platform="$1"
        platform_name=$(get_platform "$platform")
        if [ -z "$platform_name" ]; then
            log_message "${RED}Error: Invalid platform '$platform'${NC}"
            log_message "${YELLOW}Use -h or --help to see available options${NC}"
            exit 1
        fi
    else
        # Interactive platform selection
        show_platform_menu
        read -p "Enter platform: " platform
        platform_name=$(get_platform "$platform")
        if [ -z "$platform_name" ]; then
            log_message "${RED}Error: Invalid platform selection${NC}"
            exit 1
        fi
    fi
    
    log_message "${GREEN}Selected platform: $platform_name${NC}"
    
    # Check if queue file exists
    if [ ! -f "$QUEUE_FILE" ]; then
        log_message "${RED}Error: Queue file not found: $QUEUE_FILE${NC}"
        exit 1
    fi
    
    # Download archive index first
    if ! download_archive_index "$platform_name"; then
        log_message "${RED}Failed to download archive index. Exiting.${NC}"
        exit 1
    fi
    
    # Extract game titles
    local games_file=$(extract_games)
    local total_games=$(wc -l < "$games_file")
    local current_game=0
    local successful_downloads=0
    local failed_downloads=0
    
    log_message "Found $total_games games to process"
    
    # Process each game
    while IFS= read -r game_title; do
        current_game=$((current_game + 1))
        log_message "${BLUE}[$current_game/$total_games] Processing: $game_title${NC}"
        
        # Clean the title
        local clean_title=$(clean_title "$game_title")
        
        # Search for the game
        local search_results=$(search_game "$clean_title")
        
        if [ $? -eq 0 ]; then
            # Select best match
            local best_match=$(select_best_match "$clean_title" "$search_results")
            
            if [ -n "$best_match" ]; then
                # Download the game
                if download_game "$clean_title" "$best_match" "$platform_name"; then
                    remove_from_queue "$game_title"
                    successful_downloads=$((successful_downloads + 1))
                    log_message "${GREEN}✓ Completed: $game_title${NC}"
                else
                    failed_downloads=$((failed_downloads + 1))
                    log_message "${RED}✗ Download failed: $game_title${NC}"
                fi
            else
                log_message "${YELLOW}Could not find suitable match for: $game_title${NC}"
                failed_downloads=$((failed_downloads + 1))
            fi
        else
            log_message "${YELLOW}Skipping: $game_title (not found)${NC}"
            failed_downloads=$((failed_downloads + 1))
        fi
        
        # Wait before next download to be respectful to the server
        if [ $current_game -lt $total_games ]; then
            log_message "${BLUE}Waiting 3 seconds before next download...${NC}"
            sleep 3
        fi
        
    done < "$games_file"
    
    # Cleanup
    rm -f "$games_file"
    cleanup
    
    # Final summary
    log_message "${GREEN}Download session completed!${NC}"
    log_message "${GREEN}Successful downloads: $successful_downloads${NC}"
    log_message "${RED}Failed downloads: $failed_downloads${NC}"
    log_message "Check $LOG_FILE for detailed log"
}

# Trap cleanup on exit
trap cleanup EXIT

# Run main function
main "$@"
