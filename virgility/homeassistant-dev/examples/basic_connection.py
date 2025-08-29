#!/usr/bin/env python3
"""
Basic Home Assistant Connection Example

This script demonstrates how to connect to Home Assistant and retrieve basic information.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from homeassistant_api import Client
    import requests
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Make sure you have activated the virtual environment and installed requirements")
    sys.exit(1)


def test_basic_connection():
    """Test basic connection to Home Assistant."""
    
    # Configuration - you'll need to set these
    ha_url = os.getenv('HA_URL', 'http://localhost:8123')
    ha_token = os.getenv('HA_ACCESS_TOKEN', 'your-token-here')
    
    if ha_token == 'your-token-here':
        print("⚠️  Please set your Home Assistant access token in the .env file")
        print("   You can generate one in Home Assistant: Profile > Long-Lived Access Tokens")
        return False
    
    try:
        print(f"🔌 Connecting to Home Assistant at: {ha_url}")
        
        # Test basic HTTP connection first
        response = requests.get(f"{ha_url}/api/", timeout=10)
        if response.status_code == 200:
            print("✅ Home Assistant API is accessible")
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
        # Test authenticated connection
        client = Client(ha_url, ha_token)
        
        # Get basic info
        config = client.get_config()
        print(f"🏠 Home Assistant version: {config.get('version', 'Unknown')}")
        
        # Get entities count
        entities = client.get_entities()
        print(f"📱 Found {len(entities)} entities")
        
        # Get some entity examples
        if entities:
            print("\n📋 Sample entities:")
            for i, entity in enumerate(entities[:5]):
                print(f"   {i+1}. {entity.entity_id} - {entity.state}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def main():
    """Main function."""
    print("🚀 Home Assistant Basic Connection Test")
    print("=" * 50)
    
    success = test_basic_connection()
    
    if success:
        print("\n✅ Connection test successful!")
        print("🎉 You're ready to start developing with Home Assistant!")
    else:
        print("\n❌ Connection test failed!")
        print("🔧 Please check your configuration and try again")


if __name__ == "__main__":
    main()
