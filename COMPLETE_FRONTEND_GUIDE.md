# 🚀 Complete Frontend Development Guide

## 📋 **Project Overview**

You're building a **React + Vite + Tailwind + Supabase** frontend for your AI/ML agricultural platform. Here's everything you need to know.

---

## 🏗️ **Architecture & Data Flow**

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR REACT FRONTEND                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Dashboard     │  │  Field Mgmt     │  │   Analytics     │ │
│  │   - Overview    │  │  - Add Fields   │  │   - Charts      │ │
│  │   - Weather     │  │  - View Fields  │  │   - Predictions │ │
│  │   - Quick Stats │  │  - Crop Info    │  │   - Reports     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SUPABASE DATABASE                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │     Users       │  │     Farms       │  │     Fields      │ │
│  │  - Auth         │  │  - Farm Info    │  │  - Field Data   │ │
│  │  - Profiles     │  │  - Location     │  │  - Crop Types   │ │
│  │  - Permissions  │  │  - Ownership    │  │  - Coordinates  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Weather Data   │  │   Predictions   │  │   Activities    │ │
│  │  - Temperature  │  │  - Yield Pred   │  │  - Field Work   │ │
│  │  - Humidity     │  │  - Weather Fcst │  │  - Costs        │ │
│  │  - Precipitation│  │  - Market Price │  │  - Notes        │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FASTAPI BACKEND (Your AI/ML)                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │    TimesFM      │  │  Weather APIs   │  │  Market Data    │ │
│  │  - Forecasting  │  │  - OpenWeather  │  │  - Commodity    │ │
│  │  - Time Series  │  │  - NASA APIs    │  │  - Price Trends │ │
│  │  - Predictions  │  │  - Real-time    │  │  - Volume Data  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Yield Prediction│  │ Satellite Data  │  │   ML Models     │ │
│  │  - Crop Models  │  │  - NDVI Data    │  │  - Scikit-learn │ │
│  │  - Multi-field  │  │  - Soil Health  │  │  - TensorFlow   │ │
│  │  - Advanced AI  │  │  - Crop Monitor │  │  - Custom Models│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **1. PROJECT SETUP**

### **Step 1: Create React Project**
```bash
# Create new Vite + React project
npm create vite@latest agriforecast-frontend -- --template react
cd agriforecast-frontend

# Install core dependencies
npm install

# Install additional packages
npm install @supabase/supabase-js
npm install react-router-dom
npm install @tanstack/react-query
npm install axios
npm install lucide-react
npm install recharts
npm install react-hook-form
npm install @hookform/resolvers
npm install yup
npm install react-hot-toast
npm install framer-motion

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npm install @tailwindcss/forms @tailwindcss/typography
npx tailwindcss init -p
```

### **Step 2: Project Structure**
```
agriforecast-frontend/
├── public/
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── ui/              # Basic UI elements
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Modal.jsx
│   │   │   └── Loading.jsx
│   │   ├── forms/           # Form components
│   │   │   ├── FarmForm.jsx
│   │   │   ├── FieldForm.jsx
│   │   │   └── LoginForm.jsx
│   │   ├── charts/          # Chart components
│   │   │   ├── WeatherChart.jsx
│   │   │   ├── YieldChart.jsx
│   │   │   └── PriceChart.jsx
│   │   └── layout/          # Layout components
│   │       ├── Navbar.jsx
│   │       ├── Sidebar.jsx
│   │       └── Layout.jsx
│   ├── pages/               # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Farms.jsx
│   │   ├── Fields.jsx
│   │   ├── Analytics.jsx
│   │   ├── Weather.jsx
│   │   ├── Predictions.jsx
│   │   └── Settings.jsx
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.js
│   │   ├── useFarms.js
│   │   ├── useFields.js
│   │   └── useWeather.js
│   ├── services/            # API services
│   │   ├── supabase.js
│   │   ├── api.js
│   │   └── auth.js
│   ├── utils/               # Utility functions
│   │   ├── helpers.js
│   │   ├── constants.js
│   │   └── validators.js
│   ├── store/               # State management
│   │   ├── authStore.js
│   │   └── appStore.js
│   ├── styles/              # CSS files
│   │   ├── globals.css
│   │   └── components.css
│   ├── App.jsx              # Main App component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── .env.local               # Environment variables
├── package.json
├── tailwind.config.js
├── vite.config.js
└── README.md
```

---

## 🎨 **2. TAILWIND CSS CONFIGURATION**

