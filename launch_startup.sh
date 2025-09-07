#!/bin/bash

# 🌾 AgriForecast.ai Startup Launch Script
# This script launches your agricultural forecasting startup in 5 minutes

echo "🌾 AgriForecast.ai - Agricultural Forecasting Startup"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "startup_mvp.py" ]; then
    echo "❌ Error: startup_mvp.py not found. Please run this script from the timesfm directory."
    exit 1
fi

echo "🚀 Launching AgriForecast.ai MVP..."
echo ""

# Install required dependencies
echo "📦 Installing dependencies..."
pip install streamlit pandas numpy timesfm plotly sqlite3 schedule requests

# Create necessary directories
mkdir -p logs
mkdir -p data

# Set up environment variables (optional)
if [ ! -f ".env" ]; then
    echo "🔧 Creating environment file..."
    cat > .env << EOF
# API Keys (optional - will use mock data if not provided)
OPENWEATHER_API_KEY=
ALPHA_VANTAGE_API_KEY=
NASA_API_KEY=
USDA_API_KEY=

# App Configuration
APP_NAME=AgriForecast.ai
APP_VERSION=1.0.0
DEBUG=True
EOF
    echo "✅ Environment file created (.env)"
fi

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
echo "   - User registration and authentication"
echo "   - Agricultural forecasting (crop yield, weather, prices)"
echo "   - REAL-TIME data from NASA, Alpha Vantage, OpenWeatherMap"
echo "   - Automated data collection every 6 hours"
echo "   - Forecast history and analytics"
echo "   - Export and download capabilities"
echo ""
echo "🚀 Starting Streamlit app..."

# Launch Streamlit
streamlit run startup_mvp.py --server.port 8501 --server.address localhost

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
