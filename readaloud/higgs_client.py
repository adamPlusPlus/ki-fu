#!/usr/bin/env python3
"""
Higgs Audio Client
Communicates with the persistent service for fast TTS generation
"""

import os
import sys
import json
import time
import subprocess
import pyperclip

def call_higgs_service(text):
    """Call the Higgs Audio service"""
    try:
        # Check if service is running
        service_script = os.path.join(os.path.dirname(__file__), "higgs_service.py")
        
        # For now, we'll just call the service directly
        # In a real implementation, this would use IPC or HTTP
        print("🎵 Calling Higgs Audio Service...")
        
        # Generate unique filename
        import uuid
        output_filename = f"output_{uuid.uuid4().hex[:8]}.wav"
        output_path = os.path.join("audio_output", output_filename)
        
        # Call the service
        cmd = [
            sys.executable,
            service_script,
            "--text", text,
            "--output", output_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60  # Much shorter timeout since model should be loaded
        )
        
        if result.returncode == 0 and os.path.exists(output_path):
            print(f"✅ TTS generated: {output_path}")
            return {"success": True, "audio_file": output_path}
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return {"success": False, "error": f"Service call failed: {error_msg}"}
            
    except Exception as e:
        return {"success": False, "error": f"Service error: {str(e)}"}

def main():
    """Main client entry point"""
    print("📋 Higgs Audio Client")
    print("=" * 30)
    
    # Get clipboard content
    try:
        clipboard_text = pyperclip.paste()
        if not clipboard_text.strip():
            print("❌ Clipboard is empty")
            return
        
        print(f"📋 Clipboard content: {clipboard_text[:100]}...")
        print()
        
        # Call service
        result = call_higgs_service(clipboard_text)
        
        if result['success']:
            print("✅ TTS completed successfully!")
            
            # Play the audio
            audio_file = result['audio_file']
            if os.name == 'nt':  # Windows
                os.startfile(audio_file)
                print(f"🔊 Playing: {audio_file}")
            else:
                print(f"🎵 Audio saved: {audio_file}")
        else:
            print(f"❌ TTS failed: {result['error']}")
            
    except ImportError:
        print("❌ pyperclip not installed. Run: pip install pyperclip")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
