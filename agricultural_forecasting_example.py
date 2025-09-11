#!/usr/bin/env python3
"""
Practical Agricultural Forecasting Examples with TimesFM
Demonstrates real-world agricultural applications.
"""

import numpy as np
import pandas as pd
import timesfm
from datetime import datetime, timedelta

def create_crop_yield_data():
    """Create realistic crop yield data with seasonal patterns."""
    np.random.seed(42)
    n_years = 5
    n_days = n_years * 365
    
    # Create date range
    dates = pd.date_range(start='2019-01-01', periods=n_days, freq='D')
    
    # Base yield with trend (improving farming practices)
    base_yield = 3.0  # tons/hectare
    trend = np.linspace(0, 0.5, n_days)  # Gradual improvement
    
    # Seasonal pattern (harvest season)
    day_of_year = np.array([d.timetuple().tm_yday for d in dates])
    seasonal_pattern = 0.8 * np.sin(2 * np.pi * day_of_year / 365.25 - np.pi/2)
    
    # Weather effects (simplified)
    weather_effect = 0.3 * np.sin(2 * np.pi * np.arange(n_days) / 30)  # Monthly variation
    
    # Random variations
    noise = 0.2 * np.random.randn(n_days)
    
    # Combine components
    yield_data = base_yield + trend + seasonal_pattern + weather_effect + noise
    yield_data = np.maximum(yield_data, 0.5)  # Ensure positive yields
    
    return dates, yield_data

def create_soil_moisture_data():
    """Create realistic soil moisture data."""
    np.random.seed(123)
    n_days = 365
    
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=n_days, freq='D')
    
    # Base moisture level
    base_moisture = 40  # percentage
    
    # Seasonal pattern (higher in winter/spring)
    day_of_year = np.array([d.timetuple().tm_yday for d in dates])
    seasonal_pattern = 15 * np.sin(2 * np.pi * day_of_year / 365.25 + np.pi/2)
    
    # Irrigation effect (weekly pattern)
    weekly_pattern = 5 * np.sin(2 * np.pi * np.arange(n_days) / 7)
    
    # Random variations
    noise = 3 * np.random.randn(n_days)
    
    # Combine components
    moisture_data = base_moisture + seasonal_pattern + weekly_pattern + noise
    moisture_data = np.clip(moisture_data, 10, 80)  # Keep within realistic bounds
    
    return dates, moisture_data

def create_milk_production_data():
    """Create realistic daily milk production data."""
    np.random.seed(456)
    n_days = 365
    
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=n_days, freq='D')
    
    # Base production
    base_production = 500  # liters per day
    
    # Seasonal pattern (higher in spring)
    day_of_year = np.array([d.timetuple().tm_yday for d in dates])
    seasonal_pattern = 50 * np.sin(2 * np.pi * day_of_year / 365.25 - np.pi/2)
    
    # Feed quality effect (monthly variation)
    feed_effect = 20 * np.sin(2 * np.pi * np.arange(n_days) / 30)
    
    # Random variations
    noise = 15 * np.random.randn(n_days)
    
    # Combine components
    production_data = base_production + seasonal_pattern + feed_effect + noise
    production_data = np.maximum(production_data, 300)  # Ensure minimum production
    
    return dates, production_data

def create_commodity_price_data():
    """Create realistic agricultural commodity price data."""
    np.random.seed(789)
    n_days = 252  # Trading days in a year
    
    # Create date range (business days only)
    dates = pd.date_range(start='2023-01-01', periods=n_days, freq='B')
    
    # Start price
    initial_price = 200.0  # $/ton
    
    # Generate price movements
    prices = [initial_price]
    for i in range(1, n_days):
        # Random walk with slight upward trend
        daily_return = 0.0002 + 0.02 * np.random.randn()  # 0.02% daily volatility
        new_price = prices[-1] * (1 + daily_return)
        prices.append(new_price)
    
    return dates, np.array(prices)

def forecast_crop_yield():
    """Forecast crop yield for next season."""
    print("🌾 Crop Yield Forecasting")
    print("-" * 40)
    
    # Create data
    dates, yield_data = create_crop_yield_data()
    
    print(f"Historical yield data:")
    print(f"  Period: {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")
    print(f"  Average yield: {np.mean(yield_data):.2f} tons/hectare")
    print(f"  Yield range: {np.min(yield_data):.2f} - {np.max(yield_data):.2f} tons/hectare")
    
    # Initialize model
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=1,
            horizon_len=30,  # Forecast next 30 days
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    
    # Make forecast
    context = yield_data[-200:].astype(np.float32)  # Use last 200 days
    point_forecast, quantile_forecast = tfm.forecast([context], freq=[0])
    
    forecast = point_forecast[0]
    quantiles = quantile_forecast[0]
    
    print(f"\n📈 Yield Forecast:")
    print(f"  Forecast horizon: {len(forecast)} days")
    print(f"  Average predicted yield: {np.mean(forecast):.2f} tons/hectare")
    print(f"  Forecast range: {np.min(forecast):.2f} - {np.max(forecast):.2f} tons/hectare")
    print(f"  Uncertainty (90% confidence): {np.mean(quantiles[:, 0]):.2f} - {np.mean(quantiles[:, 8]):.2f} tons/hectare")
    
    return forecast, quantiles

