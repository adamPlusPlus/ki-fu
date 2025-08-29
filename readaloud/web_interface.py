#!/usr/bin/env python3
"""
ReadAloud Web Interface
A beautiful dark mode web interface for controlling TTS settings
"""
import os
import sys
import json
import threading
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
import webbrowser

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Global configuration
config_file = 'readaloud_config.json'
current_config = {}

def load_config():
    """Load configuration from file"""
    global current_config
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                current_config = json.load(f)
        else:
            current_config = {
                'tts_engine': 'higgs_audio',
                'voice': 'default',
                'temperature': 0.3,
                'volume': 0.8,
                'speed': 1.0,
                'audio_output_path': './audio_output'
            }
    except Exception as e:
        print(f"Error loading config: {e}")
        current_config = {}

def save_config():
    """Save configuration to file"""
    try:
        with open(config_file, 'w') as f:
            json.dump(current_config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def get_available_voices():
    """Get list of available voices"""
    return [
        {'id': 'default', 'name': 'Default Voice', 'description': 'Standard voice'},
        {'id': 'male', 'name': 'Male Voice', 'description': 'Deep male voice'},
        {'id': 'female', 'name': 'Female Voice', 'description': 'Clear female voice'},
        {'id': 'narrator', 'name': 'Narrator', 'description': 'Professional narrator voice'},
        {'id': 'casual', 'name': 'Casual', 'description': 'Relaxed, casual voice'}
    ]

def get_available_engines():
    """Get list of available TTS engines"""
    return [
        {'id': 'higgs_audio', 'name': 'Higgs Audio', 'description': 'High-quality AI voice synthesis'},
        {'id': 'coqui', 'name': 'Coqui TTS', 'description': 'Fast, lightweight TTS'},
        {'id': 'system', 'name': 'System TTS', 'description': 'Built-in system voice'}
    ]

@app.route('/')
def index():
    """Main page"""
    load_config()
    return render_template('index.html', 
                         config=current_config,
                         voices=get_available_voices(),
                         engines=get_available_engines())

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API endpoint for configuration"""
    global current_config
    
    if request.method == 'POST':
        data = request.get_json()
        if data:
            # Update configuration
            for key, value in data.items():
                if key in current_config:
                    current_config[key] = value
            
            # Save to file
            if save_config():
                return jsonify({'status': 'success', 'message': 'Configuration saved'})
            else:
                return jsonify({'status': 'error', 'message': 'Failed to save configuration'}), 500
    
    return jsonify(current_config)

@app.route('/api/tts', methods=['POST'])
def api_tts():
    """API endpoint for TTS operations"""
    data = request.get_json()
    action = data.get('action')
    text = data.get('text', '')
    
    try:
        if action == 'test':
            # Simple test - just return success for now
            # In a real implementation, this would call the TTS engine
            return jsonify({
                'status': 'success', 
                'message': f'Test TTS request received: "{text[:50]}..."'
            })
        
        elif action == 'read_clipboard':
            # Read clipboard content
            import pyperclip
            clipboard_text = pyperclip.paste()
            if clipboard_text.strip():
                return jsonify({
                    'status': 'success',
                    'message': f'Reading clipboard: "{clipboard_text[:100]}..."',
                    'text': clipboard_text
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Clipboard is empty'
                }), 400
        
        elif action == 'stop':
            # Stop current audio
            return jsonify({
                'status': 'success',
                'message': 'Audio stopped'
            })
        
        else:
            return jsonify({
                'status': 'error',
                'message': f'Unknown action: {action}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    try:
        # Check if Higgs Audio is available
        higgs_path = current_config.get('higgs_config', {}).get('model_path', '')
        higgs_available = os.path.exists(higgs_path) if higgs_path else False
        
        return jsonify({
            'status': 'success',
            'higgs_audio': higgs_available,
            'config_loaded': bool(current_config),
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def create_templates_directory():
    """Create templates directory if it doesn't exist"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    return templates_dir

def create_static_directory():
    """Create static directory if it doesn't exist"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    os.makedirs(static_dir, exist_ok=True)
    return static_dir

def main():
    """Main entry point"""
    # Create necessary directories
    create_templates_directory()
    create_static_directory()
    
    # Load initial configuration
    load_config()
    
    # Open browser automatically
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask app
    print("🌐 Starting ReadAloud Web Interface...")
    print("📱 Opening browser automatically...")
    print("🔧 Interface will be available at: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
