#!/usr/bin/env python3
"""
FastAPI-based Home Assistant Dashboard

This example shows how to create a modern, API-first web application
that communicates with Home Assistant.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from pydantic import BaseModel

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from config import config
except ImportError:
    print("Warning: Could not import config module")
    config = None

app = FastAPI(
    title="Home Assistant Dashboard API",
    description="Modern API for controlling Home Assistant devices",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Assistant configuration
HA_URL = os.getenv('HA_URL', 'http://localhost:8123')
HA_TOKEN = os.getenv('HA_ACCESS_TOKEN')

# Pydantic models for API
class EntityState(BaseModel):
    entity_id: str
    state: str
    attributes: Dict[str, Any]
    last_changed: str
    last_updated: str

class ServiceCall(BaseModel):
    entity_id: str
    service_data: Optional[Dict[str, Any]] = None

class ServiceResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

def get_ha_headers():
    """Get headers for Home Assistant API requests."""
    return {
        'Authorization': f'Bearer {HA_TOKEN}',
        'Content-Type': 'application/json'
    }

def call_ha_service(domain: str, service: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Call a Home Assistant service."""
    if not HA_TOKEN:
        raise HTTPException(status_code=401, detail="No access token configured")
    
    url = f"{HA_URL}/api/services/{domain}/{service}"
    response = requests.post(url, headers=get_ha_headers(), json=data or {})
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Service call failed")
    
    return response.json()

def get_ha_entities() -> List[EntityState]:
    """Get all entities from Home Assistant."""
    if not HA_TOKEN:
        raise HTTPException(status_code=401, detail="No access token configured")
    
    url = f"{HA_URL}/api/states"
    response = requests.get(url, headers=get_ha_headers())
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch entities")
    
    entities = response.json()
    return [EntityState(**entity) for entity in entities]

# API Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home Assistant Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://unpkg.com/htmx.org@1.9.10"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .entity { padding: 10px; margin: 5px; border: 1px solid #ccc; border-radius: 5px; }
            .on { background-color: #d4edda; }
            .off { background-color: #f8d7da; }
            button { padding: 5px 10px; margin: 2px; }
        </style>
    </head>
    <body>
        <h1>🏠 Home Assistant Dashboard</h1>
        <div id="entities" hx-get="/api/entities" hx-trigger="load, every 5s">
            Loading entities...
        </div>
    </body>
    </html>
    """

@app.get("/api/entities", response_model=List[EntityState])
async def get_entities():
    """Get all Home Assistant entities."""
    return get_ha_entities()

@app.get("/api/entities/{entity_id}", response_model=EntityState)
async def get_entity(entity_id: str):
    """Get a specific entity by ID."""
    entities = get_ha_entities()
    entity = next((e for e in entities if e.entity_id == entity_id), None)
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return entity

@app.post("/api/entities/{entity_id}/toggle", response_model=ServiceResponse)
async def toggle_entity(entity_id: str):
    """Toggle an entity on/off."""
    entities = get_ha_entities()
    entity = next((e for e in entities if e.entity_id == entity_id), None)
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    domain = entity_id.split('.')[0]
    
    if domain not in ['light', 'switch']:
        raise HTTPException(status_code=400, detail="Entity type not supported for toggle")
    
    current_state = entity.state
    service = 'turn_off' if current_state == 'on' else 'turn_on'
    
    try:
        result = call_ha_service(domain, service, {'entity_id': entity_id})
        return ServiceResponse(
            success=True,
            message=f"Successfully toggled {entity_id}",
            data=result
        )
    except Exception as e:
        return ServiceResponse(
            success=False,
            message=f"Failed to toggle {entity_id}: {str(e)}"
        )

@app.post("/api/services/{domain}/{service}", response_model=ServiceResponse)
async def call_service(domain: str, service: str, service_call: ServiceCall):
    """Call any Home Assistant service."""
    try:
        data = service_call.service_data or {}
        if service_call.entity_id:
            data['entity_id'] = service_call.entity_id
        
        result = call_ha_service(domain, service, data)
        return ServiceResponse(
            success=True,
            message=f"Successfully called {domain}.{service}",
            data=result
        )
    except Exception as e:
        return ServiceResponse(
            success=False,
            message=f"Failed to call {domain}.{service}: {str(e)}"
        )

@app.get("/api/domains")
async def get_domains():
    """Get all available domains."""
    entities = get_ha_entities()
    domains = {}
    
    for entity in entities:
        domain = entity.entity_id.split('.')[0]
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(entity.entity_id)
    
    return domains

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    try:
        if not HA_TOKEN:
            return {"status": "unhealthy", "reason": "No access token configured"}
        
        # Test Home Assistant connection
        url = f"{HA_URL}/api/"
        response = requests.get(url, headers=get_ha_headers(), timeout=5)
        
        if response.status_code == 200:
            return {"status": "healthy", "ha_connection": "ok"}
        else:
            return {"status": "unhealthy", "ha_connection": "failed", "status_code": response.status_code}
    
    except Exception as e:
        return {"status": "unhealthy", "ha_connection": "error", "error": str(e)}

if __name__ == "__main__":
    if not HA_TOKEN:
        print("⚠️  Warning: No Home Assistant access token configured")
        print("   Set HA_ACCESS_TOKEN environment variable or create .env file")
    
    print(f"🚀 Starting FastAPI dashboard at http://localhost:8000")
    print(f"🔌 Connecting to Home Assistant at: {HA_URL}")
    print(f"📚 API documentation at http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
