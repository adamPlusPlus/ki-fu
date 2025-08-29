"""
Abstract TTS Engine Interface

This module defines the base class that all TTS engines must implement.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import os
import tempfile
import subprocess
import platform


class TTSEngine(ABC):
    """Abstract base class for TTS engines."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.is_available = self._check_availability()
    
    @abstractmethod
    def _check_availability(self) -> bool:
        """Check if the TTS engine is available on the system."""
        pass
    
    @abstractmethod
    def synthesize(self, text: str, output_path: Optional[str] = None, 
                  voice: Optional[str] = None, **kwargs) -> str:
        """
        Synthesize text to speech.
        
        Args:
            text: Text to synthesize
            output_path: Path to save audio file (optional)
            voice: Voice to use (optional)
            **kwargs: Additional engine-specific parameters
            
        Returns:
            Path to the generated audio file
        """
        pass
    
    @abstractmethod
    def get_available_voices(self) -> list:
        """Get list of available voices."""
        pass
    
    @abstractmethod
    def get_engine_info(self) -> Dict[str, str]:
        """Get information about the TTS engine."""
        pass


class AudioPlayer:
    """Cross-platform audio player for TTS output."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self._setup_player()
    
    def _setup_player(self):
        """Setup audio player based on operating system."""
        if self.system == "windows":
            self.player_cmd = ["start", "/min", "wmplayer"]
        elif self.system == "darwin":  # macOS
            self.player_cmd = ["afplay"]
        else:  # Linux
            self.player_cmd = ["aplay"]
    
    def play(self, audio_file: str):
        """Play an audio file."""
        try:
            if self.system == "windows":
                subprocess.run(["start", audio_file], shell=True, check=True)
            elif self.system == "darwin":
                subprocess.run([*self.player_cmd, audio_file], check=True)
            else:
                subprocess.run([*self.player_cmd, audio_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error playing audio: {e}")
    
    def stop(self):
        """Stop current audio playback."""
        # This is a basic implementation - could be enhanced with process management
        if self.system == "darwin":
            subprocess.run(["pkill", "-f", "afplay"], check=False)
        elif self.system == "linux":
            subprocess.run(["pkill", "-f", "aplay"], check=False)
        # Windows doesn't have a simple way to stop wmplayer from command line
