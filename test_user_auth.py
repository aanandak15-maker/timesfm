#!/usr/bin/env python3
"""
Test the user authentication system
"""

import sqlite3
import hashlib

def test_database():
    """Test database connection and operations"""
    try:
        # Connect to database
        conn = sqlite3.connect('agriforecast_user_auth.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Test user creation
        username = "test_user"
        email = "test@example.com"
        password = "test123"
        full_name = "Test User"
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert test user
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, full_name)
        )
        
        # Test authentication
        cursor.execute(
            "SELECT id, username, email, full_name FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        
        if user:
            print(f"✅ Database test successful! User: {user[1]}")
            
            # Test farm creation
            user_id = user[0]
            cursor.execute(
                "INSERT INTO farms (user_id, name, description, location) VALUES (?, ?, ?, ?)",
                (user_id, "Test Farm", "Test farm description", "Test Location")
            )
            farm_id = cursor.lastrowid
            
            # Test field creation
            area_acres = 100.0 * 0.000247105
            cursor.execute(
                """INSERT INTO fields (user_id, farm_id, name, crop_type, latitude, longitude, 
                   area_m2, area_acres, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, farm_id, "Test Field", "Rice", 28.368911, 77.541033, 100.0, area_acres, "Test field description")
            )
            
            conn.commit()
            print(f"✅ Farm and field creation test successful!")
            
        else:
            print("❌ User authentication test failed!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing User Authentication System...")
    test_database()

