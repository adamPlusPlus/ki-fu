#!/usr/bin/env python3
"""
Flask-based Home Assistant Dashboard

This example shows how to create a standalone web application
that communicates with Home Assistant via the API.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from config import config
except ImportError:
    print("Warning: Could not import config module")
    config = None

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Home Assistant configuration
HA_URL = os.getenv('HA_URL', 'http://localhost:8123')
HA_TOKEN = os.getenv('HA_ACCESS_TOKEN')

def get_ha_headers():
    """Get headers for Home Assistant API requests."""
    return {
        'Authorization': f'Bearer {HA_TOKEN}',
        'Content-Type': 'application/json'
    }

def call_ha_service(domain, service, data=None):
    """Call a Home Assistant service."""
    if not HA_TOKEN:
        return {'error': 'No access token configured'}
    
    url = f"{HA_URL}/api/services/{domain}/{service}"
    response = requests.post(url, headers=get_ha_headers(), json=data or {})
    return response.json()

def get_ha_entities():
    """Get all entities from Home Assistant."""
    if not HA_TOKEN:
        return []
    
    url = f"{HA_URL}/api/states"
    response = requests.get(url, headers=get_ha_headers())
    if response.status_code == 200:
        return response.json()
    return []

@app.route('/')
def dashboard():
    """Main dashboard page."""
    entities = get_ha_entities()
    
    # Group entities by domain
    grouped_entities = {}
    for entity in entities:
        domain = entity['entity_id'].split('.')[0]
        if domain not in grouped_entities:
            grouped_entities[domain] = []
        grouped_entities[domain].append(entity)
    
    return render_template('dashboard.html', 
                         entities=grouped_entities,
                         ha_url=HA_URL)

@app.route('/api/entities')
def api_entities():
    """API endpoint to get entities."""
    entities = get_ha_entities()
    return jsonify(entities)

@app.route('/api/service/<domain>/<service>', methods=['POST'])
def api_service(domain, service):
    """API endpoint to call services."""
    data = request.get_json() or {}
    result = call_ha_service(domain, service, data)
    return jsonify(result)

@app.route('/control/<entity_id>')
def control_entity(entity_id):
    """Control a specific entity."""
    entities = get_ha_entities()
    entity = next((e for e in entities if e['entity_id'] == entity_id), None)
    
    if not entity:
        return "Entity not found", 404
    
    return render_template('control.html', entity=entity)

@app.route('/control/<entity_id>/toggle', methods=['POST'])
def toggle_entity(entity_id):
    """Toggle an entity on/off."""
    entity = get_ha_entities()
    entity_data = next((e for e in entity if e['entity_id'] == entity_id), None)
    
    if not entity_data:
        return jsonify({'error': 'Entity not found'}), 404
    
    domain = entity_id.split('.')[0]
    current_state = entity_data['state']
    
    if domain == 'light':
        service = 'turn_off' if current_state == 'on' else 'turn_on'
        call_ha_service('light', service, {'entity_id': entity_id})
    elif domain == 'switch':
        service = 'turn_off' if current_state == 'on' else 'turn_on'
        call_ha_service('switch', service, {'entity_id': entity_id})
    
    return redirect(url_for('control_entity', entity_id=entity_id))

if __name__ == '__main__':
    if not HA_TOKEN:
        print("⚠️  Warning: No Home Assistant access token configured")
        print("   Set HA_ACCESS_TOKEN environment variable or create .env file")
    
    print(f"🚀 Starting Flask dashboard at http://localhost:5000")
    print(f"🔌 Connecting to Home Assistant at: {HA_URL}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
