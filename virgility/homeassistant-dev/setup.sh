#!/bin/bash

# Home Assistant Development Environment Setup Script
# This script sets up the development environment and runs initial tests

set -e  # Exit on any error

echo "🚀 Setting up Home Assistant Development Environment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the homeassistant-dev directory"
    exit 1
fi

# Check Python version
echo "🐍 Checking Python version..."
python --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/Scripts/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp config/env_example.txt .env
    echo "📝 Please edit .env file with your Home Assistant configuration"
    echo "   You'll need to set HA_URL and HA_ACCESS_TOKEN"
else
    echo "✅ .env file already exists"
fi

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Home Assistant configuration"
echo "2. Generate a long-lived access token in Home Assistant"
echo "3. Test connection: python examples/basic_connection.py"
echo "4. Start developing!"
echo ""
echo "To activate the environment in the future:"
echo "  source venv/Scripts/activate"
