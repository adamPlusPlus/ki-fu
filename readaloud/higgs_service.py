#!/usr/bin/env python3
"""
Persistent Higgs Audio Service
Keeps the model loaded in memory for fast TTS generation
"""

import os
import sys
import json
import time
import threading
import subprocess
import tempfile
from pathlib import Path

class HiggsAudioService:
    def __init__(self):
        self.model_path = "H:/AI/higgs/higgs-audio"
        self.python_path = "python"
        self.script_path = "examples/generation.py"
        self.output_dir = "C:/Project/ki-fu/readaloud/audio_output"
        self.temperature = 0.3
        self.is_ready = False
        self.processing = False
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
    def start_service(self):
        """Start the persistent service"""
        print("🚀 Starting Higgs Audio Service...")
        print(f"   Model path: {self.model_path}")
        print(f"   Output dir: {self.output_dir}")
        
        # Start model loading in background
        threading.Thread(target=self._load_model, daemon=True).start()
        
    def _load_model(self):
        """Load the model in background"""
        try:
            print("📥 Loading model into memory...")
            
            # Test model loading with a simple command
            test_cmd = [
                self.python_path,
                os.path.join(self.model_path, self.script_path),
                "--transcript", "Test",
                "--out_path", os.path.join(self.output_dir, "test_load.wav"),
                "--temperature", str(self.temperature)
            ]
            
            print("   Running initial model load...")
            result = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                cwd=self.model_path,
                timeout=300  # 5 minutes for initial load
            )
            
            if result.returncode == 0:
                print("✅ Model loaded successfully!")
                self.is_ready = True
                
                # Clean up test file
                test_file = os.path.join(self.output_dir, "test_load.wav")
                if os.path.exists(test_file):
                    os.remove(test_file)
            else:
                print(f"❌ Model loading failed: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
    
    def generate_tts(self, text, output_filename=None):
        """Generate TTS audio"""
        if not self.is_ready:
            return {"success": False, "error": "Model not ready yet"}
        
        if self.processing:
            return {"success": False, "error": "Already processing another request"}
        
        try:
            self.processing = True
            
            if not output_filename:
                import uuid
                output_filename = f"output_{uuid.uuid4().hex[:8]}.wav"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            print(f"🎵 Generating TTS for: {text[:50]}...")
            
            cmd = [
                self.python_path,
                os.path.join(self.model_path, self.script_path),
                "--transcript", text,
                "--out_path", output_path,
                "--temperature", str(self.temperature)
            ]
            
            # Run generation (should be much faster now)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.model_path,
                timeout=120  # 2 minutes should be enough for loaded model
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ TTS generated: {output_path}")
                return {"success": True, "audio_file": output_path}
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                return {"success": False, "error": f"Generation failed: {error_msg}"}
                
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Generation timed out"}
        except Exception as e:
            return {"success": False, "error": f"Generation error: {str(e)}"}
        finally:
            self.processing = False
    
    def get_status(self):
        """Get service status"""
        return {
            "ready": self.is_ready,
            "processing": self.processing,
            "model_path": self.model_path,
            "output_dir": self.output_dir
        }

def main():
    """Main service entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Higgs Audio Service')
    parser.add_argument('--text', help='Text to synthesize')
    parser.add_argument('--output', help='Output audio file path')
    parser.add_argument('--service', action='store_true', help='Run as persistent service')
    
    args = parser.parse_args()
    
    if args.service:
        # Run as persistent service
        print("🎯 Higgs Audio Persistent Service")
        print("=" * 40)
        
        service = HiggsAudioService()
        service.start_service()
        
        # Keep service running
        try:
            while True:
                time.sleep(1)
                if service.is_ready:
                    print("   Service ready - waiting for requests...", end='\r')
        except KeyboardInterrupt:
            print("\n\n🛑 Service stopped by user")
    else:
        # Run single TTS request
        if not args.text or not args.output:
            print("Usage: python higgs_service.py --text 'Hello world' --output 'output.wav'")
            return
        
        service = HiggsAudioService()
        service.start_service()
        
        # Wait for service to be ready
        print("⏳ Waiting for service to be ready...")
        while not service.is_ready:
            time.sleep(1)
        
        # Generate TTS
        result = service.generate_tts(args.text, os.path.basename(args.output))
        
        if result['success']:
            print(f"✅ TTS generated: {result['audio_file']}")
            sys.exit(0)
        else:
            print(f"❌ TTS failed: {result['error']}")
            sys.exit(1)

if __name__ == "__main__":
    main()
