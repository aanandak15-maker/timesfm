#!/bin/bash

# AgriForecast Production Setup Script
echo "🚀 Setting up AgriForecast Production Environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Create virtual environment for backend
echo "📦 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install fastapi uvicorn pydantic python-multipart httpx python-dotenv sqlalchemy psycopg2-binary supabase pandas numpy scikit-learn requests aiohttp

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd agriforecast-frontend
npm install

# Create environment files
echo "🔧 Creating environment files..."
cat > .env.local << EOF
# Production Environment Variables
VITE_OPENWEATHER_API_KEY=28f1d9ac94ed94535d682b7bf6c441bb
VITE_ALPHA_VANTAGE_API_KEY=KJRXQKB09I13GUPP
VITE_NASA_API_KEY=4Od5nRoNq2NKdyFZ6ENS98kcpZg4RT3Efelbjleb
VITE_GOOGLE_MAPS_API_KEY=demo
VITE_SUPABASE_URL=https://rdzyxfeggviqxajqddae.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkenl4ZmVnZ3ZpcXhhanFkZGFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc2MTMzNTIsImV4cCI6MjA3MzE4OTM1Mn0.ugxmvyNl1wt5GcEm0_dWbrhFqp6b3qzA1yqY1uE_nqg
VITE_BACKEND_URL=http://localhost:8000
VITE_AGRICULTURAL_API_KEY=demo
EOF

cd ..

# Create startup scripts
echo "📝 Creating startup scripts..."

# Backend startup script
cat > start_backend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting AgriForecast Backend..."
source .venv/bin/activate
python api_server_production.py
EOF

# Frontend startup script
cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting AgriForecast Frontend..."
cd agriforecast-frontend
npm run dev
EOF

# Full startup script
cat > start_all.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting AgriForecast Full Stack..."

# Start backend in background
echo "Starting backend..."
source .venv/bin/activate
python api_server_production.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "Starting frontend..."
cd agriforecast-frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ AgriForecast is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
wait
EOF

# Make scripts executable
chmod +x start_backend.sh
chmod +x start_frontend.sh
chmod +x start_all.sh

echo "✅ Production setup complete!"
echo ""
echo "🚀 To start the application:"
echo "  ./start_all.sh          # Start both backend and frontend"
echo "  ./start_backend.sh      # Start only backend"
echo "  ./start_frontend.sh     # Start only frontend"
echo ""
echo "🌐 Access points:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "🔧 Next steps:"
echo "  1. Get Google Maps API key for enhanced location services"
echo "  2. Set up agricultural data APIs (see AGRICULTURAL_APIS_GUIDE.md)"
echo "  3. Integrate TimesFM model in backend"
echo "  4. Deploy to production servers"
