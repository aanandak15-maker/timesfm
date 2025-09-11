"""
Test script for Indian Weather API
"""

import requests
import json

def test_indian_weather_api():
    """Test the Indian Weather API with different endpoints"""
    
    api_key = "sk-live-Go9lYIuCVlaYmTNDy1Y0nz5hG5X8A710GiWWQldR"
    base_url = "https://weather.indianapi.in"
    lat = 28.368911
    lon = 77.541033
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Test different possible endpoints
    endpoints = [
        '/current',
        '/weather/current',
        '/api/current',
        '/v1/current',
        '/weather',
        '/current-weather',
        '/forecast/current'
    ]
    
    print("🌤️ Testing Indian Weather API Endpoints")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            params = {
                'lat': lat,
                'lon': lon
            }
            
            print(f"\n🔍 Testing: {url}")
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Response: {json.dumps(data, indent=2)[:200]}...")
                break
            else:
                print(f"❌ Failed: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test without authentication
    print(f"\n🔍 Testing without authentication...")
    try:
        url = f"{base_url}/current"
        params = {'lat': lat, 'lon': lon}
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with different parameter names
    print(f"\n🔍 Testing with different parameter names...")
    try:
        url = f"{base_url}/current"
        params = {
            'latitude': lat,
            'longitude': lon,
            'lat': lat,
            'lng': lon
        }
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_indian_weather_api()

