#!/usr/bin/env python3
"""
Simple StreamDeck Integration for ReadAloud
This script can be directly called from StreamDeck buttons
"""
import os
import sys
import json
import subprocess
import time
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def read_clipboard():
    """Read clipboard content aloud"""
    try:
        subprocess.run([sys.executable, "main.py", "--clipboard"], 
                      cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print("✓ Clipboard content read aloud")
    except Exception as e:
        print(f"✗ Error reading clipboard: {e}")

def read_selection():
    """Read selected text aloud (simulates Ctrl+C then reads clipboard)"""
    try:
        # First, simulate Ctrl+C to copy selection
        import pyperclip
        import keyboard
        import time
        
        # Store current clipboard
        original_clipboard = pyperclip.paste()
        
        # Simulate Ctrl+C
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.2)  # Wait for copy to complete
        
        # Read the new clipboard content
        subprocess.run([sys.executable, "main.py", "--clipboard"], 
                      cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Restore original clipboard
        pyperclip.copy(original_clipboard)
        print("✓ Selected text read aloud")
    except Exception as e:
        print(f"✗ Error reading selection: {e}")

def stop_audio():
    """Stop current audio playback"""
    try:
        subprocess.run([sys.executable, "main.py", "--stop"], 
                      cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print("✓ Audio stopped")
    except Exception as e:
        print(f"✗ Error stopping audio: {e}")

def read_file(file_path=None):
    """Read a specific file aloud"""
    try:
        if file_path and os.path.exists(file_path):
            subprocess.run([sys.executable, "main.py", "--file", file_path], 
                          cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            print(f"✓ File read aloud: {file_path}")
        else:
            print("✗ File not found or no file specified")
    except Exception as e:
        print(f"✗ Error reading file: {e}")

def toggle_monitoring():
    """Toggle file monitoring on/off"""
    try:
        # This would need to be implemented in the main app
        print("⚠ File monitoring toggle not yet implemented")
    except Exception as e:
        print(f"✗ Error toggling monitoring: {e}")

def main():
    """Main entry point - called from StreamDeck"""
    if len(sys.argv) < 2:
        print("Usage: python simple_integration.py <action> [file_path]")
        print("Actions: clipboard, selection, stop, file, monitor")
        return
    
    action = sys.argv[1].lower()
    
    if action == "clipboard":
        read_clipboard()
    elif action == "selection":
        read_selection()
    elif action == "stop":
        stop_audio()
    elif action == "file":
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        read_file(file_path)
    elif action == "monitor":
        toggle_monitoring()
    else:
        print(f"✗ Unknown action: {action}")
        print("Available actions: clipboard, selection, stop, file, monitor")

if __name__ == "__main__":
    main()
