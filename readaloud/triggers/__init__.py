"""
Trigger mechanisms for ReadAloud.

This package contains various ways to trigger text-to-speech synthesis.
"""

from .clipboard_trigger import ClipboardTrigger
from .file_monitor_trigger import FileMonitorTrigger
from .hotkey_trigger import HotkeyTrigger
from .text_input_trigger import TextInputTrigger

__all__ = [
    'ClipboardTrigger',
    'FileMonitorTrigger', 
    'HotkeyTrigger',
    'TextInputTrigger'
]
