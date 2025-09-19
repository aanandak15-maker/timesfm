import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class MultiFieldDataIntegration:
    """Enhanced data integration system for multiple fields"""
    
    def __init__(self):
        self.indian_weather_api_key = "sk-live-Go9lYIuCVlaYmTNDy1Y0nz5hG5X8A710GiWWQldR"
        self.indian_weather_base_url = "https://weather.indianapi.in"
        self.openweather_api_key = "28f1d9ac94ed94535d682b7bf6c441bb"
        self.openweather_base_url = "https://api.openweathermap.org/data/2.5"
        self.usda_soil_url = "https://sdmdataaccess.nrcs.usda.gov/Spatial/SDMNAD83Geographic.wfs"
        self.sentinel_hub_url = "https://services.sentinel-hub.com/api/v1"
        
        logger.info("Multi-field data integration initialized")
    
    def get_weather_data_for_field(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Get weather data for a specific field location"""
        try:
            # Try Indian Weather API first
            weather_data = self.get_indian_weather_data(latitude, longitude)
            api_source = "Indian Weather API"
            
            if not weather_data:
                weather_data = self.get_openweather_data(latitude, longitude)
                api_source = "OpenWeatherMap"
            
            if not weather_data:
                return None
            
            # Extract relevant weather data
            if api_source == "Indian Weather API":
                weather_info = {
                    'timestamp': datetime.now().isoformat(),
                    'temperature_c': weather_data.get('temperature', {}).get('value', 25),
                    'humidity': weather_data.get('humidity', {}).get('value', 70),
                    'pressure': weather_data.get('pressure', {}).get('value', 1013),
                    'wind_speed': weather_data.get('wind_speed', {}).get('value', 5),
                    'wind_direction': weather_data.get('wind_direction', {}).get('value', 0),
                    'visibility': weather_data.get('visibility', {}).get('value', 10),
                    'cloud_cover': weather_data.get('cloud_cover', {}).get('value', 50),
                    'precipitation': weather_data.get('precipitation', {}).get('value', 0),
                    'description': weather_data.get('description', 'Clear sky'),
                    'weather_main': weather_data.get('weather_main', 'Clear'),
                    'api_source': api_source,
                    'latitude': latitude,
                    'longitude': longitude
                }
            else:  # OpenWeatherMap
                weather_info = {
                    'timestamp': datetime.now().isoformat(),
                    'temperature_c': weather_data['main']['temp'],
                    'humidity': weather_data['main']['humidity'],
                    'pressure': weather_data['main']['pressure'],
                    'wind_speed': weather_data['wind']['speed'],
                    'wind_direction': weather_data['wind'].get('deg', 0),
                    'visibility': weather_data.get('visibility', 0) / 1000,  # Convert to km
                    'cloud_cover': weather_data['clouds']['all'],
                    'precipitation': weather_data.get('rain', {}).get('1h', 0) if 'rain' in weather_data else 0,
                    'description': weather_data['weather'][0]['description'],
                    'weather_main': weather_data['weather'][0]['main'],
                    'api_source': api_source,
                    'location': weather_data.get('name', 'Unknown'),
                    'country': weather_data.get('sys', {}).get('country', 'IN'),
                    'latitude': latitude,
                    'longitude': longitude
                }
            
            logger.info(f"Successfully fetched weather data from {api_source} for {latitude}, {longitude}")
            return weather_info
            
        except Exception as e:
            logger.error(f"Error getting weather data for {latitude}, {longitude}: {e}")
            return None
    
    def get_indian_weather_data(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Get weather data from Indian Weather API"""
        try:
            url = f"{self.indian_weather_base_url}/current"
            headers = {
                'Authorization': f'Bearer {self.indian_weather_api_key}',
                'Content-Type': 'application/json'
            }
            params = {
                'lat': latitude,
                'lon': longitude
            }
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info("Successfully fetched Indian Weather API data")
                return data
            else:
                logger.error(f"Indian Weather API failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting Indian weather data: {e}")
            return None
    
    def get_openweather_data(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Get weather data from OpenWeatherMap API"""
        try:
            url = f"{self.openweather_base_url}/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.openweather_api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info("Successfully fetched OpenWeatherMap data")
                return data
            else:
                logger.error(f"OpenWeatherMap API failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting OpenWeatherMap data: {e}")
            return None
    
    def get_historical_weather_data(self, latitude: float, longitude: float, days: int = 30) -> List[Dict]:
        """Generate historical weather data for a field"""
        try:
            historical_data = []
            base_date = datetime.now() - timedelta(days=days)
            
            for i in range(days):
                current_date = base_date + timedelta(days=i)
                
                # Simulate realistic weather patterns for Delhi region
                base_temp = 25 + 10 * np.sin(2 * np.pi * i / 365)  # Seasonal variation
                temp_variation = np.random.normal(0, 3)  # Daily variation
                temperature = base_temp + temp_variation
                
                # Humidity inversely related to temperature
                humidity = max(30, min(90, 80 - (temperature - 20) * 2))
                
                # Wind speed with some randomness
                wind_speed = max(0, np.random.normal(5, 2))
                
                # Precipitation (more likely in monsoon season)
                precipitation = 0
                if 150 <= i <= 250:  # Monsoon season simulation
                    if np.random.random() < 0.3:  # 30% chance of rain
                        precipitation = np.random.exponential(5)
                
                weather_record = {
                    'timestamp': current_date.isoformat(),
                    'temperature_c': round(temperature, 1),
                    'humidity': round(humidity, 1),
                    'pressure': round(1013 + np.random.normal(0, 10), 1),
                    'wind_speed': round(wind_speed, 1),
                    'wind_direction': np.random.randint(0, 360),
                    'visibility': round(10 + np.random.normal(0, 2), 1),
                    'cloud_cover': np.random.randint(0, 100),
                    'precipitation': round(precipitation, 1),
                    'description': self.get_weather_description(temperature, humidity, precipitation),
                    'weather_main': self.get_weather_main(temperature, precipitation),
                    'latitude': latitude,
                    'longitude': longitude
                }
                
                historical_data.append(weather_record)
            
            logger.info(f"Generated {len(historical_data)} historical weather records")
            return historical_data
            
        except Exception as e:
            logger.error(f"Error generating historical weather data: {e}")
            return []
    
    def get_soil_data_for_field(self, latitude: float, longitude: float) -> Dict:
        """Get soil data for a specific field location"""
        try:
            # For now, generate simulated soil data based on location
            # In production, this would integrate with USDA/FAO databases
            
            # Simulate soil characteristics based on Delhi region
            soil_data = {
                'timestamp': datetime.now().isoformat(),
                'ph': round(7.2 + np.random.normal(0, 0.3), 1),
                'nitrogen': round(45 + np.random.normal(0, 10), 1),
                'phosphorus': round(25 + np.random.normal(0, 5), 1),
                'potassium': round(180 + np.random.normal(0, 20), 1),
                'organic_matter': round(2.1 + np.random.normal(0, 0.3), 1),
                'texture': 'Loamy Clay',
                'moisture_content': round(35 + np.random.normal(0, 5), 1),
                'bulk_density': round(1.35 + np.random.normal(0, 0.05), 2),
                'cation_exchange_capacity': round(15 + np.random.normal(0, 2), 1),
                'latitude': latitude,
                'longitude': longitude,
                'data_source': 'Simulated (Delhi Region)'
            }
            
            logger.info(f"Generated soil data for {latitude}, {longitude}")
            return soil_data
            
        except Exception as e:
            logger.error(f"Error generating soil data: {e}")
            return {}
    
    def get_satellite_data_for_field(self, latitude: float, longitude: float, days: int = 30) -> List[Dict]:
        """Generate satellite/NDVI data for a field"""
        try:
            satellite_data = []
            base_date = datetime.now() - timedelta(days=days)
            
            for i in range(days):
                current_date = base_date + timedelta(days=i)
                
                # Simulate NDVI values with crop growth cycle
                # Rice growth cycle: 0-30 days (germination), 30-60 days (vegetative), 60-90 days (reproductive), 90-120 days (maturity)
                if i < 30:
                    # Germination phase
                    ndvi = 0.1 + (i / 30) * 0.3
                elif i < 60:
                    # Vegetative phase
                    ndvi = 0.4 + ((i - 30) / 30) * 0.4
                elif i < 90:
                    # Reproductive phase
                    ndvi = 0.8 + ((i - 60) / 30) * 0.1
                else:
                    # Maturity phase
                    ndvi = 0.9 - ((i - 90) / 30) * 0.2
                
                # Add some noise
                ndvi += np.random.normal(0, 0.05)
                ndvi = max(0, min(1, ndvi))  # Clamp between 0 and 1
                
                satellite_record = {
                    'timestamp': current_date.isoformat(),
                    'ndvi': round(ndvi, 3),
                    'evi': round(ndvi * 0.9, 3),  # EVI is typically lower than NDVI
                    'savi': round(ndvi * 1.1, 3),  # SAVI is typically higher than NDVI
                    'vegetation_health': self.get_vegetation_health(ndvi),
                    'crop_stage': self.get_crop_stage(i),
                    'latitude': latitude,
                    'longitude': longitude,
                    'data_source': 'Simulated (Sentinel-2)'
                }
                
                satellite_data.append(satellite_record)
            
            logger.info(f"Generated {len(satellite_data)} satellite data records")
            return satellite_data
            
        except Exception as e:
            logger.error(f"Error generating satellite data: {e}")
            return []
    
    def get_comprehensive_field_data(self, field_id: int, latitude: float, longitude: float, 
                                   crop_type: str = "Rice") -> Dict:
        """Get comprehensive data for a field including weather, soil, and satellite data"""
        try:
            logger.info(f"Fetching comprehensive data for field {field_id} at {latitude}, {longitude}")
            
            # Get real-time weather
            real_time_weather = self.get_weather_data_for_field(latitude, longitude)
            
            # Get historical weather
            historical_weather = self.get_historical_weather_data(latitude, longitude, 30)
            
            # Get soil data
            soil_data = self.get_soil_data_for_field(latitude, longitude)
            
            # Get satellite data
            satellite_data = self.get_satellite_data_for_field(latitude, longitude, 30)
            
            # Compile comprehensive data
            comprehensive_data = {
                'field_id': field_id,
                'latitude': latitude,
                'longitude': longitude,
                'crop_type': crop_type,
                'real_time_weather': real_time_weather,
                'historical_weather': historical_weather,
                'soil_data': soil_data,
                'satellite_data': satellite_data,
                'data_summary': {
                    'weather_records': len(historical_weather),
                    'satellite_records': len(satellite_data),
                    'last_updated': datetime.now().isoformat(),
                    'data_quality': 'High' if real_time_weather else 'Medium'
                }
            }
            
            logger.info(f"Comprehensive data collection completed for field {field_id}")
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"Error getting comprehensive field data: {e}")
            return {}
    
    def get_weather_description(self, temperature: float, humidity: float, precipitation: float) -> str:
        """Generate weather description based on conditions"""
        if precipitation > 5:
            return "Heavy Rain"
        elif precipitation > 1:
            return "Light Rain"
        elif temperature > 35:
            return "Hot and Dry"
        elif temperature < 10:
            return "Cold"
        elif humidity > 80:
            return "Humid"
        else:
            return "Clear Sky"
    
    def get_weather_main(self, temperature: float, precipitation: float) -> str:
        """Get main weather condition"""
        if precipitation > 1:
            return "Rain"
        elif temperature > 35:
            return "Clear"
        elif temperature < 10:
            return "Clouds"
        else:
            return "Clear"
    
    def get_vegetation_health(self, ndvi: float) -> str:
        """Determine vegetation health based on NDVI"""
        if ndvi > 0.7:
            return "Excellent"
        elif ndvi > 0.5:
            return "Good"
        elif ndvi > 0.3:
            return "Fair"
        else:
            return "Poor"
    
    def get_crop_stage(self, days_since_planting: int) -> str:
        """Determine crop growth stage based on days since planting"""
        if days_since_planting < 30:
            return "Germination"
        elif days_since_planting < 60:
            return "Vegetative"
        elif days_since_planting < 90:
            return "Reproductive"
        else:
            return "Maturity"
    
    def get_bulk_field_data(self, fields: List[Dict]) -> Dict:
        """Get data for multiple fields efficiently"""
        try:
            bulk_data = {}
            
            for field in fields:
                field_id = field['id']
                latitude = field['latitude']
                longitude = field['longitude']
                crop_type = field['crop_type']
                
                # Get comprehensive data for this field
                field_data = self.get_comprehensive_field_data(field_id, latitude, longitude, crop_type)
                bulk_data[field_id] = field_data
            
            logger.info(f"Bulk data collection completed for {len(fields)} fields")
            return bulk_data
            
        except Exception as e:
            logger.error(f"Error getting bulk field data: {e}")
            return {}




