#!/usr/bin/env python3
"""
Simple test script for clipboard TTS functionality
"""

import os
import sys
import json
import subprocess
import pyperclip

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_config():
    """Load configuration from JSON file"""
    config_path = 'readaloud_config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default config
        return {
            'tts_engine': 'higgs_audio',
            'voice': 'default',
            'temperature': 0.3,
            'volume': 0.8,
            'speed': 1.0,
            'audio_output_path': './audio_output',
            'higgs_config': {
                'model_path': 'H:/AI/higgs/higgs-audio',
                'python_path': 'python',
                'higgs_script': 'examples/generation.py'
            }
        }

def call_higgs_audio(text):
    """Call Higgs Audio TTS engine"""
    try:
        config = load_config()
        higgs_config = config.get('higgs_config', {})
        model_path = higgs_config.get('model_path', 'H:/AI/higgs/higgs-audio')
        python_path = higgs_config.get('python_path', 'python')
        script_path = higgs_config.get('higgs_script', 'examples/generation.py')

        if not os.path.exists(model_path):
            print(f"❌ Higgs Audio not found at: {model_path}")
            return False

        output_dir = config.get('audio_output_path', './audio_output')
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        import uuid
        audio_filename = f"output_{uuid.uuid4().hex[:8]}.wav"
        audio_path = os.path.join(output_dir, audio_filename)

        print(f"🔧 Calling Higgs Audio...")
        print(f"   Model path: {model_path}")
        print(f"   Script: {script_path}")
        print(f"   Text: {text[:50]}...")
        print(f"   Output: {audio_path}")

        cmd = [
            python_path,
            os.path.join(model_path, script_path),
            '--transcript', text,
            '--out_path', audio_path,
            '--temperature', str(config.get('temperature', 0.3))
        ]

        print(f"   Command: {' '.join(cmd)}")

        print(f"   Starting generation (this may take 1-2 minutes on first run)...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=model_path,
            timeout=600  # 10 minutes for first run
        )

        print(f"   Return code: {result.returncode}")
        if result.stdout:
            print(f"   Stdout: {result.stdout}")
        if result.stderr:
            print(f"   Stderr: {result.stderr}")

        if result.returncode == 0 and os.path.exists(audio_path):
            print(f"✅ Audio generated successfully: {audio_path}")
            # Play the audio
            play_audio(audio_path)
            return True
        else:
            print(f"❌ Higgs Audio failed")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Higgs Audio timed out")
        return False
    except Exception as e:
        print(f"❌ Higgs Audio error: {str(e)}")
        return False

def play_audio(audio_path):
    """Play audio file using system default player"""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(audio_path)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['afplay', audio_path])
        else:  # Linux
            subprocess.run(['aplay', audio_path])
        print(f"🔊 Playing audio: {audio_path}")
    except Exception as e:
        print(f"❌ Failed to play audio: {str(e)}")

def main():
    print("📋 ReadAloud Clipboard TTS Test")
    print("=" * 40)
    
    # Get clipboard content
    try:
        clipboard_text = pyperclip.paste()
        if not clipboard_text.strip():
            print("❌ Clipboard is empty")
            return
        
        print(f"📋 Clipboard content: {clipboard_text[:100]}...")
        print()
        
        # Call TTS
        success = call_higgs_audio(clipboard_text)
        
        if success:
            print("✅ TTS completed successfully!")
        else:
            print("❌ TTS failed")
            
    except ImportError:
        print("❌ pyperclip not installed. Run: pip install pyperclip")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
