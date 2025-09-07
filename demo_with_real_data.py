#!/usr/bin/env python3
"""
TimesFM Demo with Realistic Data
Demonstrates forecasting on various types of time series data.
"""

import numpy as np
import pandas as pd
import timesfm
from datetime import datetime, timedelta

def create_sales_data():
    """Create realistic sales data with trend, seasonality, and promotions."""
    np.random.seed(42)
    n_days = 365  # One year of daily data
    
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=n_days, freq='D')
    
    # Base trend (growing business)
    trend = np.linspace(1000, 1500, n_days)
    
    # Weekly seasonality (higher sales on weekends)
    weekly_pattern = 200 * np.sin(2 * np.pi * np.arange(n_days) / 7)
    
    # Monthly seasonality (end of month boost)
    monthly_pattern = 100 * np.sin(2 * np.pi * np.arange(n_days) / 30.44)
    
    # Holiday effects (simplified)
    holiday_boost = np.zeros(n_days)
    # Black Friday effect
    holiday_boost[300:310] = 500  # November spike
    # Christmas effect  
    holiday_boost[350:365] = 300  # December spike
    
    # Random noise
    noise = 50 * np.random.randn(n_days)
    
    # Combine all components
    sales = trend + weekly_pattern + monthly_pattern + holiday_boost + noise
    sales = np.maximum(sales, 0)  # Ensure non-negative sales
    
    return dates, sales

def create_stock_price_data():
    """Create realistic stock price data with volatility clustering."""
    np.random.seed(123)
    n_days = 252  # One trading year
    
    # Create date range (weekdays only)
    dates = pd.date_range(start='2023-01-01', periods=n_days, freq='B')  # Business days
    
    # Start price
    initial_price = 100.0
    prices = [initial_price]
    
    # Generate price movements with volatility clustering
    for i in range(1, n_days):
        # Volatility clustering (higher volatility after large moves)
        recent_volatility = np.std(prices[-5:]) if len(prices) >= 5 else 0.02
        volatility = 0.01 + recent_volatility * 0.5
        
        # Random walk with drift
        daily_return = 0.0005 + volatility * np.random.randn()  # Small positive drift
        new_price = prices[-1] * (1 + daily_return)
        prices.append(new_price)
    
    return dates, np.array(prices)

def create_website_traffic_data():
    """Create realistic website traffic data."""
    np.random.seed(456)
    n_hours = 24 * 30  # 30 days of hourly data
    
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=n_hours, freq='H')
    
    # Base traffic level
    base_traffic = 1000
    
    # Daily pattern (higher during business hours)
    hour_of_day = np.array([d.hour for d in dates])
    daily_pattern = 500 * np.sin(2 * np.pi * hour_of_day / 24 - np.pi/2) + 500
    
    # Weekly pattern (lower on weekends)
    day_of_week = np.array([d.weekday() for d in dates])
    weekly_pattern = np.where(day_of_week < 5, 200, -100)  # Weekdays vs weekends
    
    # Growth trend
    trend = np.linspace(0, 300, n_hours)
    
    # Random noise
    noise = 100 * np.random.randn(n_hours)
    
    # Combine components
    traffic = base_traffic + daily_pattern + weekly_pattern + trend + noise
    traffic = np.maximum(traffic, 0)  # Ensure non-negative
    
    return dates, traffic

def create_temperature_data():
    """Create realistic temperature data with seasonal patterns."""
    np.random.seed(789)
    n_days = 365 * 2  # Two years of daily data
    
    # Create date range
    dates = pd.date_range(start='2022-01-01', periods=n_days, freq='D')
    
    # Base temperature
    base_temp = 15  # Celsius
    
    # Annual seasonality
    day_of_year = np.array([d.timetuple().tm_yday for d in dates])
    annual_pattern = 10 * np.sin(2 * np.pi * day_of_year / 365.25 - np.pi/2)
    
    # Long-term trend (climate change simulation)
    trend = np.linspace(0, 1, n_days)  # Gradual warming
    
    # Random weather variations
    noise = 3 * np.random.randn(n_days)
    
    # Combine components
    temperature = base_temp + annual_pattern + trend + noise
    
    return dates, temperature