### **tailwind.config.js**
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
        // Agricultural color palette
        'agri': {
          'green': {
            50: '#f0fdf4',
            100: '#dcfce7',
            200: '#bbf7d0',
            300: '#86efac',
            400: '#4ade80',
            500: '#22c55e',
            600: '#16a34a',
            700: '#15803d',
            800: '#166534',
            900: '#14532d',
          },
          'brown': {
            50: '#fefaf6',
            100: '#fef3e2',
            200: '#fce4c0',
            300: '#f9d194',
            400: '#f5b866',
            500: '#f1a144',
            600: '#e58b29',
            700: '#bf7024',
            800: '#985a24',
            900: '#7c4b21',
          },
          'blue': {
            50: '#eff6ff',
            100: '#dbeafe',
            200: '#bfdbfe',
            300: '#93c5fd',
            400: '#60a5fa',
            500: '#3b82f6',
            600: '#2563eb',
            700: '#1d4ed8',
            800: '#1e40af',
            900: '#1e3a8a',
          }
        },
        // Status colors
        'success': '#22c55e',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'info': '#3b82f6',
      },
      fontFamily: {
        'sans': ['Inter', 'ui-sans-serif', 'system-ui'],
        'display': ['Poppins', 'ui-sans-serif', 'system-ui'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### **src/index.css**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap');

@layer base {
  * {
    @apply border-border;
  }
  
  body {
    @apply bg-gray-50 text-gray-900 font-sans;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
  
  h1, h2, h3, h4, h5, h6 {
    @apply font-display font-semibold;
  }
}

@layer components {
  /* Button Components */
  .btn {
    @apply inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed;
  }
  
  .btn-primary {
    @apply bg-agri-green-600 text-white hover:bg-agri-green-700 focus:ring-agri-green-500 shadow-sm;
  }
  
  .btn-secondary {
    @apply bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 focus:ring-agri-green-500 shadow-sm;
  }
  
  .btn-danger {
    @apply bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 shadow-sm;
  }
  
  .btn-sm {
    @apply px-3 py-1.5 text-sm;
  }
  
  .btn-md {
    @apply px-4 py-2 text-sm;
  }
  
  .btn-lg {
    @apply px-6 py-3 text-base;
  }
  
  /* Card Components */
  .card {
    @apply bg-white rounded-xl border border-gray-200 shadow-soft;
  }
  
  .card-header {
    @apply px-6 py-4 border-b border-gray-200;
  }
  
  .card-body {
    @apply px-6 py-4;
  }
  
  .card-footer {
    @apply px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-xl;
  }
  
  /* Form Components */
  .form-group {
    @apply space-y-2;
  }
  
  .form-label {
    @apply block text-sm font-medium text-gray-700;
  }
  
  .form-input {
    @apply block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm placeholder-gray-400 focus:border-agri-green-500 focus:ring-agri-green-500 sm:text-sm;
  }
  
  .form-select {
    @apply block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-agri-green-500 focus:ring-agri-green-500 sm:text-sm;
  }
  
  .form-error {
    @apply text-sm text-red-600;
  }
  
  /* Status Badges */
  .badge {
    @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium;
  }
  
  .badge-success {
    @apply bg-green-100 text-green-800;
  }
  
  .badge-warning {
    @apply bg-yellow-100 text-yellow-800;
  }
  
  .badge-error {
    @apply bg-red-100 text-red-800;
  }
  
  .badge-info {
    @apply bg-blue-100 text-blue-800;
  }
  
  /* Loading States */
  .skeleton {
    @apply animate-pulse bg-gray-200 rounded;
  }
  
  /* Agricultural Theme Utilities */
  .bg-gradient-agri {
    @apply bg-gradient-to-br from-agri-green-400 to-agri-green-600;
  }
  
  .text-gradient-agri {
    @apply bg-gradient-to-r from-agri-green-600 to-agri-green-700 bg-clip-text text-transparent;
  }
}

@layer utilities {
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}
```

---

## 🔧 **3. ENVIRONMENT CONFIGURATION**

### **.env.local**
```env
# Supabase Configuration
VITE_SUPABASE_URL=your_supabase_project_url_here
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Backend API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# App Configuration
VITE_APP_NAME=AgriForecast.ai
VITE_APP_VERSION=1.0.0
VITE_APP_ENVIRONMENT=development

# Optional: Third-party service keys
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_key
VITE_WEATHER_API_KEY=your_weather_api_key
```

---

## 🗄️ **4. SUPABASE DATABASE SCHEMA**

### **Tables to Create in Supabase SQL Editor:**

```sql
-- Enable Row Level Security
ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON FUNCTIONS FROM anon;

-- 1. Profiles table (extends auth.users)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE,
  full_name TEXT,
  avatar_url TEXT,
  phone TEXT,
  role TEXT DEFAULT 'farmer' CHECK (role IN ('farmer', 'admin', 'consultant')),
  subscription_tier TEXT DEFAULT 'free' CHECK (subscription_tier IN ('free', 'pro', 'enterprise')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Farms table
CREATE TABLE farms (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  location TEXT,
  address TEXT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  total_area DECIMAL(10, 2), -- in hectares
  farm_type TEXT, -- 'crop', 'livestock', 'mixed'
  owner_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Fields table
CREATE TABLE fields (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  farm_id UUID REFERENCES farms(id) ON DELETE CASCADE,
  area DECIMAL(10, 2) NOT NULL, -- in hectares
  crop_type TEXT,
  crop_variety TEXT,
  planting_date DATE,
  expected_harvest_date DATE,
  soil_type TEXT,
  irrigation_type TEXT CHECK (irrigation_type IN ('rainfed', 'drip', 'sprinkler', 'flood')),
  coordinates JSONB, -- GeoJSON polygon
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'fallow', 'harvested')),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Weather data table
CREATE TABLE weather_data (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  field_id UUID REFERENCES fields(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  temperature_max DECIMAL(5, 2),
  temperature_min DECIMAL(5, 2),
  temperature_avg DECIMAL(5, 2),
  humidity DECIMAL(5, 2),
  precipitation DECIMAL(8, 2), -- mm
  wind_speed DECIMAL(5, 2), -- km/h
  wind_direction INTEGER, -- degrees
  pressure DECIMAL(8, 2), -- hPa
  solar_radiation DECIMAL(8, 2), -- MJ/m²
  data_source TEXT DEFAULT 'api', -- 'api', 'manual', 'sensor'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(field_id, date)
);

-- 5. Predictions table
CREATE TABLE predictions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  field_id UUID REFERENCES fields(id) ON DELETE CASCADE,
  prediction_type TEXT NOT NULL CHECK (prediction_type IN ('yield', 'weather', 'price', 'disease', 'pest')),
  predicted_value DECIMAL(12, 4),
  unit TEXT, -- 'tons/ha', 'kg/ha', 'USD/ton', etc.
  confidence_score DECIMAL(3, 2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
  prediction_date DATE NOT NULL,
  forecast_horizon INTEGER, -- days ahead
  model_name TEXT,
  model_version TEXT,
  input_data JSONB, -- store input parameters
  metadata JSONB, -- additional model info
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Activities table
CREATE TABLE activities (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  field_id UUID REFERENCES fields(id) ON DELETE CASCADE,
  activity_type TEXT NOT NULL CHECK (activity_type IN ('planting', 'fertilizing', 'watering', 'harvesting', 'weeding', 'pest_control', 'soil_testing')),
  description TEXT,
  date DATE NOT NULL,
  cost DECIMAL(10, 2),
  currency TEXT DEFAULT 'USD',
  quantity DECIMAL(10, 2),
  unit TEXT, -- 'kg', 'liters', 'hours', etc.
  weather_conditions TEXT,
  notes TEXT,
  images JSONB, -- array of image URLs
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Market data table
CREATE TABLE market_data (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  commodity TEXT NOT NULL,
  market_name TEXT,
  date DATE NOT NULL,
  price DECIMAL(10, 4),
  currency TEXT DEFAULT 'USD',
  unit TEXT DEFAULT 'ton', -- 'ton', 'kg', 'quintal'
  volume DECIMAL(12, 2),
  price_change DECIMAL(8, 4), -- vs previous day
  data_source TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(commodity, market_name, date)
);

-- 8. Alerts table
CREATE TABLE alerts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  field_id UUID REFERENCES fields(id) ON DELETE CASCADE,
  alert_type TEXT NOT NULL CHECK (alert_type IN ('weather', 'pest', 'disease', 'irrigation', 'harvest', 'market')),
  severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  is_read BOOLEAN DEFAULT FALSE,
  action_required BOOLEAN DEFAULT FALSE,
  action_url TEXT,
  expires_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. Soil data table
CREATE TABLE soil_data (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  field_id UUID REFERENCES fields(id) ON DELETE CASCADE,
  test_date DATE NOT NULL,
  ph DECIMAL(3, 1),
  organic_matter DECIMAL(5, 2), -- percentage
  nitrogen DECIMAL(8, 2), -- kg/ha
  phosphorus DECIMAL(8, 2), -- kg/ha
  potassium DECIMAL(8, 2), -- kg/ha
  calcium DECIMAL(8, 2), -- kg/ha
  magnesium DECIMAL(8, 2), -- kg/ha
  sulfur DECIMAL(8, 2), -- kg/ha
  zinc DECIMAL(8, 2), -- ppm
  iron DECIMAL(8, 2), -- ppm
  manganese DECIMAL(8, 2), -- ppm
  copper DECIMAL(8, 2), -- ppm
  boron DECIMAL(8, 2), -- ppm
  electrical_conductivity DECIMAL(6, 2), -- dS/m
  cation_exchange_capacity DECIMAL(6, 2), -- cmol/kg
  lab_name TEXT,
  test_method TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_farms_owner_id ON farms(owner_id);
CREATE INDEX idx_fields_farm_id ON fields(farm_id);
CREATE INDEX idx_weather_data_field_date ON weather_data(field_id, date);
CREATE INDEX idx_predictions_field_type ON predictions(field_id, prediction_type);
CREATE INDEX idx_activities_field_date ON activities(field_id, date);
CREATE INDEX idx_market_data_commodity_date ON market_data(commodity, date);
CREATE INDEX idx_alerts_field_read ON alerts(field_id, is_read);
CREATE INDEX idx_soil_data_field_date ON soil_data(field_id, test_date);

-- Row Level Security Policies
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE farms ENABLE ROW LEVEL SECURITY;
ALTER TABLE fields ENABLE ROW LEVEL SECURITY;
ALTER TABLE weather_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE market_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE soil_data ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

-- Farms policies
CREATE POLICY "Users can view own farms" ON farms FOR SELECT USING (auth.uid() = owner_id);
CREATE POLICY "Users can insert own farms" ON farms FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "Users can update own farms" ON farms FOR UPDATE USING (auth.uid() = owner_id);
CREATE POLICY "Users can delete own farms" ON farms FOR DELETE USING (auth.uid() = owner_id);

-- Fields policies
CREATE POLICY "Users can view own fields" ON fields FOR SELECT USING (
  EXISTS (SELECT 1 FROM farms WHERE farms.id = fields.farm_id AND farms.owner_id = auth.uid())
);
CREATE POLICY "Users can insert own fields" ON fields FOR INSERT WITH CHECK (
  EXISTS (SELECT 1 FROM farms WHERE farms.id = fields.farm_id AND farms.owner_id = auth.uid())
);
CREATE POLICY "Users can update own fields" ON fields FOR UPDATE USING (
  EXISTS (SELECT 1 FROM farms WHERE farms.id = fields.farm_id AND farms.owner_id = auth.uid())
);
CREATE POLICY "Users can delete own fields" ON fields FOR DELETE USING (
  EXISTS (SELECT 1 FROM farms WHERE farms.id = fields.farm_id AND farms.owner_id = auth.uid())
);

-- Similar policies for other tables...
-- (I'll provide the complete policies if you need them)

-- Functions and triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all tables with updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_farms_updated_at BEFORE UPDATE ON farms FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_fields_updated_at BEFORE UPDATE ON fields FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 🔌 **5. API ENDPOINTS DOCUMENTATION**

### **Your Backend API Endpoints (FastAPI)**

```javascript
// Base URL: http://localhost:8000

// Authentication & Users
GET    /api/health                          // Health check
GET    /api/users/profile                   // Get user profile
PUT    /api/users/profile                   // Update user profile

// Farm Management
GET    /api/farms                           // Get all farms for user
POST   /api/farms                           // Create new farm
GET    /api/farms/{farm_id}                 // Get specific farm
PUT    /api/farms/{farm_id}                 // Update farm
DELETE /api/farms/{farm_id}                 // Delete farm

// Field Management
GET    /api/fields                          // Get all fields for user
GET    /api/fields?farm_id={farm_id}        // Get fields for specific farm
POST   /api/fields                          // Create new field
GET    /api/fields/{field_id}               // Get specific field
PUT    /api/fields/{field_id}               // Update field
DELETE /api/fields/{field_id}               // Delete field

// Weather Data
GET    /api/weather/{latitude}/{longitude}  // Get weather for coordinates
GET    /api/weather/field/{field_id}        // Get weather for field
POST   /api/weather/batch                   // Bulk weather data update

// Predictions & AI
POST   /api/predict/yield                   // Predict crop yield
POST   /api/predict/weather                 // Weather forecasting
POST   /api/predict/price                   // Market price prediction
POST   /api/forecast/timeseries             // TimesFM forecasting

// Market Data
GET    /api/market/{commodity}              // Get market prices
GET    /api/market/trends/{commodity}       // Get price trends
POST   /api/market/alerts                   // Set price alerts

// Analytics
GET    /api/analytics/dashboard             // Dashboard summary
GET    /api/analytics/yield-trends          // Yield trend analysis
GET    /api/analytics/weather-patterns      // Weather pattern analysis
GET    /api/analytics/cost-benefit          // Cost-benefit analysis

// Satellite & Remote Sensing
GET    /api/satellite/{field_id}            // Satellite data for field
GET    /api/satellite/ndvi/{field_id}       // NDVI data
GET    /api/satellite/soil-moisture/{field_id} // Soil moisture data

// Activities & Operations
GET    /api/activities                      // Get field activities
POST   /api/activities                      // Log new activity
GET    /api/activities/costs                // Activity cost analysis

// Alerts & Notifications
GET    /api/alerts                          // Get user alerts
POST   /api/alerts/mark-read               // Mark alerts as read
DELETE /api/alerts/{alert_id}              // Delete alert

// Reports & Export
GET    /api/reports/generate/{type}         // Generate reports
GET    /api/export/data/{format}           // Export data (CSV, PDF)
```

### **Request/Response Examples**

```javascript
// Example: Create Farm
POST /api/farms
{
  "name": "Green Valley Farm",
  "location": "Punjab, India",
  "latitude": 30.7333,
  "longitude": 76.7794,
  "total_area": 25.5,
  "farm_type": "crop"
}

// Response:
{
  "status": "success",
  "data": {
    "id": "uuid-here",
    "name": "Green Valley Farm",
    "location": "Punjab, India",
    "latitude": 30.7333,
    "longitude": 76.7794,
    "total_area": 25.5,
    "farm_type": "crop",
    "owner_id": "user-uuid",
    "created_at": "2024-01-01T00:00:00Z"
  }
}

// Example: Get Yield Prediction
POST /api/predict/yield
{
  "field_id": "field-uuid",
  "crop_type": "wheat",
  "area": 5.0,
  "soil_data": {
    "ph": 6.8,
    "nitrogen": 120,
    "phosphorus": 45,
    "potassium": 180
  },
  "weather_data": [
    {
      "date": "2024-01-01",
      "temperature": 22.5,
      "humidity": 65,
      "precipitation": 2.3
    }
  ]
}

// Response:
{
  "status": "success",
  "prediction": {
    "predicted_yield": 18.5,
    "confidence": 0.85,
    "yield_per_hectare": 3.7,
    "factors": {
      "weather_impact": 0.15,
      "soil_impact": 0.25,
      "crop_variety_impact": 0.10
    }
  },
  "field_id": "field-uuid"
}
```

---

## ⚛️ **6. REACT SERVICES & HOOKS**

### **src/services/supabase.js**
```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  },
  realtime: {
    params: {
      eventsPerSecond: 2
    }
  }
})

// Database helper functions
export const dbHelpers = {
  // Get user's farms
  async getFarms(userId) {
    const { data, error } = await supabase
      .from('farms')
      .select(`
        *,
        fields (
          id, name, area, crop_type, status
        )
      `)
      .eq('owner_id', userId)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Get fields for a farm
  async getFields(farmId) {
    const { data, error } = await supabase
      .from('fields')
      .select('*')
      .eq('farm_id', farmId)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Get weather data for a field
  async getWeatherData(fieldId, days = 30) {
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)
    
    const { data, error } = await supabase
      .from('weather_data')
      .select('*')
      .eq('field_id', fieldId)
      .gte('date', startDate.toISOString().split('T')[0])
      .order('date', { ascending: true })
    
    if (error) throw error
    return data
  },

  // Get predictions for a field
  async getPredictions(fieldId, type = null) {
    let query = supabase
      .from('predictions')
      .select('*')
      .eq('field_id', fieldId)
    
    if (type) {
      query = query.eq('prediction_type', type)
    }
    
    const { data, error } = await query
      .order('created_at', { ascending: false })
      .limit(50)
    
    if (error) throw error
    return data
  },

  // Get activities for a field
  async getActivities(fieldId, limit = 50) {
    const { data, error } = await supabase
      .from('activities')
      .select('*')
      .eq('field_id', fieldId)
      .order('date', { ascending: false })
      .limit(limit)
    
    if (error) throw error
    return data
  },

  // Get alerts for user
  async getAlerts(userId) {
    const { data, error } = await supabase
      .from('alerts')
      .select(`
        *,
        fields!inner (
          name,
          farms!inner (
            owner_id
          )
        )
      `)
      .eq('fields.farms.owner_id', userId)
      .eq('is_read', false)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  }
}
```

### **src/services/api.js**
```javascript
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_TIMEOUT = parseInt(import.meta.env.VITE_API_TIMEOUT) || 30000

class AgriForecastAPI {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      }
    })

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem('supabase_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data || error.message)
        return Promise.reject(error)
      }
    )
  }

  // Health check
  async healthCheck() {
    const response = await this.client.get('/api/health')
    return response.data
  }

  // Weather services
  async getWeatherData(latitude, longitude, days = 30) {
    const response = await this.client.get(`/api/weather/${latitude}/${longitude}`, {
      params: { days }
    })
    return response.data
  }

  async getFieldWeather(fieldId) {
    const response = await this.client.get(`/api/weather/field/${fieldId}`)
    return response.data
  }

  // Prediction services
  async predictYield(fieldData) {
    const response = await this.client.post('/api/predict/yield', fieldData)
    return response.data
  }

  async forecastWeather(locationData) {
    const response = await this.client.post('/api/predict/weather', locationData)
    return response.data
  }

  async predictPrice(commodity, data) {
    const response = await this.client.post('/api/predict/price', {
      commodity,
      ...data
    })
    return response.data
  }

  async forecastTimeSeries(data, horizon = 30, frequency = 'D') {
    const response = await this.client.post('/api/forecast/timeseries', {
      data,
      horizon,
      frequency
    })
    return response.data
  }

  // Market data services
  async getMarketPrices(commodity, days = 30) {
    const response = await this.client.get(`/api/market/${commodity}`, {
      params: { days }
    })
    return response.data
  }

  async getMarketTrends(commodity) {
    const response = await this.client.get(`/api/market/trends/${commodity}`)
    return response.data
  }

  // Satellite data services
  async getSatelliteData(fieldId, startDate, endDate) {
    const response = await this.client.get(`/api/satellite/${fieldId}`, {
      params: { start_date: startDate, end_date: endDate }
    })
    return response.data
  }

  async getNDVIData(fieldId) {
    const response = await this.client.get(`/api/satellite/ndvi/${fieldId}`)
    return response.data
  }

  // Analytics services
  async getDashboardAnalytics() {
    const response = await this.client.get('/api/analytics/dashboard')
    return response.data
  }

  async getYieldTrends(fieldId, period = 'year') {
    const response = await this.client.get('/api/analytics/yield-trends', {
      params: { field_id: fieldId, period }
    })
    return response.data
  }

  async getCostBenefitAnalysis(fieldId) {
    const response = await this.client.get('/api/analytics/cost-benefit', {
      params: { field_id: fieldId }
    })
    return response.data
  }

  // Activity services
  async getActivities(fieldId) {
    const response = await this.client.get('/api/activities', {
      params: { field_id: fieldId }
    })
    return response.data
  }

  async logActivity(activityData) {
    const response = await this.client.post('/api/activities', activityData)
    return response.data
  }

  // Report services
  async generateReport(type, params = {}) {
    const response = await this.client.get(`/api/reports/generate/${type}`, {
      params
    })
    return response.data
  }

  async exportData(format, filters = {}) {
    const response = await this.client.get(`/api/export/data/${format}`, {
      params: filters,
      responseType: format === 'pdf' ? 'blob' : 'json'
    })
    return response.data
  }
}

export const apiService = new AgriForecastAPI()
export default apiService
```

### **src/hooks/useAuth.js**
```javascript
import { useState, useEffect, createContext, useContext } from 'react'
import { supabase } from '../services/supabase'

const AuthContext = createContext({})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [profile, setProfile] = useState(null)

  useEffect(() => {
    // Get initial session
    const getInitialSession = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      setUser(session?.user ?? null)
      
      if (session?.user) {
        await fetchProfile(session.user.id)
      }
      
      setLoading(false)
    }

    getInitialSession()

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setUser(session?.user ?? null)
        
        if (session?.user) {
          await fetchProfile(session.user.id)
        } else {
          setProfile(null)
        }
        
        setLoading(false)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const fetchProfile = async (userId) => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single()

      if (error && error.code === 'PGRST116') {
        // Profile doesn't exist, create one
        await createProfile(userId)
      } else if (error) {
        throw error
      } else {
        setProfile(data)
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
    }
  }

  const createProfile = async (userId) => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .insert([
          {
            id: userId,
            username: user?.email?.split('@')[0] || '',
            full_name: user?.user_metadata?.full_name || '',
          }
        ])
        .select()
        .single()

      if (error) throw error
      setProfile(data)
    } catch (error) {
      console.error('Error creating profile:', error)
    }
  }

  const signIn = async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })
    return { data, error }
  }

  const signUp = async (email, password, userData = {}) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: userData
      }
    })
    return { data, error }
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    return { error }
  }

  const updateProfile = async (updates) => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .update(updates)
        .eq('id', user.id)
        .select()
        .single()

      if (error) throw error
      setProfile(data)
      return { data, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  const value = {
    user,
    profile,
    loading,
    signIn,
    signUp,
    signOut,
    updateProfile,
    fetchProfile
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
```

---

## 📱 **7. KEY COMPONENT EXAMPLES**

### **src/components/ui/Button.jsx**
```jsx
import React from 'react'
import { cn } from '../../utils/helpers'
import { Loader2 } from 'lucide-react'

const Button = React.forwardRef(({
  className,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  children,
  ...props
}, ref) => {
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    danger: 'btn-danger',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
    link: 'bg-transparent text-agri-green-600 hover:text-agri-green-700 underline focus:ring-agri-green-500'
  }

  const sizes = {
    sm: 'btn-sm',
    md: 'btn-md',
    lg: 'btn-lg'
  }

  return (
    <button
      className={cn(
        'btn',
        variants[variant],
        sizes[size],
        (loading || disabled) && 'opacity-50 cursor-not-allowed',
        className
      )}
      disabled={loading || disabled}
      ref={ref}
      {...props}
    >
      {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
      {children}
    </button>
  )
})

Button.displayName = "Button"

export default Button
```

### **src/components/ui/Card.jsx**
```jsx
import React from 'react'
import { cn } from '../../utils/helpers'

export const Card = ({ className, children, ...props }) => (
  <div className={cn('card', className)} {...props}>
    {children}
  </div>
)

export const CardHeader = ({ className, children, ...props }) => (
  <div className={cn('card-header', className)} {...props}>
    {children}
  </div>
)

export const CardBody = ({ className, children, ...props }) => (
  <div className={cn('card-body', className)} {...props}>
    {children}
  </div>
)

export const CardFooter = ({ className, children, ...props }) => (
  <div className={cn('card-footer', className)} {...props}>
    {children}
  </div>
)

export const CardTitle = ({ className, children, ...props }) => (
  <h3 className={cn('text-lg font-semibold text-gray-900', className)} {...props}>
    {children}
  </h3>
)

export const CardDescription = ({ className, children, ...props }) => (
  <p className={cn('text-sm text-gray-600', className)} {...props}>
    {children}
  </p>
)
```

### **src/pages/Dashboard.jsx**
```jsx
import React, { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useQuery } from '@tanstack/react-query'
import { supabase, dbHelpers } from '../services/supabase'
import { apiService } from '../services/api'
import { Card, CardHeader, CardBody, CardTitle, CardDescription } from '../components/ui/Card'
import Button from '../components/ui/Button'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { 
  Sprout, 
  TrendingUp, 
  CloudRain, 
  DollarSign, 
  MapPin, 
  Calendar,
  AlertTriangle,
  Activity
} from 'lucide-react'

const Dashboard = () => {
  const { user, profile } = useAuth()
  const [selectedTimeRange, setSelectedTimeRange] = useState('7d')

  // Fetch user's farms and fields
  const { data: farms, isLoading: farmsLoading } = useQuery({
    queryKey: ['farms', user?.id],
    queryFn: () => dbHelpers.getFarms(user.id),
    enabled: !!user?.id
  })

  // Fetch alerts
  const { data: alerts } = useQuery({
    queryKey: ['alerts', user?.id],
    queryFn: () => dbHelpers.getAlerts(user.id),
    enabled: !!user?.id
  })

  // Fetch weather data for first farm
  const { data: weatherData } = useQuery({
    queryKey: ['weather', farms?.[0]?.latitude],
    queryFn: () => {
      if (!farms?.[0]) return null
      return apiService.getWeatherData(
        farms[0].latitude,
        farms[0].longitude,
        parseInt(selectedTimeRange)
      )
    },
    enabled: !!farms?.[0]?.latitude
  })

  // Fetch dashboard analytics
  const { data: analytics } = useQuery({
    queryKey: ['analytics', 'dashboard'],
    queryFn: () => apiService.getDashboardAnalytics(),
    enabled: !!user?.id
  })

  // Calculate summary statistics
  const stats = [
    {
      title: 'Total Farms',
      value: farms?.length || 0,
      icon: Sprout,
      color: 'text-agri-green-600',
      bgColor: 'bg-agri-green-50',
      change: '+2 this month'
    },
    {
      title: 'Active Fields',
      value: farms?.reduce((acc, farm) => acc + (farm.fields?.length || 0), 0) || 0,
      icon: MapPin,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      change: '+1 this week'
    },
    {
      title: 'Weather Alerts',
      value: alerts?.filter(a => a.alert_type === 'weather')?.length || 0,
      icon: CloudRain,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
      change: '2 active'
    },
    {
      title: 'Predicted ROI',
      value: '12.5%',
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      change: '+2.3% vs last season'
    }
  ]

  // Prepare chart data
  const chartData = weatherData?.data?.slice(-7).map(item => ({
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    temperature: item.temperature_avg || item.temperature,
    humidity: item.humidity,
    precipitation: item.precipitation
  })) || []

  if (farmsLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-agri-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Welcome back, {profile?.full_name || profile?.username || 'Farmer'}! 👋
              </h1>
              <p className="text-gray-600 mt-1">
                Here's what's happening with your farms today
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <select 
                value={selectedTimeRange}
                onChange={(e) => setSelectedTimeRange(e.target.value)}
                className="form-select"
              >
                <option value="7">Last 7 days</option>
                <option value="14">Last 14 days</option>
                <option value="30">Last 30 days</option>
              </select>
              <Button>
                <Calendar className="w-4 h-4 mr-2" />
                Generate Report
              </Button>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card key={index} className="hover:shadow-medium transition-shadow">
              <CardBody>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                    <p className="text-xs text-gray-500 mt-1">{stat.change}</p>
                  </div>
                  <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                    <stat.icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>

        {/* Alerts Section */}
        {alerts && alerts.length > 0 && (
          <Card className="mb-8 border-l-4 border-l-yellow-400">
            <CardHeader>
              <CardTitle className="flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2 text-yellow-600" />
                Active Alerts ({alerts.length})
              </CardTitle>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {alerts.slice(0, 3).map((alert) => (
                  <div key={alert.id} className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">{alert.title}</p>
                      <p className="text-sm text-gray-600">{alert.message}</p>
                      <p className="text-xs text-gray-500">
                        {alert.fields?.name} • {new Date(alert.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <Button size="sm" variant="secondary">
                      View
                    </Button>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>
        )}

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Weather Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Weather Trends</CardTitle>
              <CardDescription>
                Temperature and precipitation for the last {selectedTimeRange} days
              </CardDescription>
            </CardHeader>
            <CardBody>
              {chartData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis yAxisId="temp" orientation="left" />
                    <YAxis yAxisId="precip" orientation="right" />
                    <Tooltip />
                    <Line 
                      yAxisId="temp"
                      type="monotone" 
                      dataKey="temperature" 
                      stroke="#22c55e" 
                      strokeWidth={2}
                      name="Temperature (°C)"
                    />
                    <Bar 
                      yAxisId="precip"
                      dataKey="precipitation" 
                      fill="#3b82f6" 
                      opacity={0.6}
                      name="Precipitation (mm)"
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-300 flex items-center justify-center">
                  <p className="text-gray-500">Loading weather data...</p>
                </div>
              )}
            </CardBody>
          </Card>

          {/* Yield Predictions */}
          <Card>
            <CardHeader>
              <CardTitle>Yield Predictions</CardTitle>
              <CardDescription>
                AI-powered yield forecasts for your fields
              </CardDescription>
            </CardHeader>
            <CardBody>
              <div className="space-y-4">
                {farms?.map((farm) => 
                  farm.fields?.map((field) => (
                    <div key={field.id} className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-medium text-gray-900">{field.name}</p>
                        <p className="text-sm text-gray-600">{field.crop_type} • {farm.name}</p>
                        <p className="text-xs text-gray-500">{field.area} hectares</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-agri-green-600">8.5 tons/ha</p>
                        <p className="text-sm text-green-600">+12% vs last year</p>
                        <p className="text-xs text-gray-500">85% confidence</p>
                      </div>
                    </div>
                  ))
                )}
                {(!farms || farms.length === 0) && (
                  <div className="text-center py-8">
                    <Sprout className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">No fields found</p>
                    <Button className="mt-4" size="sm">
                      Add Your First Field
                    </Button>
                  </div>
                )}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Activity className="w-5 h-5 mr-2" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardBody>
            <div className="space-y-4">
              {/* Mock activity data - replace with real data */}
              {[
                { type: 'fertilizing', field: 'North Field', date: '2 hours ago', cost: '$120' },
                { type: 'irrigation', field: 'South Field', date: '1 day ago', cost: '$45' },
                { type: 'pest_control', field: 'East Field', date: '3 days ago', cost: '$89' },
              ].map((activity, index) => (
                <div key={index} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-agri-green-500 rounded-full mr-3"></div>
                    <div>
                      <p className="font-medium text-gray-900 capitalize">
                        {activity.type.replace('_', ' ')}
                      </p>
                      <p className="text-sm text-gray-600">{activity.field}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">{activity.cost}</p>
                    <p className="text-xs text-gray-500">{activity.date}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard
```

---

## 🚀 **8. GETTING STARTED CHECKLIST**

### **Phase 1: Setup (Day 1-2)**
- [ ] Create React + Vite project
- [ ] Install all dependencies
- [ ] Set up Tailwind CSS configuration
- [ ] Create Supabase project and database
- [ ] Set up environment variables
- [ ] Create basic project structure

### **Phase 2: Core Components (Day 3-5)**
- [ ] Build authentication system
- [ ] Create UI components (Button, Card, Input, etc.)
- [ ] Set up routing with React Router
- [ ] Create layout components (Navbar, Sidebar)
- [ ] Build dashboard page structure

### **Phase 3: Data Integration (Day 6-8)**
- [ ] Connect to Supabase database
- [ ] Set up API service for backend integration
- [ ] Create custom hooks for data fetching
- [ ] Implement real-time subscriptions
- [ ] Add state management with React Query

### **Phase 4: Feature Implementation (Day 9-12)**
- [ ] Build farm management pages
- [ ] Create field management interface
- [ ] Add weather data visualization
- [ ] Implement prediction displays
- [ ] Create analytics dashboard

### **Phase 5: Polish & Deploy (Day 13-14)**
- [ ] Add loading states and error handling
- [ ] Implement responsive design
- [ ] Add charts and visualizations
- [ ] Test all functionality
- [ ] Deploy to production

---

## 📞 **INTEGRATION PLAN**

When you're ready to integrate, I'll help you:

1. **Connect your frontend to the FastAPI backend**
2. **Wire up all the API endpoints**
3. **Test the real-time data flow**
4. **Optimize the user experience**
5. **Deploy the complete stack**

**Start building your React frontend using this guide, and once you have the basic structure ready, share it with me. I'll help you connect everything together and make sure your AI/ML backend integrates seamlessly with your beautiful frontend! 🚀**

This gives you everything you need to build a production-ready agricultural platform that leverages all your existing AI/ML capabilities.

