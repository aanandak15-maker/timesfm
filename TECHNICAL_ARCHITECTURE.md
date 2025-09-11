# 🏗️ AgriForecast.ai - Technical Architecture

## **System Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGRIFORECAST.AI PLATFORM                │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React)          │  Backend (FastAPI)                │
│  ┌─────────────────────┐   │  ┌─────────────────────────────┐   │
│  │ Mobile Interface    │   │  │ API Server                  │   │
│  │ - Hindi/English     │   │  │ - Authentication            │   │
│  │ - Offline Support   │   │  │ - Data Processing           │   │
│  │ - GPS Integration   │   │  │ - AI Integration            │   │
│  │ - Voice Commands    │   │  │ - Real-time Updates         │   │
│  └─────────────────────┘   │  └─────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                        EXTERNAL APIs                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │ SoilGrids   │ │ OpenWeather │ │ NASA Earth  │ │ Alpha Vant. ││
│  │ (FREE)      │ │ (API Key)   │ │ (Token)     │ │ (API Key)   ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
│  ┌─────────────┐ ┌─────────────┐                               │
│  │ OpenStreet  │ │ Mapbox      │                               │
│  │ (FREE)      │ │ (Token)     │                               │
│  └─────────────┘ └─────────────┘                               │
├─────────────────────────────────────────────────────────────────┤
│                        AI/ML ENGINE                            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Google TimesFM Forecasting Model                           ││
│  │ - Yield Predictions                                        ││
│  │ - Weather Analysis                                          ││
│  │ - Crop Health Monitoring                                    ││
│  │ - Market Price Predictions                                  ││
│  └─────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│                        DATA STORAGE                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │ PostgreSQL  │ │ IndexedDB   │ │ LocalStorage│               │
│  │ (Production)│ │ (Offline)   │ │ (Settings)  │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## **Frontend Architecture**

### **Component Structure**
```
src/
├── components/
│   ├── agricultural/           # Agricultural-specific components
│   │   ├── FarmerReadySoilAnalysis.tsx
│   │   ├── WeatherWidget.tsx
│   │   ├── YieldPredictionCard.tsx
│   │   └── ...
│   ├── layout/                 # Layout components
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── MobileNav.tsx
│   └── common/                 # Reusable components
│       ├── Button.tsx
│       ├── Card.tsx
│       └── ...
├── pages/                      # Page components
│   ├── dashboard/
│   ├── fields/
│   ├── analytics/
│   └── settings/
├── services/                   # API services
│   ├── api.ts
│   ├── soilgridsApi.ts
│   ├── weatherApi.ts
│   └── ...
├── utils/                      # Utility functions
│   ├── translations.ts
│   ├── offlineStorage.ts
│   ├── gpsService.ts
│   └── ...
└── types/                      # TypeScript definitions
    ├── index.ts
    └── ...
```

### **State Management**
- **React Query**: Server state management
- **Context API**: Global state (user, settings)
- **Local State**: Component-level state
- **Offline Storage**: IndexedDB for offline data

## **Backend Architecture**

### **API Structure**
```
api_server_production.py
├── Authentication Endpoints
│   ├── POST /auth/login
│   ├── POST /auth/register
│   └── POST /auth/refresh
├── Farm Management
│   ├── GET /farms
│   ├── POST /farms
│   ├── PUT /farms/{id}
│   └── DELETE /farms/{id}
├── Field Operations
│   ├── GET /fields
│   ├── POST /fields
│   ├── PUT /fields/{id}
│   └── DELETE /fields/{id}
├── Agricultural Data
│   ├── GET /weather
│   ├── GET /soil-analysis
│   ├── GET /yield-prediction
│   └── GET /market-data
└── Health & Monitoring
    ├── GET /health
    ├── GET /status
    └── GET /metrics
```

### **Data Flow**
1. **User Input** → Frontend validation
2. **API Request** → Backend processing
3. **External APIs** → Data fetching
4. **AI Processing** → TimesFM analysis
5. **Response** → Frontend display
6. **Offline Sync** → Data persistence

## **Database Schema**

