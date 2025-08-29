#!/usr/bin/env python3
"""
StreamDeck Plugin for ReadAloud

This plugin allows StreamDeck to trigger ReadAloud TTS functionality.
"""

import json
import websocket
import threading
import time
import os
import sys
from typing import Dict, Any, Optional

# Add the parent directory to Python path to import ReadAloud
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ReadAloud
from config import Config


class StreamDeckPlugin:
    """StreamDeck plugin for ReadAloud TTS."""
    
    def __init__(self):
        """Initialize the StreamDeck plugin."""
        self.config = Config()
        self.app = None
        self.ws = None
        self.running = False
        self.actions = {
            'read_clipboard': self._read_clipboard,
            'read_selection': self._read_selection,
            'stop_audio': self._stop_audio,
            'read_file': self._read_file,
            'toggle_monitoring': self._toggle_monitoring
        }
        
        # Initialize ReadAloud in background mode
        self._setup_readaloud()
        
        # StreamDeck connection settings
        self.streamdeck_host = self.config.get('streamdeck.host', 'localhost')
        self.streamdeck_port = self.config.get('streamdeck.port', 8000)
        self.streamdeck_token = self.config.get('streamdeck.token', '')
    
    def _setup_readaloud(self):
        """Setup ReadAloud application in background mode."""
        try:
            config = {
                'tts_engine': self.config.get('tts_engine', 'auto'),
                'voice': self.config.get('voice', 'default'),
                'temperature': self.config.get('temperature', 0.3),
                'seed': self.config.get('seed'),
                'background_mode': True
            }
            
            self.app = ReadAloud(config)
            print("ReadAloud initialized for StreamDeck integration")
            
        except Exception as e:
            print(f"Error initializing ReadAloud: {e}")
    
    def start(self):
        """Start the StreamDeck plugin."""
        print("Starting StreamDeck plugin...")
        self.running = True
        
        # Start WebSocket connection to StreamDeck
        self._connect_streamdeck()
        
        # Start background monitoring
        self._start_background_monitoring()
    
    def stop(self):
        """Stop the StreamDeck plugin."""
        print("Stopping StreamDeck plugin...")
        self.running = False
        
        if self.ws:
            self.ws.close()
        
        if self.app:
            # Stop any running operations
            for trigger in self.app.triggers.values():
                if hasattr(trigger, 'stop_monitoring'):
                    trigger.stop_monitoring()
    
    def _connect_streamdeck(self):
        """Connect to StreamDeck via WebSocket."""
        try:
            ws_url = f"ws://{self.streamdeck_host}:{self.streamdeck_port}/plugin"
            
            def on_message(ws, message):
                self._handle_streamdeck_message(message)
            
            def on_error(ws, error):
                print(f"StreamDeck WebSocket error: {error}")
            
            def on_close(ws, close_status_code, close_msg):
                print("StreamDeck WebSocket connection closed")
                if self.running:
                    # Reconnect after delay
                    time.sleep(5)
                    self._connect_streamdeck()
            
            def on_open(ws):
                print("Connected to StreamDeck")
                # Register plugin
                self._register_plugin(ws)
            
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            # Start WebSocket in a separate thread
            ws_thread = threading.Thread(target=self.ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
        except Exception as e:
            print(f"Error connecting to StreamDeck: {e}")
    
    def _register_plugin(self, ws):
        """Register this plugin with StreamDeck."""
        try:
            registration = {
                "action": "register_plugin",
                "plugin_name": "ReadAloud",
                "version": "1.0.0",
                "capabilities": list(self.actions.keys()),
                "token": self.streamdeck_token
            }
            
            ws.send(json.dumps(registration))
            print("Plugin registered with StreamDeck")
            
        except Exception as e:
            print(f"Error registering plugin: {e}")
    
    def _handle_streamdeck_message(self, message):
        """Handle incoming messages from StreamDeck."""
        try:
            data = json.loads(message)
            action = data.get('action')
            params = data.get('params', {})
            
            if action in self.actions:
                print(f"Executing StreamDeck action: {action}")
                self.actions[action](params)
            else:
                print(f"Unknown StreamDeck action: {action}")
                
        except json.JSONDecodeError:
            print(f"Invalid JSON message from StreamDeck: {message}")
        except Exception as e:
            print(f"Error handling StreamDeck message: {e}")
    
    def _read_clipboard(self, params: Dict[str, Any]):
        """Read clipboard content."""
        if self.app:
            self.app.read_clipboard()
    
    def _read_selection(self, params: Dict[str, Any]):
        """Read selected text."""
        if self.app:
            # Simulate Ctrl+C to copy selection
            import keyboard
            keyboard.send('ctrl+c')
            time.sleep(0.1)  # Small delay
            self.app.read_clipboard()
    
    def _stop_audio(self, params: Dict[str, Any]):
        """Stop current audio playback."""
        if self.app:
            self.app.stop_audio()
    
    def _read_file(self, params: Dict[str, Any]):
        """Read a specific file."""
        if self.app and 'file_path' in params:
            file_path = params['file_path']
            if os.path.exists(file_path):
                self.app.read_file(file_path)
            else:
                print(f"File not found: {file_path}")
    
    def _toggle_monitoring(self, params: Dict[str, Any]):
        """Toggle file monitoring."""
        if self.app and 'file_path' in params:
            file_path = params['file_path']
            # This would need to be implemented in the main app
            print(f"Toggle monitoring for: {file_path}")
    
    def _start_background_monitoring(self):
        """Start background monitoring for StreamDeck triggers."""
        if not self.app:
            return
        
        # Start clipboard monitoring in background
        try:
            self.app.start_clipboard_monitoring()
        except Exception as e:
            print(f"Error starting clipboard monitoring: {e}")
        
        # Start hotkey monitoring in background
        try:
            self.app.start_hotkey_monitoring()
        except Exception as e:
            print(f"Error starting hotkey monitoring: {e}")
    
    def send_status(self, status: str):
        """Send status update to StreamDeck."""
        if self.ws and self.ws.sock:
            try:
                message = {
                    "action": "status_update",
                    "status": status,
                    "timestamp": time.time()
                }
                self.ws.send(json.dumps(message))
            except Exception as e:
                print(f"Error sending status to StreamDeck: {e}")


def main():
    """Main entry point for StreamDeck plugin."""
    plugin = StreamDeckPlugin()
    
    try:
        plugin.start()
        
        # Keep the plugin running
        while plugin.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down StreamDeck plugin...")
    finally:
        plugin.stop()


if __name__ == "__main__":
    main()
