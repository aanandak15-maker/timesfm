"""
Setup script for Love at First Sight Platform
Creates demo user and sample data
"""

import sqlite3
import hashlib
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def setup_love_platform():
    """Setup the love platform with demo data"""
    db_path = "agriforecast_love.db"
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Initialize database schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            crop_type TEXT,
            area_acres REAL NOT NULL,
            latitude REAL,
            longitude REAL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    try:
        # Create demo user
        username = "demo"
        email = "demo@farm.com"
        password = "demo"
        full_name = "Demo Farmer"
        
        password_hash = hash_password(password)
        
        # Insert user (ignore if exists)
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))
        
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()
        if user_row:
            user_id = user_row[0]
            
            # Create sample fields
            fields_data = [
                ("North Field", "Rice", 5.0, 28.368911, 77.541033),
                ("South Field", "Wheat", 3.5, 28.369000, 77.541100),
                ("East Field", "Corn", 4.2, 28.368800, 77.540900),
            ]
            
            for field_name, crop_type, area, lat, lon in fields_data:
                cursor.execute('''
                    INSERT OR IGNORE INTO fields (user_id, name, crop_type, area_acres, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, field_name, crop_type, area, lat, lon))
        
        conn.commit()
        print("✅ Love at First Sight platform setup completed!")
        print(f"🚀 Username: {username}")
        print(f"🔑 Password: {password}")
        print(f"🌾 Sample fields: {len(fields_data)} fields created")
        print("")
        print("🎯 Platform ready for instant user love!")
        
    except Exception as e:
        print(f"❌ Error setting up platform: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    setup_love_platform()
