#!/bin/bash
# ReadAloud StreamDeck Integration Startup Script
# This script starts ReadAloud in background mode for StreamDeck integration

echo "Starting ReadAloud StreamDeck Integration..."

# Change to the ReadAloud directory
cd "$(dirname "$0")/.."

# Start background service
echo "Starting background service..."
nohup python background_service.py --daemon > logs/background.log 2>&1 &
BACKGROUND_PID=$!

# Wait a moment for service to start
sleep 3

# Start StreamDeck plugin
echo "Starting StreamDeck plugin..."
nohup python streamdeck/plugin.py > logs/streamdeck.log 2>&1 &
PLUGIN_PID=$!

# Save PIDs for later use
echo $BACKGROUND_PID > logs/background.pid
echo $PLUGIN_PID > logs/streamdeck.pid

echo "ReadAloud StreamDeck integration started successfully!"
echo "Background service PID: $BACKGROUND_PID"
echo "StreamDeck plugin PID: $PLUGIN_PID"
echo "The service is now running in the background."
echo "Check logs/ directory for output logs."
echo "Use 'kill $BACKGROUND_PID $PLUGIN_PID' to stop the services."
