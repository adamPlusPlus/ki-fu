#!/bin/bash
# Example: Read clipboard content with ReadAloud

echo "📋 ReadAloud - Clipboard Reading Example"
echo "========================================"

# Check if ReadAloud is available
if [ ! -f "../main.py" ]; then
    echo "Error: ReadAloud not found. Please run this from the examples directory."
    exit 1
fi

echo "This example will monitor your clipboard for changes and read new content aloud."
echo "Press Ctrl+C to stop."
echo

# Start clipboard monitoring
cd ..
python main.py --clipboard
