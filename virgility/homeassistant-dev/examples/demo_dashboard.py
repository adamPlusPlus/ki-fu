#!/usr/bin/env python3
"""
Demo Dashboard with Sample Data

This example shows how the dashboard will look and function
with sample Home Assistant data, so you can test the UI
before connecting to your actual Home Assistant instance.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request, redirect, url_for

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from config import config
except ImportError:
    print("Warning: Could not import config module")
    config = None

app = Flask(__name__)
app.secret_key = 'demo-secret-key'

# Sample Home Assistant data for demonstration
SAMPLE_ENTITIES = {
    'light': [
        {
            'entity_id': 'light.living_room',
            'state': 'on',
            'attributes': {
                'friendly_name': 'Living Room Light',
                'brightness': 255,
                'rgb_color': [255, 255, 255]
            }
        },
        {
            'entity_id': 'light.kitchen',
            'state': 'off',
            'attributes': {
                'friendly_name': 'Kitchen Light',
                'brightness': 0
            }
        },
        {
            'entity_id': 'light.bedroom',
            'state': 'on',
            'attributes': {
                'friendly_name': 'Bedroom Light',
                'brightness': 128,
                'color_temp': 4000
            }
        }
    ],
    'switch': [
        {
            'entity_id': 'switch.coffee_maker',
            'state': 'off',
            'attributes': {
                'friendly_name': 'Coffee Maker'
            }
        },
        {
            'entity_id': 'switch.tv',
            'state': 'on',
            'attributes': {
                'friendly_name': 'TV'
            }
        }
    ],
    'climate': [
        {
            'entity_id': 'climate.thermostat',
            'state': 'heat',
            'attributes': {
                'friendly_name': 'Thermostat',
                'temperature': 22,
                'target_temp_high': 24,
                'target_temp_low': 20
            }
        }
    ],
    'sensor': [
        {
            'entity_id': 'sensor.temperature',
            'state': '23.5',
            'attributes': {
                'friendly_name': 'Temperature',
                'unit_of_measurement': '°C'
            }
        },
        {
            'entity_id': 'sensor.humidity',
            'state': '45',
            'attributes': {
                'friendly_name': 'Humidity',
                'unit_of_measurement': '%'
            }
        }
    ],
    'binary_sensor': [
        {
            'entity_id': 'binary_sensor.motion',
            'state': 'off',
            'attributes': {
                'friendly_name': 'Motion Sensor'
            }
        },
        {
            'entity_id': 'binary_sensor.door',
            'state': 'on',
            'attributes': {
                'friendly_name': 'Front Door'
            }
        }
    ]
}

def get_sample_entities():
    """Return sample entities grouped by domain."""
    return SAMPLE_ENTITIES

@app.route('/')
def dashboard():
    """Main dashboard page with sample data."""
    entities = get_sample_entities()
    
    return render_template('dashboard.html', 
                         entities=entities,
                         ha_url="http://demo:8123")

@app.route('/api/entities')
def api_entities():
    """API endpoint to get sample entities."""
    # Flatten the grouped entities
    all_entities = []
    for domain_entities in SAMPLE_ENTITIES.values():
        all_entities.extend(domain_entities)
    return jsonify(all_entities)

@app.route('/control/<entity_id>')
def control_entity(entity_id):
    """Control a specific entity (demo mode)."""
    # Find the entity in sample data
    entity = None
    for domain_entities in SAMPLE_ENTITIES.values():
        for e in domain_entities:
            if e['entity_id'] == entity_id:
                entity = e
                break
        if entity:
            break
    
    if not entity:
        return "Entity not found", 404
    
    return render_template('control.html', entity=entity)

@app.route('/control/<entity_id>/toggle', methods=['POST'])
def toggle_entity(entity_id):
    """Toggle an entity on/off (demo mode)."""
    # Find and toggle the entity
    for domain_entities in SAMPLE_ENTITIES.values():
        for entity in domain_entities:
            if entity['entity_id'] == entity_id:
                # Toggle the state
                if entity['state'] == 'on':
                    entity['state'] = 'off'
                else:
                    entity['state'] = 'on'
                
                # Add some demo feedback
                print(f"🎯 Demo: Toggled {entity_id} to {entity['state']}")
                break
    
    return redirect(url_for('control_entity', entity_id=entity_id))

@app.route('/demo-info')
def demo_info():
    """Show demo information and setup instructions."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Demo Dashboard Info</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; }
            .demo-box { background: #f0f8ff; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; }
            .success { background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; }
            code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏠 Home Assistant Dashboard Demo</h1>
            
            <div class="demo-box">
                <h2>🎯 What You're Seeing</h2>
                <p>This is a <strong>demo dashboard</strong> with sample smart home devices. 
                The buttons and controls are functional, but they're only changing local demo data.</p>
                
                <h3>Demo Features:</h3>
                <ul>
                    <li>✅ Sample lights, switches, climate controls, and sensors</li>
                    <li>✅ Functional toggle buttons (changes demo data)</li>
                    <li>✅ Responsive design that works on mobile</li>
                    <li>✅ Real-time updates (every 30 seconds)</li>
                </ul>
            </div>
            
            <div class="warning">
                <h2>⚠️ Why You're Not Hearing/Controlling Real Devices</h2>
                <p>This is just a <strong>demo</strong>! To control your actual Home Assistant devices:</p>
                <ol>
                    <li>Generate a long-lived access token in Home Assistant</li>
                    <li>Configure your <code>.env</code> file with real credentials</li>
                    <li>Run the real dashboard instead of this demo</li>
                </ol>
            </div>
            
            <div class="success">
                <h2>🚀 Next Steps to Get Real Control</h2>
                <p><strong>1. Get Your Access Token:</strong></p>
                <ul>
                    <li>Open Home Assistant web interface</li>
                    <li>Go to Profile → Long-Lived Access Tokens</li>
                    <li>Create a new token for "Development Dashboard"</li>
                    <li>Copy the generated token</li>
                </ul>
                
                <p><strong>2. Configure Your Environment:</strong></p>
                <ul>
                    <li>Edit <code>.env</code> file with your HA_URL and HA_ACCESS_TOKEN</li>
                    <li>Set HA_URL to your Home Assistant IP (e.g., <code>http://192.168.1.100:8123</code>)</li>
                </ul>
                
                <p><strong>3. Run the Real Dashboard:</strong></p>
                <ul>
                    <li><code>python examples/flask_dashboard.py</code> (for Flask version)</li>
                    <li><code>python examples/fastapi_dashboard.py</code> (for FastAPI version)</li>
                </ul>
            </div>
            
            <div class="demo-box">
                <h2>🎮 Try the Demo Controls</h2>
                <p>Go back to the <a href="/">main dashboard</a> and try clicking the toggle buttons. 
                You'll see the demo data change, which shows how the real dashboard will work!</p>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🎭 Starting Demo Dashboard with Sample Data")
    print("=" * 50)
    print("🔌 This is a DEMO - no real Home Assistant connection")
    print("📱 Sample devices: lights, switches, climate, sensors")
    print("🎯 Try the toggle buttons to see demo functionality")
    print("📖 Visit /demo-info for setup instructions")
    print("")
    print("🚀 Demo dashboard running at http://localhost:5000")
    print("📚 Demo info at http://localhost:5000/demo-info")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
