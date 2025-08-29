# Home Assistant Development Environment

This project provides a development environment for building applications that interact with Home Assistant Green.

## Setup

### Prerequisites
- Python 3.13+
- Git (for version control)

### Installation
1. Navigate to this directory
2. Activate the virtual environment:
   ```bash
   # On Windows with Git Bash
   source venv/Scripts/activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
homeassistant-dev/
├── venv/                 # Python virtual environment
├── src/                  # Source code
├── tests/                # Test files
├── examples/             # Example scripts
├── config/               # Configuration files
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Available Libraries

### Core Home Assistant Libraries
- **homeassistant-api**: Official Python client for Home Assistant
- **requests**: HTTP library for REST API calls
- **websockets**: WebSocket support for real-time communication
- **aiohttp**: Async HTTP client/server framework
- **asyncio-mqtt**: MQTT client for IoT communication

### Development Tools
- **pytest**: Testing framework
- **black**: Code formatter
- **flake8**: Linter
- **mypy**: Type checker

## Quick Start

1. **Basic Connection Example**:
   ```python
   from homeassistant_api import Client
   
   # Connect to Home Assistant
   client = Client('http://your-ha-instance:8123', 'your-access-token')
   
   # Get all entities
   entities = client.get_entities()
   print(f"Found {len(entities)} entities")
   ```

2. **WebSocket Example**:
   ```python
   import asyncio
   import websockets
   
   async def listen_to_events():
       uri = "ws://your-ha-instance:8123/api/websocket"
       async with websockets.connect(uri) as websocket:
           # Send authentication
           await websocket.send('{"type": "auth", "access_token": "your-token"}')
           
           # Listen for events
           async for message in websocket:
               print(f"Received: {message}")
   ```

## Configuration

Create a `.env` file in the config directory:
```env
HA_URL=http://your-ha-instance:8123
HA_ACCESS_TOKEN=your-long-lived-access-token
HA_SSL_VERIFY=true
```

## Development Workflow

1. **Code Formatting**: `black src/`
2. **Linting**: `flake8 src/`
3. **Type Checking**: `mypy src/`
4. **Testing**: `pytest tests/`

## Useful Resources

- [Home Assistant REST API Documentation](https://developers.home-assistant.io/docs/api/rest/)
- [Home Assistant Python API](https://github.com/elad-bar/ha-api)
- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)

## Next Steps

1. Configure your Home Assistant instance
2. Create your first integration
3. Build custom dashboards
4. Implement automation scripts
