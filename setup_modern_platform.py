"""
Quick Setup Script for Modern AgriForecast Platform
Creates test user and sample data
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database_schema(cursor):
    """Initialize the database schema"""
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farm_id) REFERENCES farms (id)
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
    
    # Yield predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS yield_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            prediction_date DATE NOT NULL,
            predicted_yield REAL,
            confidence_score REAL,
            scenario TEXT,
            model_version TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (field_id) REFERENCES fields (id)
        )
    ''')

def setup_modern_platform():
    """Setup the modern platform with test data"""
    db_path = "agriforecast_modern.db"
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Initialize database schema first
    init_database_schema(cursor)
    
    try:
        # Create test user
        username = "anand"
        email = "anand@agriforecast.ai"
        password = "password123"
        full_name = "Anand Kumar"
        
        password_hash = hash_password(password)
        
        # Insert user (ignore if exists)
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))
        
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        
        # Create test farm
        farm_name = "Anand's Farm"
        cursor.execute('''
            INSERT OR IGNORE INTO farms (user_id, name, location, total_area_acres, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, farm_name, "Delhi, India", 25.5, "Main agricultural farm"))
        
        # Get farm ID
        cursor.execute('SELECT id FROM farms WHERE name = ? AND user_id = ?', (farm_name, user_id))
        farm_id = cursor.fetchone()[0]
        
        # Create test fields
        fields_data = [
            ("Rice Field 1", "Rice", 5.0, 28.368911, 77.541033, "Loamy"),
            ("Wheat Field 1", "Wheat", 8.0, 28.369000, 77.541100, "Clay"),
            ("Corn Field 1", "Corn", 6.5, 28.368800, 77.540900, "Sandy"),
            ("Soybean Field 1", "Soybean", 6.0, 28.369100, 77.541200, "Loamy")
        ]
        
        for field_name, crop_type, area, lat, lon, soil in fields_data:
            cursor.execute('''
                INSERT OR IGNORE INTO fields (farm_id, name, crop_type, area_acres, latitude, longitude, soil_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (farm_id, field_name, crop_type, area, lat, lon, soil))
        
        # Create sample weather data
        cursor.execute('SELECT id FROM fields WHERE farm_id = ?', (farm_id,))
        field_ids = [row[0] for row in cursor.fetchall()]
        
        # Add weather data for last 7 days
        for field_id in field_ids:
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).date()
                cursor.execute('''
                    INSERT OR IGNORE INTO weather_data 
                    (field_id, date, temperature, humidity, rainfall, wind_speed, pressure)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (field_id, date, 28.5 + i, 65 + i*2, 0.1*i, 10 + i, 1013 + i))
        
        # Create sample yield predictions
        for field_id in field_ids:
            cursor.execute('''
                INSERT OR IGNORE INTO yield_predictions 
                (field_id, prediction_date, predicted_yield, confidence_score, scenario, model_version)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (field_id, datetime.now().date(), 3.2, 0.85, "normal", "timesfm-1.0"))
        
        conn.commit()
        print("✅ Modern platform setup completed successfully!")
        print(f"📧 Username: {username}")
        print(f"🔑 Password: {password}")
        print(f"🏡 Farm: {farm_name}")
        print(f"🌾 Fields: {len(fields_data)} fields created")
        
    except Exception as e:
        print(f"❌ Error setting up platform: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    setup_modern_platform()
