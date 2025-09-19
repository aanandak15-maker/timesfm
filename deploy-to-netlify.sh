#!/bin/bash

# AgriForecast Netlify Deployment Script
echo "🌾 AgriForecast Netlify Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "agriforecast-frontend/package.json" ]; then
    echo "❌ Error: agriforecast-frontend directory not found."
    echo "Please run this script from the project root directory."
    exit 1
fi

# Navigate to frontend directory
cd agriforecast-frontend

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building for production..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "🚀 Ready for Netlify deployment!"
    echo ""
    echo "Next steps:"
    echo "1. Go to https://netlify.com"
    echo "2. Click 'New site from Git'"
    echo "3. Connect your GitHub repository"
    echo "4. Set build settings:"
    echo "   - Base directory: agriforecast-frontend"
    echo "   - Build command: npm run build"
    echo "   - Publish directory: agriforecast-frontend/dist"
    echo "5. Add environment variables in Netlify dashboard"
    echo "6. Deploy!"
    echo ""
    echo "📁 Build output is in: agriforecast-frontend/dist"
    echo "📋 See DEPLOY_TO_NETLIFY.md for detailed instructions"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

echo "🎉 Deployment preparation complete!"
