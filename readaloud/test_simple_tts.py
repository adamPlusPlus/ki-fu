#!/usr/bin/env python3
"""
Simple test script to test TTS functionality
"""
import os
import sys
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_tts():
    """Test the TTS engine with a simple call"""
    
    # Import the TTS functions
    from web_interface import _call_tts_engine, load_config
    
    # Load configuration
    load_config()
    
    # Test text
    test_text = "Hello! This is a test of the ReadAloud text-to-speech system."
    
    print(f"🔍 Testing TTS with text: {test_text}")
    print(f"📁 Current directory: {os.getcwd()}")
    
    # Call TTS engine
    try:
        result = _call_tts_engine(test_text)
        print(f"✅ TTS Result: {result}")
        
        if result['success']:
            print(f"🎵 Audio file generated: {result.get('audio_file', 'N/A')}")
        else:
            print(f"❌ TTS failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"💥 Exception occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_tts()
