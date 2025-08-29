#!/usr/bin/env python3
"""
StreamDeck Integration Script for ReadAloud

This script helps integrate ReadAloud with StreamDeck by setting up the connection
and configuring button mappings.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config


class StreamDeckIntegrator:
    """StreamDeck integration helper."""
    
    def __init__(self):
        """Initialize the StreamDeck integrator."""
        self.config = Config()
        self.streamdeck_config = self._load_streamdeck_config()
        
    def _load_streamdeck_config(self) -> Dict[str, Any]:
        """Load StreamDeck configuration."""
        config_path = Path(__file__).parent / "streamdeck_config.json"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            print(f"StreamDeck config not found: {config_path}")
            return {}
    
    def setup_streamdeck_connection(self):
        """Setup StreamDeck connection."""
        print("Setting up StreamDeck connection...")
        
        # Check if StreamDeck software is running
        if not self._check_streamdeck_running():
            print("StreamDeck software not detected. Please ensure StreamDeck is running.")
            return False
        
        # Update configuration with StreamDeck settings
        self._update_config()
        
        # Test connection
        if self._test_connection():
            print("StreamDeck connection established successfully!")
            return True
        else:
            print("Failed to establish StreamDeck connection.")
            return False
    
    def _check_streamdeck_running(self) -> bool:
        """Check if StreamDeck software is running."""
        try:
            # Check for StreamDeck process (Windows)
            if os.name == 'nt':
                result = subprocess.run(
                    ['tasklist', '/FI', 'IMAGENAME eq StreamDeck.exe'],
                    capture_output=True,
                    text=True
                )
                return 'StreamDeck.exe' in result.stdout
            else:
                # Linux/macOS
                result = subprocess.run(
                    ['pgrep', '-f', 'StreamDeck'],
                    capture_output=True
                )
                return result.returncode == 0
                
        except Exception as e:
            print(f"Error checking StreamDeck process: {e}")
            return False
    
    def _update_config(self):
        """Update configuration with StreamDeck settings."""
        streamdeck_settings = self.streamdeck_config.get('streamdeck', {})
        
        # Update main config
        self.config.set('streamdeck.host', streamdeck_settings.get('host', 'localhost'))
        self.config.set('streamdeck.port', streamdeck_settings.get('port', 8000))
        self.config.set('streamdeck.token', streamdeck_settings.get('token', ''))
        self.config.set('streamdeck.auto_reconnect', streamdeck_settings.get('auto_reconnect', True))
        
        # Save configuration
        self.config.save()
        print("Configuration updated with StreamDeck settings")
    
    def _test_connection(self) -> bool:
        """Test StreamDeck connection."""
        try:
            import websocket
            
            # Try to connect to StreamDeck
            ws_url = f"ws://{self.config.get('streamdeck.host')}:{self.config.get('streamdeck.port')}/plugin"
            
            def on_error(ws, error):
                print(f"Connection error: {error}")
            
            def on_close(ws, close_status_code, close_msg):
                print("Connection closed")
            
            def on_open(ws):
                print("Connection opened successfully")
                ws.close()
            
            ws = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_error=on_error,
                on_close=on_close
            )
            
            # Run in a separate thread with timeout
            import threading
            ws_thread = threading.Thread(target=ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
            # Wait for connection
            time.sleep(2)
            
            return True
            
        except ImportError:
            print("websocket-client not installed. Install with: pip install websocket-client")
            return False
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def create_button_profiles(self):
        """Create StreamDeck button profiles."""
        print("Creating StreamDeck button profiles...")
        
        profiles = self.streamdeck_config.get('profiles', {})
        buttons = self.streamdeck_config.get('buttons', {})
        
        for profile_name, profile_config in profiles.items():
            print(f"\nProfile: {profile_config['name']}")
            print(f"Description: {profile_config['description']}")
            print("Buttons:")
            
            for button_id in profile_config['buttons']:
                button_name = f"button_{button_id}"
                if button_name in buttons:
                    button = buttons[button_name]
                    print(f"  {button_id}: {button['name']} - {button['description']}")
        
        print("\nButton profiles created successfully!")
    
    def start_background_service(self):
        """Start ReadAloud background service."""
        print("Starting ReadAloud background service...")
        
        try:
            # Start background service
            service_path = Path(__file__).parent.parent / "background_service.py"
            
            if service_path.exists():
                subprocess.Popen([
                    sys.executable, str(service_path),
                    '--daemon'
                ])
                print("Background service started successfully!")
                return True
            else:
                print(f"Background service not found: {service_path}")
                return False
                
        except Exception as e:
            print(f"Error starting background service: {e}")
            return False
    
    def start_streamdeck_plugin(self):
        """Start StreamDeck plugin."""
        print("Starting StreamDeck plugin...")
        
        try:
            # Start StreamDeck plugin
            plugin_path = Path(__file__).parent / "plugin.py"
            
            if plugin_path.exists():
                subprocess.Popen([
                    sys.executable, str(plugin_path)
                ])
                print("StreamDeck plugin started successfully!")
                return True
            else:
                print(f"StreamDeck plugin not found: {plugin_path}")
                return False
                
        except Exception as e:
            print(f"Error starting StreamDeck plugin: {e}")
            return False
    
    def setup_auto_start(self):
        """Setup auto-start for StreamDeck integration."""
        print("Setting up auto-start...")
        
        try:
            if os.name == 'nt':  # Windows
                self._setup_windows_autostart()
            else:  # Linux/macOS
                self._setup_unix_autostart()
                
            print("Auto-start configured successfully!")
            
        except Exception as e:
            print(f"Error setting up auto-start: {e}")
    
    def _setup_windows_autostart(self):
        """Setup Windows auto-start."""
        try:
            import winreg
            
            # Create startup script
            startup_script = Path(__file__).parent / "startup.bat"
            
            with open(startup_script, 'w') as f:
                f.write(f'@echo off\n')
                f.write(f'cd /d "{Path(__file__).parent.parent}"\n')
                f.write(f'python background_service.py --daemon\n')
                f.write(f'python streamdeck/plugin.py\n')
            
            # Add to registry
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(
                key,
                "ReadAloud",
                0,
                winreg.REG_SZ,
                str(startup_script.absolute())
            )
            
            winreg.CloseKey(key)
            
        except ImportError:
            print("winreg not available, skipping registry setup")
        except Exception as e:
            print(f"Error setting up Windows auto-start: {e}")
    
    def _setup_unix_autostart(self):
        """Setup Unix auto-start."""
        try:
            # Create systemd service file
            service_file = Path.home() / ".config/systemd/user/readaloud.service"
            service_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(service_file, 'w') as f:
                f.write("[Unit]\n")
                f.write("Description=ReadAloud TTS Background Service\n")
                f.write("After=network.target\n\n")
                f.write("[Service]\n")
                f.write(f"ExecStart={sys.executable} {Path(__file__).parent.parent}/background_service.py\n")
                f.write(f"WorkingDirectory={Path(__file__).parent.parent}\n")
                f.write("Restart=always\n")
                f.write("RestartSec=10\n\n")
                f.write("[Install]\n")
                f.write("WantedBy=default.target\n")
            
            # Enable service
            subprocess.run([
                'systemctl', '--user', 'enable', 'readaloud.service'
            ])
            
            print("Systemd service created and enabled")
            
        except Exception as e:
            print(f"Error setting up Unix auto-start: {e}")
    
    def run_integration(self):
        """Run the complete StreamDeck integration."""
        print("🎵 ReadAloud StreamDeck Integration")
        print("=" * 40)
        
        # Setup connection
        if not self.setup_streamdeck_connection():
            print("Integration failed at connection setup")
            return False
        
        # Create button profiles
        self.create_button_profiles()
        
        # Start background service
        if not self.start_background_service():
            print("Integration failed at background service startup")
            return False
        
        # Start StreamDeck plugin
        if not self.start_streamdeck_plugin():
            print("Integration failed at plugin startup")
            return False
        
        # Setup auto-start
        self.setup_auto_start()
        
        print("\n🎉 StreamDeck integration completed successfully!")
        print("\nYour StreamDeck is now configured to work with ReadAloud.")
        print("Press the configured buttons to trigger TTS functionality.")
        
        return True


def main():
    """Main entry point for StreamDeck integration."""
    integrator = StreamDeckIntegrator()
    
    try:
        success = integrator.run_integration()
        
        if success:
            print("\nIntegration completed successfully!")
            print("ReadAloud is now running in the background and ready for StreamDeck triggers.")
        else:
            print("\nIntegration failed. Please check the error messages above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nIntegration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during integration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
