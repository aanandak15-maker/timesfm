#!/bin/bash

# Launch Phase 2 Systems - Advanced Analytics & Reporting
echo "🚀 Starting Phase 2: Advanced Analytics & Reporting Systems..."

# Activate virtual environment
source .venv/bin/activate

echo "📊 Starting Advanced Analytics Dashboard (Port 8508)..."
streamlit run advanced_analytics_dashboard.py --server.port 8508 --server.address localhost &
sleep 2

echo "📄 Starting Report Generation System (Port 8509)..."
streamlit run report_generation_system.py --server.port 8509 --server.address localhost &
sleep 2

echo "🌾 Starting Phase 1 Systems (Ports 8502-8507)..."
streamlit run agriforecast_mvp.py --server.port 8502 --server.address localhost &
sleep 1

streamlit run agriforecast_multi_field.py --server.port 8503 --server.address localhost &
sleep 1

streamlit run agriforecast_user_simple.py --server.port 8504 --server.address localhost &
sleep 1

streamlit run agriforecast_mobile.py --server.port 8507 --server.address localhost &
sleep 1

echo "✅ All Phase 2 Systems Started!"
echo ""
echo "🌐 Access Your Complete Agricultural Platform:"
echo "   • User Authentication: http://localhost:8504"
echo "   • Mobile System: http://localhost:8507"
echo "   • Multi-Field System: http://localhost:8503"
echo "   • MVP System: http://localhost:8502"
echo "   • 📊 Advanced Analytics: http://localhost:8508"
echo "   • 📄 Report Generation: http://localhost:8509"
echo ""
echo "🎯 Phase 2 Complete: Business Intelligence & Reporting"
echo "   📊 Advanced Analytics Dashboard - Yield trends, ROI analysis, field comparison"
echo "   📄 Report Generation System - PDF reports, Excel export, email automation"
echo ""
echo "Press Ctrl+C to stop all systems"

