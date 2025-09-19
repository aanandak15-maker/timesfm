#!/bin/bash

# AgriForecast Build Script for Netlify
echo "🌾 Building AgriForecast for Netlify..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the agriforecast-frontend directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Check for TypeScript errors
echo "🔍 Checking TypeScript..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📁 Build output is in the 'dist' directory"
    echo "🚀 Ready for Netlify deployment!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

echo "🎉 AgriForecast is ready for deployment!"
