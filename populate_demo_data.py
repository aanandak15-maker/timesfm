#!/usr/bin/env python3
"""
Populate AgriForecast.ai with comprehensive demo data
Creates realistic farms, fields, weather, and market data
"""

import sqlite3
import json
import requests
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# API base URL
API_BASE = "http://localhost:8000"

def create_demo_fields():
    """Create demo fields for existing farms"""
    
    # Field data for each farm
    demo_fields = [
        # Farm 1: Green Field (Dankaur)
        {
            "farm_id": "1",
            "name": "North Wheat Field",
            "crop_type": "Wheat",
            "area_acres": 0.4,
            "latitude": 28.6139,
            "longitude": 77.2090
        },
        {
            "farm_id": "1",
            "name": "South Rice Field", 
            "crop_type": "Rice",
            "area_acres": 0.6,
            "latitude": 28.6139,
            "longitude": 77.2090
        },
        
        # Farm 2: Test Farm
        {
            "farm_id": "2",
            "name": "Main Corn Field",
            "crop_type": "Corn",
            "area_acres": 5.0,
            "latitude": 28.7041,
            "longitude": 77.1025
        },
        {
            "farm_id": "2",
            "name": "Secondary Soybean Field",
            "crop_type": "Soybean",
            "area_acres": 3.0,
            "latitude": 28.7041,
            "longitude": 77.1025
        },
        {
            "farm_id": "2",
            "name": "Vegetable Garden",
            "crop_type": "Tomatoes",
            "area_acres": 2.0,
            "latitude": 28.7041,
            "longitude": 77.1025
        },
        
        # Farm 3: Anand's Farm (Delhi)
        {
            "farm_id": "3",
            "name": "Organic Wheat Field",
            "crop_type": "Wheat",
            "area_acres": 8.0,
            "latitude": 28.6139,
            "longitude": 77.2090
        },
        {
            "farm_id": "3",
            "name": "Basmati Rice Field",
            "crop_type": "Rice",
            "area_acres": 10.0,
            "latitude": 28.6139,
            "longitude": 77.2090
        },
        {
            "farm_id": "3",
            "name": "Sugarcane Field",
            "crop_type": "Sugarcane",
            "area_acres": 7.0,
            "latitude": 28.6139,
            "longitude": 77.2090
        },
        
        # Farm 4: Small Farm
        {
            "farm_id": "4",
            "name": "Herb Garden",
            "crop_type": "Basil",
            "area_acres": 0.3,
            "latitude": 28.5355,
            "longitude": 77.3910
        },
        {
            "farm_id": "4",
            "name": "Lettuce Patch",
            "crop_type": "Lettuce",
            "area_acres": 0.7,
            "latitude": 28.5355,
            "longitude": 77.3910
        }
    ]
    
    print("🌾 Creating demo fields...")
    
    for field in demo_fields:
        try:
            response = requests.post(f"{API_BASE}/api/fields", json=field)
            if response.status_code == 200:
                print(f"✅ Created field: {field['name']} ({field['crop_type']})")
            else:
                print(f"❌ Failed to create field: {field['name']} - {response.text}")
        except Exception as e:
            print(f"❌ Error creating field {field['name']}: {e}")

def create_demo_weather_data():
    """Create demo weather data for the last 30 days"""
    print("🌤️ Creating demo weather data...")
    
    # Generate weather data for the last 30 days
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # Generate realistic weather data
        weather_data = {
            "date": date_str,
            "temperature_avg": round(random.uniform(15, 35), 1),
            "temperature_min": round(random.uniform(10, 25), 1),
            "temperature_max": round(random.uniform(25, 40), 1),
            "humidity": round(random.uniform(40, 90), 1),
            "precipitation": round(random.uniform(0, 15), 1),
            "wind_speed": round(random.uniform(5, 25), 1),
            "pressure": round(random.uniform(1000, 1020), 1),
            "uv_index": random.randint(1, 11),
            "visibility": round(random.uniform(5, 15), 1)
        }
        
        try:
            response = requests.post(f"{API_BASE}/api/weather", json=weather_data)
            if response.status_code == 200:
                print(f"✅ Created weather data for {date_str}")
            else:
                print(f"❌ Failed to create weather data for {date_str}")
        except Exception as e:
            print(f"❌ Error creating weather data for {date_str}: {e}")

