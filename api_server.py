#!/usr/bin/env python3
"""
FastAPI wrapper for AgriForecast.ai backend services
Exposes REST APIs for React frontend consumption
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uvicorn
import logging
from datetime import datetime, date
import sqlite3
import pandas as pd
import numpy as np
import json

# Import your existing services
try:
    from forecasting_service import ForecastingService
    from comprehensive_soil_analysis import get_comprehensive_analysis_data
    FORECASTING_AVAILABLE = True
except ImportError:
    FORECASTING_AVAILABLE = False
    logging.warning("Forecasting service not available")

try:
    from multi_field_yield_prediction import MultiFieldYieldPrediction
    YIELD_PREDICTION_AVAILABLE = True
except ImportError:
    YIELD_PREDICTION_AVAILABLE = False
    logging.warning("Yield prediction not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AgriForecast.ai API",
    description="AI-powered agricultural forecasting API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",  # React frontend
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Create React App
        "http://localhost:8080",  # Vue/other
        "https://localhost:3001", # HTTPS variants
        "https://localhost:5173",
        "https://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize services
forecast_service = None
yield_predictor = None

if FORECASTING_AVAILABLE:
    try:
        forecast_service = ForecastingService()
    except Exception as e:
        logger.error(f"Failed to initialize forecasting service: {e}")

if YIELD_PREDICTION_AVAILABLE:
    try:
        yield_predictor = MultiFieldYieldPrediction()
    except Exception as e:
        logger.error(f"Failed to initialize yield predictor: {e}")

# Database helper
class DatabaseHelper:
    def __init__(self):
        self.db_paths = {
            'production': 'agriforecast_production.db',
            'multi_field': 'agriforecast_multi_field.db',
            'analytics': 'agriforecast_analytics.db',
            'mobile': 'agriforecast_mobile.db',
            'simple': 'agriforecast_simple.db'
        }
    
    def get_connection(self, db_name='production'):
        try:
            return sqlite3.connect(self.db_paths.get(db_name, self.db_paths['production']))
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise HTTPException(status_code=500, detail="Database connection failed")
    
    def execute_query(self, query: str, params: tuple = (), db_name='production'):
        try:
            conn = self.get_connection(db_name)
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
            else:
                conn.commit()
                result = {"affected_rows": cursor.rowcount}
            
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

db_helper = DatabaseHelper()

# Pydantic models
class WeatherRequest(BaseModel):
    latitude: float
    longitude: float
    days: Optional[int] = 30

class YieldPredictionRequest(BaseModel):
    field_id: str
    crop_type: str
    area: float
    soil_data: Optional[Dict] = {}
    weather_data: Optional[List[Dict]] = []

class ForecastRequest(BaseModel):
    data: List[float]
    horizon: Optional[int] = 30
    frequency: Optional[str] = "D"

class FieldData(BaseModel):
    name: str
    farm_id: str
    area_acres: float
    crop_type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class FarmData(BaseModel):
    name: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    total_area: Optional[float] = None

# API Routes
@app.get("/")
async def root():
    return {
        "message": "AgriForecast.ai API v1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "forecasting": FORECASTING_AVAILABLE,
            "yield_prediction": YIELD_PREDICTION_AVAILABLE
        }
    }

@app.get("/api/health")
async def health_check():
    try:
        # Test database connection
        test_query = "SELECT 1 as test"
        db_helper.execute_query(test_query)
        db_status = "healthy"
    except:
        db_status = "error"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "services": {
            "forecasting": FORECASTING_AVAILABLE,
            "yield_prediction": YIELD_PREDICTION_AVAILABLE
        }
    }

# Farm management endpoints
@app.get("/api/farms")
async def get_farms(user_id: Optional[str] = Query(None)):
    """Get all farms or farms for a specific user"""
    try:
        if user_id:
            query = "SELECT * FROM farms WHERE owner_id = ?"
            params = (user_id,)
        else:
            query = "SELECT * FROM farms LIMIT 100"
            params = ()
        
        farms = db_helper.execute_query(query, params)
        return {"status": "success", "data": farms}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching farms: {str(e)}")

@app.post("/api/farms")
async def create_farm(farm_data: FarmData):
    """Create a new farm"""
    try:
        query = """
        INSERT INTO farms (name, location, latitude, longitude, total_area, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            farm_data.name,
            farm_data.location,
            farm_data.latitude,
            farm_data.longitude,
            farm_data.total_area,
            datetime.now().isoformat()
        )
        
        result = db_helper.execute_query(query, params)
        return {"status": "success", "message": "Farm created successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating farm: {str(e)}")

