# 🎨 UI Development Guide for Home Assistant

This guide covers the different approaches to building user interfaces that interact with Home Assistant, from simple custom cards to full-stack web applications.

## 🚀 **Quick Start: Choose Your Approach**

### **Option 1: Custom Lovelace Cards (Frontend Only)**
**Best for**: Simple UI enhancements, custom widgets, quick prototypes
**Complexity**: ⭐⭐ (Easy)
**Deployment**: Via HACS (Home Assistant Community Store)

### **Option 2: Custom Integrations (Backend + Frontend)**
**Best for**: Complex functionality, custom services, deep integration
**Complexity**: ⭐⭐⭐⭐ (Advanced)
**Deployment**: As Home Assistant custom components

### **Option 3: Standalone Web Applications**
**Best for**: Full control, modern web development, external access
**Complexity**: ⭐⭐⭐ (Intermediate)
**Deployment**: Anywhere (local, cloud, container)

## 🎯 **Option 1: Custom Lovelace Cards**

### **What You Need**
- JavaScript/TypeScript knowledge
- HTML/CSS skills
- **No Python backend required**

### **Example: Simple Custom Card**
```javascript
// custom-card.js
class CustomCard extends HTMLElement {
    setConfig(config) {
        this.config = config;
        this.render();
    }
    
    render() {
        this.innerHTML = `
            <ha-card header="Custom Card">
                <div class="card-content">
                    <p>Hello from custom card!</p>
                    <ha-switch 
                        .checked="${this.config.default_state === 'on'}"
                        @change="${this.handleToggle}">
                    </ha-switch>
                </div>
            </ha-card>
        `;
    }
    
    handleToggle(ev) {
        const state = ev.target.checked ? 'on' : 'off';
        this.callService('input_boolean', 'turn_' + state, {
            entity_id: this.config.entity_id
        });
    }
}

customElements.define('custom-card', CustomCard);
```

### **Deployment via HACS**
1. Create a GitHub repository with your custom card
2. Add it to HACS as a custom repository
3. Install and configure in Home Assistant

## 🔧 **Option 2: Custom Integrations**

### **What You Need**
- ✅ **Our current Python environment** (essential!)
- Python knowledge
- Home Assistant integration development skills

### **Project Structure**
```
custom_component/
├── __init__.py
├── manifest.json
├── config_flow.py
├── const.py
├── translations/
├── frontend/
│   ├── dist/
│   └── src/
└── services.yaml
```

### **Example: Custom Integration with UI**
```python
# __init__.py
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "my_custom_integration"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    # Register frontend
    hass.http.register_static_path(
        f"/{DOMAIN}/frontend",
        hass.config.path("custom_components", DOMAIN, "frontend", "dist"),
        cache_headers=False
    )
    
    return True
```

## 🌐 **Option 3: Standalone Web Applications**

### **What You Need**
- ✅ **Our current Python environment** (for backend)
- Web framework knowledge
- Frontend development skills

### **Available Examples in This Project**

#### **Flask Dashboard** (`examples/flask_dashboard.py`)
- **Features**: Full-featured web dashboard, device control, real-time updates
- **Best for**: Traditional web applications, quick prototypes
- **Run it**: `python examples/flask_dashboard.py`

#### **FastAPI Dashboard** (`examples/fastapi_dashboard.py`)
- **Features**: Modern API-first design, automatic documentation, async support
- **Best for**: Modern web development, API development, microservices
- **Run it**: `python examples/fastapi_dashboard.py`

### **Running the Examples**

1. **Configure Home Assistant**:
   ```bash
   cp config/env_example.txt .env
   # Edit .env with your HA_URL and HA_ACCESS_TOKEN
   ```

2. **Start Flask Dashboard**:
   ```bash
   python examples/flask_dashboard.py
   # Open http://localhost:5000
   ```

3. **Start FastAPI Dashboard**:
   ```bash
   python examples/fastapi_dashboard.py
   # Open http://localhost:8000
   # API docs at http://localhost:8000/docs
   ```

## 🛠️ **Development Tools & Workflow**

### **Backend Development**
```bash
# Activate environment
source venv/Scripts/activate

# Code quality
black src/ examples/
flake8 src/ examples/
mypy src/ examples/

# Testing
pytest tests/
```

### **Frontend Development**
```bash
# For custom cards (if using Node.js)
npm install -g @home-assistant/cli
ha card install

# For standalone apps
# Use your preferred frontend framework (React, Vue, Svelte)
```

## 📱 **Mobile & Responsive Design**

### **Mobile-First Approach**
- Use responsive CSS frameworks (Bootstrap, Tailwind)
- Implement touch-friendly controls
- Consider PWA (Progressive Web App) features

### **Example: Responsive Dashboard**
```css
/* Mobile-first CSS */
.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 15px;
    padding: 15px;
}

@media (min-width: 768px) {
    .dashboard-grid {
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        padding: 20px;
    }
}
```

## 🔐 **Security Considerations**

### **Authentication**
- Use long-lived access tokens
- Implement proper session management
- Consider OAuth2 for external apps

### **API Security**
- Validate all inputs
- Implement rate limiting
- Use HTTPS in production

### **Example: Secure API Endpoint**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    if not is_valid_token(token.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token.credentials

@app.get("/secure-endpoint")
async def secure_endpoint(token: str = Depends(verify_token)):
    return {"message": "Access granted"}
```

## 🚀 **Deployment Options**

### **Local Development**
- Run on your development machine
- Access via localhost
- Good for testing and development

### **Home Assistant Add-on**
- Package as Home Assistant add-on
- Integrate with Home Assistant ecosystem
- Easy deployment for users

### **Docker Container**
- Containerize your application
- Deploy anywhere Docker runs
- Consistent environment

### **Cloud Deployment**
- Deploy to cloud platforms (Heroku, AWS, Azure)
- External access from anywhere
- Scalable infrastructure

## 📚 **Learning Resources**

### **Home Assistant Development**
- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- [Custom Integration Tutorial](https://developers.home-assistant.io/docs/creating_integration_manifest/)
- [Frontend Development](https://developers.home-assistant.io/docs/frontend/)

### **Web Development**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Modern JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### **UI/UX Design**
- [Material Design](https://material.io/design)
- [Home Assistant Design System](https://developers.home-assistant.io/docs/frontend/design-system/)

## 🎯 **Next Steps**

1. **Start Simple**: Begin with a basic Flask or FastAPI dashboard
2. **Learn the APIs**: Understand Home Assistant's REST and WebSocket APIs
3. **Build Incrementally**: Add features one at a time
4. **Test Thoroughly**: Use the testing tools in your environment
5. **Deploy**: Choose your deployment strategy

## 🔧 **Need Help?**

- Run the examples to see how they work
- Check the API documentation at `/docs` (FastAPI)
- Use the test suite to verify your setup
- Review Home Assistant logs for debugging

---

**Happy UI building! 🎨✨**
