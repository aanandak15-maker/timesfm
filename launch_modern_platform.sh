#!/bin/bash

# Launch Modern AgriForecast Platform
echo "🚀 Launching Modern AgriForecast.ai Platform..."

# Activate virtual environment
source .venv/bin/activate

# Setup platform if needed
echo "📋 Setting up platform..."
python setup_modern_platform.py

# Launch the modern platform
echo "🌾 Starting Modern AgriForecast Platform..."
echo "📍 URL: http://localhost:8502"
echo "👤 Username: anand"
echo "🔑 Password: password123"
echo ""
echo "Press Ctrl+C to stop the server"

streamlit run agriforecast_modern.py --server.port 8502 --server.address localhost

