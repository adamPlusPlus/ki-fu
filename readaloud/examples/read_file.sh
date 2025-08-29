#!/bin/bash
# Example: Read file content with ReadAloud

echo "📄 ReadAloud - File Reading Example"
echo "==================================="

# Check if ReadAloud is available
if [ ! -f "../main.py" ]; then
    echo "Error: ReadAloud not found. Please run this from the examples directory."
    exit 1
fi

# Check if file argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <file_path>"
    echo "Example: $0 ../README.md"
    exit 1
fi

FILE_PATH="$1"

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File '$FILE_PATH' not found."
    exit 1
fi

echo "Reading file: $FILE_PATH"
echo "Press Ctrl+C to stop."
echo

# Read the file
cd ..
python main.py --file "$FILE_PATH"
