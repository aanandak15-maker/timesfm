"""
Test different authentication methods for Indian Weather API
"""

import requests
import json

def test_auth_methods():
    """Test different ways to send the API key"""
    
    api_key = "sk-live-Go9lYIuCVlaYmTNDy1Y0nz5hG5X8A710GiWWQldR"
    base_url = "https://weather.indianapi.in"
    lat = 28.368911
    lon = 77.541033
    
    print("🔑 Testing Different Authentication Methods")
    print("=" * 50)
    
    # Method 1: Bearer token in header
    print("\n1. Bearer token in Authorization header:")
    try:
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(f"{base_url}/current", headers=headers, params={'lat': lat, 'lon': lon})
        print(f"Status: {response.status_code}, Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 2: API key in header
    print("\n2. API key in X-API-Key header:")
    try:
        headers = {'X-API-Key': api_key}
        response = requests.get(f"{base_url}/current", headers=headers, params={'lat': lat, 'lon': lon})
        print(f"Status: {response.status_code}, Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 3: API key in params
    print("\n3. API key in query parameters:")
    try:
        params = {'lat': lat, 'lon': lon, 'api_key': api_key}
        response = requests.get(f"{base_url}/current", params=params)
        print(f"Status: {response.status_code}, Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 4: API key in params with different name
    print("\n4. API key as 'key' parameter:")
    try:
        params = {'lat': lat, 'lon': lon, 'key': api_key}
        response = requests.get(f"{base_url}/current", params=params)
        print(f"Status: {response.status_code}, Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 5: API key in params as 'token'
    print("\n5. API key as 'token' parameter:")
    try:
        params = {'lat': lat, 'lon': lon, 'token': api_key}
        response = requests.get(f"{base_url}/current", params=params)
        print(f"Status: {response.status_code}, Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 6: Both header and params
    print("\n6. Both Authorization header and params:")
    try:
        headers = {'Authorization': f'Bearer {api_key}'}
        params = {'lat': lat, 'lon': lon, 'api_key': api_key}
        response = requests.get(f"{base_url}/current", headers=headers, params=params)
        print(f"Status: {response.status_code}, Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 7: Check if it needs a different base URL
    print("\n7. Testing with different base URLs:")
    base_urls = [
        "https://weather.indianapi.in",
        "https://api.weather.indianapi.in",
        "https://weather.indianapi.in/api",
        "https://weather.indianapi.in/v1"
    ]
    
    for base in base_urls:
        try:
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(f"{base}/current", headers=headers, params={'lat': lat, 'lon': lon})
            print(f"  {base}/current: {response.status_code} - {response.text[:50]}")
        except Exception as e:
            print(f"  {base}/current: Error - {e}")

if __name__ == "__main__":
    test_auth_methods()

