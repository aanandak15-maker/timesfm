#!/usr/bin/env python3
"""
Debug field addition functionality
"""

from agriforecast_production import ProductionPlatform

def test_field_addition():
    """Test field addition functionality"""
    print("🔍 Testing field addition functionality...")
    
    platform = ProductionPlatform()
    
    # Test with the existing user and farm
    user_id = 1  # anand user
    farm_id = 3  # Anand's Farm
    
    print(f"Testing with user_id: {user_id}, farm_id: {farm_id}")
    
    # Test field creation
    try:
        field_id = platform.create_field(
            farm_id=farm_id,
            name="Test Field Debug",
            crop_type="Rice",
            area_acres=2.5,
            latitude=28.368911,
            longitude=77.541033,
            soil_type="Loamy"
        )
        print(f"✅ Field created successfully with ID: {field_id}")
        
        # Test getting fields
        fields_df = platform.get_farm_fields(farm_id)
        print(f"✅ Found {len(fields_df)} fields in farm {farm_id}")
        print("Fields:")
        for _, field in fields_df.iterrows():
            print(f"  - {field['name']} (ID: {field['id']})")
            
    except Exception as e:
        print(f"❌ Error creating field: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_field_addition()
