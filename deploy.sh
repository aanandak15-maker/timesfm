#!/bin/bash

# 🚀 AgriForecast.ai Production Deployment Script
# This script sets up the complete agricultural forecasting platform

echo "🌾 AgriForecast.ai - Production Deployment"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "agriforecast_modern.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Create production environment
echo "📦 Setting up production environment..."

# Backend setup
echo "🔧 Setting up FastAPI backend..."
pip install -r requirements.txt 2>/dev/null || pip install fastapi uvicorn aiohttp python-multipart streamlit pandas numpy scikit-learn

# Frontend setup
echo "🎨 Setting up React frontend..."
cd agri-aura-frontend
npm install
npm run build
cd ..

# Create production configuration
echo "⚙️ Creating production configuration..."
cat > .env.production << EOF
# Production Environment Variables
DATABASE_URL=sqlite:///./agriforecast_production.db
OPENWEATHER_API_KEY=your_openweather_api_key
TIMESFM_MODEL_PATH=./models/timesfm
ENVIRONMENT=production
DEBUG=false
EOF

# Create Docker configuration
echo "🐳 Creating Docker configuration..."
cat > docker-compose.yml << EOF
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./agriforecast.db
    volumes:
      - ./data:/app/data
    command: uvicorn fastapi_integration:app --host 0.0.0.0 --port 8000

  frontend:
    build: ./agri-aura-frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend
EOF

# Create Dockerfile for backend
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "fastapi_integration:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create Dockerfile for frontend
cat > agri-aura-frontend/Dockerfile << EOF
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]
EOF

echo "✅ Production setup complete!"
echo ""
echo "🚀 Deployment Options:"
echo "1. Local Development:"
echo "   Backend:  python -m uvicorn fastapi_integration:app --host 0.0.0.0 --port 8000"
echo "   Frontend: cd agri-aura-frontend && npm run dev"
echo ""
echo "2. Docker Deployment:"
echo "   docker-compose up -d"
echo ""
echo "3. Manual Production:"
echo "   Backend:  uvicorn fastapi_integration:app --host 0.0.0.0 --port 8000"
echo "   Frontend: cd agri-aura-frontend && npm run build && npm run preview"
echo ""
echo "🌐 Access Points:"
echo "   React Frontend: http://localhost:3000"
echo "   FastAPI Backend: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "🎉 Your agricultural forecasting platform is ready for production!"
