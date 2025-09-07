#!/usr/bin/env python3
"""
Test script to debug the production platform
"""

import sqlite3
import pandas as pd
from agriforecast_production import ProductionDatabase, ProductionPlatform

def test_database():
    """Test database functionality"""
    print("Testing Production Database...")
    
    # Initialize database
    db = ProductionDatabase()
    
    # Test user creation
    print("\n1. Testing user creation...")
    try:
        user_id = db.create_user("testuser2", "test2@example.com", "password123", "Test User 2")
        print(f"Created user with ID: {user_id}")
    except sqlite3.IntegrityError:
        # User already exists, get existing user
        user = db.get_user_by_username("testuser2")
        if user:
            user_id = user['id']
            print(f"Using existing user with ID: {user_id}")
        else:
            print("Error: Could not create or find user")
            return
    
    # Test farm creation (using ProductionPlatform)
    print("\n2. Testing farm creation...")
    platform = ProductionPlatform()
    farm_id = platform.create_farm(user_id, "Test Farm", "Test Location", 10.0)
    print(f"Created farm with ID: {farm_id}")
    
    # Test field creation
    print("\n3. Testing field creation...")
    field_id = platform.create_field(farm_id, "Test Field", "Rice", 5.0, 28.368911, 77.541033, "Loamy")
    print(f"Created field with ID: {field_id}")
    
    # Test getting farms
    print("\n4. Testing get_user_farms...")
    farms_df = platform.get_user_farms(user_id)
    print(f"Found {len(farms_df)} farms:")
    print(farms_df)
    
    # Test getting fields
    print("\n5. Testing get_farm_fields...")
    fields_df = platform.get_farm_fields(farm_id)
    print(f"Found {len(fields_df)} fields:")
    print(fields_df)
    
    # Test field data
    print("\n6. Testing get_field_data...")
    field_data = platform.get_field_data(field_id)
    print(f"Field data: {field_data}")
    
    print("\n✅ Database tests completed successfully!")

if __name__ == "__main__":
    test_database()