# Field management endpoints
@app.get("/api/fields")
async def get_fields(farm_id: Optional[str] = Query(None)):
    """Get all fields or fields for a specific farm"""
    try:
        if farm_id:
            query = """
            SELECT f.*, fa.name as farm_name 
            FROM fields f 
            LEFT JOIN farms fa ON f.farm_id = fa.id 
            WHERE f.farm_id = ?
            """
            params = (farm_id,)
        else:
            query = """
            SELECT f.*, fa.name as farm_name 
            FROM fields f 
            LEFT JOIN farms fa ON f.farm_id = fa.id 
            LIMIT 100
            """
            params = ()
        
        fields = db_helper.execute_query(query, params)
        return {"status": "success", "data": fields}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching fields: {str(e)}")

@app.post("/api/fields")
async def create_field(field_data: FieldData):
    """Create a new field"""
    try:
        query = """
        INSERT INTO fields (name, farm_id, area_acres, crop_type, latitude, longitude, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            field_data.name,
            field_data.farm_id,
            field_data.area_acres,
            field_data.crop_type,
            field_data.latitude,
            field_data.longitude,
            datetime.now().isoformat()
        )
        
        result = db_helper.execute_query(query, params)
        return {"status": "success", "message": "Field created successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating field: {str(e)}")

# Weather endpoints
@app.get("/api/weather/{latitude}/{longitude}")
async def get_weather_data(latitude: float, longitude: float, days: int = 30):
    """Get real-time weather data for coordinates"""
    try:
        if forecast_service:
            weather_data = forecast_service.get_real_weather_data(latitude, longitude, days)
            return {
                "status": "success",
                "data": weather_data.to_dict('records'),
                "location": {"latitude": latitude, "longitude": longitude}
            }
        else:
            # Fallback to simulated data
            dates = pd.date_range(start=datetime.now() - pd.Timedelta(days=days), end=datetime.now(), freq='D')
            weather_data = []
            for date in dates:
                weather_data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "temperature": np.random.normal(25, 5),
                    "humidity": np.random.normal(60, 15),
                    "precipitation": np.random.exponential(2),
                    "wind_speed": np.random.normal(10, 3),
                    "pressure": np.random.normal(1013, 10)
                })
            
            return {
                "status": "success",
                "data": weather_data,
                "location": {"latitude": latitude, "longitude": longitude},
                "note": "Simulated data - forecasting service not available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather data error: {str(e)}")

# Prediction endpoints
@app.post("/api/predict/yield")
async def predict_yield(request: YieldPredictionRequest):
    """Predict crop yield for a field"""
    try:
        if yield_predictor:
            prediction = yield_predictor.predict_yield(
                crop_type=request.crop_type,
                field_area=request.area,
                weather_data=request.weather_data or [],
                soil_data=request.soil_data or {}
            )
            return {
                "status": "success",
                "prediction": prediction,
                "field_id": request.field_id
            }
        else:
            # Fallback prediction
            base_yields = {
                'Rice': 4.5, 'Wheat': 3.2, 'Corn': 5.8, 
                'Soybean': 2.1, 'Cotton': 1.8, 'Sugarcane': 70.0
            }
            base_yield = base_yields.get(request.crop_type, 3.0)
            predicted_yield = base_yield * request.area * np.random.normal(1.0, 0.1)
            
            return {
                "status": "success",
                "prediction": {
                    "predicted_yield": round(predicted_yield, 2),
                    "confidence": 0.85,
                    "yield_per_hectare": round(predicted_yield / request.area, 2)
                },
                "field_id": request.field_id,
                "note": "Simulated prediction - yield predictor not available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yield prediction error: {str(e)}")

@app.post("/api/forecast/timeseries")
async def forecast_timeseries(request: ForecastRequest):
    """Forecast time series using TimesFM"""
    try:
        if forecast_service and hasattr(forecast_service, 'forecast_time_series'):
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
        else:
            # Simple forecasting fallback
            data = np.array(request.data)
            trend = np.polyfit(range(len(data)), data, 1)[0]
            last_value = data[-1]
            
            predictions = []
            for i in range(request.horizon):
                next_val = last_value + trend * (i + 1) + np.random.normal(0, np.std(data) * 0.1)
                predictions.append(next_val)
            
            dates = pd.date_range(start=datetime.now(), periods=request.horizon, freq=request.frequency)
            confidence_intervals = [[p - np.std(data) * 0.2, p + np.std(data) * 0.2] for p in predictions]
            
            return {
                "status": "success",
                "forecast": predictions,
                "confidence_intervals": confidence_intervals,
                "dates": [d.isoformat() for d in dates],
                "note": "Simple forecast - TimesFM not available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast error: {str(e)}")

# Market data endpoints
@app.get("/api/market/{commodity}")
async def get_market_prices(commodity: str, days: int = 30):
    """Get market prices for commodity"""
    try:
        if forecast_service and hasattr(forecast_service, 'get_market_prices'):
            prices = forecast_service.get_market_prices(commodity, days)
            return {
                "status": "success",
                "commodity": commodity,
                "data": prices
            }
        else:
            # Simulated market data
            dates = pd.date_range(start=datetime.now() - pd.Timedelta(days=days), end=datetime.now(), freq='D')
            base_prices = {
                'wheat': 200, 'corn': 180, 'rice': 350, 'soybean': 400, 'cotton': 1500
            }
            base_price = base_prices.get(commodity.lower(), 250)
            
            prices = []
            for i, date in enumerate(dates):
                price = base_price * (1 + np.sin(i/10) * 0.1 + np.random.normal(0, 0.05))
                prices.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "price": round(price, 2),
                    "volume": np.random.randint(1000, 10000)
                })
            
            return {
                "status": "success",
                "commodity": commodity,
                "data": prices,
                "note": "Simulated data - market service not available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data error: {str(e)}")

# Analytics endpoints
@app.get("/api/analytics/dashboard")
async def get_dashboard_analytics():
    """Get dashboard analytics data"""
    try:
        # Get summary statistics
        farms_count = db_helper.execute_query("SELECT COUNT(*) as count FROM farms")[0]['count']
        fields_count = db_helper.execute_query("SELECT COUNT(*) as count FROM fields")[0]['count']
        
        # Get recent predictions (if table exists)
        try:
            recent_predictions = db_helper.execute_query(
                "SELECT * FROM yield_predictions ORDER BY created_at DESC LIMIT 10"
            )
        except:
            recent_predictions = []
        
        return {
            "status": "success",
            "data": {
                "summary": {
                    "total_farms": farms_count,
                    "total_fields": fields_count,
                    "recent_predictions": len(recent_predictions)
                },
                "recent_predictions": recent_predictions
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

# Satellite data endpoints
@app.get("/api/satellite/{field_id}")
async def get_satellite_data(field_id: str, start_date: date, end_date: date):
    """Get satellite data for field"""
    try:
        if forecast_service and hasattr(forecast_service, 'get_satellite_data'):
            satellite_data = forecast_service.get_satellite_data(field_id, start_date, end_date)
            return {
                "status": "success",
                "field_id": field_id,
                "data": satellite_data
            }
        else:
            # Simulated satellite data
            dates = pd.date_range(start=start_date, end=end_date, freq='W')
            satellite_data = []
            
            for date in dates:
                satellite_data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "ndvi": round(np.random.normal(0.7, 0.1), 3),
                    "soil_moisture": round(np.random.normal(0.3, 0.05), 3),
                    "temperature": round(np.random.normal(25, 3), 1),
                    "cloud_cover": round(np.random.uniform(0, 0.8), 2)
                })
            
            return {
                "status": "success",
                "field_id": field_id,
                "data": satellite_data,
                "note": "Simulated data - satellite service not available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Satellite data error: {str(e)}")

# Field Boundary Detection endpoints
@app.post("/api/field-boundary/detect")
async def detect_field_boundary(request: dict):
    """Detect field boundary using various methods"""
    try:
        field_id = request.get("field_id")
        method = request.get("method", "gps")  # gps, satellite, manual, estimated
        latitude = request.get("latitude")
        longitude = request.get("longitude")
        area = request.get("area", 1.0)
        
        # Mock boundary detection based on method
        if method == "gps":
            # Simulate GPS walk-through detection
            boundary = {
                "center": {"lat": latitude, "lng": longitude},
                "polygon": [
                    {"lat": latitude + 0.001, "lng": longitude + 0.001},
                    {"lat": latitude + 0.001, "lng": longitude - 0.001},
                    {"lat": latitude - 0.001, "lng": longitude - 0.001},
                    {"lat": latitude - 0.001, "lng": longitude + 0.001},
                    {"lat": latitude + 0.001, "lng": longitude + 0.001}
                ],
                "area": area,
                "perimeter": 400,  # meters
                "method": "gps",
                "accuracy": 85
            }
        elif method == "satellite":
            # Simulate satellite imagery analysis
            boundary = {
                "center": {"lat": latitude, "lng": longitude},
                "polygon": [
                    {"lat": latitude + 0.0008, "lng": longitude + 0.0008},
                    {"lat": latitude + 0.0008, "lng": longitude - 0.0008},
                    {"lat": latitude - 0.0008, "lng": longitude - 0.0008},
                    {"lat": latitude - 0.0008, "lng": longitude + 0.0008},
                    {"lat": latitude + 0.0008, "lng": longitude + 0.0008}
                ],
                "area": area * 0.95,  # Slightly different from input
                "perimeter": 380,
                "method": "satellite",
                "accuracy": 92
            }
        else:
            # Estimated boundary
            side_length = (area * 4046.86) ** 0.5 / 111000
            boundary = {
                "center": {"lat": latitude, "lng": longitude},
                "polygon": [
                    {"lat": latitude + side_length/2, "lng": longitude + side_length/2},
                    {"lat": latitude + side_length/2, "lng": longitude - side_length/2},
                    {"lat": latitude - side_length/2, "lng": longitude - side_length/2},
                    {"lat": latitude - side_length/2, "lng": longitude + side_length/2},
                    {"lat": latitude + side_length/2, "lng": longitude + side_length/2}
                ],
                "area": area,
                "perimeter": side_length * 4 * 111000,
                "method": "estimated",
                "accuracy": 60
            }
        
        return {
            "status": "success",
            "field_id": field_id,
            "boundary": boundary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Boundary detection error: {str(e)}")

@app.get("/api/satellite-images/{field_id}")
async def get_satellite_images(field_id: str, lat: float, lng: float):
    """Get satellite images for field boundary detection"""
    try:
        # Mock satellite images
        images = [
            {
                "id": f"sentinel_{field_id}_001",
                "date": "2024-01-15",
                "source": "sentinel-2",
                "resolution": 10,
                "cloud_cover": 5,
                "url": f"https://services.sentinel-hub.com/api/v1/process?lat={lat}&lng={lng}"
            },
            {
                "id": f"landsat_{field_id}_001", 
                "date": "2024-01-20",
                "source": "landsat-8",
                "resolution": 30,
                "cloud_cover": 10,
                "url": f"https://earthengine.googleapis.com/v1alpha2/landsat?lat={lat}&lng={lng}"
            }
        ]
        
        return {
            "status": "success",
            "field_id": field_id,
            "images": images
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Satellite images error: {str(e)}")

# Comprehensive Soil Analysis endpoints
@app.get("/api/soil-analysis/{field_id}")
async def get_soil_analysis(field_id: str):
    """Get comprehensive soil analysis for field"""
    try:
        analysis_data = get_comprehensive_analysis_data(field_id)
        return {
            "status": "success",
            "field_id": field_id,
            "data": analysis_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Soil analysis error: {str(e)}")

@app.get("/api/crop-stages/{field_id}")
async def get_crop_stages(field_id: str):
    """Get crop stage tracking for field"""
    try:
        analysis_data = get_comprehensive_analysis_data(field_id)
        return {
            "status": "success",
            "field_id": field_id,
            "crop_stages": analysis_data["crop_stages"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop stages error: {str(e)}")

@app.get("/api/disease-pest/{field_id}")
async def get_disease_pest_monitoring(field_id: str):
    """Get disease and pest monitoring for field"""
    try:
        analysis_data = get_comprehensive_analysis_data(field_id)
        return {
            "status": "success",
            "field_id": field_id,
            "disease_pest": analysis_data["disease_pest"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disease pest monitoring error: {str(e)}")

@app.get("/api/nutrient-status/{field_id}")
async def get_nutrient_status(field_id: str):
    """Get nutrient status tracking for field"""
    try:
        analysis_data = get_comprehensive_analysis_data(field_id)
        return {
            "status": "success",
            "field_id": field_id,
            "nutrient_status": analysis_data["nutrient_status"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Nutrient status error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting AgriForecast.ai API Server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 ReDoc Documentation: http://localhost:8000/redoc")
    print("🌐 Health Check: http://localhost:8000/api/health")
    
    uvicorn.run(
        "api_server:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
