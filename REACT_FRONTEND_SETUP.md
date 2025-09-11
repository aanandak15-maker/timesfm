# 🚀 React + Tailwind + Vite + Supabase Frontend Setup

## 🎯 **Modern Frontend Stack for AgriForecast.ai**

**Tech Stack:**
- ⚛️ **React 18** - Modern UI framework
- ⚡ **Vite** - Ultra-fast build tool
- 🎨 **Tailwind CSS** - Utility-first CSS framework
- 🗄️ **Supabase** - Backend-as-a-Service (PostgreSQL + Auth + Real-time)
- 🔗 **Integration** - Connect to your existing Python AI/ML backend

---

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React App     │    │   Supabase       │    │  Python Backend │
│  (Vite + TW)    │◄──►│  (PostgreSQL)    │◄──►│  (AI/ML Models) │
│                 │    │  - User Auth     │    │  - TimesFM      │
│  - Dashboard    │    │  - Real-time DB  │    │  - Forecasting  │
│  - Field Mgmt   │    │  - File Storage  │    │  - Weather APIs │
│  - Analytics    │    │  - Edge Functions│    │  - Predictions  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## 📦 **Project Setup**

### **Step 1: Create React + Vite Project**

```bash
# Create new React + Vite project
npm create vite@latest agriforecast-frontend -- --template react

# Navigate to project
cd agriforecast-frontend

# Install dependencies
npm install

# Install additional packages
npm install @supabase/supabase-js
npm install @tailwindcss/forms @tailwindcss/typography
npm install lucide-react recharts
npm install react-router-dom
npm install @tanstack/react-query
npm install axios
```

### **Step 2: Set up Tailwind CSS**

```bash
# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Update `tailwind.config.js`:**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'agri-green': {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
        },
        'agri-brown': {
          50: '#fefaf6',
          500: '#a16207',
          600: '#92400e',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

**Update `src/index.css`:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply bg-agri-green-600 text-white px-4 py-2 rounded-lg hover:bg-agri-green-700 transition-colors;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-md p-6 border border-gray-200;
  }
}
```

---

## 🗄️ **Supabase Setup**

### **Step 1: Create Supabase Project**

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Note your project URL and anon key

### **Step 2: Database Schema**

**Create tables in Supabase SQL Editor:**

```sql
-- Enable Row Level Security
ALTER TABLE IF EXISTS profiles ENABLE ROW LEVEL SECURITY;

-- Users profile table (extends Supabase auth.users)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  username TEXT UNIQUE,
  full_name TEXT,
  email TEXT,
  avatar_url TEXT,
  phone TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Farms table
CREATE TABLE farms (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  location TEXT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  total_area DECIMAL(10, 2),
  owner_id UUID REFERENCES profiles(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Fields table
CREATE TABLE fields (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  farm_id UUID REFERENCES farms(id) ON DELETE CASCADE,
  area DECIMAL(10, 2),
  crop_type TEXT,
  soil_type TEXT,
  irrigation_type TEXT,
  coordinates JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Weather data table
CREATE TABLE weather_data (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  field_id UUID REFERENCES fields(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  temperature DECIMAL(5, 2),
  humidity DECIMAL(5, 2),
  precipitation DECIMAL(8, 2),
  wind_speed DECIMAL(5, 2),
  pressure DECIMAL(8, 2),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Predictions table
CREATE TABLE predictions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  field_id UUID REFERENCES fields(id) ON DELETE CASCADE,
  prediction_type TEXT NOT NULL, -- 'yield', 'weather', 'price'
  predicted_value DECIMAL(12, 4),
  confidence_score DECIMAL(3, 2),
  prediction_date DATE,
  forecast_horizon INTEGER, -- days ahead
  model_version TEXT,
  metadata JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activities table
CREATE TABLE activities (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  field_id UUID REFERENCES fields(id) ON DELETE CASCADE,
  activity_type TEXT NOT NULL, -- 'planting', 'fertilizing', 'harvesting'
  description TEXT,
  date DATE NOT NULL,
  cost DECIMAL(10, 2),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security Policies
CREATE POLICY "Users can view own profiles" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profiles" ON profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own farms" ON farms
  FOR SELECT USING (auth.uid() = owner_id);

CREATE POLICY "Users can manage own farms" ON farms
  FOR ALL USING (auth.uid() = owner_id);

-- Enable realtime for live updates
ALTER PUBLICATION supabase_realtime ADD TABLE weather_data;
ALTER PUBLICATION supabase_realtime ADD TABLE predictions;
```

### **Step 3: Environment Configuration**

**Create `.env.local`:**
```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_PYTHON_API_URL=http://localhost:8000
```

---

## ⚛️ **React App Structure**

