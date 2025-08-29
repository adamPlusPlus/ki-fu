"""
Hotkey Trigger for ReadAloud.

This module provides functionality to trigger TTS using global hotkeys.
"""

import keyboard
import pyperclip
import time
from typing import Callable, Optional


class HotkeyTrigger:
    """Trigger TTS using global hotkeys."""
    
    def __init__(self, callback: Callable[[str], None]):
        """
        Initialize hotkey trigger.
        
        Args:
            callback: Function to call with selected text
        """
        self.callback = callback
        self.running = False
        
        # Default hotkeys
        self.hotkeys = {
            'read_selection': 'ctrl+shift+r',
            'read_clipboard': 'ctrl+shift+c',
            'stop_audio': 'ctrl+shift+s'
        }
    
    def setup_hotkeys(self):
        """Setup global hotkeys."""
        try:
            # Hotkey to read selected text
            keyboard.add_hotkey(
                self.hotkeys['read_selection'],
                self._read_selected_text,
                suppress=True
            )
            
            # Hotkey to read clipboard
            keyboard.add_hotkey(
                self.hotkeys['read_clipboard'],
                self._read_clipboard,
                suppress=True
            )
            
            # Hotkey to stop audio
            keyboard.add_hotkey(
                self.hotkeys['stop_audio'],
                self._stop_audio,
                suppress=True
            )
            
            print("Hotkeys registered:")
            print(f"  {self.hotkeys['read_selection']}: Read selected text")
            print(f"  {self.hotkeys['read_clipboard']}: Read clipboard")
            print(f"  {self.hotkeys['stop_audio']}: Stop audio")
            
        except Exception as e:
            print(f"Error setting up hotkeys: {e}")
    
    def _read_selected_text(self):
        """Read currently selected text."""
        try:
            # Copy selected text to clipboard
            keyboard.send('ctrl+c')
            time.sleep(0.1)  # Small delay to ensure copy completes
            
            # Get text from clipboard
            text = pyperclip.paste()
            
            if text and text.strip():
                print(f"Reading selected text: {text[:50]}...")
                self.callback(text)
            else:
                print("No text selected")
                
        except Exception as e:
            print(f"Error reading selected text: {e}")
    
    def _read_clipboard(self):
        """Read clipboard content."""
        try:
            text = pyperclip.paste()
            
            if text and text.strip():
                print(f"Reading clipboard: {text[:50]}...")
                self.callback(text)
            else:
                print("Clipboard is empty")
                
        except Exception as e:
            print(f"Error reading clipboard: {e}")
    
    def _stop_audio(self):
        """Stop current audio playback."""
        # This will be handled by the main application
        print("Stop audio requested")
        # You can implement audio stopping logic here
    
    def start_monitoring(self):
        """Start monitoring for hotkeys."""
        self.setup_hotkeys()
        self.running = True
        print("Hotkey monitoring started. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring for hotkeys."""
        self.running = False
        keyboard.unhook_all()
        print("Hotkey monitoring stopped.")
    
    def set_hotkey(self, action: str, key_combination: str):
        """Set a custom hotkey for an action."""
        if action in self.hotkeys:
            # Remove old hotkey
            keyboard.remove_hotkey(self.hotkeys[action])
            
            # Set new hotkey
            self.hotkeys[action] = key_combination
            
            # Re-register if monitoring is active
            if self.running:
                self.setup_hotkeys()
            
            print(f"Hotkey for {action} changed to: {key_combination}")
        else:
            print(f"Unknown action: {action}")
    
    def get_hotkeys(self):
        """Get current hotkey configuration."""
        return self.hotkeys.copy()
