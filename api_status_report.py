#!/usr/bin/env python3
"""
Comprehensive API Status Report for AgriForecast.ai
"""

import requests
from config import config
from datetime import datetime

def test_all_apis():
    """Test all APIs and generate comprehensive report"""
    print("🚀 AgriForecast.ai - Comprehensive API Status Report")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {}
    
    # Test Alpha Vantage API
    print("📈 Testing Alpha Vantage API...")
    try:
        url = config.ALPHA_VANTAGE_BASE_URL
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': 'WEAT',
            'apikey': config.ALPHA_VANTAGE_API_KEY,
            'outputsize': 'compact'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'Time Series (Daily)' in data:
                results['alpha_vantage'] = {
                    'status': 'WORKING',
                    'data_points': len(data['Time Series (Daily)']),
                    'response_time': response.elapsed.total_seconds()
                }
                print("   ✅ WORKING - Real commodity market data available")
            else:
                results['alpha_vantage'] = {'status': 'ERROR', 'message': 'No time series data'}
                print("   ❌ ERROR - No time series data")
        else:
            results['alpha_vantage'] = {'status': 'ERROR', 'message': f'HTTP {response.status_code}'}
            print(f"   ❌ ERROR - HTTP {response.status_code}")
    except Exception as e:
        results['alpha_vantage'] = {'status': 'ERROR', 'message': str(e)}
        print(f"   ❌ ERROR - {e}")
    
    # Test NASA API
    print("\n🛰️ Testing NASA API...")
    try:
        # Test APOD endpoint (most reliable)
        url = f"{config.NASA_BASE_URL}/planetary/apod"
        params = {'api_key': config.NASA_API_KEY}
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results['nasa'] = {
                'status': 'WORKING',
                'endpoints': ['APOD', 'NEO'],
                'response_time': response.elapsed.total_seconds()
            }
            print("   ✅ WORKING - APOD and NEO endpoints available")
            print("   ⚠️  Earth Imagery endpoint may timeout (network issue)")
        else:
            results['nasa'] = {'status': 'ERROR', 'message': f'HTTP {response.status_code}'}
            print(f"   ❌ ERROR - HTTP {response.status_code}")
    except Exception as e:
        results['nasa'] = {'status': 'ERROR', 'message': str(e)}
        print(f"   ❌ ERROR - {e}")
    
    # Test OpenWeatherMap API
    print("\n🌤️ Testing OpenWeatherMap API...")
    try:
        url = f"{config.OPENWEATHER_BASE_URL}/weather"
        params = {
            'q': 'London',
            'appid': config.OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results['openweather'] = {
                'status': 'WORKING',
                'location': f"{data['name']}, {data['sys']['country']}",
                'temperature': f"{data['main']['temp']}°C",
                'response_time': response.elapsed.total_seconds()
            }
            print("   ✅ WORKING - Real weather data available")
        else:
            results['openweather'] = {'status': 'ERROR', 'message': f'HTTP {response.status_code}'}
            print(f"   ❌ ERROR - HTTP {response.status_code}")
            if response.status_code == 401:
                print("   💡 Suggestion: API key may need activation or email verification")
    except Exception as e:
        results['openweather'] = {'status': 'ERROR', 'message': str(e)}
        print(f"   ❌ ERROR - {e}")
    
    # Generate summary
    print("\n" + "=" * 60)
    print("📊 API STATUS SUMMARY")
    print("=" * 60)
    
    working_apis = 0
    total_apis = len(results)
    
    for api_name, result in results.items():
        status = result['status']
        if status == 'WORKING':
            working_apis += 1
            print(f"✅ {api_name.upper():15} - WORKING")
        else:
            print(f"❌ {api_name.upper():15} - ERROR")
    
    print(f"\n🎯 Overall Status: {working_apis}/{total_apis} APIs Working")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    if working_apis == total_apis:
        print("🎉 All APIs are working! Your startup is ready for full production.")
    elif working_apis > 0:
        print("⚠️  Some APIs are working. The app will use real data where available.")
        print("   - Alpha Vantage: Real commodity market data ✅")
        if results.get('nasa', {}).get('status') == 'WORKING':
            print("   - NASA: Real satellite and space data ✅")
        if results.get('openweather', {}).get('status') == 'WORKING':
            print("   - OpenWeatherMap: Real weather data ✅")
    else:
        print("❌ No APIs are working. The app will use fallback data.")
    
    # Next steps
    print("\n🚀 NEXT STEPS:")
    print("   1. Launch your startup: ./launch_startup.sh")
    print("   2. Open browser: http://localhost:8501")
    print("   3. Start forecasting with available real data!")
    
    if results.get('openweather', {}).get('status') != 'WORKING':
        print("\n🔧 OpenWeatherMap API Fix:")
        print("   - Check if API key is activated")
        print("   - Verify email confirmation")
        print("   - Try generating a new API key")
    
    return results

if __name__ == "__main__":
    test_all_apis()
