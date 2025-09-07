#!/bin/bash

echo "🚀 Starting TimesFM Web Frontend..."
echo "=================================="
echo ""
echo "The web interface will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Features available:"
echo "✅ Interactive forecasting dashboard"
echo "✅ Multiple agricultural data types"
echo "✅ CSV file upload support"
echo "✅ Real-time visualization"
echo "✅ Download forecast results"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit
streamlit run timesfm_frontend.py --server.port 8501 --server.address localhost
