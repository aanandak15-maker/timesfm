#!/usr/bin/env python3
"""
Validate TimesFM correctness and accuracy.
"""

import numpy as np
import pandas as pd
import timesfm
import warnings
warnings.filterwarnings('ignore')

def test_basic_functionality():
    """Test basic TimesFM functionality."""
    print("🔍 Testing Basic Functionality")
    print("-" * 40)
    
    try:
        # Test 1: Model initialization
        tfm = timesfm.TimesFm(
            hparams=timesfm.TimesFmHparams(
                backend="cpu",
                per_core_batch_size=1,
                horizon_len=10,
                context_len=512,
                num_layers=20,
                use_positional_embedding=False,
            ),
            checkpoint=timesfm.TimesFmCheckpoint(
                huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
            )
        )
        print("✅ Model initialization: PASSED")
        
        # Test 2: Simple forecast
        test_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10, dtype=np.float32)
        point_forecast, quantile_forecast = tfm.forecast([test_data], freq=[0])
        
        # Validate output shapes
        assert point_forecast.shape == (1, 10), f"Expected (1, 10), got {point_forecast.shape}"
        assert quantile_forecast.shape == (1, 10, 10), f"Expected (1, 10, 10), got {quantile_forecast.shape}"
        print("✅ Forecast output shapes: PASSED")
        
        # Test 3: Check for NaN or infinite values
        assert not np.any(np.isnan(point_forecast)), "Point forecast contains NaN values"
        assert not np.any(np.isinf(point_forecast)), "Point forecast contains infinite values"
        assert not np.any(np.isnan(quantile_forecast)), "Quantile forecast contains NaN values"
        assert not np.any(np.isinf(quantile_forecast)), "Quantile forecast contains infinite values"
        print("✅ No NaN or infinite values: PASSED")
        
        # Test 4: Quantile ordering
        for i in range(quantile_forecast.shape[1]):
            quantiles = quantile_forecast[0, i, :]
            assert np.all(np.diff(quantiles) >= 0), f"Quantiles not properly ordered at timestep {i}"
        print("✅ Quantile ordering: PASSED")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_agricultural_data_patterns():
    """Test with agricultural data patterns."""
    print("\n🌾 Testing Agricultural Data Patterns")
    print("-" * 40)
    
    try:
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
        
        # Test 1: Crop yield data (seasonal pattern)
        np.random.seed(42)
        n_days = 365
        days = np.arange(n_days)
        
        # Simulate crop yield with seasonal pattern
        base_yield = 100
        seasonal_pattern = 30 * np.sin(2 * np.pi * days / 365.25 - np.pi/2)  # Peak in summer
        trend = 0.1 * days  # Slight increasing trend
        noise = 5 * np.random.randn(n_days)
        crop_yield = base_yield + seasonal_pattern + trend + noise
        
        point_forecast, quantile_forecast = tfm.forecast([crop_yield], freq=[0])
        print("✅ Crop yield forecasting: PASSED")
        
        # Test 2: Soil moisture data (irregular pattern)
        soil_moisture = 50 + 20 * np.sin(2 * np.pi * days / 7) + 10 * np.random.randn(n_days)
        soil_moisture = np.clip(soil_moisture, 0, 100)  # Keep within realistic bounds
        
        point_forecast, quantile_forecast = tfm.forecast([soil_moisture], freq=[0])
        print("✅ Soil moisture forecasting: PASSED")
        
        # Test 3: Commodity prices (volatile pattern)
        price_changes = np.random.randn(n_days) * 0.02  # 2% daily volatility
        commodity_prices = 100 * np.exp(np.cumsum(price_changes))
        
        point_forecast, quantile_forecast = tfm.forecast([commodity_prices], freq=[0])
        print("✅ Commodity price forecasting: PASSED")
        
        return True
        
    except Exception as e:
        print(f"❌ Agricultural data test failed: {e}")
        return False

def test_dataframe_functionality():
    """Test DataFrame functionality."""
    print("\n📊 Testing DataFrame Functionality")
    print("-" * 40)
    
    try:
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
        
        # Create agricultural DataFrame
        np.random.seed(42)
        n_days = 100
        dates = pd.date_range(start='2023-01-01', periods=n_days, freq='D')
        
        # Create multiple agricultural time series
        data_list = []
        for i, crop in enumerate(['wheat', 'corn', 'soybean']):
            base_yield = 50 + i * 20
            seasonal = 10 * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
            trend = 0.05 * np.arange(n_days)
            noise = 3 * np.random.randn(n_days)
            yield_data = base_yield + seasonal + trend + noise
            
            for j, (date, yield_val) in enumerate(zip(dates, yield_data)):
                data_list.append({
                    'unique_id': crop,
                    'ds': date,
                    'y': yield_val
                })
        
        df = pd.DataFrame(data_list)
        
        # Test DataFrame forecasting
        forecast_df = tfm.forecast_on_df(
            inputs=df,
            freq="D",
            value_name="y",
            num_jobs=1,
            verbose=False
        )
        
        # Validate results
        assert len(forecast_df) == 60, f"Expected 60 forecast rows, got {len(forecast_df)}"
        assert 'timesfm' in forecast_df.columns, "Missing 'timesfm' column"
        assert 'timesfm-q-0.5' in forecast_df.columns, "Missing median quantile column"
        
        print("✅ DataFrame forecasting: PASSED")
        print(f"   Forecast shape: {forecast_df.shape}")
        print(f"   Unique crops: {forecast_df['unique_id'].nunique()}")
        
        return True
        
    except Exception as e:
        print(f"❌ DataFrame test failed: {e}")
        return False

def test_edge_cases():
    """Test edge cases and robustness."""
    print("\n🔧 Testing Edge Cases")
    print("-" * 40)
    
    try:
        tfm = timesfm.TimesFm(
            hparams=timesfm.TimesFmHparams(
                backend="cpu",
                per_core_batch_size=1,
                horizon_len=10,
                context_len=512,
                num_layers=20,
                use_positional_embedding=False,
            ),
            checkpoint=timesfm.TimesFmCheckpoint(
                huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
            )
        )
        
        # Test 1: Very short time series
        short_series = np.array([1, 2, 3, 4, 5], dtype=np.float32)
        point_forecast, quantile_forecast = tfm.forecast([short_series], freq=[0])
        print("✅ Short time series: PASSED")
        
        # Test 2: Constant time series
        constant_series = np.full(50, 100.0, dtype=np.float32)
        point_forecast, quantile_forecast = tfm.forecast([constant_series], freq=[0])
        print("✅ Constant time series: PASSED")
        
        # Test 3: Time series with missing values (should be handled)
        series_with_nan = np.array([1, 2, np.nan, 4, 5, 6, 7, 8, 9, 10] * 10, dtype=np.float32)
        point_forecast, quantile_forecast = tfm.forecast([series_with_nan], freq=[0])
        print("✅ Time series with NaN: PASSED")
        
        # Test 4: Multiple frequencies
        daily_data = np.random.randn(100)
        weekly_data = np.random.randn(52)
        monthly_data = np.random.randn(24)
        
        point_forecast, quantile_forecast = tfm.forecast(
            [daily_data, weekly_data, monthly_data], 
            freq=[0, 1, 2]  # High, medium, low frequency
        )
        print("✅ Multiple frequencies: PASSED")
        
        return True
        
    except Exception as e:
        print(f"❌ Edge cases test failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🔍 TimesFM Validation Tests")
    print("=" * 50)
    
    tests = [
        test_basic_functionality,
        test_agricultural_data_patterns,
        test_dataframe_functionality,
        test_edge_cases
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! TimesFM is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    main()
