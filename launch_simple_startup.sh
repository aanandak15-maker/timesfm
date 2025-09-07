#!/bin/bash

# 🌾 AgriForecast.ai - Simplified Startup Launch Script
# No authentication required - direct access to forecasting platform

echo "🌾 AgriForecast.ai - Simplified Agricultural Forecasting Platform"
echo "=================================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "agriforecast_simple.py" ]; then
    echo "❌ Error: agriforecast_simple.py not found. Please run this script from the timesfm directory."
    exit 1
fi

echo "🚀 Launching AgriForecast.ai (No Authentication Required)..."
echo ""

# Install required dependencies
echo "📦 Installing dependencies..."
pip install streamlit pandas numpy timesfm plotly requests

# Create necessary directories
mkdir -p logs
mkdir -p data

# Start the real data pipeline in background
echo "🔄 Starting real data pipeline with API integration..."
python real_data_pipeline.py > logs/real_data_pipeline.log 2>&1 &
DATA_PIPELINE_PID=$!
echo "✅ Real data pipeline started (PID: $DATA_PIPELINE_PID)"

# Wait a moment for pipeline to initialize
sleep 3

# Start the main application
echo "🌐 Starting AgriForecast.ai web application..."
echo ""
echo "🎉 Your startup is launching!"
echo "📱 Frontend: http://localhost:8501"
echo "📊 Admin: Built into the app"
echo "📁 Logs: logs/real_data_pipeline.log"
echo ""
echo "💡 Features available:"
echo "   - Direct access (no login required)"
echo "   - Agricultural forecasting (crop yield, weather, prices)"
echo "   - REAL-TIME data from NASA, Alpha Vantage, OpenWeatherMap"
echo "   - Automated data collection every 6 hours"
echo "   - Forecast history and analytics"
echo "   - Export and download capabilities"
echo "   - Professional business interface"
echo ""
echo "🚀 Starting Streamlit app..."

# Launch Streamlit
streamlit run agriforecast_simple.py --server.port 8501 --server.address localhost

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Shutting down AgriForecast.ai..."
    kill $DATA_PIPELINE_PID 2>/dev/null
    echo "✅ Shutdown complete"
    exit 0
}

# Set up signal handlers for graceful shutdown
trap cleanup SIGINT SIGTERM

echo "✅ AgriForecast.ai is running!"
echo "🌐 Open your browser to: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop"
