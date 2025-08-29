#!/usr/bin/env python3
"""
ReadAloud GUI Interface

A simple graphical interface for the ReadAloud TTS tool.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ReadAloud
from config import Config


class ReadAloudGUI:
    """Graphical user interface for ReadAloud."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("ReadAloud - Text-to-Speech Tool")
        self.root.geometry("800x600")
        
        # Initialize ReadAloud
        self.config = Config()
        self.app = None
        self.message_queue = queue.Queue()
        
        # Setup GUI
        self.setup_gui()
        self.setup_readaloud()
        
        # Start message processing
        self.process_messages()
    
    def setup_gui(self):
        """Setup the graphical interface."""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ReadAloud TTS Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # TTS Engine selection
        ttk.Label(main_frame, text="TTS Engine:").grid(row=1, column=0, sticky=tk.W)
        self.engine_var = tk.StringVar(value=self.config.get('tts_engine', 'auto'))
        engine_combo = ttk.Combobox(main_frame, textvariable=self.engine_var, 
                                   values=['auto', 'higgs_audio', 'coqui'], 
                                   state='readonly', width=15)
        engine_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Voice selection
        ttk.Label(main_frame, text="Voice:").grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        self.voice_var = tk.StringVar(value=self.config.get('voice', 'default'))
        voice_combo = ttk.Combobox(main_frame, textvariable=self.voice_var, 
                                  values=['default'], width=15)
        voice_combo.grid(row=1, column=3, sticky=tk.W, padx=(10, 0))
        
        # Text input area
        ttk.Label(main_frame, text="Text to Read:").grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        
        self.text_input = scrolledtext.ScrolledText(main_frame, height=8, width=80)
        self.text_input.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=(0, 20))
        
        # Read button
        read_button = ttk.Button(button_frame, text="Read Text", 
                                command=self.read_text, style="Accent.TButton")
        read_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        stop_button = ttk.Button(button_frame, text="Stop Audio", 
                                command=self.stop_audio)
        stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # File operations frame
        file_frame = ttk.LabelFrame(main_frame, text="File Operations", padding="10")
        file_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Open file button
        open_file_button = ttk.Button(file_frame, text="Open File", 
                                     command=self.open_file)
        open_file_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Monitor file button
        monitor_file_button = ttk.Button(file_frame, text="Monitor File", 
                                        command=self.monitor_file)
        monitor_file_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clipboard button
        clipboard_button = ttk.Button(file_frame, text="Read Clipboard", 
                                     command=self.read_clipboard)
        clipboard_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Hotkeys button
        hotkeys_button = ttk.Button(file_frame, text="Enable Hotkeys", 
                                    command=self.toggle_hotkeys)
        hotkeys_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=7, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure log frame grid weights
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def setup_readaloud(self):
        """Setup the ReadAloud application."""
        try:
            config = {
                'tts_engine': self.engine_var.get(),
                'voice': self.voice_var.get(),
                'temperature': self.config.get('temperature', 0.3),
                'seed': self.config.get('seed')
            }
            
            self.app = ReadAloud(config)
            self.log("ReadAloud initialized successfully")
            
            # Update voice list
            self.update_voice_list()
            
        except Exception as e:
            self.log(f"Error initializing ReadAloud: {e}")
            messagebox.showerror("Error", f"Failed to initialize ReadAloud: {e}")
    
    def update_voice_list(self):
        """Update the list of available voices."""
        if self.app and self.app.tts_engine:
            try:
                voices = self.app.tts_engine.get_available_voices()
                if voices:
                    self.voice_var.set(voices[0])
                    # Update combobox values
                    for widget in self.root.winfo_children():
                        if isinstance(widget, ttk.Frame):
                            for child in widget.winfo_children():
                                if isinstance(child, ttk.Combobox) and child.cget('textvariable') == self.voice_var:
                                    child['values'] = voices
                                    break
            except Exception as e:
                self.log(f"Error updating voice list: {e}")
    
    def read_text(self):
        """Read the text from the input area."""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to read.")
            return
        
        self.status_var.set("Reading text...")
        self.log(f"Reading text: {text[:50]}...")
        
        # Run TTS in a separate thread
        thread = threading.Thread(target=self._read_text_thread, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _read_text_thread(self, text):
        """Read text in a separate thread."""
        try:
            self.app._handle_text(text)
            self.message_queue.put(("status", "Ready"))
            self.message_queue.put(("log", "Text reading completed"))
        except Exception as e:
            self.message_queue.put(("status", "Error")
            self.message_queue.put(("log", f"Error reading text: {e}"))
    
    def stop_audio(self):
        """Stop current audio playback."""
        if self.app:
            self.app.stop_audio()
            self.status_var.set("Audio stopped")
            self.log("Audio playback stopped")
    
    def open_file(self):
        """Open and read a file."""
        file_path = filedialog.askopenfilename(
            title="Select file to read",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", content)
                
                self.status_var.set(f"File loaded: {os.path.basename(file_path)}")
                self.log(f"File loaded: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")
    
    def monitor_file(self):
        """Start monitoring a file for changes."""
        file_path = filedialog.askopenfilename(
            title="Select file to monitor",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.status_var.set(f"Monitoring: {os.path.basename(file_path)}")
            self.log(f"Starting file monitoring: {file_path}")
            
            # Start monitoring in a separate thread
            thread = threading.Thread(target=self._monitor_file_thread, args=(file_path,))
            thread.daemon = True
            thread.start()
    
    def _monitor_file_thread(self, file_path):
        """Monitor file in a separate thread."""
        try:
            self.app.start_file_monitoring(file_path)
        except Exception as e:
            self.message_queue.put(("log", f"Error monitoring file: {e}"))
    
    def read_clipboard(self):
        """Read clipboard content."""
        self.status_var.set("Reading clipboard...")
        self.log("Reading clipboard content...")
        
        # Run in a separate thread
        thread = threading.Thread(target=self._read_clipboard_thread)
        thread.daemon = True
        thread.start()
    
    def _read_clipboard_thread(self):
        """Read clipboard in a separate thread."""
        try:
            self.app.read_clipboard()
            self.message_queue.put(("status", "Ready"))
        except Exception as e:
            self.message_queue.put(("status", "Error")
            self.message_queue.put(("log", f"Error reading clipboard: {e}"))
    
    def toggle_hotkeys(self):
        """Toggle global hotkeys."""
        if not hasattr(self, 'hotkeys_active'):
            self.hotkeys_active = False
        
        if not self.hotkeys_active:
            self.status_var.set("Enabling hotkeys...")
            self.log("Enabling global hotkeys...")
            
            # Start hotkeys in a separate thread
            thread = threading.Thread(target=self._start_hotkeys_thread)
            thread.daemon = True
            thread.start()
            
            self.hotkeys_active = True
        else:
            self.status_var.set("Disabling hotkeys...")
            self.log("Disabling global hotkeys...")
            
            if self.app:
                self.app.triggers['hotkeys'].stop_monitoring()
            
            self.hotkeys_active = False
            self.status_var.set("Hotkeys disabled")
    
    def _start_hotkeys_thread(self):
        """Start hotkeys in a separate thread."""
        try:
            self.app.start_hotkey_monitoring()
        except Exception as e:
            self.message_queue.put(("log", f"Error starting hotkeys: {e}"))
    
    def log(self, message):
        """Add a message to the log."""
        self.message_queue.put(("log", message))
    
    def process_messages(self):
        """Process messages from the message queue."""
        try:
            while True:
                msg_type, message = self.message_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_var.set(message)
                elif msg_type == "log":
                    self.log_text.insert(tk.END, f"{message}\n")
                    self.log_text.see(tk.END)
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_messages)


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = ReadAloudGUI(root)
    
    # Handle window close
    def on_closing():
        if hasattr(app, 'app') and app.app:
            # Stop any running operations
            for trigger in app.app.triggers.values():
                if hasattr(trigger, 'stop_monitoring'):
                    trigger.stop_monitoring()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
