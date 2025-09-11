#!/bin/bash

# Launch AgriForecast.ai User Authentication System
echo "🌾 Starting AgriForecast.ai User Authentication System..."

# Activate virtual environment
source .venv/bin/activate

# Launch the user authentication system
streamlit run agriforecast_user_auth.py --server.port 8504 --server.address localhost

echo "✅ User Authentication System launched!"
echo "🌐 Access at: http://localhost:8504"

