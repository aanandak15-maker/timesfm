#!/usr/bin/env python3
"""
Simple TimesFM example demonstrating basic functionality.
"""

import numpy as np
import pandas as pd
import timesfm

def main():
    """Run a simple TimesFM example."""
    print("🚀 TimesFM Simple Example")
    print("=" * 40)
    
    # Create sample time series
    np.random.seed(42)
    n_points = 100
    
    # Create a time series with trend and seasonality
    trend = np.linspace(100, 200, n_points)
    seasonal = 20 * np.sin(2 * np.pi * np.arange(n_points) / 30)  # Monthly seasonality
    noise = 5 * np.random.randn(n_points)
    values = trend + seasonal + noise
    
    print(f"📊 Created time series with {n_points} points")
    print(f"   Mean: {np.mean(values):.2f}")
    print(f"   Std: {np.std(values):.2f}")
    
    # Initialize model
    print("\n🤖 Initializing TimesFM model...")
    tfm = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend="cpu",
            per_core_batch_size=1,
            horizon_len=20,  # Forecast 20 steps ahead
            context_len=512,
            num_layers=20,
            use_positional_embedding=False,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(
            huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
        )
    )
    print("✅ Model initialized successfully")
    
    # Make forecast
    print("\n🔮 Making forecast...")
    forecast_input = [values.astype(np.float32)]
    frequency_input = [0]  # High frequency (daily)
    
    point_forecast, quantile_forecast = tfm.forecast(
        forecast_input,
        freq=frequency_input,
    )
    
    print("✅ Forecast completed!")
    print(f"   Forecast horizon: {point_forecast.shape[1]} steps")
    print(f"   Point forecast shape: {point_forecast.shape}")
    print(f"   Quantile forecast shape: {quantile_forecast.shape}")
    
    # Display results
    print("\n📈 Forecast Results:")
    print(f"   First 5 values: {point_forecast[0, :5]}")
    print(f"   Last 5 values: {point_forecast[0, -5:]}")
    print(f"   Forecast mean: {np.mean(point_forecast[0]):.2f}")
    print(f"   Forecast std: {np.std(point_forecast[0]):.2f}")
    
    # Test DataFrame forecasting
    print("\n📊 Testing DataFrame forecasting...")
    dates = pd.date_range(start='2020-01-01', periods=n_points, freq='D')
    df = pd.DataFrame({
        'unique_id': 'test_series',
        'ds': dates,
        'y': values
    })
    
    forecast_df = tfm.forecast_on_df(
        inputs=df,
        freq="D",  # Daily frequency
        value_name="y",
        num_jobs=1,
        verbose=False
    )
    
    print("✅ DataFrame forecast completed!")
    print(f"   Input DataFrame shape: {df.shape}")
    print(f"   Forecast DataFrame shape: {forecast_df.shape}")
    print(f"   Forecast columns: {list(forecast_df.columns)}")
    
    print("\n🎉 All tests completed successfully!")
    print("\n💡 Key Features Demonstrated:")
    print("   • Zero-shot forecasting (no training required)")
    print("   • Array input forecasting")
    print("   • DataFrame input forecasting")
    print("   • Quantile forecasting for uncertainty")
    print("   • CPU-based inference")

if __name__ == "__main__":
    main()

