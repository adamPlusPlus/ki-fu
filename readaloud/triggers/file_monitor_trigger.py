"""
File Monitor Trigger for ReadAloud.

This module provides functionality to monitor files for changes and trigger TTS.
"""

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable, Optional, List


class FileChangeHandler(FileSystemEventHandler):
    """Handle file system events for monitored files."""
    
    def __init__(self, callback: Callable[[str, str], None]):
        """
        Initialize file change handler.
        
        Args:
            callback: Function to call with file path and content
        """
        self.callback = callback
        self.last_modified = {}
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith(('.txt', '.md', '.py', '.js', '.html')):
            # Check if file was actually modified (not just accessed)
            try:
                current_mtime = os.path.getmtime(event.src_path)
                last_mtime = self.last_modified.get(event.src_path, 0)
                
                if current_mtime > last_mtime:
                    self.last_modified[event.src_path] = current_mtime
                    
                    # Read file content and trigger callback
                    try:
                        with open(event.src_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if content.strip():
                            print(f"File changed: {event.src_path}")
                            self.callback(event.src_path, content)
                    except Exception as e:
                        print(f"Error reading file {event.src_path}: {e}")
                        
            except Exception as e:
                print(f"Error handling file change for {event.src_path}: {e}")


class FileMonitorTrigger:
    """Monitor files for changes and trigger TTS."""
    
    def __init__(self, callback: Callable[[str, str], None]):
        """
        Initialize file monitor trigger.
        
        Args:
            callback: Function to call with file path and content
        """
        self.callback = callback
        self.observer = Observer()
        self.handler = FileChangeHandler(callback)
        self.monitored_paths = []
    
    def add_file(self, file_path: str):
        """Add a file to monitor."""
        if os.path.exists(file_path):
            self.monitored_paths.append(file_path)
            directory = os.path.dirname(file_path)
            self.observer.schedule(self.handler, directory, recursive=False)
            print(f"Monitoring file: {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    def add_directory(self, directory_path: str, recursive: bool = True):
        """Add a directory to monitor."""
        if os.path.exists(directory_path):
            self.observer.schedule(self.handler, directory_path, recursive=recursive)
            print(f"Monitoring directory: {directory_path}")
        else:
            print(f"Directory not found: {directory_path}")
    
    def start_monitoring(self):
        """Start monitoring files and directories."""
        if self.monitored_paths:
            self.observer.start()
            print("File monitoring started. Press Ctrl+C to stop.")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop_monitoring()
        else:
            print("No files or directories to monitor.")
    
    def stop_monitoring(self):
        """Stop monitoring files and directories."""
        self.observer.stop()
        self.observer.join()
        print("File monitoring stopped.")
    
    def read_file(self, file_path: str):
        """Read a file immediately and trigger callback."""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content.strip():
                    self.callback(file_path, content)
                    return content
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")
        
        return None
