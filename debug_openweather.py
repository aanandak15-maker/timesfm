#!/usr/bin/env python3
"""
Debug OpenWeatherMap API connection
"""

import requests
from config import config

def debug_openweather_api():
    """Debug OpenWeatherMap API connection"""
    print("🌤️ Debugging OpenWeatherMap API...")
    print(f"API Key: {config.OPENWEATHER_API_KEY}")
    print(f"Key Length: {len(config.OPENWEATHER_API_KEY)}")
    
    # Test different endpoints
    endpoints = [
        {
            'name': 'Current Weather',
            'url': f"{config.OPENWEATHER_BASE_URL}/weather",
            'params': {
                'q': 'London',
                'appid': config.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
        },
        {
            'name': 'Forecast',
            'url': f"{config.OPENWEATHER_BASE_URL}/forecast",
            'params': {
                'q': 'London',
                'appid': config.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
        },
        {
            'name': 'One Call API',
            'url': f"{config.OPENWEATHER_BASE_URL}/onecall",
            'params': {
                'lat': 51.5074,
                'lon': -0.1278,
                'appid': config.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing {endpoint['name']}...")
        try:
            response = requests.get(endpoint['url'], params=endpoint['params'], timeout=10)
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Response keys: {list(data.keys())}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test with different API key format
    print(f"\n🔧 Testing API key format...")
    test_key = config.OPENWEATHER_API_KEY.strip()
    print(f"   Original key: '{config.OPENWEATHER_API_KEY}'")
    print(f"   Stripped key: '{test_key}'")
    print(f"   Key starts with letter: {test_key[0].isalpha()}")
    print(f"   Key contains only alphanumeric: {test_key.isalnum()}")

if __name__ == "__main__":
    debug_openweather_api()

