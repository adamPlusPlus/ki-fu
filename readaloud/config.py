"""
Configuration management for ReadAloud.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration management for ReadAloud."""
    
    DEFAULT_CONFIG = {
        'tts_engine': 'auto',
        'voice': 'default',
        'temperature': 0.3,
        'seed': None,
        'audio_output_path': './audio_output',
        'higgs_config': {
            'model_path': '',
            'python_path': 'python',
            'higgs_script': 'examples/generation.py'
        },
        'coqui_config': {
            'model_name': 'tts_models/en/ljspeech/tacotron2-DDC'
        },
        'hotkeys': {
            'read_selection': 'ctrl+shift+r',
            'read_clipboard': 'ctrl+shift+c',
            'stop_audio': 'ctrl+shift+s'
        },
        'monitoring': {
            'clipboard_interval': 1.0,
            'file_check_interval': 1.0
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration."""
        if config_path is None:
            config_path = self._get_default_config_path()
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        # Try to find config in current directory or user home
        possible_paths = [
            './readaloud_config.json',
            './.readaloud_config.json',
            os.path.expanduser('~/.readaloud_config.json'),
            os.path.expanduser('~/.config/readaloud/config.json')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Return default path in current directory
        return './readaloud_config.json'
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # Merge with default config
                config = self.DEFAULT_CONFIG.copy()
                self._deep_merge(config, user_config)
                return config
                
            except Exception as e:
                print(f"Error loading config from {self.config_path}: {e}")
                print("Using default configuration")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Deep merge two dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving config to {self.config_path}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save to file
        self._save_config(self.config)
    
    def save(self):
        """Save current configuration to file."""
        self._save_config(self.config)
    
    def get_tts_config(self, engine: str) -> Dict[str, Any]:
        """Get TTS engine specific configuration."""
        return self.config.get(f'{engine}_config', {})
    
    def get_hotkeys(self) -> Dict[str, str]:
        """Get hotkey configuration."""
        return self.config.get('hotkeys', {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration."""
        return self.config.get('monitoring', {})
    
    def create_sample_config(self):
        """Create a sample configuration file."""
        sample_config = {
            'tts_engine': 'auto',
            'voice': 'default',
            'temperature': 0.3,
            'seed': 42,
            'audio_output_path': './audio_output',
            'higgs_config': {
                'model_path': '/path/to/higgs-audio',
                'python_path': 'python',
                'higgs_script': 'examples/generation.py'
            },
            'coqui_config': {
                'model_name': 'tts_models/en/ljspeech/tacotron2-DDC'
            },
            'hotkeys': {
                'read_selection': 'ctrl+shift+r',
                'read_clipboard': 'ctrl+shift+c',
                'stop_audio': 'ctrl+shift+s'
            },
            'monitoring': {
                'clipboard_interval': 1.0,
                'file_check_interval': 1.0
            }
        }
        
        sample_path = Path('./readaloud_config_sample.json')
        try:
            with open(sample_path, 'w', encoding='utf-8') as f:
                json.dump(sample_config, f, indent=2, ensure_ascii=False)
            print(f"Sample configuration created: {sample_path}")
        except Exception as e:
            print(f"Error creating sample config: {e}")


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file."""
    return Config(config_path)
