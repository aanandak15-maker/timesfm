#!/usr/bin/env python3
"""
Advanced Weather Integration for Agricultural Platform
7-day forecasts, alerts, and historical analysis
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class AdvancedWeatherIntegration:
    """Advanced weather integration with 7-day forecasts and alerts"""
    
    def __init__(self, openweather_api_key: str):
        self.api_key = openweather_api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_7_day_forecast(self, latitude: float, longitude: float) -> Dict:
        """Get 7-day weather forecast"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process forecast data
            forecast_data = []
            for item in data['list']:
                forecast_data.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'wind_speed': item['wind']['speed'],
                    'wind_direction': item['wind']['deg'],
                    'precipitation': item.get('rain', {}).get('3h', 0),
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                })
            
            return {
                'status': 'success',
                'forecast': forecast_data,
                'city': data['city']['name'],
                'country': data['city']['country']
            }
            
        except Exception as e:
            logger.error(f"Weather forecast error: {e}")
            return self._generate_simulated_forecast(latitude, longitude)
    
    def get_weather_alerts(self, latitude: float, longitude: float) -> List[Dict]:
        """Get weather alerts and warnings"""
        try:
            # OpenWeatherMap doesn't have alerts in free tier, so we'll simulate
            alerts = []
            
            # Check for extreme weather conditions
            current_weather = self.get_current_weather(latitude, longitude)
            if current_weather['status'] == 'success':
                temp = current_weather['temperature']
                humidity = current_weather['humidity']
                wind_speed = current_weather['wind_speed']
                
                # Temperature alerts
                if temp > 35:
                    alerts.append({
                        'type': 'heat_warning',
                        'severity': 'high',
                        'message': f'High temperature warning: {temp}°C',
                        'recommendation': 'Consider irrigation and shade for crops'
                    })
                elif temp < 5:
                    alerts.append({
                        'type': 'frost_warning',
                        'severity': 'high',
                        'message': f'Frost warning: {temp}°C',
                        'recommendation': 'Protect crops from frost damage'
                    })
                
                # Humidity alerts
                if humidity > 80:
                    alerts.append({
                        'type': 'high_humidity',
                        'severity': 'medium',
                        'message': f'High humidity: {humidity}%',
                        'recommendation': 'Monitor for fungal diseases'
                    })
                
                # Wind alerts
                if wind_speed > 15:
                    alerts.append({
                        'type': 'high_wind',
                        'severity': 'medium',
                        'message': f'High wind speed: {wind_speed} m/s',
                        'recommendation': 'Secure equipment and check for crop damage'
                    })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Weather alerts error: {e}")
            return []
    
    def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """Get current weather conditions"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'status': 'success',
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind']['deg'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'visibility': data.get('visibility', 0),
                'cloud_cover': data['clouds']['all']
            }
            
        except Exception as e:
            logger.error(f"Current weather error: {e}")
            return self._generate_simulated_current_weather(latitude, longitude)
    
    def get_historical_weather(self, latitude: float, longitude: float, days: int = 30) -> Dict:
        """Get historical weather data (simulated for now)"""
        try:
            # For now, we'll simulate historical data
            # In production, you'd use a historical weather API
            historical_data = []
            
            for i in range(days):
                date = datetime.now() - timedelta(days=i)
                historical_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'temperature': round(np.random.normal(25, 5), 1),
                    'humidity': round(np.random.normal(60, 15), 1),
                    'precipitation': round(np.random.exponential(2), 1),
                    'wind_speed': round(np.random.exponential(3), 1)
                })
            
            return {
                'status': 'success',
                'historical_data': historical_data,
                'days': days
            }
            
        except Exception as e:
            logger.error(f"Historical weather error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def analyze_weather_trends(self, historical_data: List[Dict]) -> Dict:
        """Analyze weather trends for agricultural insights"""
        try:
            df = pd.DataFrame(historical_data)
            
            # Calculate trends
            temp_trend = np.polyfit(range(len(df)), df['temperature'], 1)[0]
            humidity_trend = np.polyfit(range(len(df)), df['humidity'], 1)[0]
            precipitation_trend = np.polyfit(range(len(df)), df['precipitation'], 1)[0]
            
            # Calculate averages
            avg_temp = df['temperature'].mean()
            avg_humidity = df['humidity'].mean()
            avg_precipitation = df['precipitation'].mean()
            
            # Generate insights
            insights = []
            
            if temp_trend > 0.1:
                insights.append("Temperature is rising - monitor for heat stress")
            elif temp_trend < -0.1:
                insights.append("Temperature is falling - watch for frost risk")
            
            if humidity_trend > 0.5:
                insights.append("Humidity increasing - higher disease risk")
            elif humidity_trend < -0.5:
                insights.append("Humidity decreasing - may need irrigation")
            
            if precipitation_trend > 0.1:
                insights.append("Precipitation increasing - good for crops")
            elif precipitation_trend < -0.1:
                insights.append("Precipitation decreasing - consider irrigation")
            
            return {
                'status': 'success',
                'trends': {
                    'temperature_trend': round(temp_trend, 3),
                    'humidity_trend': round(humidity_trend, 3),
                    'precipitation_trend': round(precipitation_trend, 3)
                },
                'averages': {
                    'temperature': round(avg_temp, 1),
                    'humidity': round(avg_humidity, 1),
                    'precipitation': round(avg_precipitation, 1)
                },
                'insights': insights
            }
            
        except Exception as e:
            logger.error(f"Weather trends analysis error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_simulated_forecast(self, latitude: float, longitude: float) -> Dict:
        """Generate simulated 7-day forecast"""
        forecast_data = []
        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            forecast_data.append({
                'datetime': date.strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': round(np.random.normal(25, 5), 1),
                'humidity': round(np.random.normal(60, 15), 1),
                'pressure': round(np.random.normal(1013, 10), 1),
                'wind_speed': round(np.random.exponential(3), 1),
                'wind_direction': np.random.randint(0, 360),
                'precipitation': round(np.random.exponential(1), 1),
                'description': np.random.choice(['Clear sky', 'Partly cloudy', 'Overcast', 'Light rain']),
                'icon': '01d'
            })
        
        return {
            'status': 'simulated',
            'forecast': forecast_data,
            'city': 'Simulated Location',
            'country': 'IN'
        }
    
    def _generate_simulated_current_weather(self, latitude: float, longitude: float) -> Dict:
        """Generate simulated current weather"""
        return {
            'status': 'simulated',
            'temperature': round(np.random.normal(25, 5), 1),
            'humidity': round(np.random.normal(60, 15), 1),
            'pressure': round(np.random.normal(1013, 10), 1),
            'wind_speed': round(np.random.exponential(3), 1),
            'wind_direction': np.random.randint(0, 360),
            'description': np.random.choice(['Clear sky', 'Partly cloudy', 'Overcast']),
            'icon': '01d',
            'visibility': 10000,
            'cloud_cover': np.random.randint(0, 100)
        }

# Example usage
if __name__ == "__main__":
    # Test the weather integration
    weather = AdvancedWeatherIntegration("your_api_key_here")
    
    # Test 7-day forecast
    forecast = weather.get_7_day_forecast(28.368911, 77.541033)
    print("7-Day Forecast:", json.dumps(forecast, indent=2))
    
    # Test weather alerts
    alerts = weather.get_weather_alerts(28.368911, 77.541033)
    print("Weather Alerts:", json.dumps(alerts, indent=2))