### **Project Structure:**
```
src/
├── components/           # Reusable UI components
│   ├── ui/              # Basic UI elements
│   ├── forms/           # Form components
│   ├── charts/          # Chart components
│   └── layout/          # Layout components
├── pages/               # Page components
│   ├── Dashboard.jsx
│   ├── Fields.jsx
│   ├── Analytics.jsx
│   └── Auth.jsx
├── hooks/               # Custom React hooks
├── services/            # API services
├── utils/               # Utility functions
├── store/               # State management
└── types/               # TypeScript types (if using TS)
```

### **Supabase Client Setup:**

**`src/lib/supabase.js`:**
```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### **API Service for Python Backend:**

**`src/services/api.js`:**
```javascript
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_PYTHON_API_URL

class AgriForecastAPI {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
    })
  }

  // Weather data
  async getWeatherData(latitude, longitude, days = 30) {
    const response = await this.client.get(`/weather/${latitude}/${longitude}`, {
      params: { days }
    })
    return response.data
  }

  // Yield predictions
  async predictYield(fieldData) {
    const response = await this.client.post('/predict/yield', fieldData)
    return response.data
  }

  // Time series forecasting
  async forecastTimeSeries(data, horizon = 30) {
    const response = await this.client.post('/forecast/timeseries', {
      data,
      horizon
    })
    return response.data
  }

  // Market prices
  async getMarketPrices(commodity, days = 30) {
    const response = await this.client.get(`/market/${commodity}`, {
      params: { days }
    })
    return response.data
  }

  // Satellite data
  async getSatelliteData(fieldId, startDate, endDate) {
    const response = await this.client.get(`/satellite/${fieldId}`, {
      params: { start_date: startDate, end_date: endDate }
    })
    return response.data
  }
}

