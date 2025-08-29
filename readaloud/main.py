#!/usr/bin/env python3
"""
ReadAloud - Main Application

A comprehensive text-to-speech tool with multiple trigger mechanisms.
"""

import os
import sys
import argparse
import time
import threading
from pathlib import Path
from typing import Optional, Dict, Any

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tts_engine import TTSEngine, AudioPlayer
from engines.higgs_audio import HiggsAudioEngine
from engines.coqui_tts import CoquiTTSEngine
from triggers import (
    ClipboardTrigger, 
    FileMonitorTrigger, 
    HotkeyTrigger, 
    TextInputTrigger
)


class ReadAloud:
    """Main ReadAloud application class."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize ReadAloud application."""
        self.config = config or {}
        self.tts_engine = None
        self.audio_player = AudioPlayer()
        self.current_audio = None
        self.running = False
        
        # Initialize TTS engine
        self._setup_tts_engine()
        
        # Initialize triggers
        self.triggers = {
            'clipboard': ClipboardTrigger(self._handle_text),
            'file_monitor': FileMonitorTrigger(self._handle_file_change),
            'hotkeys': HotkeyTrigger(self._handle_text),
            'text_input': TextInputTrigger(self._handle_text)
        }
    
    def _setup_tts_engine(self):
        """Setup the TTS engine based on configuration and availability."""
        engine_name = self.config.get('tts_engine', 'auto').lower()
        
        if engine_name == 'higgs_audio' or engine_name == 'auto':
            try:
                self.tts_engine = HiggsAudioEngine(self.config.get('higgs_config', {}))
                if self.tts_engine.is_available:
                    print("Using Higgs Audio TTS engine")
                    return
            except Exception as e:
                print(f"Higgs Audio not available: {e}")
        
        if engine_name == 'coqui' or engine_name == 'auto':
            try:
                self.tts_engine = CoquiTTSEngine(self.config.get('coqui_config', {}))
                if self.tts_engine.is_available:
                    print("Using Coqui TTS engine")
                    return
            except Exception as e:
                print(f"Coqui TTS not available: {e}")
        
        # Fallback to system TTS if available
        print("No TTS engine available. Please install Higgs Audio or Coqui TTS.")
        sys.exit(1)
    
    def _handle_text(self, text: str):
        """Handle text input from various triggers."""
        if not text or not text.strip():
            return
        
        print(f"Processing text: {text[:100]}...")
        
        try:
            # Generate audio
            output_path = self.tts_engine.synthesize(
                text,
                voice=self.config.get('voice'),
                temperature=self.config.get('temperature', 0.3),
                seed=self.config.get('seed')
            )
            
            # Play audio
            self.current_audio = output_path
            self.audio_player.play(output_path)
            
            print(f"Audio generated and playing: {output_path}")
            
        except Exception as e:
            print(f"Error processing text: {e}")
    
    def _handle_file_change(self, file_path: str, content: str):
        """Handle file change events."""
        print(f"File changed: {file_path}")
        self._handle_text(content)
    
    def start_clipboard_monitoring(self):
        """Start monitoring clipboard for changes."""
        print("Starting clipboard monitoring...")
        self.triggers['clipboard'].start_monitoring()
    
    def start_file_monitoring(self, file_path: str):
        """Start monitoring a file for changes."""
        print(f"Starting file monitoring for: {file_path}")
        self.triggers['file_monitor'].add_file(file_path)
        self.triggers['file_monitor'].start_monitoring()
    
    def start_hotkey_monitoring(self):
        """Start monitoring for global hotkeys."""
        print("Starting hotkey monitoring...")
        self.triggers['hotkeys'].start_monitoring()
    
    def start_interactive_mode(self):
        """Start interactive text input mode."""
        print("Starting interactive mode...")
        self.triggers['text_input'].interactive_input()
    
    def read_file(self, file_path: str):
        """Read a file immediately."""
        self.triggers['text_input'].read_from_file(file_path)
    
    def read_clipboard(self):
        """Read current clipboard content."""
        self.triggers['clipboard'].read_current()
    
    def stop_audio(self):
        """Stop current audio playback."""
        if self.current_audio:
            self.audio_player.stop()
            self.current_audio = None
            print("Audio stopped")
    
    def get_engine_info(self):
        """Get information about the current TTS engine."""
        if self.tts_engine:
            info = self.tts_engine.get_engine_info()
            print("TTS Engine Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print("No TTS engine available")
    
    def get_available_voices(self):
        """Get list of available voices."""
        if self.tts_engine:
            voices = self.tts_engine.get_available_voices()
            print("Available voices:")
            for voice in voices:
                print(f"  {voice}")
        else:
            print("No TTS engine available")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="ReadAloud - Text-to-Speech Tool")
    
    # TTS options
    parser.add_argument('--engine', choices=['higgs_audio', 'coqui', 'auto'], 
                       default='auto', help='TTS engine to use')
    parser.add_argument('--voice', help='Voice to use for synthesis')
    parser.add_argument('--temperature', type=float, default=0.3, 
                       help='Temperature for text generation')
    parser.add_argument('--seed', type=int, help='Random seed for generation')
    
    # Trigger options
    parser.add_argument('--clipboard', action='store_true', 
                       help='Monitor clipboard for changes')
    parser.add_argument('--monitor', metavar='FILE', 
                       help='Monitor a file for changes')
    parser.add_argument('--hotkeys', action='store_true', 
                       help='Enable global hotkeys')
    parser.add_argument('--interactive', action='store_true', 
                       help='Start interactive mode')
    parser.add_argument('--file', metavar='FILE', 
                       help='Read a specific file')
    
    # Configuration
    parser.add_argument('--config', metavar='FILE', 
                       help='Configuration file path')
    parser.add_argument('--info', action='store_true', 
                       help='Show TTS engine information')
    parser.add_argument('--voices', action='store_true', 
                       help='Show available voices')
    
    args = parser.parse_args()
    
    # Load configuration
    config = {
        'tts_engine': args.engine,
        'voice': args.voice,
        'temperature': args.temperature,
        'seed': args.seed
    }
    
    # Create application
    app = ReadAloud(config)
    
    # Handle info requests
    if args.info:
        app.get_engine_info()
        return
    
    if args.voices:
        app.get_available_voices()
        return
    
    # Handle different modes
    if args.file:
        app.read_file(args.file)
    elif args.clipboard:
        app.start_clipboard_monitoring()
    elif args.monitor:
        app.start_file_monitoring(args.monitor)
    elif args.hotkeys:
        app.start_hotkey_monitoring()
    elif args.interactive:
        app.start_interactive_mode()
    else:
        # Default to interactive mode
        app.start_interactive_mode()


if __name__ == "__main__":
    main()
