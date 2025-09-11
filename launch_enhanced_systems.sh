#!/bin/bash

# Launch Enhanced AgriForecast.ai Systems
echo "🚀 Starting Enhanced AgriForecast.ai Systems..."

# Activate virtual environment
source .venv/bin/activate

echo "🌾 Starting User Authentication System (Port 8504)..."
streamlit run agriforecast_user_simple.py --server.port 8504 --server.address localhost &
sleep 2

echo "📱 Starting Mobile-Optimized System (Port 8507)..."
streamlit run agriforecast_mobile.py --server.port 8507 --server.address localhost &
sleep 2

echo "🌾 Starting Multi-Field System (Port 8503)..."
streamlit run agriforecast_multi_field.py --server.port 8503 --server.address localhost &
sleep 2

echo "🌾 Starting MVP System (Port 8502)..."
streamlit run agriforecast_mvp.py --server.port 8502 --server.address localhost &
sleep 2

echo "✅ All Enhanced Systems Started!"
echo ""
echo "🌐 Access Your Systems:"
echo "   • User Authentication: http://localhost:8504"
echo "   • Mobile System: http://localhost:8507"
echo "   • Multi-Field System: http://localhost:8503"
echo "   • MVP System: http://localhost:8502"
echo ""
echo "🎯 Recommended: Start with User Authentication System"
echo "   http://localhost:8504"
echo ""
echo "Press Ctrl+C to stop all systems"

