#!/usr/bin/env python3
"""
Download and prepare crop yield data for TimesFM
This script creates realistic agricultural time series data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_crop_yield_data():
    """Create realistic crop yield time series data"""
    
    # Generate 2 years of daily data
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create realistic crop yield patterns
    np.random.seed(42)  # For reproducible results
    
    # Base yield with seasonal patterns
    base_yield = 3.0  # tons/hectare
    
    # Seasonal component (higher in growing season)
    seasonal = 0.5 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25 - np.pi/2)
    
    # Trend component (slight increase over time)
    trend = 0.001 * np.arange(len(dates))
    
    # Random noise
    noise = 0.1 * np.random.normal(0, 1, len(dates))
    
    # Weather effects (drought periods)
    weather_effect = np.zeros(len(dates))
    # Simulate drought in summer 2022
    drought_start = 150  # June 2022
    drought_end = 200    # July 2022
    weather_effect[drought_start:drought_end] = -0.3
    
    # Calculate final yield
    yield_values = base_yield + seasonal + trend + noise + weather_effect
    
    # Ensure positive values
    yield_values = np.maximum(yield_values, 0.5)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'value': yield_values.round(2)
    })
    
    return df

def create_soil_moisture_data():
    """Create realistic soil moisture time series data"""
    
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    np.random.seed(123)
    
    # Base moisture level
    base_moisture = 45.0  # percentage
    
    # Seasonal pattern (higher in winter, lower in summer)
    seasonal = 15 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25 + np.pi/2)
    
    # Rainfall effects (random spikes)
    rainfall_effect = np.zeros(len(dates))
    # Add random rainfall events
    rainfall_days = np.random.choice(len(dates), size=50, replace=False)
    rainfall_effect[rainfall_days] = np.random.uniform(5, 15, 50)
    
    # Irrigation effects (regular increases)
    irrigation_effect = np.zeros(len(dates))
    # Simulate irrigation every 3 days in growing season
    for i in range(100, len(dates)-100, 3):  # Growing season
        irrigation_effect[i] = 3
    
    # Random noise
    noise = 2 * np.random.normal(0, 1, len(dates))
    
    # Calculate final moisture
    moisture_values = base_moisture + seasonal + rainfall_effect + irrigation_effect + noise
    
    # Ensure realistic range (20-80%)
    moisture_values = np.clip(moisture_values, 20, 80)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'value': moisture_values.round(1)
    })
    
    return df

def create_commodity_price_data():
    """Create realistic commodity price time series data"""
    
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    np.random.seed(456)
    
    # Base price
    base_price = 200.0  # $/ton
    
    # Trend (inflation)
    trend = 0.05 * np.arange(len(dates))
    
    # Seasonal pattern (higher prices in harvest season)
    seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25 - np.pi/4)
    
    # Market volatility
    volatility = 10 * np.random.normal(0, 1, len(dates))
    
    # Supply shocks (random events)
    shock_effect = np.zeros(len(dates))
    shock_days = np.random.choice(len(dates), size=10, replace=False)
    shock_effect[shock_days] = np.random.uniform(-30, 50, 10)
    
    # Calculate final price
    price_values = base_price + trend + seasonal + volatility + shock_effect
    
    # Ensure positive values
    price_values = np.maximum(price_values, 100)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'value': price_values.round(2)
    })
    
    return df

def create_weather_data():
    """Create realistic temperature time series data"""
    
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    np.random.seed(789)
    
    # Base temperature
    base_temp = 15.0  # Celsius
    
    # Strong seasonal pattern
    seasonal = 15 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25 - np.pi/2)
    
    # Climate trend (warming)
    trend = 0.02 * np.arange(len(dates))
    
    # Daily variation
    daily_variation = 5 * np.random.normal(0, 1, len(dates))
    
    # Heat waves and cold spells
    extreme_events = np.zeros(len(dates))
    # Heat wave in summer 2022
    heat_wave_start = 180
    heat_wave_end = 190
    extreme_events[heat_wave_start:heat_wave_end] = 8
    
    # Cold spell in winter 2022
    cold_spell_start = 350
    cold_spell_end = 360
    extreme_events[cold_spell_start:cold_spell_end] = -10
    
    # Calculate final temperature
    temp_values = base_temp + seasonal + trend + daily_variation + extreme_events
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'value': temp_values.round(1)
    })
    
    return df

def main():
    """Create and save all agricultural datasets"""
    
    print("🌾 Creating Agricultural Datasets for TimesFM")
    print("=" * 50)
    
    # Create datasets
    datasets = {
        'crop_yield_data.csv': create_crop_yield_data(),
        'soil_moisture_data.csv': create_soil_moisture_data(),
        'commodity_price_data.csv': create_commodity_price_data(),
        'weather_temperature_data.csv': create_weather_data()
    }
    
    # Save datasets
    for filename, df in datasets.items():
        df.to_csv(filename, index=False)
        print(f"✅ Created {filename} - {len(df)} records")
        print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"   Value range: {df['value'].min():.2f} to {df['value'].max():.2f}")
        print()
    
    # Create a combined sample file
    sample_df = create_crop_yield_data().head(100)  # First 100 days
    sample_df.to_csv('sample_agricultural_data.csv', index=False)
    print(f"✅ Created sample_agricultural_data.csv - {len(sample_df)} records")
    
    print("\n🎉 All datasets created successfully!")
    print("\n📁 Files created:")
    for filename in datasets.keys():
        print(f"   - {filename}")
    print("   - sample_agricultural_data.csv")
    
    print("\n🚀 Ready to upload to TimesFM frontend at http://localhost:8501")
    print("\n💡 Each dataset is formatted correctly for TimesFM:")
    print("   - Column names: 'date', 'value'")
    print("   - Date format: YYYY-MM-DD")
    print("   - Numeric values only")
    print("   - No missing values")

if __name__ == "__main__":
    main()