def create_demo_market_data():
    """Create demo market price data"""
    print("💰 Creating demo market data...")
    
    # Crop prices (per kg in USD)
    crop_prices = {
        "Wheat": 0.25,
        "Rice": 0.35,
        "Corn": 0.20,
        "Soybean": 0.45,
        "Tomatoes": 1.20,
        "Sugarcane": 0.15,
        "Basil": 8.00,
        "Lettuce": 2.50
    }
    
    # Generate price data for the last 30 days
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        for crop, base_price in crop_prices.items():
            # Add some price variation
            variation = random.uniform(-0.1, 0.1)  # ±10% variation
            price = round(base_price * (1 + variation), 2)
            
            market_data = {
                "date": date_str,
                "crop_type": crop,
                "price_per_kg": price,
                "market": "Local Market",
                "quality": random.choice(["Grade A", "Grade B", "Premium"]),
                "volume_available": random.randint(100, 1000)
            }
            
            try:
                response = requests.post(f"{API_BASE}/api/market", json=market_data)
                if response.status_code == 200:
                    print(f"✅ Created market data for {crop} on {date_str}")
                else:
                    print(f"❌ Failed to create market data for {crop}")
            except Exception as e:
                print(f"❌ Error creating market data for {crop}: {e}")

def create_demo_yield_predictions():
    """Create demo yield prediction data"""
    print("📊 Creating demo yield predictions...")
    
    # Get all fields
    try:
        response = requests.get(f"{API_BASE}/api/fields")
        if response.status_code == 200:
            fields = response.json().get('data', [])
            
            for field in fields:
                # Generate yield prediction based on crop type
                crop_yields = {
                    "Wheat": (2.5, 4.0),
                    "Rice": (3.0, 6.0),
                    "Corn": (8.0, 12.0),
                    "Soybean": (2.0, 4.0),
                    "Tomatoes": (20.0, 40.0),
                    "Sugarcane": (60.0, 100.0),
                    "Basil": (1.0, 2.0),
                    "Lettuce": (15.0, 25.0)
                }
                
                crop_type = field.get('crop_type', 'Wheat')
                min_yield, max_yield = crop_yields.get(crop_type, (2.0, 4.0))
                
                prediction_data = {
                    "field_id": field['id'],
                    "predicted_yield": round(random.uniform(min_yield, max_yield), 2),
                    "confidence": round(random.uniform(0.75, 0.95), 2),
                    "prediction_date": datetime.now().strftime("%Y-%m-%d"),
                    "factors": {
                        "weather_score": round(random.uniform(0.6, 0.9), 2),
                        "soil_health": round(random.uniform(0.7, 0.95), 2),
                        "crop_health": round(random.uniform(0.8, 0.95), 2),
                        "pest_pressure": round(random.uniform(0.1, 0.4), 2)
                    }
                }
                
                response = requests.post(f"{API_BASE}/api/yield-predictions", json=prediction_data)
                if response.status_code == 200:
                    print(f"✅ Created yield prediction for {field['name']}")
                else:
                    print(f"❌ Failed to create yield prediction for {field['name']}")
                    
    except Exception as e:
        print(f"❌ Error creating yield predictions: {e}")

def main():
    """Main function to populate all demo data"""
    print("🚀 Starting AgriForecast.ai Demo Data Population...")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE}/api/health")
        if response.status_code != 200:
            print("❌ API server is not running. Please start the FastAPI server first.")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        return
    
    print("✅ API server is running")
    
    # Create demo data
    create_demo_fields()
    create_demo_weather_data()
    create_demo_market_data()
    create_demo_yield_predictions()
    
    print("=" * 50)
    print("🎉 Demo data population completed!")
    print("🌾 Your AgriForecast.ai platform is now populated with realistic demo data")
    print("📱 Visit http://localhost:3001 to see your data in action!")

if __name__ == "__main__":
    main()
