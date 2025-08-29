"""
Tests for configuration module.
"""

import os
import tempfile
import unittest
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear environment variables
        self.old_env = dict(os.environ)
        for key in ['HA_URL', 'HA_ACCESS_TOKEN', 'HA_SSL_VERIFY']:
            if key in os.environ:
                del os.environ[key]
    
    def tearDown(self):
        """Clean up test environment."""
        # Restore environment variables
        os.environ.clear()
        os.environ.update(self.old_env)
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        
        self.assertEqual(config.ha_url, 'http://localhost:8123')
        self.assertIsNone(config.ha_access_token)
        self.assertTrue(config.ha_ssl_verify)
        self.assertFalse(config.debug)
        self.assertEqual(config.log_level, 'INFO')
    
    def test_environment_override(self):
        """Test that environment variables override defaults."""
        os.environ['HA_URL'] = 'http://test:8123'
        os.environ['HA_ACCESS_TOKEN'] = 'test-token'
        os.environ['HA_SSL_VERIFY'] = 'false'
        os.environ['DEBUG'] = 'true'
        
        config = Config()
        
        self.assertEqual(config.ha_url, 'http://test:8123')
        self.assertEqual(config.ha_access_token, 'test-token')
        self.assertFalse(config.ha_ssl_verify)
        self.assertTrue(config.debug)
    
    def test_config_file_loading(self):
        """Test loading configuration from file."""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("HA_URL=http://file:8123\n")
            f.write("HA_ACCESS_TOKEN=file-token\n")
            f.write("DEBUG=true\n")
            config_file = f.name
        
        try:
            config = Config(config_file)
            
            self.assertEqual(config.ha_url, 'http://file:8123')
            self.assertEqual(config.ha_access_token, 'file-token')
            self.assertTrue(config.debug)
        finally:
            # Clean up
            os.unlink(config_file)
    
    def test_validation(self):
        """Test configuration validation."""
        config = Config()
        
        # Should fail without access token
        self.assertFalse(config.validate())
        
        # Should pass with required values
        config.ha_access_token = 'test-token'
        self.assertTrue(config.validate())
    
    def test_client_config(self):
        """Test getting client configuration."""
        config = Config()
        config.ha_access_token = 'test-token'
        
        client_config = config.get_ha_client_config()
        
        expected = {
            'url': 'http://localhost:8123',
            'token': 'test-token',
            'ssl_verify': True
        }
        self.assertEqual(client_config, expected)


if __name__ == '__main__':
    unittest.main()
