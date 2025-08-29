#!/bin/bash

# Setup script for ki-fu project manager alias
# This script helps you set up the 'ki' command alias

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="ki.sh"

echo "🔧 Setting up ki-fu project manager alias..."
echo ""

# Detect shell
if [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
    SHELL_NAME="bash"
elif [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_NAME="zsh"
else
    echo "⚠️  Unsupported shell: $SHELL"
    echo "Please manually add the following alias to your shell configuration:"
    echo ""
    echo "alias ki='$SCRIPT_DIR/$SCRIPT_NAME'"
    echo ""
    exit 1
fi

# Check if alias already exists
if grep -q "alias ki=" "$SHELL_RC" 2>/dev/null; then
    echo "✅ Alias 'ki' already exists in $SHELL_RC"
    echo "Current alias:"
    grep "alias ki=" "$SHELL_RC"
    echo ""
    echo "To update it, please edit $SHELL_RC manually"
else
    echo "📝 Adding 'ki' alias to $SHELL_RC..."
    echo "" >> "$SHELL_RC"
    echo "# ki-fu project manager alias" >> "$SHELL_RC"
    echo "alias ki='$SCRIPT_DIR/$SCRIPT_NAME'" >> "$SHELL_RC"
    echo "✅ Alias added successfully!"
    echo ""
    echo "🔄 To activate the alias, please:"
    echo "   1. Restart your terminal, OR"
    echo "   2. Run: source $SHELL_RC"
fi

echo ""
echo "🎯 Usage examples:"
echo "   ki readaloud     # Start ReadAloud web interface"
echo "   ki readaloud-cli # Start ReadAloud CLI"
echo "   ki help          # Show help"
echo ""
echo "📁 Script location: $SCRIPT_DIR/$SCRIPT_NAME"
echo "🔗 Shell config: $SHELL_RC"
echo ""
echo "✨ Setup complete! The 'ki' command will be available after restarting your terminal."