### **Core Tables**
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Farms table
CREATE TABLE farms (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    location POINT,
    area DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Fields table
CREATE TABLE fields (
    id UUID PRIMARY KEY,
    farm_id UUID REFERENCES farms(id),
    name VARCHAR(100) NOT NULL,
    crop_type VARCHAR(50),
    planting_date DATE,
    area DECIMAL(10,2),
    coordinates POLYGON,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Weather data table
CREATE TABLE weather_data (
    id UUID PRIMARY KEY,
    field_id UUID REFERENCES fields(id),
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    rainfall DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Soil analysis table
CREATE TABLE soil_analysis (
    id UUID PRIMARY KEY,
    field_id UUID REFERENCES fields(id),
    ph DECIMAL(3,1),
    organic_carbon DECIMAL(4,2),
    nitrogen DECIMAL(6,2),
    phosphorus DECIMAL(6,2),
    potassium DECIMAL(6,2),
    analyzed_at TIMESTAMP DEFAULT NOW()
);

-- Yield predictions table
CREATE TABLE yield_predictions (
    id UUID PRIMARY KEY,
    field_id UUID REFERENCES fields(id),
    predicted_yield DECIMAL(8,2),
    confidence_interval JSONB,
    factors JSONB,
    predicted_at TIMESTAMP DEFAULT NOW()
);
```

## **API Integration Architecture**

### **External API Services**
```typescript
// SoilGrids API (FREE)
class SoilGridsService {
  async getSoilData(lat: number, lon: number): Promise<SoilData>
  async getSoilProperties(bbox: BoundingBox): Promise<SoilProperties>
}

// OpenWeatherMap API
class WeatherService {
  async getCurrentWeather(lat: number, lon: number): Promise<WeatherData>
  async getForecast(lat: number, lon: number): Promise<ForecastData>
  async getHistoricalWeather(lat: number, lon: number, date: string): Promise<HistoricalWeather>
}

// NASA Earthdata API
class NasaService {
  async getSatelliteImages(lat: number, lon: number): Promise<SatelliteImage[]>
  async getNDVIData(bbox: BoundingBox): Promise<NDVIData>
  async getLandsatData(lat: number, lon: number): Promise<LandsatData>
}

// Alpha Vantage API
class MarketService {
  async getCommodityPrices(symbol: string): Promise<PriceData>
  async getPriceHistory(symbol: string, period: string): Promise<PriceHistory>
  async getMarketTrends(symbol: string): Promise<TrendData>
}
```

## **AI/ML Pipeline**

### **TimesFM Integration**
```python
class TimesFMPredictor:
    def __init__(self):
        self.model = load_timesfm_model()
        self.preprocessor = DataPreprocessor()
    
    def predict_yield(self, field_data: FieldData) -> YieldPrediction:
        # Prepare input data
        input_data = self.preprocessor.prepare_data(field_data)
        
        # Run TimesFM prediction
        prediction = self.model.predict(input_data)
        
        # Post-process results
        return self.postprocess_prediction(prediction)
    
    def predict_weather_impact(self, weather_data: WeatherData) -> WeatherImpact:
        # Analyze weather patterns
        impact = self.model.analyze_weather(weather_data)
        return impact
```

### **Data Processing Pipeline**
1. **Data Collection** → External APIs
2. **Data Validation** → Input validation
3. **Data Preprocessing** → Feature engineering
4. **Model Inference** → TimesFM prediction
5. **Post-processing** → Result formatting
6. **Storage** → Database persistence

## **Offline Architecture**

### **Service Worker**
```javascript
// sw.js
self.addEventListener('install', (event) => {
  // Cache resources for offline use
});

self.addEventListener('fetch', (event) => {
  // Serve from cache when offline
});

self.addEventListener('sync', (event) => {
  // Sync data when online
});
```

### **Offline Storage**
```typescript
class OfflineStorage {
  async saveData(type: DataType, data: any): Promise<string>
  async getData(type: DataType): Promise<OfflineData[]>
  async syncData(): Promise<void>
  async clearSyncedData(): Promise<void>
}
```

## **Deployment Architecture**

### **Frontend (Vercel)**
- **Build**: Vite production build
- **CDN**: Global edge locations
- **SSL**: Automatic HTTPS
- **Domains**: Custom domain support

### **Backend (Render)**
- **Runtime**: Python 3.11
- **Server**: Uvicorn ASGI server
- **Database**: PostgreSQL
- **Monitoring**: Built-in health checks

### **Environment Variables**
```bash
# Frontend (.env)
VITE_API_URL=https://timesfm.onrender.com
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-supabase-key
VITE_OPENWEATHER_API_KEY=your-openweather-key
VITE_ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
VITE_NASA_API_KEY=your-nasa-token
VITE_MAPBOX_API_KEY=your-mapbox-token

# Backend (Render)
DATABASE_URL=postgresql://...
OPENWEATHER_API_KEY=your-openweather-key
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
NASA_API_KEY=your-nasa-token
MAPBOX_API_KEY=your-mapbox-token
```

## **Security Architecture**

### **Authentication**
- **JWT Tokens**: Secure user authentication
- **Phone OTP**: Mobile number verification
- **Session Management**: Secure session handling

### **API Security**
- **CORS**: Configured for production domains
- **Rate Limiting**: API request throttling
- **Input Validation**: Pydantic model validation
- **Error Handling**: Secure error responses

### **Data Protection**
- **Encryption**: Sensitive data encryption
- **Backup**: Automated database backups
- **Monitoring**: Security event logging

## **Performance Optimization**

### **Frontend**
- **Code Splitting**: Lazy loading of components
- **Image Optimization**: Compressed images
- **Caching**: Service worker caching
- **Bundle Size**: Optimized build output

### **Backend**
- **Database Indexing**: Optimized queries
- **Caching**: Redis for frequently accessed data
- **Async Processing**: Non-blocking operations
- **Connection Pooling**: Database connection optimization

## **Monitoring & Analytics**

### **Application Monitoring**
- **Uptime**: 99.9% target
- **Response Time**: <3 seconds
- **Error Rate**: <1% target
- **User Activity**: Real-time analytics

### **Business Metrics**
- **User Growth**: Monthly active users
- **Feature Usage**: Component analytics
- **API Usage**: Request patterns
- **Revenue**: Subscription metrics

---

*This technical architecture document provides a complete overview of the AgriForecast.ai system design and implementation.*
