"""
Setup script for AgriForecast.ai Best UX Platform
Initializes database and creates sample data for testing
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta
import random

def setup_best_ux_platform():
    """Setup the best UX platform with sample data"""
    
    db_path = "agriforecast_best_ux.db"
    
    # Remove existing database to start fresh
    import os
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  Removed existing database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📦 Creating database tables...")
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            user_type TEXT DEFAULT 'farmer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            preferences TEXT
        )
    ''')
    
    # Farms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            location TEXT,
            total_area_acres REAL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Fields table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farm_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            crop_type TEXT,
            area_acres REAL NOT NULL,
            latitude REAL,
            longitude REAL,
            soil_type TEXT,
            planting_date DATE,
            expected_harvest_date DATE,
            status TEXT DEFAULT 'active',
            health_score REAL DEFAULT 85.0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farm_id) REFERENCES farms (id)
        )
    ''')
    
    # Insights table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            insight_type TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            action_required BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (field_id) REFERENCES fields (id)
        )
    ''')
    
    # Weather data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            date DATE NOT NULL,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            wind_speed REAL,
            pressure REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (field_id) REFERENCES fields (id)
        )
    ''')
    
    print("✅ Database tables created successfully")
    
    # Create sample users
    print("👥 Creating sample users...")
    
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    sample_users = [
        {
            "username": "farmer",
            "email": "farmer@example.com",
            "password": "password123",
            "full_name": "John Farmer",
            "user_type": "farmer"
        },
        {
            "username": "student",
            "email": "student@university.edu",
            "password": "student123",
            "full_name": "Sarah Student",
            "user_type": "student"
        },
        {
            "username": "anand",
            "email": "anand@example.com",
            "password": "password123",
            "full_name": "Anand Kumar",
            "user_type": "farmer"
        }
    ]
    
    user_ids = {}
    for user in sample_users:
        password_hash = hash_password(user["password"])
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, user_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (user["username"], user["email"], password_hash, user["full_name"], user["user_type"]))
        user_ids[user["username"]] = cursor.lastrowid
        print(f"   👤 Created user: {user['full_name']} ({user['username']})")
    
    # Create sample farms
    print("🏡 Creating sample farms...")
    
    sample_farms = [
        {
            "user": "farmer",
            "name": "Green Valley Farm",
            "location": "Punjab, India",
            "total_area": 25.5,
            "description": "Organic farming operation specializing in rice and wheat"
        },
        {
            "user": "anand",
            "name": "Anand's Farm",
            "location": "Haryana, India", 
            "total_area": 15.0,
            "description": "Modern sustainable farming with smart irrigation"
        },
        {
            "user": "student",
            "name": "University Research Farm",
            "location": "Delhi, India",
            "total_area": 5.0,
            "description": "Agricultural research and education facility"
        }
    ]
    
    farm_ids = {}
    for farm in sample_farms:
        cursor.execute('''
            INSERT INTO farms (user_id, name, location, total_area_acres, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_ids[farm["user"]], farm["name"], farm["location"], farm["total_area"], farm["description"]))
        farm_ids[f"{farm['user']}_farm"] = cursor.lastrowid
        print(f"   🏡 Created farm: {farm['name']}")
    
    # Create sample fields
    print("🌾 Creating sample fields...")
    
    sample_fields = [
        # Farmer's fields
        {
            "farm": "farmer_farm",
            "name": "Rice Field A",
            "crop_type": "Rice",
            "area": 5.0,
            "lat": 30.7046,
            "lng": 76.7179,
            "soil": "Clay",
            "health": 85.0
        },
        {
            "farm": "farmer_farm", 
            "name": "Wheat Field B",
            "crop_type": "Wheat",
            "area": 8.0,
            "lat": 30.7056,
            "lng": 76.7189,
            "soil": "Loamy",
            "health": 92.0
        },
        {
            "farm": "farmer_farm",
            "name": "Corn Field C", 
            "crop_type": "Corn",
            "area": 6.5,
            "lat": 30.7066,
            "lng": 76.7199,
            "soil": "Sandy",
            "health": 78.0
        },
        {
            "farm": "farmer_farm",
            "name": "Soybean Field D",
            "crop_type": "Soybean", 
            "area": 6.0,
            "lat": 30.7076,
            "lng": 76.7209,
            "soil": "Silty",
            "health": 88.0
        },
        # Anand's fields
        {
            "farm": "anand_farm",
            "name": "North Field",
            "crop_type": "Rice",
            "area": 7.0,
            "lat": 28.368911,
            "lng": 77.541033,
            "soil": "Clay",
            "health": 90.0
        },
        {
            "farm": "anand_farm",
            "name": "South Field", 
            "crop_type": "Wheat",
            "area": 8.0,
            "lat": 28.368811,
            "lng": 77.541133,
            "soil": "Loamy",
            "health": 87.0
        },
        # Student's research fields
        {
            "farm": "student_farm",
            "name": "Test Plot A",
            "crop_type": "Rice",
            "area": 1.0,
            "lat": 28.6139,
            "lng": 77.2090,
            "soil": "Loamy",
            "health": 95.0
        },
        {
            "farm": "student_farm",
            "name": "Test Plot B",
            "crop_type": "Wheat", 
            "area": 1.5,
            "lat": 28.6149,
            "lng": 77.2100,
            "soil": "Clay",
            "health": 93.0
        }
    ]
    
    field_ids = []
    for field in sample_fields:
        cursor.execute('''
            INSERT INTO fields (farm_id, name, crop_type, area_acres, latitude, longitude, soil_type, health_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (farm_ids[field["farm"]], field["name"], field["crop_type"], field["area"], 
              field["lat"], field["lng"], field["soil"], field["health"]))
        field_ids.append(cursor.lastrowid)
        print(f"   🌾 Created field: {field['name']} ({field['crop_type']})")
    
    # Create sample insights
    print("💡 Creating sample insights...")
    
    sample_insights = [
        {
            "field_id": field_ids[0],  # Rice Field A
            "type": "irrigation",
            "title": "Irrigation Needed",
            "message": "Soil moisture is below optimal level. Water your rice field today for best growth.",
            "priority": "high",
            "action_required": True
        },
        {
            "field_id": field_ids[1],  # Wheat Field B
            "type": "weather",
            "title": "Perfect Weather",
            "message": "Sunny weather with light rain expected. Great conditions for crop growth.",
            "priority": "medium",
            "action_required": False
        },
        {
            "field_id": field_ids[2],  # Corn Field C
            "type": "market",
            "title": "Market Opportunity",
            "message": "Corn prices have increased significantly. Consider timing your harvest sales.",
            "priority": "medium",
            "action_required": False
        },
        {
            "field_id": field_ids[0],  # Rice Field A
            "type": "health",
            "title": "Field Health Good",
            "message": "Your rice field is showing healthy growth patterns. Continue current care routine.",
            "priority": "low",
            "action_required": False
        }
    ]
    
    for insight in sample_insights:
        cursor.execute('''
            INSERT INTO insights (field_id, insight_type, title, message, priority, action_required)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (insight["field_id"], insight["type"], insight["title"], insight["message"], 
              insight["priority"], insight["action_required"]))
        print(f"   💡 Created insight: {insight['title']}")
    
    # Create sample weather data
    print("🌤️  Creating sample weather data...")
    
    for field_id in field_ids[:3]:  # Add weather data for first 3 fields
        for i in range(7):  # Last 7 days
            date = datetime.now() - timedelta(days=i)
            temp = round(random.uniform(20, 35), 1)
            humidity = round(random.uniform(40, 80), 1)
            rainfall = round(random.uniform(0, 15), 1) if random.random() > 0.7 else 0
            wind_speed = round(random.uniform(5, 20), 1)
            pressure = round(random.uniform(1000, 1020), 1)
            
            cursor.execute('''
                INSERT INTO weather_data (field_id, date, temperature, humidity, rainfall, wind_speed, pressure)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (field_id, date.date(), temp, humidity, rainfall, wind_speed, pressure))
    
    print(f"   🌤️  Created weather data for {len(field_ids[:3])} fields")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Best UX Platform setup completed successfully!")
    print("\n📊 Summary:")
    print(f"   👥 Users: {len(sample_users)}")
    print(f"   🏡 Farms: {len(sample_farms)}")
    print(f"   🌾 Fields: {len(sample_fields)}")
    print(f"   💡 Insights: {len(sample_insights)}")
    print(f"   🌤️  Weather records: {len(field_ids[:3]) * 7}")
    
    print("\n🚀 Ready to launch!")
    print("   Use: streamlit run agriforecast_best_ux.py --server.port 8505")
    
    print("\n🔑 Login credentials:")
    for user in sample_users:
        print(f"   {user['full_name']}: {user['username']} / {user['password']}")

if __name__ == "__main__":
    setup_best_ux_platform()




