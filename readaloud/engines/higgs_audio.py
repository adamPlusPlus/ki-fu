"""
Higgs Audio TTS Engine Implementation

This module provides integration with the Higgs Audio TTS engine.
"""

import os
import tempfile
import subprocess
import json
from typing import Optional, Dict, Any, List
from pathlib import Path

from ..tts_engine import TTSEngine


class HiggsAudioEngine(TTSEngine):
    """Higgs Audio TTS engine implementation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.model_path = self.config.get('model_path', '')
        self.python_path = self.config.get('python_path', 'python')
        self.higgs_script = self.config.get('higgs_script', 'examples/generation.py')
        super().__init__(config)
    
    def _check_availability(self) -> bool:
        """Check if Higgs Audio is available."""
        try:
            # Check if the Higgs Audio repository exists
            if not self.model_path:
                # Try to find it in common locations
                possible_paths = [
                    os.path.expanduser("~/higgs-audio"),
                    "./higgs-audio",
                    "../higgs-audio"
                ]
                
                for path in possible_paths:
                    if os.path.exists(os.path.join(path, "examples", "generation.py")):
                        self.model_path = path
                        break
            
            if not self.model_path or not os.path.exists(self.model_path):
                print("Higgs Audio repository not found. Please set model_path in config.")
                return False
            
            # Check if the generation script exists
            script_path = os.path.join(self.model_path, self.higgs_script)
            if not os.path.exists(script_path):
                print(f"Higgs Audio generation script not found at: {script_path}")
                return False
            
            # Check if Python dependencies are available
            try:
                result = subprocess.run(
                    [self.python_path, "-c", "import torch, transformers"],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print("Required Python packages not available. Please install torch and transformers.")
                    return False
            except FileNotFoundError:
                print(f"Python interpreter not found at: {self.python_path}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error checking Higgs Audio availability: {e}")
            return False
    
    def synthesize(self, text: str, output_path: Optional[str] = None, 
                  voice: Optional[str] = None, **kwargs) -> str:
        """
        Synthesize text to speech using Higgs Audio.
        
        Args:
            text: Text to synthesize
            output_path: Path to save audio file
            voice: Voice reference audio file (optional)
            **kwargs: Additional parameters (temperature, seed, etc.)
            
        Returns:
            Path to the generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Higgs Audio is not available")
        
        # Prepare output path
        if not output_path:
            output_path = tempfile.mktemp(suffix='.wav')
        
        # Prepare command arguments
        cmd = [
            self.python_path,
            os.path.join(self.model_path, self.higgs_script),
            "--transcript", text,
            "--out_path", output_path
        ]
        
        # Add optional parameters
        if voice and os.path.exists(voice):
            cmd.extend(["--ref_audio", voice])
        
        # Add other parameters from kwargs
        if 'temperature' in kwargs:
            cmd.extend(["--temperature", str(kwargs['temperature'])])
        if 'seed' in kwargs:
            cmd.extend(["--seed", str(kwargs['seed'])])
        
        try:
            # Run Higgs Audio generation
            result = subprocess.run(
                cmd,
                cwd=self.model_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Check if output file was created
            if os.path.exists(output_path):
                return output_path
            else:
                raise RuntimeError("Audio file was not generated")
                
        except subprocess.CalledProcessError as e:
            print(f"Higgs Audio generation failed: {e}")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
            raise RuntimeError(f"Higgs Audio generation failed: {e}")
    
    def get_available_voices(self) -> List[str]:
        """Get list of available reference voices."""
        voices = []
        
        # Look for reference audio files in common locations
        ref_dirs = [
            os.path.join(self.model_path, "examples", "ref_audio"),
            os.path.join(self.model_path, "ref_audio"),
            "./ref_audio"
        ]
        
        for ref_dir in ref_dirs:
            if os.path.exists(ref_dir):
                for file in os.listdir(ref_dir):
                    if file.lower().endswith(('.wav', '.mp3', '.flac')):
                        voices.append(os.path.join(ref_dir, file))
        
        return voices
    
    def get_engine_info(self) -> Dict[str, str]:
        """Get information about the Higgs Audio engine."""
        return {
            "name": "Higgs Audio",
            "version": "v2",
            "model_path": self.model_path,
            "available": str(self.is_available),
            "description": "High-quality, expressive speech synthesis from Boson AI"
        }
    
    def install_instructions(self) -> str:
        """Get installation instructions for Higgs Audio."""
        return """
        To install Higgs Audio:
        
        1. Clone the repository:
           git clone https://github.com/boson-ai/higgs-audio.git
        
        2. Install dependencies:
           pip install -r requirements.txt
        
        3. Download models (if required)
        
        4. Set the model_path in your configuration
        """
