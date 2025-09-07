#!/usr/bin/env python3
"""
Test real API connections to verify what's actually working
"""

import requests
import json
from datetime import datetime

def test_openweather_api():
    """Test OpenWeatherMap API"""
    print("🌤️ Testing OpenWeatherMap API...")
    
    api_key = "28f1d9ac94ed94535d682b7bf6c441bb"
    lat, lon = 28.368911, 77.541033  # Delhi coordinates
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ OpenWeatherMap API: WORKING")
            print(f"   Temperature: {data['main']['temp']}°C")
            print(f"   Humidity: {data['main']['humidity']}%")
            print(f"   Pressure: {data['main']['pressure']} hPa")
            return True
        else:
            print(f"❌ OpenWeatherMap API: FAILED ({response.status_code})")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ OpenWeatherMap API: ERROR - {e}")
        return False

def test_alpha_vantage_api():
    """Test Alpha Vantage API"""
    print("\n💰 Testing Alpha Vantage API...")
    
    api_key = "KJRXQKB09I13GUPP"
    symbol = "WEAT"  # Wheat ETF
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                print("✅ Alpha Vantage API: WORKING")
                # Get latest price
                latest_date = max(data['Time Series (Daily)'].keys())
                latest_price = data['Time Series (Daily)'][latest_date]['4. close']
                print(f"   Latest {symbol} Price: ${latest_price}")
                return True
            else:
                print("❌ Alpha Vantage API: No time series data")
                print(f"   Response keys: {list(data.keys())}")
                return False
        else:
            print(f"❌ Alpha Vantage API: FAILED ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Alpha Vantage API: ERROR - {e}")
        return False

def test_nasa_api():
    """Test NASA API"""
    print("\n🛰️ Testing NASA API...")
    
    api_key = "4Od5nRoNq2NKdyFZ6ENS98kcpZg4RT3Efelbjleb"
    
    # Test NASA APOD (Astronomy Picture of the Day) - simpler endpoint
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ NASA API: WORKING")
            print(f"   APOD Title: {data.get('title', 'N/A')}")
            return True
        else:
            print(f"❌ NASA API: FAILED ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ NASA API: ERROR - {e}")
        return False

def test_timesfm_model():
    """Test TimesFM model availability"""
    print("\n🤖 Testing TimesFM Model...")
    
    try:
        import timesfm
        print("✅ TimesFM: AVAILABLE")
        
        # Try to create a simple model instance
        try:
            model = timesfm.TimesFm(
                hparams=timesfm.TimesFmHparams(
                    backend="cpu",
                    per_core_batch_size=1,
                    horizon_len=30,
                    context_len=512,
                    num_layers=20,
                    use_positional_embedding=False,
                ),
                checkpoint=timesfm.TimesFmCheckpoint(
                    huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
                )
            )
            print("✅ TimesFM Model: LOADED SUCCESSFULLY")
            return True
        except Exception as e:
            print(f"❌ TimesFM Model: LOADING FAILED - {e}")
            return False
            
    except ImportError:
        print("❌ TimesFM: NOT INSTALLED")
        return False

def main():
    """Run all API tests"""
    print("🔍 TESTING REAL API CONNECTIONS")
    print("=" * 50)
    
    results = {
        'openweather': test_openweather_api(),
        'alpha_vantage': test_alpha_vantage_api(),
        'nasa': test_nasa_api(),
        'timesfm': test_timesfm_model()
    }
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print("=" * 50)
    
    for api, working in results.items():
        status = "✅ WORKING" if working else "❌ NOT WORKING"
        print(f"{api.upper()}: {status}")
    
    working_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 RESULT: {working_count}/{total_count} APIs working")
    
    if working_count == total_count:
        print("🎉 ALL APIS ARE WORKING! Real data is flowing.")
    elif working_count > 0:
        print("⚠️  PARTIAL: Some APIs working, some using fallbacks.")
    else:
        print("❌ CRITICAL: No APIs working, all data is simulated.")

if __name__ == "__main__":
    main()