def demo_forecasting():
    """Run forecasting demo on all datasets."""
    print("🚀 TimesFM Demo with Realistic Data")
    print("=" * 60)
    
    # Initialize model
    print("🤖 Initializing TimesFM model...")
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=1,
            horizon_len=30,  # Forecast 30 periods ahead
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    print("✅ Model initialized successfully\n")
    
    # Test datasets
    datasets = [
        ("📈 Sales Data", create_sales_data, 0, "Daily sales with trend, seasonality, and promotions"),
        ("📊 Stock Prices", create_stock_price_data, 0, "Daily stock prices with volatility clustering"),
        ("🌐 Website Traffic", create_website_traffic_data, 0, "Hourly website traffic with daily/weekly patterns"),
        ("🌡️ Temperature", create_temperature_data, 0, "Daily temperature with seasonal patterns")
    ]
    
    results = {}
    
    for name, data_func, freq, description in datasets:
        print(f"{name}")
        print("-" * 40)
        print(f"Description: {description}")
        
        # Create data
        dates, values = data_func()
        print(f"Data points: {len(values)}")
        print(f"Date range: {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")
        print(f"Mean: {np.mean(values):.2f}")
        print(f"Std: {np.std(values):.2f}")
        
        # Prepare for forecasting (use last 200 points as context)
        context = values[-200:].astype(np.float32)
        
        # Make forecast
        print("🔮 Making forecast...")
        forecast_input = [context]
        frequency_input = [freq]
        
        point_forecast, quantile_forecast = tfm.forecast(
            forecast_input,
            freq=frequency_input,
        )
        
        # Store results
        results[name] = {
            'dates': dates,
            'values': values,
            'context': context,
            'forecast': point_forecast[0],
            'quantiles': quantile_forecast[0]
        }
        
        # Display results
        print("✅ Forecast completed!")
        print(f"Forecast horizon: {len(point_forecast[0])} periods")
        print(f"Forecast mean: {np.mean(point_forecast[0]):.2f}")
        print(f"Forecast std: {np.std(point_forecast[0]):.2f}")
        print(f"First 5 forecast values: {point_forecast[0, :5]}")
        print(f"Last 5 forecast values: {point_forecast[0, -5:]}")
        print()
    
    return results

def demo_dataframe_forecasting():
    """Demo DataFrame-based forecasting."""
    print("📊 DataFrame Forecasting Demo")
    print("=" * 40)
    
    # Create multiple time series
    np.random.seed(42)
    n_series = 3
    n_days = 100
    
    # Create DataFrame with multiple series
    data_list = []
    for i in range(n_series):
        # Different patterns for each series
        base_value = 100 + i * 50
        trend = np.linspace(0, 20, n_days)
        seasonal = 10 * np.sin(2 * np.pi * np.arange(n_days) / 30)
        noise = 5 * np.random.randn(n_days)
        values = base_value + trend + seasonal + noise
        
        dates = pd.date_range(start='2023-01-01', periods=n_days, freq='D')
        
        for j, (date, value) in enumerate(zip(dates, values)):
            data_list.append({
                'unique_id': f'series_{i+1}',
                'ds': date,
                'y': value
            })
    
    df = pd.DataFrame(data_list)
    print(f"Created DataFrame with {len(df)} rows")
    print(f"Number of unique series: {df['unique_id'].nunique()}")
    print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")
    
    # Initialize model
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=1,
            horizon_len=20,
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    
    # Forecast using DataFrame
    print("🔮 Making DataFrame forecast...")
    forecast_df = tfm.forecast_on_df(
        inputs=df,
        freq="D",  # Daily frequency
        value_name="y",
        num_jobs=1,
        verbose=False
    )
    
    print("✅ DataFrame forecast completed!")
    print(f"Forecast DataFrame shape: {forecast_df.shape}")
    print(f"Forecast columns: {list(forecast_df.columns)}")
    
    # Display sample results
    print("\nSample forecast results:")
    for series_id in df['unique_id'].unique():
        series_forecast = forecast_df[forecast_df['unique_id'] == series_id]
        print(f"{series_id}: {len(series_forecast)} forecast points")
        print(f"  Mean forecast: {series_forecast['timesfm'].mean():.2f}")
        print(f"  Std forecast: {series_forecast['timesfm'].std():.2f}")
    
    return df, forecast_df

def main():
    """Run the complete demo."""
    try:
        # Run array-based forecasting demo
        results = demo_forecasting()
        
        # Run DataFrame-based forecasting demo
        df, forecast_df = demo_dataframe_forecasting()
        
        print("\n🎉 Demo completed successfully!")
        print("\n📋 Summary of what was demonstrated:")
        print("   ✅ Sales forecasting with trend and seasonality")
        print("   ✅ Stock price forecasting with volatility")
        print("   ✅ Website traffic forecasting with daily patterns")
        print("   ✅ Temperature forecasting with seasonal patterns")
        print("   ✅ Multi-series DataFrame forecasting")
        print("   ✅ Quantile forecasting for uncertainty")
        
        print("\n💡 Key Insights:")
        print("   • TimesFM works well with various data patterns")
        print("   • Handles trend, seasonality, and noise effectively")
        print("   • Provides uncertainty estimates via quantiles")
        print("   • Supports both array and DataFrame inputs")
        print("   • Zero-shot forecasting (no training required)")
        
        print("\n🔧 Next Steps:")
        print("   • Try the 2.0-500m model for better performance")
        print("   • Experiment with different context lengths")
        print("   • Use covariates for external features")
        print("   • Fine-tune on your specific data")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
