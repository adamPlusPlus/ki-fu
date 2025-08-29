#!/bin/bash
# Example: Monitor file changes with ReadAloud

echo "👀 ReadAloud - File Monitoring Example"
echo "======================================"

# Check if ReadAloud is available
if [ ! -f "../main.py" ]; then
    echo "Error: ReadAloud not found. Please run this from the examples directory."
    exit 1
fi

# Check if file argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <file_path>"
    echo "Example: $0 ../README.md"
    echo
    echo "This will monitor the file for changes and read new content aloud."
    exit 1
fi

FILE_PATH="$1"

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File '$FILE_PATH' not found."
    exit 1
fi

echo "Monitoring file: $FILE_PATH"
echo "Make changes to the file to hear them read aloud."
echo "Press Ctrl+C to stop."
echo

# Start file monitoring
cd ..
python main.py --monitor "$FILE_PATH"
