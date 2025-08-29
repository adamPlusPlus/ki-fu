"""
Configuration management for Home Assistant development environment.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration manager for Home Assistant development."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file (default: .env in project root)
        """
        if config_file is None:
            # Look for .env file in project root
            project_root = Path(__file__).parent.parent
            config_file = project_root / ".env"
        
        self.config_file = Path(config_file)
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file and environment variables."""
        # Load from .env file if it exists
        if self.config_file.exists():
            self._load_env_file()
        
        # Environment variables take precedence
        self._load_env_vars()
    
    def _load_env_file(self):
        """Load configuration from .env file."""
        try:
            with open(self.config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_file}: {e}")
    
    def _load_env_vars(self):
        """Load configuration from environment variables."""
        # Home Assistant settings
        self.ha_url = os.getenv('HA_URL', 'http://localhost:8123')
        self.ha_access_token = os.getenv('HA_ACCESS_TOKEN')
        self.ha_ssl_verify = os.getenv('HA_SSL_VERIFY', 'true').lower() == 'true'
        
        # MQTT settings
        self.mqtt_broker = os.getenv('MQTT_BROKER')
        self.mqtt_port = int(os.getenv('MQTT_PORT', '1883'))
        self.mqtt_username = os.getenv('MQTT_USERNAME')
        self.mqtt_password = os.getenv('MQTT_PASSWORD')
        
        # Development settings
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        errors = []
        
        if not self.ha_url:
            errors.append("HA_URL is required")
        
        if not self.ha_access_token:
            errors.append("HA_ACCESS_TOKEN is required")
        
        if errors:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    def get_ha_client_config(self) -> dict:
        """
        Get configuration for Home Assistant client.
        
        Returns:
            Dictionary with client configuration
        """
        return {
            'url': self.ha_url,
            'token': self.ha_access_token,
            'ssl_verify': self.ha_ssl_verify
        }
    
    def get_mqtt_config(self) -> dict:
        """
        Get MQTT configuration.
        
        Returns:
            Dictionary with MQTT configuration
        """
        if not self.mqtt_broker:
            return {}
        
        config = {
            'broker': self.mqtt_broker,
            'port': self.mqtt_port
        }
        
        if self.mqtt_username:
            config['username'] = self.mqtt_username
        if self.mqtt_password:
            config['password'] = self.mqtt_password
        
        return config
    
    def print_config(self):
        """Print current configuration (without sensitive data)."""
        print("🔧 Current Configuration:")
        print(f"   Home Assistant URL: {self.ha_url}")
        print(f"   SSL Verify: {self.ha_ssl_verify}")
        print(f"   Debug Mode: {self.debug}")
        print(f"   Log Level: {self.log_level}")
        
        if self.mqtt_broker:
            print(f"   MQTT Broker: {self.mqtt_broker}:{self.mqtt_port}")
        
        if self.ha_access_token:
            print(f"   Access Token: {'*' * 10}{self.ha_access_token[-4:]}")
        else:
            print("   Access Token: Not set")


# Global configuration instance
config = Config()
