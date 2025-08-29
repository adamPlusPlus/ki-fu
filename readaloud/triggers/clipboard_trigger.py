"""
Clipboard Trigger for ReadAloud.

This module provides functionality to read text from the clipboard.
"""

import pyperclip
from typing import Callable, Optional
import time


class ClipboardTrigger:
    """Trigger TTS when clipboard content changes."""
    
    def __init__(self, callback: Callable[[str], None], 
                 check_interval: float = 1.0):
        """
        Initialize clipboard trigger.
        
        Args:
            callback: Function to call with clipboard text
            check_interval: How often to check clipboard (seconds)
        """
        self.callback = callback
        self.check_interval = check_interval
        self.last_content = pyperclip.paste()
        self.running = False
    
    def start_monitoring(self):
        """Start monitoring clipboard for changes."""
        self.running = True
        print("Clipboard monitoring started. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                current_content = pyperclip.paste()
                
                if current_content != self.last_content and current_content.strip():
                    print(f"Clipboard content changed: {current_content[:50]}...")
                    self.callback(current_content)
                    self.last_content = current_content
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\nClipboard monitoring stopped.")
            self.running = False
    
    def stop_monitoring(self):
        """Stop monitoring clipboard."""
        self.running = False
    
    def read_current(self):
        """Read current clipboard content immediately."""
        content = pyperclip.paste()
        if content.strip():
            self.callback(content)
        return content