def forecast_soil_moisture():
    """Forecast soil moisture for irrigation planning."""
    print("\n💧 Soil Moisture Forecasting")
    print("-" * 40)
    
    # Create data
    dates, moisture_data = create_soil_moisture_data()
    
    print(f"Historical soil moisture data:")
    print(f"  Period: {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")
    print(f"  Average moisture: {np.mean(moisture_data):.1f}%")
    print(f"  Moisture range: {np.min(moisture_data):.1f}% - {np.max(moisture_data):.1f}%")
    
    # Initialize model
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=1,
            horizon_len=14,  # Forecast next 2 weeks
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    
    # Make forecast
    context = moisture_data[-100:].astype(np.float32)  # Use last 100 days
    point_forecast, quantile_forecast = tfm.forecast([context], freq=[0])
    
    forecast = point_forecast[0]
    quantiles = quantile_forecast[0]
    
    print(f"\n📈 Moisture Forecast:")
    print(f"  Forecast horizon: {len(forecast)} days")
    print(f"  Average predicted moisture: {np.mean(forecast):.1f}%")
    print(f"  Forecast range: {np.min(forecast):.1f}% - {np.max(forecast):.1f}%")
    
    # Irrigation recommendations
    avg_moisture = np.mean(forecast)
    if avg_moisture < 30:
        print(f"  🚨 IRRIGATION NEEDED: Moisture below 30% threshold")
    elif avg_moisture < 40:
        print(f"  ⚠️  Monitor closely: Moisture approaching irrigation threshold")
    else:
        print(f"  ✅ Adequate moisture: No irrigation needed")
    
    return forecast, quantiles

def forecast_milk_production():
    """Forecast daily milk production."""
    print("\n🐄 Milk Production Forecasting")
    print("-" * 40)
    
    # Create data
    dates, production_data = create_milk_production_data()
    
    print(f"Historical milk production data:")
    print(f"  Period: {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")
    print(f"  Average production: {np.mean(production_data):.0f} liters/day")
    print(f"  Production range: {np.min(production_data):.0f} - {np.max(production_data):.0f} liters/day")
    
    # Initialize model
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=1,
            horizon_len=30,  # Forecast next 30 days
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    
    # Make forecast
    context = production_data[-150:].astype(np.float32)  # Use last 150 days
    point_forecast, quantile_forecast = tfm.forecast([context], freq=[0])
    
    forecast = point_forecast[0]
    quantiles = quantile_forecast[0]
    
    print(f"\n📈 Production Forecast:")
    print(f"  Forecast horizon: {len(forecast)} days")
    print(f"  Average predicted production: {np.mean(forecast):.0f} liters/day")
    print(f"  Forecast range: {np.min(forecast):.0f} - {np.max(forecast):.0f} liters/day")
    
    # Production planning
    total_forecast = np.sum(forecast)
    print(f"  Total predicted production: {total_forecast:.0f} liters over {len(forecast)} days")
    
    return forecast, quantiles

def forecast_commodity_prices():
    """Forecast agricultural commodity prices."""
    print("\n💰 Commodity Price Forecasting")
    print("-" * 40)
    
    # Create data
    dates, price_data = create_commodity_price_data()
    
    print(f"Historical price data:")
    print(f"  Period: {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")
    print(f"  Average price: ${np.mean(price_data):.2f}/ton")
    print(f"  Price range: ${np.min(price_data):.2f} - ${np.max(price_data):.2f}/ton")
    
    # Initialize model
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=1,
            horizon_len=30,  # Forecast next 30 trading days
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    
    # Make forecast
    context = price_data[-100:].astype(np.float32)  # Use last 100 days
    point_forecast, quantile_forecast = tfm.forecast([context], freq=[0])
    
    forecast = point_forecast[0]
    quantiles = quantile_forecast[0]
    
    print(f"\n📈 Price Forecast:")
    print(f"  Forecast horizon: {len(forecast)} trading days")
    print(f"  Average predicted price: ${np.mean(forecast):.2f}/ton")
    print(f"  Forecast range: ${np.min(forecast):.2f} - ${np.max(forecast):.2f}/ton")
    
    # Price trend analysis
    current_price = price_data[-1]
    forecast_price = np.mean(forecast)
    price_change = ((forecast_price - current_price) / current_price) * 100
    
    print(f"  Current price: ${current_price:.2f}/ton")
    print(f"  Predicted price: ${forecast_price:.2f}/ton")
    print(f"  Expected change: {price_change:+.1f}%")
    
    if price_change > 5:
        print(f"  📈 BULLISH: Consider holding or buying")
    elif price_change < -5:
        print(f"  📉 BEARISH: Consider selling or hedging")
    else:
        print(f"  ➡️  NEUTRAL: Monitor market conditions")
    
    return forecast, quantiles

def main():
    """Run all agricultural forecasting examples."""
    print("🌾 Agricultural Forecasting with TimesFM")
    print("=" * 60)
    
    try:
        # Run all forecasting examples
        yield_forecast, yield_quantiles = forecast_crop_yield()
        moisture_forecast, moisture_quantiles = forecast_soil_moisture()
        production_forecast, production_quantiles = forecast_milk_production()
        price_forecast, price_quantiles = forecast_commodity_prices()
        
        print("\n🎉 All Agricultural Forecasts Completed Successfully!")
        print("\n📋 Summary of Applications:")
        print("   ✅ Crop yield forecasting for harvest planning")
        print("   ✅ Soil moisture forecasting for irrigation management")
        print("   ✅ Milk production forecasting for dairy operations")
        print("   ✅ Commodity price forecasting for market decisions")
        
        print("\n💡 Key Benefits for Agriculture:")
        print("   • Optimize resource allocation")
        print("   • Reduce water and feed waste")
        print("   • Improve harvest timing")
        print("   • Better market timing decisions")
        print("   • Risk management and planning")
        
        print("\n🔧 Next Steps:")
        print("   • Replace demo data with your actual agricultural data")
        print("   • Experiment with different forecast horizons")
        print("   • Use uncertainty estimates for risk management")
        print("   • Integrate with your farm management systems")
        
    except Exception as e:
        print(f"❌ Error during agricultural forecasting: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

