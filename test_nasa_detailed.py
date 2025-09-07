#!/usr/bin/env python3
"""
Detailed NASA API test with longer timeout
"""

import requests
from config import config

def test_nasa_detailed():
    """Test NASA API with detailed debugging"""
    print("🛰️ Testing NASA API with detailed debugging...")
    print(f"API Key: {config.NASA_API_KEY}")
    print(f"Base URL: {config.NASA_BASE_URL}")
    
    # Test different NASA endpoints
    endpoints = [
        {
            'name': 'Earth Imagery',
            'url': f"{config.NASA_BASE_URL}/planetary/earth/imagery",
            'params': {
                'lat': 40.7128,
                'lon': -74.0060,
                'date': '2024-01-01',
                'api_key': config.NASA_API_KEY
            }
        },
        {
            'name': 'APOD (Astronomy Picture of the Day)',
            'url': f"{config.NASA_BASE_URL}/planetary/apod",
            'params': {
                'api_key': config.NASA_API_KEY
            }
        },
        {
            'name': 'Near Earth Objects',
            'url': f"{config.NASA_BASE_URL}/neo/rest/v1/feed",
            'params': {
                'api_key': config.NASA_API_KEY
            }
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing {endpoint['name']}...")
        try:
            # Try with longer timeout
            response = requests.get(endpoint['url'], params=endpoint['params'], timeout=30)
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Time: {response.elapsed.total_seconds():.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Response keys: {list(data.keys())}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout after 30 seconds")
        except requests.exceptions.ConnectionError as e:
            print(f"   🔌 Connection Error: {e}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test without API key (NASA allows some endpoints without key)
    print(f"\n🔍 Testing NASA without API key...")
    try:
        response = requests.get(f"{config.NASA_BASE_URL}/planetary/apod", timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ NASA API is accessible (no key needed for APOD)")
        else:
            print(f"   ❌ NASA API not accessible: {response.text}")
    except Exception as e:
        print(f"   ❌ NASA API not accessible: {e}")

if __name__ == "__main__":
    test_nasa_detailed()
