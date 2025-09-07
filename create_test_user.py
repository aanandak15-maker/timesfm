#!/usr/bin/env python3
"""
Create a test user for immediate testing
"""

from agriforecast_production import ProductionDatabase, ProductionPlatform

def create_test_user():
    """Create a test user with sample data"""
    print("Creating test user and sample data...")
    
    # Initialize database
    db = ProductionDatabase()
    platform = ProductionPlatform()
    
    try:
        # Create test user
        user_id = db.create_user("anand", "anand@example.com", "password123", "Anand Test User")
        print(f"✅ Created user: anand (ID: {user_id})")
    except Exception as e:
        # User might already exist
        user = db.get_user_by_username("anand")
        if user:
            user_id = user['id']
            print(f"✅ Using existing user: anand (ID: {user_id})")
        else:
            print(f"❌ Error creating user: {e}")
            return
    
    try:
        # Create test farm
        farm_id = platform.create_farm(user_id, "Anand's Farm", "Delhi, India", 25.0)
        print(f"✅ Created farm: Anand's Farm (ID: {farm_id})")
    except Exception as e:
        print(f"❌ Error creating farm: {e}")
        return
    
    try:
        # Create test fields
        field1_id = platform.create_field(farm_id, "Rice Field 1", "Rice", 5.0, 28.368911, 77.541033, "Loamy")
        field2_id = platform.create_field(farm_id, "Wheat Field 1", "Wheat", 3.0, 28.369911, 77.542033, "Sandy")
        field3_id = platform.create_field(farm_id, "Corn Field 1", "Corn", 4.0, 28.370911, 77.543033, "Clay")
        
        print(f"✅ Created fields:")
        print(f"   - Rice Field 1 (ID: {field1_id})")
        print(f"   - Wheat Field 1 (ID: {field2_id})")
        print(f"   - Corn Field 1 (ID: {field3_id})")
        
    except Exception as e:
        print(f"❌ Error creating fields: {e}")
        return
    
    print("\n🎉 Test user setup complete!")
    print("You can now login with:")
    print("Username: anand")
    print("Password: password123")
    print("\n🌐 Access the platform at: http://localhost:8501")

if __name__ == "__main__":
    create_test_user()
