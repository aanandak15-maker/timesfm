#!/bin/bash

echo "🚀 Starting AgriForecast.ai Production Platform..."
echo "🌾 Agricultural Intelligence Platform - Single Application"
echo ""

# Activate virtual environment
source .venv/bin/activate

# Start the production platform
echo "🌐 Starting Production Platform (Port 8501)..."
streamlit run agriforecast_production.py --server.port 8501 --server.address localhost

echo ""
echo "✅ Production Platform Started!"
echo "🌐 Access: http://localhost:8501"
echo "🎯 Single unified platform with all features"
echo ""
echo "Press Ctrl+C to stop the platform"

