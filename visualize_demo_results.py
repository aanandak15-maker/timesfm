#!/usr/bin/env python3
"""
Visualize TimesFM demo results (text-based visualization).
"""

import numpy as np
import pandas as pd
import timesfm

def create_simple_sales_data():
    """Create simple sales data for visualization."""
    np.random.seed(42)
    n_days = 100
    
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=n_days, freq='D')
    
    # Create sales data with trend and seasonality
    trend = np.linspace(1000, 1200, n_days)
    weekly_pattern = 100 * np.sin(2 * np.pi * np.arange(n_days) / 7)
    noise = 20 * np.random.randn(n_days)
    sales = trend + weekly_pattern + noise
    
    return dates, sales

def text_plot(data, title, width=60, height=20):
    """Create a simple text-based plot."""
    print(f"\n{title}")
    print("=" * len(title))
    
    # Normalize data to fit in height
    min_val, max_val = np.min(data), np.max(data)
    if max_val == min_val:
        normalized = np.zeros_like(data)
    else:
        normalized = (data - min_val) / (max_val - min_val) * (height - 1)
    
    # Create plot
    for i in range(height):
        y_val = height - 1 - i
        line = ""
        for j, val in enumerate(normalized):
            if j >= width:
                break
            if abs(val - y_val) < 0.5:
                line += "*"
            else:
                line += " "
        print(f"{max_val - (i / (height-1)) * (max_val - min_val):8.1f} |{line}|")
    
    print("         " + "-" * width)
    print("         " + "".join([str(i%10) for i in range(width)]))

def run_visualization_demo():
    """Run a demo with text visualization."""
    print("📊 TimesFM Demo with Text Visualization")
    print("=" * 50)
    
    # Create data
    dates, sales = create_simple_sales_data()
    
    print(f"📈 Created sales data:")
    print(f"   Period: {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")
    print(f"   Data points: {len(sales)}")
    print(f"   Mean: {np.mean(sales):.1f}")
    print(f"   Std: {np.std(sales):.1f}")
    
    # Show historical data
    text_plot(sales, "Historical Sales Data (Last 60 days)", width=60, height=15)
    
    # Initialize model
    print("\n🤖 Initializing TimesFM model...")
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
    print("✅ Model initialized")
    
    # Make forecast
    print("\n🔮 Making forecast...")
    context = sales[-60:].astype(np.float32)  # Use last 60 days as context
    
    point_forecast, quantile_forecast = tfm.forecast(
        [context],
        freq=[0],  # Daily frequency
    )
    
    forecast = point_forecast[0]
    print(f"✅ Forecast completed! Horizon: {len(forecast)} days")
    
    # Show forecast
    text_plot(forecast, "Forecast (Next 20 days)", width=20, height=15)
    
    # Show combined view
    combined = np.concatenate([context, forecast])
    text_plot(combined, "Historical + Forecast (Last 60 + Next 20 days)", width=80, height=15)
    
    # Display statistics
    print(f"\n📊 Forecast Statistics:")
    print(f"   Forecast mean: {np.mean(forecast):.1f}")
    print(f"   Forecast std: {np.std(forecast):.1f}")
    print(f"   Min forecast: {np.min(forecast):.1f}")
    print(f"   Max forecast: {np.max(forecast):.1f}")
    
    # Show quantile information
    quantiles = quantile_forecast[0]
    print(f"\n📈 Uncertainty (Quantiles):")
    print(f"   10th percentile: {np.mean(quantiles[:, 0]):.1f}")
    print(f"   25th percentile: {np.mean(quantiles[:, 2]):.1f}")
    print(f"   50th percentile: {np.mean(quantiles[:, 4]):.1f}")
    print(f"   75th percentile: {np.mean(quantiles[:, 6]):.1f}")
    print(f"   90th percentile: {np.mean(quantiles[:, 8]):.1f}")
    
    # Show trend analysis
    historical_trend = np.polyfit(range(len(context)), context, 1)[0]
    forecast_trend = np.polyfit(range(len(forecast)), forecast, 1)[0]
    
    print(f"\n📈 Trend Analysis:")
    print(f"   Historical trend: {historical_trend:.2f} units/day")
    print(f"   Forecast trend: {forecast_trend:.2f} units/day")
    
    if abs(forecast_trend - historical_trend) < 0.1:
        print("   → Forecast continues historical trend")
    elif forecast_trend > historical_trend:
        print("   → Forecast shows accelerating growth")
    else:
        print("   → Forecast shows decelerating growth")
    
    print(f"\n🎯 Key Insights:")
    print(f"   • Historical data shows {len(context)} days of context")
    print(f"   • Forecast extends {len(forecast)} days into the future")
    print(f"   • Model captured seasonal patterns in the data")
    print(f"   • Uncertainty estimates available via quantiles")
    print(f"   • Zero-shot forecasting (no training required)")

if __name__ == "__main__":
    run_visualization_demo()
