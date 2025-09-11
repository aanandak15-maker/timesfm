#!/usr/bin/env python3
"""
Data Migration Script
Migrates data from Streamlit SQLite database to FastAPI backend
"""

import sqlite3
import requests
import json
from datetime import datetime

# Configuration
STREAMLIT_DB = "agriforecast_modern.db"
FASTAPI_URL = "http://localhost:8000"

def migrate_data():
    """Migrate data from Streamlit to FastAPI"""
    print("🔄 Starting data migration...")
    
    # Connect to Streamlit database
    conn = sqlite3.connect(STREAMLIT_DB)
    cursor = conn.cursor()
    
    try:
        # 1. Migrate Users
        print("📝 Migrating users...")
        cursor.execute("SELECT id, username, email, full_name FROM users")
        users = cursor.fetchall()
        
        for user in users:
            user_data = {
                "id": str(user[0]),
                "username": user[1],
                "email": user[2],
                "full_name": user[3] or user[1],
                "role": "farmer"
            }
            
            try:
                response = requests.post(f"{FASTAPI_URL}/api/users", json=user_data)
                if response.status_code == 201:
                    print(f"✅ User {user[1]} migrated")
                else:
                    print(f"⚠️ User {user[1]} already exists or error: {response.status_code}")
            except Exception as e:
                print(f"❌ Error migrating user {user[1]}: {e}")
        
        # 2. Migrate Farms
        print("🏡 Migrating farms...")
        cursor.execute("SELECT id, user_id, name, location, total_area_acres, description FROM farms")
        farms = cursor.fetchall()
        
        for farm in farms:
            farm_data = {
                "id": str(farm[0]),
                "user_id": str(farm[1]),
                "name": farm[2],
                "location": farm[3] or "",
                "total_area_acres": farm[4] or 0.0,
                "description": farm[5] or ""
            }
            
            try:
                response = requests.post(f"{FASTAPI_URL}/api/farms", json=farm_data)
                if response.status_code == 201:
                    print(f"✅ Farm {farm[2]} migrated")
                else:
                    print(f"⚠️ Farm {farm[2]} already exists or error: {response.status_code}")
            except Exception as e:
                print(f"❌ Error migrating farm {farm[2]}: {e}")
        
        # 3. Migrate Fields
        print("🌾 Migrating fields...")
        cursor.execute("""
            SELECT id, farm_id, name, crop_type, area_acres, latitude, longitude, 
                   soil_type, planting_date, expected_harvest_date, status
            FROM fields
        """)
        fields = cursor.fetchall()
        
        for field in fields:
            field_data = {
                "id": str(field[0]),
                "farm_id": str(field[1]),
                "name": field[2],
                "crop_type": field[3] or "Unknown",
                "area_acres": field[4] or 0.0,
                "latitude": field[5],
                "longitude": field[6],
                "soil_type": field[7] or "Unknown",
                "planting_date": field[8],
                "harvest_date": field[9],
                "status": field[10] or "active"
            }
            
            try:
                response = requests.post(f"{FASTAPI_URL}/api/fields", json=field_data)
                if response.status_code == 201:
                    print(f"✅ Field {field[2]} migrated")
                else:
                    print(f"⚠️ Field {field[2]} already exists or error: {response.status_code}")
            except Exception as e:
                print(f"❌ Error migrating field {field[2]}: {e}")
        
        # 4. Migrate Weather Data
        print("🌤️ Migrating weather data...")
        cursor.execute("SELECT field_id, date, temperature, humidity, rainfall, wind_speed, pressure FROM weather_data")
        weather_data = cursor.fetchall()
        
        for weather in weather_data:
            weather_record = {
                "field_id": str(weather[0]),
                "date": weather[1],
                "temperature": weather[2],
                "humidity": weather[3],
                "rainfall": weather[4],
                "wind_speed": weather[5],
                "pressure": weather[6]
            }
            
            try:
                response = requests.post(f"{FASTAPI_URL}/api/weather-data", json=weather_record)
                if response.status_code == 201:
                    print(f"✅ Weather data for field {weather[0]} migrated")
                else:
                    print(f"⚠️ Weather data already exists or error: {response.status_code}")
            except Exception as e:
                print(f"❌ Error migrating weather data: {e}")
        
        # 5. Migrate Yield Predictions
        print("🔮 Migrating yield predictions...")
        cursor.execute("SELECT field_id, prediction_date, predicted_yield, confidence_score, scenario, model_version FROM yield_predictions")
        predictions = cursor.fetchall()
        
        for prediction in predictions:
            prediction_data = {
                "field_id": str(prediction[0]),
                "prediction_date": prediction[1],
                "predicted_yield": prediction[2],
                "confidence_score": prediction[3],
                "scenario": prediction[4] or "default",
                "model_version": prediction[5] or "v1.0"
            }
            
            try:
                response = requests.post(f"{FASTAPI_URL}/api/yield-predictions", json=prediction_data)
                if response.status_code == 201:
                    print(f"✅ Yield prediction for field {prediction[0]} migrated")
                else:
                    print(f"⚠️ Yield prediction already exists or error: {response.status_code}")
            except Exception as e:
                print(f"❌ Error migrating yield prediction: {e}")
        
        print("✅ Data migration completed!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_data()

