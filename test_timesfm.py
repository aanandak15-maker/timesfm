#!/usr/bin/env python3
"""
Simple test script to verify TimesFM installation and basic functionality.
"""

import numpy as np
import timesfm

def test_timesfm_installation():
    """Test basic TimesFM functionality."""
    print("🚀 Testing TimesFM installation...")
    
    try:
        # Test 1: Import and basic initialization
        print("✅ TimesFM imported successfully")
        
        # Test 2: Create a simple time series
        print("📊 Creating test time series...")
        np.random.seed(42)
        test_series = np.sin(np.linspace(0, 4*np.pi, 100)) + 0.1 * np.random.randn(100)
        print(f"   Created time series with {len(test_series)} points")
        
        # Test 3: Initialize model (this will download the model if not present)
        print("🤖 Initializing TimesFM model...")
        print("   Note: This will download the model checkpoint on first run (~500MB)")
        
        tfm = timesfm.TimesFm(
            hparams=timesfm.TimesFmHparams(
                backend="cpu",  # Use CPU for compatibility
                per_core_batch_size=1,
                horizon_len=32,
                context_len=512,
                num_layers=20,
                use_positional_embedding=False,
            ),
            checkpoint=timesfm.TimesFmCheckpoint(
                huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
            )
        )
        print("✅ Model initialized successfully")
        
        # Test 4: Make a forecast
        print("🔮 Making a forecast...")
        forecast_input = [test_series]
        frequency_input = [0]  # High frequency
        
        point_forecast, quantile_forecast = tfm.forecast(
            forecast_input,
            freq=frequency_input,
        )
        
        print(f"✅ Forecast completed successfully!")
        print(f"   Point forecast shape: {point_forecast.shape}")
        print(f"   Quantile forecast shape: {quantile_forecast.shape}")
        print(f"   Forecast horizon: {point_forecast.shape[1]} steps")
        
        # Test 5: Display some results
        print("\n📈 Sample forecast results:")
        print(f"   First 5 forecast values: {point_forecast[0, :5]}")
        print(f"   Last 5 forecast values: {point_forecast[0, -5:]}")
        
        print("\n🎉 All tests passed! TimesFM is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_timesfm_installation()
    if success:
        print("\n✨ TimesFM is ready to use!")
    else:
        print("\n💥 There were issues with the installation.")

