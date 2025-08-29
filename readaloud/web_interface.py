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

# Global Higgs service instance
higgs_service = None
higgs_service_thread = None

def load_config():
    """Load configuration from file"""
    global current_config
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                current_config = json.load(f)
        else:
            current_config = {}
        
        # Ensure all required config keys exist with defaults
        defaults = {
            'tts_engine': 'higgs_audio',
            'voice': 'default',
            'temperature': 0.3,
            'volume': 0.8,
            'speed': 1.0,
            'audio_output_path': './audio_output'
        }
        
        # Merge existing config with defaults
        for key, default_value in defaults.items():
            if key not in current_config:
                current_config[key] = default_value
                
    except Exception as e:
        print(f"Error loading config: {e}")
        current_config = {
            'tts_engine': 'higgs_audio',
            'voice': 'default',
            'temperature': 0.3,
            'volume': 0.8,
            'speed': 1.0,
            'audio_output_path': './audio_output'
        }

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
            # Actually call the TTS engine
            try:
                result = _call_tts_engine(text)
                if result['success']:
                    return jsonify({
                        'status': 'success', 
                        'message': f'Text synthesized and playing: "{text[:50]}..."',
                        'audio_file': result.get('audio_file', '')
                    })
                else:
                    return jsonify({
                        'status': 'error',
                        'message': f'TTS failed: {result["error"]}'
                    }), 500
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': f'TTS error: {str(e)}'
                }), 500
        
        elif action == 'read_clipboard':
            # Read clipboard content and synthesize it
            try:
                import pyperclip
                clipboard_text = pyperclip.paste()
                if clipboard_text.strip():
                    # Call TTS engine with clipboard text
                    result = _call_tts_engine(clipboard_text)
                    if result['success']:
                        return jsonify({
                            'status': 'success',
                            'message': f'Clipboard text synthesized and playing: "{clipboard_text[:100]}..."',
                            'text': clipboard_text,
                            'audio_file': result.get('audio_file', '')
                        })
                    else:
                        return jsonify({
                            'status': 'error',
                            'message': f'Clipboard TTS failed: {result["error"]}'
                        }), 500
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Clipboard is empty'
                    }), 400
            except ImportError:
                return jsonify({
                    'status': 'error',
                    'message': 'pyperclip not installed. Run: pip install pyperclip'
                }), 500
        
        elif action == 'read_selection':
            # Read selected text aloud (simulates Ctrl+C then reads clipboard)
            try:
                import pyperclip
                import keyboard
                import time
                
                # Store current clipboard
                original_clipboard = pyperclip.paste()
                
                # Simulate Ctrl+C to copy selection
                keyboard.press_and_release('ctrl+c')
                time.sleep(0.2)  # Wait for copy to complete
                
                # Get the new clipboard content
                new_clipboard_text = pyperclip.paste()
                
                if new_clipboard_text.strip() and new_clipboard_text != original_clipboard:
                    # Call TTS engine with selected text
                    result = _call_tts_engine(new_clipboard_text)
                    if result['success']:
                        return jsonify({
                            'status': 'success',
                            'message': f'Selected text synthesized and playing: "{new_clipboard_text[:100]}..."',
                            'text': new_clipboard_text,
                            'audio_file': result.get('audio_file', '')
                        })
                    else:
                        return jsonify({
                            'status': 'error',
                            'message': f'Selection TTS failed: {result["error"]}'
                        }), 500
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'No text selected or selection failed'
                    }), 400
                    
            except ImportError as e:
                missing_module = 'pyperclip' if 'pyperclip' in str(e) else 'keyboard'
                return jsonify({
                    'status': 'error',
                    'message': f'{missing_module} not installed. Run: pip install {missing_module}'
                }), 500
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Selection reading failed: {str(e)}'
                }), 500
        
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
        
        # Get Higgs service status
        higgs_service_status = get_higgs_service_status()
        
        return jsonify({
            'status': 'success',
            'higgs_audio': higgs_available,
            'config_loaded': bool(current_config),
            'higgs_service': higgs_service_status,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/service/start', methods=['POST'])
def api_start_service():
    """API endpoint to start Higgs Audio service"""
    try:
        success = start_higgs_service()
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Higgs Audio service started successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to start Higgs Audio service'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error starting service: {str(e)}'
        }), 500

@app.route('/api/service/stop', methods=['POST'])
def api_stop_service():
    """API endpoint to stop Higgs Audio service"""
    try:
        stop_higgs_service()
        return jsonify({
            'status': 'success',
            'message': 'Higgs Audio service stopped successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error stopping service: {str(e)}'
        }), 500

