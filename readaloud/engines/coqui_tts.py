"""
Coqui TTS Engine Implementation

This module provides integration with Coqui TTS as a fallback option.
"""

import os
import tempfile
from typing import Optional, Dict, Any, List

from ..tts_engine import TTSEngine


class CoquiTTSEngine(TTSEngine):
    """Coqui TTS engine implementation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.model_name = self.config.get('model_name', 'tts_models/en/ljspeech/tacotron2-DDC')
        super().__init__(config)
    
    def _check_availability(self) -> bool:
        """Check if Coqui TTS is available."""
        try:
            import TTS
            return True
        except ImportError:
            print("Coqui TTS not available. Install with: pip install TTS")
            return False
    
    def synthesize(self, text: str, output_path: Optional[str] = None, 
                  voice: Optional[str] = None, **kwargs) -> str:
        """
        Synthesize text to speech using Coqui TTS.
        
        Args:
            text: Text to synthesize
            output_path: Path to save audio file
            voice: Voice to use (optional)
            **kwargs: Additional parameters
            
        Returns:
            Path to the generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Coqui TTS is not available")
        
        try:
            from TTS.api import TTS
            
            # Prepare output path
            if not output_path:
                output_path = tempfile.mktemp(suffix='.wav')
            
            # Initialize TTS
            tts = TTS(self.model_name)
            
            # Synthesize speech
            tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker=voice if voice else None,
                **kwargs
            )
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Coqui TTS synthesis failed: {e}")
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voices."""
        try:
            from TTS.api import TTS
            tts = TTS(self.model_name)
            return tts.speakers if hasattr(tts, 'speakers') else []
        except:
            return []
    
    def get_engine_info(self) -> Dict[str, str]:
        """Get information about the Coqui TTS engine."""
        return {
            "name": "Coqui TTS",
            "model": self.model_name,
            "available": str(self.is_available),
            "description": "Fast, lightweight TTS engine"
        }
    
    def get_available_models(self) -> List[str]:
        """Get list of available TTS models."""
        try:
            from TTS.api import TTS
            return TTS.list_models()
        except:
            return []
