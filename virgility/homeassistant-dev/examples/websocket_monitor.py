#!/usr/bin/env python3
"""
Home Assistant WebSocket Event Monitor

This script demonstrates how to connect to Home Assistant via WebSocket
and monitor events in real-time.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    import websockets
    import aiohttp
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Make sure you have activated the virtual environment and installed requirements")
    sys.exit(1)


class HomeAssistantWebSocket:
    """WebSocket client for Home Assistant."""
    
    def __init__(self, url: str, token: str):
        self.url = url.replace('http://', 'ws://').replace('https://', 'wss://')
        self.token = token
        self.websocket = None
        
    async def connect(self):
        """Connect to Home Assistant WebSocket API."""
        ws_url = f"{self.url}/api/websocket"
        print(f"🔌 Connecting to WebSocket: {ws_url}")
        
        try:
            self.websocket = await websockets.connect(ws_url)
            print("✅ WebSocket connection established")
            
            # Authenticate
            auth_message = {
                "type": "auth",
                "access_token": self.token
            }
            await self.websocket.send(json.dumps(auth_message))
            
            # Wait for auth response
            response = await self.websocket.recv()
            auth_response = json.loads(response)
            
            if auth_response.get("type") == "auth_ok":
                print("✅ Authentication successful")
                return True
            else:
                print(f"❌ Authentication failed: {auth_response}")
                return False
                
        except Exception as e:
            print(f"❌ WebSocket connection failed: {e}")
            return False
    
    async def subscribe_to_events(self):
        """Subscribe to all events."""
        subscribe_message = {
            "id": 1,
            "type": "subscribe_events"
        }
        await self.websocket.send(json.dumps(subscribe_message))
        print("📡 Subscribed to all events")
    
    async def listen_for_events(self, duration: int = 60):
        """Listen for events for a specified duration."""
        print(f"👂 Listening for events for {duration} seconds...")
        print("Press Ctrl+C to stop early")
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            while True:
                if asyncio.get_event_loop().time() - start_time > duration:
                    print(f"\n⏰ Time limit reached ({duration} seconds)")
                    break
                
                # Wait for message with timeout
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                    event = json.loads(message)
                    
                    if event.get("type") == "event":
                        self._print_event(event)
                    elif event.get("type") == "pong":
                        # Handle pong messages (keep-alive)
                        pass
                    else:
                        print(f"📨 Other message: {event.get('type', 'unknown')}")
                        
                except asyncio.TimeoutError:
                    # Send ping to keep connection alive
                    ping_message = {"id": 2, "type": "ping"}
                    await self.websocket.send(json.dumps(ping_message))
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user")
        except Exception as e:
            print(f"❌ Error during event listening: {e}")
    
    def _print_event(self, event: Dict[str, Any]):
        """Print event information in a readable format."""
        event_data = event.get("event", {})
        event_type = event_data.get("event_type", "unknown")
        
        print(f"\n📅 Event: {event_type}")
        print(f"   Time: {event_data.get('time_fired', 'unknown')}")
        
        # Print entity information if available
        if "data" in event_data:
            data = event_data["data"]
            if "entity_id" in data:
                print(f"   Entity: {data['entity_id']}")
            if "new_state" in data:
                new_state = data["new_state"]
                print(f"   State: {new_state.get('state', 'unknown')}")
                print(f"   Attributes: {new_state.get('attributes', {})}")
    
    async def close(self):
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            print("🔌 WebSocket connection closed")


async def main():
    """Main function."""
    print("🚀 Home Assistant WebSocket Event Monitor")
    print("=" * 50)
    
    # Configuration
    ha_url = os.getenv('HA_URL', 'http://localhost:8123')
    ha_token = os.getenv('HA_ACCESS_TOKEN', 'your-token-here')
    
    if ha_token == 'your-token-here':
        print("⚠️  Please set your Home Assistant access token in the .env file")
        print("   You can generate one in Home Assistant: Profile > Long-Lived Access Tokens")
        return
    
    # Create WebSocket client
    client = HomeAssistantWebSocket(ha_url, ha_token)
    
    try:
        # Connect and authenticate
        if not await client.connect():
            return
        
        # Subscribe to events
        await client.subscribe_to_events()
        
        # Listen for events
        await client.listen_for_events(duration=60)
        
    except Exception as e:
        print(f"❌ Error in main: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
