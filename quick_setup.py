#!/usr/bin/env python3
"""
Quick setup script to create test data for immediate testing
"""

import sqlite3
import hashlib
from datetime import datetime

def quick_setup():
    """Create test user and sample data quickly"""
    print("🚀 Quick Setup: Creating test user and sample data...")
    
    # Connect to database
    conn = sqlite3.connect("agriforecast_production.db")
    cursor = conn.cursor()
    
    try:
        # Create test user
        username = "anand"
        email = "anand@example.com"
        password = "password123"
        full_name = "Anand Test User"
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert user (ignore if exists)
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, full_name))
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_result = cursor.fetchone()
        if user_result:
            user_id = user_result[0]
            print(f"✅ User ready: {username} (ID: {user_id})")
        else:
            print("❌ Failed to create user")
            return
        
        # Create test farm
        farm_name = "Anand's Farm"
        location = "Delhi, India"
        total_area = 25.0
        
        cursor.execute("""
            INSERT OR IGNORE INTO farms (user_id, name, location, total_area_acres)
            VALUES (?, ?, ?, ?)
        """, (user_id, farm_name, location, total_area))
        
        # Get farm ID
        cursor.execute("SELECT id FROM farms WHERE user_id = ? AND name = ?", (user_id, farm_name))
        farm_result = cursor.fetchone()
        if farm_result:
            farm_id = farm_result[0]
            print(f"✅ Farm ready: {farm_name} (ID: {farm_id})")
        else:
            print("❌ Failed to create farm")
            return
        
        # Create test fields
        fields_data = [
            ("Rice Field 1", "Rice", 5.0, 28.368911, 77.541033, "Loamy"),
            ("Wheat Field 1", "Wheat", 3.0, 28.369911, 77.542033, "Sandy"),
            ("Corn Field 1", "Corn", 4.0, 28.370911, 77.543033, "Clay"),
            ("Soybean Field 1", "Soybean", 2.5, 28.371911, 77.544033, "Loamy"),
        ]
        
        created_fields = []
        for field_name, crop_type, area, lat, lon, soil_type in fields_data:
            cursor.execute("""
                INSERT OR IGNORE INTO fields (farm_id, name, crop_type, area_acres, latitude, longitude, soil_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (farm_id, field_name, crop_type, area, lat, lon, soil_type))
            
            # Get field ID
            cursor.execute("SELECT id FROM fields WHERE farm_id = ? AND name = ?", (farm_id, field_name))
            field_result = cursor.fetchone()
            if field_result:
                created_fields.append((field_name, field_result[0]))
        
        print(f"✅ Created {len(created_fields)} fields:")
        for field_name, field_id in created_fields:
            print(f"   - {field_name} (ID: {field_id})")
        
        # Commit changes
        conn.commit()
        
        print("\n🎉 Quick setup complete!")
        print("=" * 50)
        print("🌐 Access your platform at: http://localhost:8501")
        print("👤 Login with:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print("=" * 50)
        print("📋 What you can do now:")
        print("   1. Login to the platform")
        print("   2. Go to '🌾 Field Management' to see your fields")
        print("   3. Go to '🔮 AI Forecasting' to test AI predictions")
        print("   4. Go to '🌍 Weather & Soil' to monitor conditions")
        print("   5. Go to '🌱 Crop Management' to manage crops")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    quick_setup()