@app.route('/api/service/status')
def api_service_status():
    """API endpoint to get service status"""
    try:
        status = get_higgs_service_status()
        return jsonify({
            'status': 'success',
            'service': status
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting service status: {str(e)}'
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

def start_higgs_service():
    """Start the Higgs Audio service in background"""
    global higgs_service, higgs_service_thread
    
    if higgs_service is not None:
        return True  # Already running
    
    try:
        # Import the service class
        from higgs_service import HiggsAudioService
        
        # Create and start service
        higgs_service = HiggsAudioService()
        higgs_service.start_service()
        
        # Start service monitoring in background thread
        def service_monitor():
            while higgs_service and not getattr(higgs_service, '_stop', False):
                time.sleep(1)
        
        higgs_service_thread = threading.Thread(target=service_monitor, daemon=True)
        higgs_service_thread.start()
        
        print("🚀 Higgs Audio service started successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start Higgs service: {str(e)}")
        higgs_service = None
        return False

def stop_higgs_service():
    """Stop the Higgs Audio service"""
    global higgs_service, higgs_service_thread
    
    if higgs_service:
        higgs_service._stop = True
        higgs_service = None
    
    if higgs_service_thread:
        higgs_service_thread.join(timeout=1)
        higgs_service_thread = None
    
    print("🛑 Higgs Audio service stopped")

def get_higgs_service_status():
    """Get the current status of the Higgs service"""
    if higgs_service is None:
        return {
            'running': False,
            'ready': False,
            'processing': False,
            'status': 'Not running'
        }
    
    try:
        status = higgs_service.get_status()
        return {
            'running': True,
            'ready': status.get('ready', False),
            'processing': status.get('processing', False),
            'status': 'Ready' if status.get('ready', False) else 'Loading model...'
        }
    except Exception as e:
        return {
            'running': True,
            'ready': False,
            'processing': False,
            'status': f'Error: {str(e)}'
        }

def _call_tts_engine(text):
    """Call the TTS engine to synthesize text"""
    try:
        # Get the current TTS engine configuration
        engine = current_config.get('tts_engine', 'higgs_audio')
        
        if engine == 'higgs_audio':
            return _call_higgs_audio(text)
        elif engine == 'coqui':
            return _call_coqui_tts(text)
        else:
            return {'success': False, 'error': f'Unknown TTS engine: {engine}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def _call_higgs_audio(text):
    """Call Higgs Audio TTS engine"""
    try:
        # First, try to use the persistent service if available
        if higgs_service and higgs_service.is_ready:
            print("🎵 Using persistent Higgs Audio service...")
            
            # Generate unique filename
            import uuid
            audio_filename = f"output_{uuid.uuid4().hex[:8]}.wav"
            
            # Use the service
            result = higgs_service.generate_tts(text, audio_filename)
            
            if result['success']:
                # Play the audio
                _play_audio(result['audio_file'])
                return result
            else:
                return result
        
        # Fallback to direct script call if service not available
        print("⚠️  Persistent service not available, using direct script...")
        
        # Get Higgs Audio configuration
        higgs_config = current_config.get('higgs_config', {})
        model_path = higgs_config.get('model_path', 'H:/AI/higgs/higgs-audio')
        python_path = higgs_config.get('python_path', 'python')
        script_path = higgs_config.get('higgs_script', 'examples/generation.py')
        
        # Check if Higgs Audio is available
        if not os.path.exists(model_path):
            return {'success': False, 'error': f'Higgs Audio not found at: {model_path}'}
        
        # Create output directory with absolute path
        output_dir = current_config.get('audio_output_path', './audio_output')
        output_dir = os.path.abspath(output_dir)  # Convert to absolute path
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate unique filename
        import uuid
        audio_filename = f"output_{uuid.uuid4().hex[:8]}.wav"
        audio_path = os.path.join(output_dir, audio_filename)
        
        # Call Higgs Audio generation script
        import subprocess
        import sys
        
        # Build the command
        cmd = [
            python_path,
            os.path.join(model_path, script_path),
            '--transcript', text,
            '--out_path', audio_path,
            'temperature', str(current_config.get('temperature', 0.3))
        ]
        
        # Run the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=model_path,
            timeout=600  # 10 minute timeout for first run
        )
        
        if result.returncode == 0 and os.path.exists(audio_path):
            # Play the audio
            _play_audio(audio_path)
            return {'success': True, 'audio_file': audio_path}
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return {'success': False, 'error': f'Higgs Audio failed: {error_msg}'}
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Higgs Audio timed out'}
    except Exception as e:
        return {'success': False, 'error': f'Higgs Audio error: {str(e)}'}

def _call_coqui_tts(text):
    """Call Coqui TTS engine (placeholder)"""
    return {'success': False, 'error': 'Coqui TTS not yet implemented'}

def _play_audio(audio_path):
    """Play the generated audio file"""
    try:
        import subprocess
        import platform
        
        system = platform.system()
        
        if system == "Windows":
            # Use Windows start command
            subprocess.run(['start', audio_path], shell=True, check=True)
        elif system == "Darwin":  # macOS
            # Use afplay
            subprocess.run(['afplay', audio_path], check=True)
        else:  # Linux
            # Use aplay or mpv
            try:
                subprocess.run(['aplay', audio_path], check=True)
            except FileNotFoundError:
                subprocess.run(['mpv', audio_path], check=True)
                
    except Exception as e:
        print(f"Warning: Could not play audio: {e}")
        # Audio file was still generated, just not played

def main():
    """Main entry point"""
    # Create necessary directories
    create_templates_directory()
    create_static_directory()
    
    # Load initial configuration
    load_config()
    
    # Start Higgs Audio service automatically
    print("🚀 Starting Higgs Audio service...")
    if start_higgs_service():
        print("✅ Higgs Audio service started successfully!")
    else:
        print("⚠️  Higgs Audio service failed to start, will use fallback mode")
    
    # Open browser automatically
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask app
    print("🌐 Starting ReadAloud Web Interface...")
    print("📱 Opening browser automatically...")
    print("🔧 Interface will be available at: http://localhost:5000")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        # Clean up service when web interface stops
        print("🛑 Stopping Higgs Audio service...")
        stop_higgs_service()

if __name__ == '__main__':
    main()
