#!/bin/bash

# AgriForecast.ai Multi-Field Management System Launch Script
# This script launches all the agricultural forecasting systems

echo "🌾 AgriForecast.ai Multi-Field Management System"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo "🚀 Starting Multi-Field Management System..."
echo ""

# Launch the multi-field management system
echo "📊 Launching Multi-Field Management System on port 8503..."
streamlit run agriforecast_multi_field.py --server.port 8503 --server.address localhost &

# Wait a moment for the system to start
sleep 3

echo ""
echo "✅ Multi-Field Management System is now running!"
echo ""
echo "🌐 Access your systems:"
echo "   • Multi-Field Management: http://localhost:8503"
echo "   • Single Field MVP:      http://localhost:8502"
echo "   • Simple Forecasting:    http://localhost:8501"
echo ""
echo "🎯 Features Available:"
echo "   • Multi-field management"
echo "   • Field comparison dashboard"
echo "   • Bulk operations and reporting"
echo "   • Field hierarchy (farm → field → zones)"
echo "   • Analytics and insights"
echo "   • Data import/export"
echo ""
echo "📱 To stop the system, press Ctrl+C"
echo ""

# Keep the script running
wait




