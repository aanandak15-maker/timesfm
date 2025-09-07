#!/usr/bin/env python3
"""
Comprehensive TimesFM example demonstrating various features.
"""

import numpy as np
import pandas as pd
import timesfm
from datetime import datetime, timedelta

def create_sample_data():
    """Create sample time series data."""
    # Create a synthetic time series with trend and seasonality
    np.random.seed(42)
    n_points = 200
    
    # Time index
    dates = pd.date_range(start='2020-01-01', periods=n_points, freq='D')
    
    # Create time series with trend and seasonality
    trend = np.linspace(100, 200, n_points)
    seasonal = 20 * np.sin(2 * np.pi * np.arange(n_points) / 365.25)  # Annual seasonality
    noise = 5 * np.random.randn(n_points)
    
    values = trend + seasonal + noise
    
    return dates, values

def example_1_basic_forecasting():
    """Example 1: Basic time series forecasting."""
    print("🔮 Example 1: Basic Time Series Forecasting")
    print("=" * 50)
    
    # Create sample data
    dates, values = create_sample_data()
    
    # Initialize model
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=1,
            horizon_len=30,  # Forecast 30 days ahead
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    
    # Prepare input (use last 100 points as context)
    context = values[-100:].astype(np.float32)
    
    # Make forecast
    forecast_input = [context]
    frequency_input = [0]  # Daily frequency
    
    point_forecast, quantile_forecast = tfm.forecast(
        forecast_input,
        freq=frequency_input,
    )
    
    # Display results
    print(f"✅ Forecast completed!")
    print(f"   Context length: {len(context)}")
    print(f"   Forecast horizon: {point_forecast.shape[1]} days")
    print(f"   Point forecast mean: {np.mean(point_forecast[0]):.2f}")
    print(f"   Point forecast std: {np.std(point_forecast[0]):.2f}")
    
    return context, point_forecast[0], quantile_forecast[0]

def example_2_dataframe_forecasting():
    """Example 2: Forecasting with pandas DataFrame."""
    print("\n📊 Example 2: DataFrame Forecasting")
    print("=" * 50)
    
    # Create sample DataFrame
    dates, values = create_sample_data()
    
    df = pd.DataFrame({
        'unique_id': 'series_1',
        'ds': dates,
        'y': values
    })
    
    # Initialize model
    tfm = timesfm.TimesFm(
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
    
    # Forecast using DataFrame
    forecast_df = tfm.forecast_on_df(
        inputs=df,
        freq="D",  # Daily frequency
        value_name="y",
        num_jobs=1,
        verbose=True
    )
    
    print(f"✅ DataFrame forecast completed!")
    print(f"   Input DataFrame shape: {df.shape}")
    print(f"   Forecast DataFrame shape: {forecast_df.shape}")
    print(f"   Forecast columns: {list(forecast_df.columns)}")
    
    return df, forecast_df

def example_3_multiple_series():
    """Example 3: Forecasting multiple time series."""
    print("\n📈 Example 3: Multiple Time Series Forecasting")
    print("=" * 50)
    
    # Create multiple time series
    np.random.seed(42)
    n_series = 3
    n_points = 150
    
    series_list = []
    for i in range(n_series):
        # Different patterns for each series
        trend = np.linspace(50 + i*20, 150 + i*20, n_points)
        seasonal = (10 + i*5) * np.sin(2 * np.pi * np.arange(n_points) / 30)  # Monthly seasonality
        noise = (3 + i) * np.random.randn(n_points)
        values = trend + seasonal + noise
        series_list.append(values.astype(np.float32))
    
    # Initialize model
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=3,  # Batch size for 3 series
            horizon_len=20,
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    
    # Make forecasts for all series
    frequency_input = [0] * n_series  # All daily frequency
    
    point_forecast, quantile_forecast = tfm.forecast(
        series_list,
        freq=frequency_input,
    )
    
    print(f"✅ Multiple series forecast completed!")
    print(f"   Number of series: {len(series_list)}")
    print(f"   Forecast shape: {point_forecast.shape}")
    print(f"   Quantile forecast shape: {quantile_forecast.shape}")
    
    # Display summary statistics
    for i in range(n_series):
        print(f"   Series {i+1} forecast mean: {np.mean(point_forecast[i]):.2f}")
        print(f"   Series {i+1} forecast std: {np.std(point_forecast[i]):.2f}")
    
    return series_list, point_forecast, quantile_forecast

def example_4_different_frequencies():
    """Example 4: Different frequency types."""
    print("\n⏰ Example 4: Different Frequency Types")
    print("=" * 50)
    
    # Create time series of different frequencies
    np.random.seed(42)
    
    # High frequency (daily) - 100 points
    daily_series = np.cumsum(np.random.randn(100)) + 100
    
    # Medium frequency (weekly) - 50 points  
    weekly_series = np.cumsum(np.random.randn(50)) + 200
    
    # Low frequency (monthly) - 24 points
    monthly_series = np.cumsum(np.random.randn(24)) + 300
    
    series_list = [daily_series, weekly_series, monthly_series]
    frequency_list = [0, 1, 2]  # High, medium, low frequency
    
    # Initialize model
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=3,
            horizon_len=10,
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    
    # Make forecasts
    point_forecast, quantile_forecast = tfm.forecast(
        series_list,
        freq=frequency_list,
    )
    
    print(f"✅ Multi-frequency forecast completed!")
    freq_names = ["High (Daily)", "Medium (Weekly)", "Low (Monthly)"]
    
    for i, (series, freq_name) in enumerate(zip(series_list, freq_names)):
        print(f"   {freq_name}:")
        print(f"     Input length: {len(series)}")
        print(f"     Forecast mean: {np.mean(point_forecast[i]):.2f}")
        print(f"     Forecast std: {np.std(point_forecast[i]):.2f}")
    
    return series_list, point_forecast, frequency_list

def main():
    """Run all examples."""
    print("🚀 TimesFM Comprehensive Examples")
    print("=" * 60)
    
    try:
        # Run examples
        context, forecast1, quantiles1 = example_1_basic_forecasting()
        df, forecast_df = example_2_dataframe_forecasting()
        series_list, forecast3, quantiles3 = example_3_multiple_series()
        freq_series, forecast4, frequencies = example_4_different_frequencies()
        
        print("\n🎉 All examples completed successfully!")
        print("\n📋 Summary:")
        print("   ✅ Basic forecasting")
        print("   ✅ DataFrame forecasting") 
        print("   ✅ Multiple series forecasting")
        print("   ✅ Different frequency types")
        
        print("\n💡 Key Features Demonstrated:")
        print("   • Zero-shot forecasting (no training required)")
        print("   • Multiple input formats (arrays, DataFrames)")
        print("   • Batch processing for multiple series")
        print("   • Different frequency handling")
        print("   • Quantile forecasting for uncertainty")
        
        print("\n🔧 Next Steps:")
        print("   • Try the 2.0-500m model for better performance")
        print("   • Experiment with fine-tuning on your data")
        print("   • Explore covariates support for external features")
        print("   • Check out the notebooks/ directory for more examples")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
