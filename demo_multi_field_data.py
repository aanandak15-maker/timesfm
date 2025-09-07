#!/usr/bin/env python3
"""
Demo script to populate the multi-field system with sample data
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random

def create_demo_data():
    """Create demo data for the multi-field system"""
    
    # Connect to database
    conn = sqlite3.connect('agriforecast_multi_field.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM field_data")
    cursor.execute("DELETE FROM yield_predictions")
    cursor.execute("DELETE FROM field_zones")
    cursor.execute("DELETE FROM fields")
    cursor.execute("DELETE FROM farms")
    
    # Create demo farms
    farms_data = [
        ("Green Valley Farm", "Premium organic farming operation", "Delhi, India"),
        ("Sunrise Agriculture", "Traditional family farm", "Punjab, India"),
        ("TechFarm Solutions", "Modern precision agriculture", "Haryana, India")
    ]
    
    farm_ids = []
    for farm in farms_data:
        cursor.execute(
            "INSERT INTO farms (name, description, location) VALUES (?, ?, ?)",
            farm
        )
        farm_ids.append(cursor.lastrowid)
    
    # Create demo fields
    fields_data = [
        # Green Valley Farm fields
        (farm_ids[0], "North Field", "Rice", 28.368911, 77.541033, 325.12, "Main rice cultivation area"),
        (farm_ids[0], "South Field", "Wheat", 28.365000, 77.540000, 450.25, "Winter wheat production"),
        (farm_ids[0], "East Field", "Corn", 28.370000, 77.545000, 280.75, "Summer corn field"),
        
        # Sunrise Agriculture fields
        (farm_ids[1], "Field A", "Soybean", 30.900000, 75.800000, 500.00, "Primary soybean field"),
        (farm_ids[1], "Field B", "Cotton", 30.905000, 75.805000, 350.50, "Cotton cultivation zone"),
        
        # TechFarm Solutions fields
        (farm_ids[2], "Zone 1", "Sugarcane", 29.000000, 76.500000, 800.00, "High-tech sugarcane field"),
        (farm_ids[2], "Zone 2", "Rice", 29.005000, 76.505000, 400.25, "Precision rice farming"),
        (farm_ids[2], "Zone 3", "Wheat", 29.010000, 76.510000, 300.75, "Automated wheat field")
    ]
    
    field_ids = []
    for field in fields_data:
        area_acres = field[5] * 0.000247105  # Convert m² to acres
        cursor.execute(
            """INSERT INTO fields (farm_id, name, crop_type, latitude, longitude, 
               area_m2, area_acres, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (field[0], field[1], field[2], field[3], field[4], field[5], area_acres, field[6])
        )
        field_ids.append(cursor.lastrowid)
    
    # Create demo field zones
    zones_data = [
        # North Field zones
        (field_ids[0], "Zone A", "High Yield", "28.368911,77.541033", 100.0, "Best performing zone"),
        (field_ids[0], "Zone B", "Medium Yield", "28.368900,77.541000", 150.0, "Standard production zone"),
        (field_ids[0], "Zone C", "Low Yield", "28.368950,77.541050", 75.12, "Challenging soil conditions"),
        
        # South Field zones
        (field_ids[1], "Zone 1", "Irrigated", "28.365000,77.540000", 200.0, "Fully irrigated section"),
        (field_ids[1], "Zone 2", "Rainfed", "28.365100,77.540100", 250.25, "Rain-dependent area"),
        
        # East Field zones
        (field_ids[2], "North Section", "Organic", "28.370000,77.545000", 150.0, "Organic farming zone"),
        (field_ids[2], "South Section", "Conventional", "28.370100,77.545100", 130.75, "Traditional farming"),
        
        # Field A zones
        (field_ids[3], "Sector 1", "High Fertility", "30.900000,75.800000", 250.0, "Rich soil area"),
        (field_ids[3], "Sector 2", "Medium Fertility", "30.900100,75.800100", 250.0, "Average soil quality"),
        
        # Field B zones
        (field_ids[4], "Cotton Zone A", "Premium", "30.905000,75.805000", 175.0, "Premium cotton area"),
        (field_ids[4], "Cotton Zone B", "Standard", "30.905100,75.805100", 175.5, "Standard cotton zone"),
        
        # Zone 1 zones
        (field_ids[5], "Block A", "High Tech", "29.000000,76.500000", 400.0, "Automated irrigation"),
        (field_ids[5], "Block B", "Standard", "29.000100,76.500100", 400.0, "Traditional methods"),
        
        # Zone 2 zones
        (field_ids[6], "Precision Zone", "AI Managed", "29.005000,76.505000", 200.0, "AI-controlled farming"),
        (field_ids[6], "Manual Zone", "Human Managed", "29.005100,76.505100", 200.25, "Manual operations"),
        
        # Zone 3 zones
        (field_ids[7], "Automated Section", "Robotic", "29.010000,76.510000", 150.0, "Robotic farming"),
        (field_ids[7], "Hybrid Section", "Semi-Auto", "29.010100,76.510100", 150.75, "Semi-automated")
    ]
    
    for zone in zones_data:
        cursor.execute(
            """INSERT INTO field_zones (field_id, zone_name, zone_type, coordinates, 
               area_m2, description) VALUES (?, ?, ?, ?, ?, ?)""",
            zone
        )
    
    # Create demo field data
    for field_id in field_ids:
        # Weather data
        weather_data = {
            'temperature_c': round(random.uniform(20, 35), 1),
            'humidity': round(random.uniform(40, 80), 1),
            'pressure': round(random.uniform(1000, 1020), 1),
            'wind_speed': round(random.uniform(2, 15), 1),
            'precipitation': round(random.uniform(0, 10), 1),
            'description': random.choice(['Clear sky', 'Partly cloudy', 'Overcast', 'Light rain']),
            'api_source': 'Demo Data'
        }
        
        cursor.execute(
            "INSERT INTO field_data (field_id, data_type, data_json) VALUES (?, ?, ?)",
            (field_id, 'weather', json.dumps(weather_data))
        )
        
        # Soil data
        soil_data = {
            'ph': round(random.uniform(6.0, 7.5), 1),
            'nitrogen': round(random.uniform(30, 120), 1),
            'phosphorus': round(random.uniform(15, 50), 1),
            'potassium': round(random.uniform(100, 250), 1),
            'organic_matter': round(random.uniform(1.5, 3.0), 1),
            'texture': random.choice(['Loamy Clay', 'Sandy Loam', 'Clay Loam', 'Silty Clay']),
            'data_source': 'Demo Data'
        }
        
        cursor.execute(
            "INSERT INTO field_data (field_id, data_type, data_json) VALUES (?, ?, ?)",
            (field_id, 'soil', json.dumps(soil_data))
        )
        
        # Yield prediction data
        yield_data = {
            'predicted_yield': round(random.uniform(2.0, 8.0), 2),
            'confidence_score': round(random.uniform(0.6, 0.95), 2),
            'scenarios': {
                'drought': round(random.uniform(1.5, 6.0), 2),
                'normal': round(random.uniform(2.0, 8.0), 2),
                'optimal': round(random.uniform(2.5, 10.0), 2)
            },
            'recommendations': [
                "Monitor soil moisture levels",
                "Apply fertilizer as needed",
                "Check for pest infestations"
            ],
            'risk_factors': [
                {
                    'type': 'Weather Risk',
                    'severity': random.choice(['Low', 'Medium', 'High']),
                    'description': 'Potential weather impact on yield'
                }
            ]
        }
        
        cursor.execute(
            "INSERT INTO yield_predictions (field_id, prediction_type, prediction_data, confidence_score) VALUES (?, ?, ?, ?)",
            (field_id, 'yield_forecast', json.dumps(yield_data), yield_data['confidence_score'])
        )
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("✅ Demo data created successfully!")
    print(f"   • {len(farm_ids)} farms created")
    print(f"   • {len(field_ids)} fields created")
    print(f"   • {len(zones_data)} zones created")
    print(f"   • Weather, soil, and yield data added for all fields")
    print("")
    print("🌐 Access your multi-field system at: http://localhost:8503")

if __name__ == "__main__":
    create_demo_data()
