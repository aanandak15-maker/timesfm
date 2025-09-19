#!/usr/bin/env python3
"""
Fresh test of OpenWeatherMap API with different approaches
"""

import requests
from config import config

def test_openweather_fresh():
    """Test OpenWeatherMap API with fresh approach"""
    print("🌤️ Fresh OpenWeatherMap API Test")
    print("=" * 40)
    
    api_key = "28f1d9ac94ed94535d682b7bf6c441bb"
    print(f"API Key: {api_key}")
    print(f"Key Length: {len(api_key)}")
    
    # Test different approaches
    test_cases = [
        {
            'name': 'Current Weather - London',
            'url': 'https://api.openweathermap.org/data/2.5/weather',
            'params': {
                'q': 'London',
                'appid': api_key,
                'units': 'metric'
            }
        },
        {
            'name': 'Current Weather - New York',
            'url': 'https://api.openweathermap.org/data/2.5/weather',
            'params': {
                'q': 'New York',
                'appid': api_key,
                'units': 'metric'
            }
        },
        {
            'name': 'Weather by Coordinates',
            'url': 'https://api.openweathermap.org/data/2.5/weather',
            'params': {
                'lat': 40.7128,
                'lon': -74.0060,
                'appid': api_key,
                'units': 'metric'
            }
        },
        {
            'name': 'Forecast - London',
            'url': 'https://api.openweathermap.org/data/2.5/forecast',
            'params': {
                'q': 'London',
                'appid': api_key,
                'units': 'metric'
            }
        },
        {
            'name': 'One Call API',
            'url': 'https://api.openweathermap.org/data/2.5/onecall',
            'params': {
                'lat': 51.5074,
                'lon': -0.1278,
                'appid': api_key,
                'units': 'metric'
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        try:
            response = requests.get(test_case['url'], params=test_case['params'], timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response Time: {response.elapsed.total_seconds():.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ SUCCESS!")
                if 'main' in data:
                    print(f"   Temperature: {data['main']['temp']}°C")
                    print(f"   Humidity: {data['main']['humidity']}%")
                if 'name' in data:
                    print(f"   Location: {data['name']}")
                return True
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test API key format
    print(f"\n🔧 API Key Analysis:")
    print(f"   Starts with number: {api_key[0].isdigit()}")
    print(f"   Contains only hex: {all(c in '0123456789abcdef' for c in api_key)}")
    print(f"   Length is 32: {len(api_key) == 32}")
    
    # Try with different base URL
    print(f"\n🌐 Testing different base URL...")
    try:
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', 
                              params={'q': 'London', 'appid': api_key}, 
                              timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ API is working with direct URL!")
            return True
        else:
            print(f"   ❌ Still error: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    return False

if __name__ == "__main__":
    success = test_openweather_fresh()
    if success:
        print("\n🎉 OpenWeatherMap API is working!")
    else:
        print("\n❌ OpenWeatherMap API still not working")
        print("💡 Possible issues:")
        print("   - API key needs activation")
        print("   - Account needs email verification")
        print("   - API key might be for different service")
        print("   - Rate limiting or quota exceeded")




