#!/bin/bash

# AgriForecast.ai Best UX Platform Launcher
# Market-Leading Agricultural Platform for Farmers and Students

echo "🌾 AgriForecast.ai - Best UX Platform"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if Streamlit is available
if ! python3 -c "import streamlit" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Streamlit not found. Installing...${NC}"
    pip install streamlit
fi

# Check if required packages are available
echo -e "${BLUE}📦 Checking dependencies...${NC}"
required_packages=("pandas" "plotly" "numpy" "requests")
missing_packages=()

for package in "${required_packages[@]}"; do
    if ! python3 -c "import $package" &> /dev/null; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Installing missing packages: ${missing_packages[*]}${NC}"
    pip install "${missing_packages[@]}"
fi

# Setup platform database
echo -e "${BLUE}🗄️  Setting up platform database...${NC}"
if [ -f "setup_best_ux.py" ]; then
    python3 setup_best_ux.py
else
    echo -e "${RED}❌ setup_best_ux.py not found${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo ""

# Launch the platform
echo -e "${BLUE}🚀 Launching Best UX Platform on port 8505...${NC}"
echo ""
echo -e "${YELLOW}🌐 Platform will be available at: http://localhost:8505${NC}"
echo ""
echo -e "${GREEN}🔑 Login credentials:${NC}"
echo "   👨‍🌾 Farmer: farmer / password123"
echo "   👩‍🎓 Student: student / student123"  
echo "   👤 Anand: anand / password123"
echo ""
echo -e "${BLUE}📱 Features:${NC}"
echo "   🏠 Farmer-first dashboard with critical insights"
echo "   📱 Mobile-first design with bottom navigation"
echo "   🎯 Simplified 4-section navigation"
echo "   💡 AI-powered insights and recommendations"
echo "   🌾 Smart field management"
echo "   📊 Visual data storytelling"
echo "   ♿ Accessibility optimized"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the platform${NC}"
echo ""

# Launch Streamlit
if [ -f "agriforecast_best_ux.py" ]; then
    streamlit run agriforecast_best_ux.py --server.port 8505 --server.headless true
else
    echo -e "${RED}❌ agriforecast_best_ux.py not found${NC}"
    exit 1
fi




