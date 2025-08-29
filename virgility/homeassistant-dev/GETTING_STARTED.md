# Getting Started with Home Assistant Development

## 🚀 Quick Start

### 1. Environment Setup
Your development environment is already set up! You have:
- ✅ Python 3.13.3
- ✅ Virtual environment with all dependencies
- ✅ Project structure with examples and tests
- ✅ Configuration management system

### 2. Configure Your Home Assistant Connection

#### Step 1: Generate Access Token
1. Open your Home Assistant web interface
2. Go to **Profile** (bottom left)
3. Scroll down to **Long-Lived Access Tokens**
4. Click **Create Token**
5. Give it a name (e.g., "Development API")
6. Copy the generated token

#### Step 2: Create Configuration File
1. Copy the example configuration:
   ```bash
   cp config/env_example.txt .env
   ```

2. Edit the `.env` file with your settings:
   ```env
   HA_URL=http://your-ha-ip:8123
   HA_ACCESS_TOKEN=your-copied-token-here
   HA_SSL_VERIFY=true
   ```

### 3. Test Your Connection

Run the basic connection test:
```bash
python examples/basic_connection.py
```

If successful, you'll see:
```
✅ Connection test successful!
🎉 You're ready to start developing with Home Assistant!
```

## 🛠️ Available Tools

### Core Libraries
- **`homeassistant-api`**: Official Python client
- **`websockets`**: Real-time WebSocket communication
- **`aiohttp`**: Async HTTP client/server
- **`asyncio-mqtt`**: MQTT client for IoT devices

### Development Tools
- **`pytest`**: Testing framework
- **`black`**: Code formatter
- **`flake8`**: Linter
- **`mypy`**: Type checker

## 📚 Examples

### Basic Connection (`examples/basic_connection.py`)
- Connects to Home Assistant
- Retrieves basic information
- Lists available entities

### WebSocket Monitor (`examples/websocket_monitor.py`)
- Real-time event monitoring
- WebSocket connection management
- Event parsing and display

## 🔧 Development Workflow

### 1. Activate Environment
```bash
source venv/Scripts/activate
```

### 2. Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### 3. Testing
```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_config.py::TestConfig::test_validation
```

### 4. Running Examples
```bash
# Basic connection test
python examples/basic_connection.py

# WebSocket event monitor
python examples/websocket_monitor.py
```

## 🏗️ Project Structure

```
homeassistant-dev/
├── venv/                 # Virtual environment
├── src/                  # Source code
│   └── config.py        # Configuration management
├── tests/                # Test files
├── examples/             # Example scripts
├── config/               # Configuration templates
├── requirements.txt      # Dependencies
├── setup.sh             # Setup script
└── README.md            # Project documentation
```

## 🔌 API Endpoints

### REST API
- **Base URL**: `http://your-ha-ip:8123/api/`
- **Authentication**: Bearer token in headers
- **Documentation**: [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)

### WebSocket API
- **URL**: `ws://your-ha-ip:8123/api/websocket`
- **Authentication**: JSON message with access token
- **Real-time**: Subscribe to events, state changes, and more

## 📱 Common Use Cases

### 1. Device Control
```python
from homeassistant_api import Client

client = Client('http://your-ha:8123', 'your-token')

# Turn on a light
client.call_service('light', 'turn_on', entity_id='light.living_room')

# Get device state
state = client.get_entity('light.living_room')
print(f"Light is: {state.state}")
```

### 2. Event Monitoring
```python
# See websocket_monitor.py for full example
# Subscribe to specific events
# Monitor state changes
# Trigger actions based on events
```

### 3. Automation
```python
# Create complex automation rules
# Schedule tasks
# Respond to sensor data
# Integrate with external services
```

## 🚨 Troubleshooting

### Common Issues

#### Connection Refused
- Check if Home Assistant is running
- Verify the IP address and port
- Ensure network connectivity

#### Authentication Failed
- Verify your access token
- Check token permissions
- Ensure token hasn't expired

#### Import Errors
- Activate virtual environment: `source venv/Scripts/activate`
- Install requirements: `pip install -r requirements.txt`

### Debug Mode
Enable debug logging in your `.env` file:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📖 Next Steps

1. **Explore the API**: Use the examples to understand available endpoints
2. **Build Your First App**: Start with a simple device controller
3. **Create Custom Integrations**: Build Python-based components
4. **Develop Frontend**: Create custom Lovelace cards
5. **Automation**: Build complex automation workflows

## 🔗 Useful Resources

- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- [REST API Reference](https://developers.home-assistant.io/docs/api/rest/)
- [Python API Library](https://github.com/elad-bar/ha-api)
- [Community Forum](https://community.home-assistant.io/)
- [GitHub Repository](https://github.com/home-assistant/core)

## 🆘 Need Help?

- Check the troubleshooting section above
- Review the example scripts
- Run the test suite to verify your setup
- Check Home Assistant logs for detailed error messages

---

**Happy coding! 🎉**