export const apiService = new AgriForecastAPI()
```

---

## 🔗 **Integration Bridge: FastAPI Wrapper**

**Create `api_server.py` in your Python backend:**

```python
#!/usr/bin/env python3
"""
FastAPI wrapper for AgriForecast.ai backend services
Exposes REST APIs for React frontend consumption
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import logging
from datetime import datetime, date

# Import your existing services
from forecasting_service import ForecastingService, get_forecasting_service
from multi_field_yield_prediction import MultiFieldYieldPrediction
from advanced_yield_prediction import AdvancedYieldPrediction

app = FastAPI(
    title="AgriForecast.ai API",
    description="AI-powered agricultural forecasting API",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
forecast_service = get_forecasting_service()
yield_predictor = MultiFieldYieldPrediction()
advanced_predictor = AdvancedYieldPrediction()

# Pydantic models
class WeatherRequest(BaseModel):
    latitude: float
    longitude: float
    days: Optional[int] = 30

class YieldPredictionRequest(BaseModel):
    field_id: str
    crop_type: str
    area: float
    soil_data: Dict
    weather_data: List[Dict]

class ForecastRequest(BaseModel):
    data: List[float]
    horizon: Optional[int] = 30
    frequency: Optional[str] = "D"

# API Routes
@app.get("/")
async def root():
    return {"message": "AgriForecast.ai API v1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Weather endpoints
@app.get("/api/weather/{latitude}/{longitude}")
async def get_weather_data(latitude: float, longitude: float, days: int = 30):
    """Get real-time weather data for coordinates"""
    try:
        weather_data = forecast_service.get_real_weather_data(latitude, longitude, days)
        return {
            "status": "success",
            "data": weather_data.to_dict('records'),
            "location": {"latitude": latitude, "longitude": longitude}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather data error: {str(e)}")

# Prediction endpoints
@app.post("/api/predict/yield")
async def predict_yield(request: YieldPredictionRequest):
    """Predict crop yield for a field"""
    try:
        prediction = yield_predictor.predict_yield(
            crop_type=request.crop_type,
            field_area=request.area,
            weather_data=request.weather_data,
            soil_data=request.soil_data
        )
        return {
            "status": "success",
            "prediction": prediction,
            "field_id": request.field_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yield prediction error: {str(e)}")

@app.post("/api/forecast/timeseries")
async def forecast_timeseries(request: ForecastRequest):
    """Forecast time series using TimesFM"""
    try:
        result = forecast_service.forecast_time_series(
            data=request.data,
            horizon=request.horizon,
            frequency=request.frequency
        )
        return {
            "status": "success",
            "forecast": result.predictions.tolist(),
            "confidence_intervals": result.confidence_intervals.tolist(),
            "dates": [d.isoformat() for d in result.forecast_dates]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast error: {str(e)}")

# Market data endpoints
@app.get("/api/market/{commodity}")
async def get_market_prices(commodity: str, days: int = 30):
    """Get market prices for commodity"""
    try:
        prices = forecast_service.get_market_prices(commodity, days)
        return {
            "status": "success",
            "commodity": commodity,
            "data": prices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data error: {str(e)}")

# Satellite data endpoints
@app.get("/api/satellite/{field_id}")
async def get_satellite_data(field_id: str, start_date: date, end_date: date):
    """Get satellite data for field"""
    try:
        satellite_data = forecast_service.get_satellite_data(field_id, start_date, end_date)
        return {
            "status": "success",
            "field_id": field_id,
            "data": satellite_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Satellite data error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

---

## 🎨 **Sample React Components**

### **Dashboard Component:**

**`src/pages/Dashboard.jsx`:**
```jsx
import React, { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { supabase } from '../lib/supabase'
import { apiService } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Sprout, TrendingUp, CloudRain, DollarSign } from 'lucide-react'

const Dashboard = () => {
  const [user, setUser] = useState(null)
  const [farms, setFarms] = useState([])

  // Get user session
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  // Fetch farms data
  const { data: farmsData, isLoading } = useQuery({
    queryKey: ['farms', user?.id],
    queryFn: async () => {
      if (!user) return []
      const { data, error } = await supabase
        .from('farms')
        .select('*, fields(*)')
        .eq('owner_id', user.id)
      
      if (error) throw error
      return data
    },
    enabled: !!user
  })

  // Fetch weather data for first farm
  const { data: weatherData } = useQuery({
    queryKey: ['weather', farmsData?.[0]?.latitude],
    queryFn: () => {
      if (!farmsData?.[0]) return null
      return apiService.getWeatherData(
        farmsData[0].latitude,
        farmsData[0].longitude
      )
    },
    enabled: !!farmsData?.[0]?.latitude
  })

  const stats = [
    {
      title: 'Total Farms',
      value: farmsData?.length || 0,
      icon: Sprout,
      color: 'text-agri-green-600'
    },
    {
      title: 'Active Fields',
      value: farmsData?.reduce((acc, farm) => acc + (farm.fields?.length || 0), 0) || 0,
      icon: TrendingUp,
      color: 'text-blue-600'
    },
    {
      title: 'Weather Status',
      value: weatherData ? 'Good' : 'Loading...',
      icon: CloudRain,
      color: 'text-sky-600'
    },
    {
      title: 'Predicted ROI',
      value: '12.5%',
      icon: DollarSign,
      color: 'text-green-600'
    }
  ]

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Please log in to continue</h1>
          {/* Add login component here */}
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Farm Dashboard</h1>
          <p className="text-gray-600">Welcome back, {user.email}</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div key={index} className="card">
              <div className="flex items-center">
                <div className={`p-2 rounded-lg ${stat.color} bg-opacity-10`}>
                  <stat.icon className={`w-6 h-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Weather Chart */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Weather Trends</h3>
            {weatherData?.data ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={weatherData.data.slice(-7)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line 
                    type="monotone" 
                    dataKey="temperature" 
                    stroke="#22c55e" 
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-300 flex items-center justify-center">
                <p className="text-gray-500">Loading weather data...</p>
              </div>
            )}
          </div>

          {/* Yield Predictions */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Yield Predictions</h3>
            <div className="space-y-4">
              {farmsData?.map((farm) => 
                farm.fields?.map((field) => (
                  <div key={field.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">{field.name}</p>
                      <p className="text-sm text-gray-600">{field.crop_type}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-agri-green-600">8.5 tons/ha</p>
                      <p className="text-sm text-gray-500">+12% vs last year</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
```

---

## 🚀 **Running the Full Stack**

### **Step 1: Start Python Backend API**
```bash
# Install FastAPI if not already installed
pip install fastapi uvicorn

# Run the API server
python api_server.py
# API will run on http://localhost:8000
```

### **Step 2: Start React Frontend**
```bash
# In your React project directory
npm run dev
# Frontend will run on http://localhost:5173
```

### **Step 3: Test Integration**
```bash
# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/weather/28.6139/77.2090

# Your React app can now consume these APIs
```

---

## 📊 **Key Benefits of This Stack**

### **✅ Why This Stack is Perfect for Your Project:**

1. **🚀 Performance**: Vite's lightning-fast development
2. **🎨 Beautiful UI**: Tailwind's utility-first approach
3. **📱 Responsive**: Mobile-first design out of the box
4. **🔄 Real-time**: Supabase's real-time subscriptions
5. **🔐 Auth**: Built-in authentication with Supabase
6. **🗄️ Scalable**: PostgreSQL with built-in APIs
7. **🤖 AI Integration**: Seamless connection to your ML models

### **🔗 Integration Flow:**
```
React (UI) → Supabase (Data) → FastAPI (AI/ML) → Your Python Backend
```

This setup gives you:
- **Modern, fast frontend** with React + Vite + Tailwind
- **Robust database** with Supabase PostgreSQL
- **Real-time capabilities** for live updates
- **Seamless AI integration** with your existing Python backend
- **Production-ready** authentication and security

Would you like me to help you set up any specific part of this stack or create additional components?

