"""
Real Data Integration Service for AgriForecast.ai
Integrates real APIs for weather, market, and agricultural data
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np

class RealDataService:
    """Service for integrating real agricultural data from various APIs"""
    
    def __init__(self):
        # API Keys
        self.openweather_key = "28f1d9ac94ed94535d682b7bf6c441bb"
        self.alpha_vantage_key = "KJRXQKB09I13GUPP"
        self.indian_weather_key = "sk-live-Go9lYIuCVlaYmTNDy1Y0nz5hG5X8A710GiWWQldR"
        self.indian_weather_base = "https://weather.indianapi.in"
        
        # Cache for API responses
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        return time.time() - self.cache[key]['timestamp'] < self.cache_duration
    
    def _cache_data(self, key: str, data: Any):
        """Cache API response data"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def _get_cached_data(self, key: str) -> Optional[Any]:
        """Get cached data if valid"""
        if self._is_cache_valid(key):
            return self.cache[key]['data']
        return None
    
    def get_real_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get real weather data from multiple sources"""
        cache_key = f"weather_{latitude}_{longitude}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # Try OpenWeatherMap first
        weather_data = self._get_openweather_data(latitude, longitude)
        if weather_data:
            self._cache_data(cache_key, weather_data)
            return weather_data
        
        # Try Indian Weather API as backup
        weather_data = self._get_indian_weather_data(latitude, longitude)
        if weather_data:
            self._cache_data(cache_key, weather_data)
            return weather_data
        
        # Fallback to simulated data
        return self._get_fallback_weather(latitude, longitude)
    
    def _get_openweather_data(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get weather data from OpenWeatherMap API"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': round(data['main']['temp'], 1),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
                    'condition': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'source': 'OpenWeatherMap',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"OpenWeatherMap API error: {e}")
        
        return None
    
    def _get_indian_weather_data(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get weather data from Indian Weather API"""
        try:
            url = f"{self.indian_weather_base}/api/current"
            params = {'lat': lat, 'lon': lon}
            headers = {'Authorization': f'Bearer {self.indian_weather_key}'}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': round(data.get('temperature', 25), 1),
                    'humidity': data.get('humidity', 60),
                    'pressure': data.get('pressure', 1013),
                    'wind_speed': round(data.get('wind_speed', 10), 1),
                    'condition': data.get('condition', 'Clear').title(),
                    'icon': '01d',
                    'source': 'Indian Weather API',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Indian Weather API error: {e}")
        
        return None
    
    def _get_fallback_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """Generate fallback weather data"""
        # Simulate weather based on location and season
        base_temp = 25 + (lat - 28) * 0.5  # Rough temperature estimation
        season_factor = 1 + 0.3 * np.sin(2 * np.pi * datetime.now().timetuple().tm_yday / 365)
        
        return {
            'temperature': round(base_temp * season_factor, 1),
            'humidity': np.random.randint(40, 80),
            'pressure': np.random.randint(1000, 1020),
            'wind_speed': round(np.random.uniform(5, 15), 1),
            'condition': np.random.choice(['Clear', 'Partly Cloudy', 'Cloudy']),
            'icon': '01d',
            'source': 'Simulated',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_market_prices(self, commodity: str = "RICE") -> Dict[str, Any]:
        """Get real market prices from Alpha Vantage"""
        cache_key = f"market_{commodity}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # Try Alpha Vantage
        market_data = self._get_alpha_vantage_data(commodity)
        if market_data:
            self._cache_data(cache_key, market_data)
            return market_data
        
        # Fallback to simulated data
        return self._get_fallback_market_data(commodity)
    
    def _get_alpha_vantage_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get market data from Alpha Vantage"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'COMMODITY',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    latest = data['data'][0]
                    return {
                        'price': float(latest.get('value', 0)),
                        'currency': 'USD',
                        'change': float(latest.get('change', 0)),
                        'change_percent': float(latest.get('change_percent', 0)),
                        'source': 'Alpha Vantage',
                        'timestamp': datetime.now().isoformat()
                    }
        except Exception as e:
            print(f"Alpha Vantage API error: {e}")
        
        return None
    
    def _get_fallback_market_data(self, commodity: str) -> Dict[str, Any]:
        """Generate fallback market data"""
        base_prices = {
            'RICE': 4.17,
            'WHEAT': 3.45,
            'CORN': 2.89,
            'SOYBEAN': 5.23,
            'COTTON': 0.85
        }
        
        base_price = base_prices.get(commodity, 3.0)
        change = np.random.uniform(-0.2, 0.2)
        
        return {
            'price': round(base_price + change, 2),
            'currency': 'USD',
            'change': round(change, 2),
            'change_percent': round((change / base_price) * 100, 1),
            'source': 'Simulated',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_historical_weather(self, lat: float, lon: float, days: int = 7) -> List[Dict[str, Any]]:
        """Get historical weather data"""
        cache_key = f"historical_weather_{lat}_{lon}_{days}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # Generate historical data (in real implementation, use historical API)
        historical_data = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            weather = self._get_fallback_weather(lat, lon)
            weather['date'] = date.strftime('%Y-%m-%d')
            historical_data.append(weather)
        
        self._cache_data(cache_key, historical_data)
        return historical_data
    
    def get_soil_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get soil data (simulated for now)"""
        # In real implementation, integrate with soil databases
        return {
            'ph': round(np.random.uniform(6.0, 7.5), 1),
            'nitrogen': round(np.random.uniform(20, 50), 1),
            'phosphorus': round(np.random.uniform(15, 40), 1),
            'potassium': round(np.random.uniform(100, 200), 1),
            'organic_matter': round(np.random.uniform(2.0, 4.0), 1),
            'soil_type': np.random.choice(['Loamy', 'Clay', 'Sandy', 'Silty']),
            'source': 'Simulated',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_ndvi_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get NDVI (vegetation index) data"""
        # In real implementation, integrate with satellite data APIs
        return {
            'ndvi': round(np.random.uniform(0.3, 0.8), 2),
            'vegetation_health': np.random.choice(['Poor', 'Fair', 'Good', 'Excellent']),
            'source': 'Simulated',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_weather_forecast(self, lat: float, lon: float, days: int = 5) -> List[Dict[str, Any]]:
        """Get weather forecast"""
        cache_key = f"forecast_{lat}_{lon}_{days}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # Generate forecast data (in real implementation, use forecast API)
        forecast_data = []
        for i in range(days):
            date = datetime.now() + timedelta(days=i+1)
            weather = self._get_fallback_weather(lat, lon)
            weather['date'] = date.strftime('%Y-%m-%d')
            weather['day'] = date.strftime('%A')
            forecast_data.append(weather)
        
        self._cache_data(cache_key, forecast_data)
        return forecast_data
    
    def get_comprehensive_field_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get comprehensive data for a field"""
        return {
            'weather': self.get_real_weather(lat, lon),
            'historical_weather': self.get_historical_weather(lat, lon, 7),
            'forecast': self.get_weather_forecast(lat, lon, 5),
            'soil': self.get_soil_data(lat, lon),
            'ndvi': self.get_ndvi_data(lat, lon),
            'market_prices': {
                'rice': self.get_market_prices('RICE'),
                'wheat': self.get_market_prices('WHEAT'),
                'corn': self.get_market_prices('CORN')
            }
        }

# Global instance
real_data_service = RealDataService()




