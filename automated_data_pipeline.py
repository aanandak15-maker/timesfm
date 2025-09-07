#!/usr/bin/env python3
"""
Automated Data Pipeline for AgriForecast.ai
Collects, processes, and stores agricultural data from multiple sources
"""

import requests
import pandas as pd
import numpy as np
import sqlite3
import json
import schedule
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AgriculturalDataPipeline:
    """Automated data collection and processing pipeline"""
    
    def __init__(self):
        self.setup_database()
        self.api_keys = self.load_api_keys()
        
    def setup_database(self):
        """Initialize database for storing collected data"""
        self.db_path = "agricultural_data.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for different data types
        tables = {
            'weather_data': '''
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    date TEXT NOT NULL,
                    temperature REAL,
                    humidity REAL,
                    rainfall REAL,
                    wind_speed REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'market_data': '''
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    commodity TEXT NOT NULL,
                    date TEXT NOT NULL,
                    price REAL,
                    volume REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'satellite_data': '''
                CREATE TABLE IF NOT EXISTS satellite_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    date TEXT NOT NULL,
                    ndvi REAL,
                    evi REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'government_data': '''
                CREATE TABLE IF NOT EXISTS government_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    date TEXT NOT NULL,
                    data_type TEXT NOT NULL,
                    value REAL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        for table_name, create_sql in tables.items():
            cursor.execute(create_sql)
        
        conn.commit()
        conn.close()
        logger.info("Database setup completed")
    
    def load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables"""
        return {
            'openweather': os.getenv('OPENWEATHER_API_KEY', ''),
            'alpha_vantage': os.getenv('ALPHA_VANTAGE_API_KEY', ''),
            'nasa': os.getenv('NASA_API_KEY', ''),
            'usda': os.getenv('USDA_API_KEY', '')
        }
    
    def fetch_weather_data(self, location: str = "Global") -> pd.DataFrame:
        """Fetch weather data from OpenWeatherMap API"""
        try:
            # Mock implementation - in production, use real API
            logger.info(f"Fetching weather data for {location}")
            
            # Generate realistic weather data
            dates = pd.date_range(
                start=datetime.now() - timedelta(days=30),
                end=datetime.now(),
                freq='D'
            )
            
            np.random.seed(42)
            base_temp = 15
            seasonal = 15 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25 - np.pi/2)
            noise = 5 * np.random.normal(0, 1, len(dates))
            temperatures = base_temp + seasonal + noise
            
            humidity = 50 + 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25) + 10 * np.random.normal(0, 1, len(dates))
            rainfall = np.maximum(0, 5 * np.random.exponential(1, len(dates)))
            wind_speed = 10 + 5 * np.random.normal(0, 1, len(dates))
            
            weather_df = pd.DataFrame({
                'location': location,
                'date': dates.strftime('%Y-%m-%d'),
                'temperature': temperatures.round(1),
                'humidity': np.clip(humidity, 0, 100).round(1),
                'rainfall': rainfall.round(1),
                'wind_speed': np.maximum(wind_speed, 0).round(1)
            })
            
            logger.info(f"Collected {len(weather_df)} weather records")
            return weather_df
            
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return pd.DataFrame()
    
    def fetch_market_data(self, commodities: List[str] = None) -> pd.DataFrame:
        """Fetch commodity market data"""
        if commodities is None:
            commodities = ['wheat', 'corn', 'soybeans', 'rice']
        
        try:
            logger.info(f"Fetching market data for {commodities}")
            
            market_data = []
            for commodity in commodities:
                # Mock implementation - in production, use real API
                dates = pd.date_range(
                    start=datetime.now() - timedelta(days=30),
                    end=datetime.now(),
                    freq='D'
                )
                
                np.random.seed(hash(commodity) % 2**32)
                base_price = 200 + hash(commodity) % 100
                trend = 0.05 * np.arange(len(dates))
                volatility = 20 * np.random.normal(0, 1, len(dates))
                prices = base_price + trend + volatility
                
                volume = 1000 + 500 * np.random.normal(0, 1, len(dates))
                
                commodity_df = pd.DataFrame({
                    'commodity': commodity,
                    'date': dates.strftime('%Y-%m-%d'),
                    'price': np.maximum(prices, 50).round(2),
                    'volume': np.maximum(volume, 100).round(0)
                })
                
                market_data.append(commodity_df)
            
            combined_df = pd.concat(market_data, ignore_index=True)
            logger.info(f"Collected {len(combined_df)} market records")
            return combined_df
            
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return pd.DataFrame()
    
    def fetch_satellite_data(self, locations: List[str] = None) -> pd.DataFrame:
        """Fetch satellite data (NDVI, EVI)"""
        if locations is None:
            locations = ['Global', 'North America', 'Europe', 'Asia']
        
        try:
            logger.info(f"Fetching satellite data for {locations}")
            
            satellite_data = []
            for location in locations:
                # Mock implementation - in production, use NASA API
                dates = pd.date_range(
                    start=datetime.now() - timedelta(days=30),
                    end=datetime.now(),
                    freq='D'
                )
                
                np.random.seed(hash(location) % 2**32)
                base_ndvi = 0.5 + 0.2 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
                ndvi = base_ndvi + 0.1 * np.random.normal(0, 1, len(dates))
                
                base_evi = 0.3 + 0.15 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
                evi = base_evi + 0.05 * np.random.normal(0, 1, len(dates))
                
                satellite_df = pd.DataFrame({
                    'location': location,
                    'date': dates.strftime('%Y-%m-%d'),
                    'ndvi': np.clip(ndvi, 0, 1).round(3),
                    'evi': np.clip(evi, 0, 1).round(3)
                })
                
                satellite_data.append(satellite_df)
            
            combined_df = pd.concat(satellite_data, ignore_index=True)
            logger.info(f"Collected {len(combined_df)} satellite records")
            return combined_df
            
        except Exception as e:
            logger.error(f"Error fetching satellite data: {e}")
            return pd.DataFrame()
    
    def fetch_government_data(self) -> pd.DataFrame:
        """Fetch government agricultural data"""
        try:
            logger.info("Fetching government agricultural data")
            
            # Mock implementation - in production, use USDA/FAO APIs
            dates = pd.date_range(
                start=datetime.now() - timedelta(days=30),
                end=datetime.now(),
                freq='D'
            )
            
            government_data = []
            
            # Crop production data
            np.random.seed(123)
            production = 1000 + 100 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25) + 50 * np.random.normal(0, 1, len(dates))
            
            production_df = pd.DataFrame({
                'source': 'USDA',
                'date': dates.strftime('%Y-%m-%d'),
                'data_type': 'crop_production',
                'value': np.maximum(production, 500).round(0),
                'metadata': json.dumps({'unit': 'tons', 'crop': 'wheat'})
            })
            
            government_data.append(production_df)
            
            # Export data
            exports = 200 + 50 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25) + 25 * np.random.normal(0, 1, len(dates))
            
            export_df = pd.DataFrame({
                'source': 'USDA',
                'date': dates.strftime('%Y-%m-%d'),
                'data_type': 'exports',
                'value': np.maximum(exports, 50).round(0),
                'metadata': json.dumps({'unit': 'tons', 'crop': 'wheat'})
            })
            
            government_data.append(export_df)
            
            combined_df = pd.concat(government_data, ignore_index=True)
            logger.info(f"Collected {len(combined_df)} government records")
            return combined_df
            
        except Exception as e:
            logger.error(f"Error fetching government data: {e}")
            return pd.DataFrame()
    
    def store_weather_data(self, data: pd.DataFrame):
        """Store weather data in database"""
        if data.empty:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for _, row in data.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO weather_data 
                (location, date, temperature, humidity, rainfall, wind_speed)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['location'], row['date'], row['temperature'],
                row['humidity'], row['rainfall'], row['wind_speed']
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"Stored {len(data)} weather records")
    
    def store_market_data(self, data: pd.DataFrame):
        """Store market data in database"""
        if data.empty:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for _, row in data.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO market_data 
                (commodity, date, price, volume)
                VALUES (?, ?, ?, ?)
            ''', (
                row['commodity'], row['date'], row['price'], row['volume']
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"Stored {len(data)} market records")
    
    def store_satellite_data(self, data: pd.DataFrame):
        """Store satellite data in database"""
        if data.empty:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for _, row in data.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO satellite_data 
                (location, date, ndvi, evi)
                VALUES (?, ?, ?, ?)
            ''', (
                row['location'], row['date'], row['ndvi'], row['evi']
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"Stored {len(data)} satellite records")
    
    def store_government_data(self, data: pd.DataFrame):
        """Store government data in database"""
        if data.empty:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for _, row in data.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO government_data 
                (source, date, data_type, value, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                row['source'], row['date'], row['data_type'], 
                row['value'], row['metadata']
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"Stored {len(data)} government records")
    
    def run_daily_collection(self):
        """Run daily data collection"""
        logger.info("Starting daily data collection")
        
        try:
            # Collect weather data
            weather_data = self.fetch_weather_data()
            self.store_weather_data(weather_data)
            
            # Collect market data
            market_data = self.fetch_market_data()
            self.store_market_data(market_data)
            
            # Collect satellite data
            satellite_data = self.fetch_satellite_data()
            self.store_satellite_data(satellite_data)
            
            # Collect government data
            government_data = self.fetch_government_data()
            self.store_government_data(government_data)
            
            logger.info("Daily data collection completed successfully")
            
        except Exception as e:
            logger.error(f"Error in daily data collection: {e}")
    
    def get_latest_data(self, data_type: str, limit: int = 100) -> pd.DataFrame:
        """Get latest data from database"""
        conn = sqlite3.connect(self.db_path)
        
        if data_type == 'weather':
            query = "SELECT * FROM weather_data ORDER BY date DESC LIMIT ?"
        elif data_type == 'market':
            query = "SELECT * FROM market_data ORDER BY date DESC LIMIT ?"
        elif data_type == 'satellite':
            query = "SELECT * FROM satellite_data ORDER BY date DESC LIMIT ?"
        elif data_type == 'government':
            query = "SELECT * FROM government_data ORDER BY date DESC LIMIT ?"
        else:
            conn.close()
            return pd.DataFrame()
        
        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()
        return df
    
    def setup_scheduler(self):
        """Setup automated scheduling"""
        # Schedule daily data collection at 6 AM
        schedule.every().day.at("06:00").do(self.run_daily_collection)
        
        # Schedule weekly data cleanup (remove old data)
        schedule.every().week.do(self.cleanup_old_data)
        
        logger.info("Scheduler setup completed")
    
    def cleanup_old_data(self):
        """Remove data older than 2 years"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
        
        tables = ['weather_data', 'market_data', 'satellite_data', 'government_data']
        for table in tables:
            cursor.execute(f"DELETE FROM {table} WHERE date < ?", (cutoff_date,))
            deleted = cursor.rowcount
            logger.info(f"Cleaned up {deleted} old records from {table}")
        
        conn.commit()
        conn.close()
    
    def run_scheduler(self):
        """Run the scheduler"""
        logger.info("Starting data pipeline scheduler")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function"""
    pipeline = AgriculturalDataPipeline()
    
    # Run initial data collection
    pipeline.run_daily_collection()
    
    # Setup and run scheduler
    pipeline.setup_scheduler()
    pipeline.run_scheduler()

if __name__ == "__main__":
    main()
