#!/usr/bin/env python3
"""
Background Service Manager for ReadAloud

This module provides a background service that can run ReadAloud without user interaction.
"""

import os
import sys
import time
import threading
import signal
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ReadAloud
from config import Config


class BackgroundService:
    """Background service for ReadAloud TTS."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the background service."""
        self.config = Config(config_path)
        self.app = None
        self.running = False
        self.monitored_files = {}
        self.service_threads = {}
        
        # Setup logging
        self._setup_logging()
        
        # Setup signal handlers
        self._setup_signal_handlers()
        
        # Initialize ReadAloud
        self._setup_readaloud()
    
    def _setup_logging(self):
        """Setup logging for the background service."""
        log_dir = Path("./logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "readaloud_background.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("ReadAloudBackground")
        self.logger.info("Background service logging initialized")
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        if hasattr(signal, 'SIGBREAK'):  # Windows
            signal.signal(signal.SIGBREAK, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def _setup_readaloud(self):
        """Setup ReadAloud application for background operation."""
        try:
            config = {
                'tts_engine': self.config.get('tts_engine', 'auto'),
                'voice': self.config.get('voice', 'default'),
                'temperature': self.config.get('temperature', 0.3),
                'seed': self.config.get('seed'),
                'background_mode': True
            }
            
            self.app = ReadAloud(config)
            self.logger.info("ReadAloud initialized for background operation")
            
        except Exception as e:
            self.logger.error(f"Error initializing ReadAloud: {e}")
            raise
    
    def start(self):
        """Start the background service."""
        if self.running:
            self.logger.warning("Service is already running")
            return
        
        self.logger.info("Starting ReadAloud background service...")
        self.running = True
        
        # Start background monitoring
        self._start_background_monitoring()
        
        # Start file monitoring if configured
        self._start_file_monitoring()
        
        # Start clipboard monitoring
        self._start_clipboard_monitoring()
        
        self.logger.info("Background service started successfully")
    
    def stop(self):
        """Stop the background service."""
        if not self.running:
            return
        
        self.logger.info("Stopping background service...")
        self.running = False
        
        # Stop all monitoring threads
        for name, thread in self.service_threads.items():
            if thread.is_alive():
                self.logger.info(f"Stopping {name} thread...")
                # Signal threads to stop (they should check self.running)
        
        # Stop ReadAloud
        if self.app:
            for trigger in self.app.triggers.values():
                if hasattr(trigger, 'stop_monitoring'):
                    trigger.stop_monitoring()
        
        self.logger.info("Background service stopped")
    
    def _start_background_monitoring(self):
        """Start background monitoring threads."""
        # Start a main monitoring thread
        monitor_thread = threading.Thread(
            target=self._background_monitor_loop,
            name="BackgroundMonitor",
            daemon=True
        )
        monitor_thread.start()
        self.service_threads['background_monitor'] = monitor_thread
        
        self.logger.info("Background monitoring started")
    
    def _background_monitor_loop(self):
        """Main background monitoring loop."""
        while self.running:
            try:
                # Check system status
                self._check_system_status()
                
                # Process any pending tasks
                self._process_pending_tasks()
                
                # Sleep for a bit
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error in background monitor loop: {e}")
                time.sleep(30)  # Wait longer on error
    
    def _start_file_monitoring(self):
        """Start file monitoring for configured files."""
        monitored_files = self.config.get('monitored_files', [])
        
        if not monitored_files:
            self.logger.info("No files configured for monitoring")
            return
        
        for file_path in monitored_files:
            if os.path.exists(file_path):
                self.add_file_monitoring(file_path)
            else:
                self.logger.warning(f"Monitored file not found: {file_path}")
    
    def add_file_monitoring(self, file_path: str):
        """Add a file to monitoring."""
        if file_path in self.monitored_files:
            self.logger.info(f"File already being monitored: {file_path}")
            return
        
        try:
            self.app.start_file_monitoring(file_path)
            self.monitored_files[file_path] = {
                'added_time': time.time(),
                'last_modified': os.path.getmtime(file_path) if os.path.exists(file_path) else 0
            }
            self.logger.info(f"Added file monitoring: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error adding file monitoring for {file_path}: {e}")
    
    def remove_file_monitoring(self, file_path: str):
        """Remove a file from monitoring."""
        if file_path not in self.monitored_files:
            return
        
        try:
            # Stop monitoring this specific file
            # This would need to be implemented in the FileMonitorTrigger
            del self.monitored_files[file_path]
            self.logger.info(f"Removed file monitoring: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error removing file monitoring for {file_path}: {e}")
    
    def _start_clipboard_monitoring(self):
        """Start clipboard monitoring in background."""
        try:
            clipboard_thread = threading.Thread(
                target=self._clipboard_monitor_loop,
                name="ClipboardMonitor",
                daemon=True
            )
            clipboard_thread.start()
            self.service_threads['clipboard_monitor'] = clipboard_thread
            
            self.logger.info("Clipboard monitoring started")
            
        except Exception as e:
            self.logger.error(f"Error starting clipboard monitoring: {e}")
    
    def _clipboard_monitor_loop(self):
        """Clipboard monitoring loop."""
        import pyperclip
        
        last_content = pyperclip.paste()
        
        while self.running:
            try:
                current_content = pyperclip.paste()
                
                if current_content != last_content and current_content.strip():
                    self.logger.info(f"Clipboard content changed, length: {len(current_content)}")
                    
                    # Process clipboard content
                    self._process_clipboard_content(current_content)
                    
                    last_content = current_content
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                self.logger.error(f"Error in clipboard monitor loop: {e}")
                time.sleep(5)
    
    def _process_clipboard_content(self, content: str):
        """Process clipboard content."""
        try:
            # Check if content is suitable for TTS
            if len(content) > 1000:
                self.logger.info("Clipboard content too long, truncating")
                content = content[:1000] + "..."
            
            # Generate and play audio
            if self.app and self.app.tts_engine:
                self.logger.info("Generating TTS for clipboard content")
                self.app._handle_text(content)
            else:
                self.logger.warning("TTS engine not available")
                
        except Exception as e:
            self.logger.error(f"Error processing clipboard content: {e}")
    
    def _check_system_status(self):
        """Check system status and health."""
        try:
            # Check disk space
            disk_usage = self._check_disk_space()
            if disk_usage > 90:  # 90% full
                self.logger.warning(f"Disk usage high: {disk_usage}%")
            
            # Check memory usage
            memory_usage = self._check_memory_usage()
            if memory_usage > 80:  # 80% full
                self.logger.warning(f"Memory usage high: {memory_usage}%")
            
            # Check TTS engine status
            if self.app and self.app.tts_engine:
                if not self.app.tts_engine.is_available:
                    self.logger.error("TTS engine became unavailable")
            
        except Exception as e:
            self.logger.error(f"Error checking system status: {e}")
    
    def _check_disk_space(self) -> float:
        """Check disk space usage."""
        try:
            import psutil
            disk = psutil.disk_usage('.')
            return (disk.used / disk.total) * 100
        except ImportError:
            return 0.0
    
    def _check_memory_usage(self) -> float:
        """Check memory usage."""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return memory.percent
        except ImportError:
            return 0.0
    
    def _process_pending_tasks(self):
        """Process any pending background tasks."""
        # This could include:
        # - Cleaning up old audio files
        # - Processing queued TTS requests
        # - Updating file monitoring status
        # - Sending status updates
        
        try:
            # Clean up old audio files
            self._cleanup_old_audio_files()
            
        except Exception as e:
            self.logger.error(f"Error processing pending tasks: {e}")
    
    def _cleanup_old_audio_files(self):
        """Clean up old audio files."""
        try:
            audio_dir = Path("./audio_output")
            if not audio_dir.exists():
                return
            
            current_time = time.time()
            max_age = 3600  # 1 hour
            
            for audio_file in audio_dir.glob("*.wav"):
                if current_time - audio_file.stat().st_mtime > max_age:
                    audio_file.unlink()
                    self.logger.debug(f"Cleaned up old audio file: {audio_file}")
                    
        except Exception as e:
            self.logger.error(f"Error cleaning up audio files: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current service status."""
        return {
            'running': self.running,
            'monitored_files': list(self.monitored_files.keys()),
            'threads': {name: thread.is_alive() for name, thread in self.service_threads.items()},
            'tts_engine_available': self.app.tts_engine.is_available if self.app else False,
            'uptime': time.time() - getattr(self, '_start_time', time.time())
        }
    
    def run(self):
        """Run the background service."""
        try:
            self.start()
            self._start_time = time.time()
            
            # Keep the service running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt")
        finally:
            self.stop()


def main():
    """Main entry point for background service."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ReadAloud Background Service")
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--pid-file', help='PID file path')
    
    args = parser.parse_args()
    
    # Create service
    service = BackgroundService(args.config)
    
    if args.daemon:
        # Run as daemon
        import daemon
        import daemon.pidfile
        
        pid_file = args.pid_file or "./readaloud.pid"
        
        with daemon.DaemonContext(
            pidfile=daemon.pidfile.PIDLockFile(pid_file),
            working_directory='.',
            umask=0o002
        ):
            service.run()
    else:
        # Run in foreground
        service.run()


if __name__ == "__main__":
    main()
