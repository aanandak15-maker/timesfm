#!/usr/bin/env python3
"""
Configuration file for AgriForecast.ai
Contains API keys and application settings
"""

import os
from typing import Dict

class Config:
    """Application configuration"""
    
    # API Keys
    NASA_API_KEY = "4Od5nRoNq2NKdyFZ6ENS98kcpZg4RT3Efelbjleb"
    ALPHA_VANTAGE_API_KEY = "KJRXQKB09I13GUPP"
    OPENWEATHER_API_KEY = "28f1d9ac94ed94535d682b7bf6c441bb"
    
    # App Configuration
    APP_NAME = "AgriForecast.ai"
    APP_VERSION = "1.0.0"
    DEBUG = True
    
    # Database Configuration
    DATABASE_URL = "sqlite:///agriforecast.db"
    
    # Security
    SECRET_KEY = "agriforecast-secret-key-2024"
    JWT_SECRET = "agriforecast-jwt-secret-2024"
    
    # API Endpoints
    NASA_BASE_URL = "https://api.nasa.gov"
    ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # Data Collection Settings
    DEFAULT_LOCATION = "Global"
    DEFAULT_COMMODITIES = ["wheat", "corn", "soybeans", "rice"]
    DEFAULT_LOCATIONS = ["Global", "North America", "Europe", "Asia"]
    
    # Forecast Settings
    DEFAULT_FORECAST_HORIZON = 30  # days
    DEFAULT_CONTEXT_LENGTH = 512
    DEFAULT_BATCH_SIZE = 32
    
    # Subscription Plans
    SUBSCRIPTION_PLANS = {
        'free': {
            'forecasts_per_month': 3,
            'price': 0,
            'features': ['basic_forecasts', 'email_support']
        },
        'pro': {
            'forecasts_per_month': 50,
            'price': 29,
            'features': ['advanced_forecasts', 'email_alerts', 'priority_support']
        },
        'business': {
            'forecasts_per_month': 200,
            'price': 99,
            'features': ['unlimited_forecasts', 'api_access', 'custom_models', 'phone_support']
        },
        'enterprise': {
            'forecasts_per_month': -1,  # unlimited
            'price': 299,
            'features': ['unlimited_forecasts', 'api_access', 'custom_models', 'dedicated_support', 'white_label']
        }
    }
    
    @classmethod
    def get_api_key(cls, service: str) -> str:
        """Get API key for a specific service"""
        api_keys = {
            'nasa': cls.NASA_API_KEY,
            'alpha_vantage': cls.ALPHA_VANTAGE_API_KEY,
            'openweather': cls.OPENWEATHER_API_KEY
        }
        return api_keys.get(service, '')
    
    @classmethod
    def get_api_url(cls, service: str) -> str:
        """Get base URL for a specific service"""
        urls = {
            'nasa': cls.NASA_BASE_URL,
            'alpha_vantage': cls.ALPHA_VANTAGE_BASE_URL,
            'openweather': cls.OPENWEATHER_BASE_URL
        }
        return urls.get(service, '')

# Global configuration instance
config = Config()
