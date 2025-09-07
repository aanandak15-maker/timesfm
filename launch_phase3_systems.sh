#!/bin/bash

# Launch Phase 3 Systems - Agricultural Workflow Integration
echo "🚀 Starting Phase 3: Agricultural Workflow Integration..."

# Activate virtual environment
source .venv/bin/activate

echo "🌾 Starting Crop Management System (Port 8510)..."
streamlit run crop_management_system.py --server.port 8510 --server.address localhost &
sleep 2

echo "🌱 Starting Soil Health System (Port 8511)..."
streamlit run soil_health_system.py --server.port 8511 --server.address localhost &
sleep 2

echo "🌾 Starting Phase 1 & 2 Systems (Ports 8502-8509)..."
streamlit run agriforecast_mvp.py --server.port 8502 --server.address localhost &
sleep 1

streamlit run agriforecast_multi_field.py --server.port 8503 --server.address localhost &
sleep 1

streamlit run agriforecast_user_simple.py --server.port 8504 --server.address localhost &
sleep 1

streamlit run agriforecast_mobile.py --server.port 8507 --server.address localhost &
sleep 1

streamlit run advanced_analytics_dashboard.py --server.port 8508 --server.address localhost &
sleep 1

streamlit run report_generation_system.py --server.port 8509 --server.address localhost &
sleep 1

echo "✅ All Phase 3 Systems Started!"
echo ""
echo "🌐 Access Your Complete Agricultural Platform:"
echo "   • User Authentication: http://localhost:8504"
echo "   • Mobile System: http://localhost:8507"
echo "   • Multi-Field System: http://localhost:8503"
echo "   • MVP System: http://localhost:8502"
echo "   • 📊 Advanced Analytics: http://localhost:8508"
echo "   • 📄 Report Generation: http://localhost:8509"
echo "   • 🌾 Crop Management: http://localhost:8510"
echo "   • 🌱 Soil Health: http://localhost:8511"
echo ""
echo "🎯 Phase 3 Complete: Agricultural Workflow Integration"
echo "   🌾 Crop Management - Planting, growth stages, harvest planning, pest alerts"
echo "   🌱 Soil Health - Soil testing, fertilizer recommendations, irrigation"
echo ""
echo "Press Ctrl+C to stop all systems"
