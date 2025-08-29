"""
Text Input Trigger for ReadAloud.

This module provides functionality to trigger TTS from direct text input.
"""

from typing import Callable, Optional


class TextInputTrigger:
    """Trigger TTS from direct text input."""
    
    def __init__(self, callback: Callable[[str], None]):
        """
        Initialize text input trigger.
        
        Args:
            callback: Function to call with input text
        """
        self.callback = callback
    
    def read_text(self, text: str):
        """Read text directly."""
        if text and text.strip():
            print(f"Reading text: {text[:50]}...")
            self.callback(text)
        else:
            print("No text provided")
    
    def interactive_input(self):
        """Start interactive text input mode."""
        print("Interactive text input mode. Type 'quit' to exit.")
        print("Enter text to read aloud:")
        
        try:
            while True:
                text = input("> ").strip()
                
                if text.lower() == 'quit':
                    print("Exiting interactive mode.")
                    break
                
                if text:
                    self.read_text(text)
                else:
                    print("Please enter some text.")
                    
        except KeyboardInterrupt:
            print("\nInteractive mode interrupted.")
    
    def read_from_file(self, file_path: str):
        """Read text from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.strip():
                print(f"Reading file: {file_path}")
                self.callback(content)
            else:
                print(f"File is empty: {file_path}")
                
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
    
    def batch_read(self, texts: list):
        """Read multiple texts in sequence."""
        for i, text in enumerate(texts, 1):
            if text and text.strip():
                print(f"Reading text {i}/{len(texts)}: {text[:50]}...")
                self.callback(text)
            else:
                print(f"Skipping empty text {i}")
