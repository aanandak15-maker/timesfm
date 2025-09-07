# TimesFM Quick Start Guide

## ✅ Installation Complete!

TimesFM has been successfully installed and tested on your system. Here's what was set up:

### Environment Setup
- **Python 3.11.10** (via pyenv)
- **TimesFM 1.3.0** with PyTorch backend
- **All dependencies** installed and working

### Test Results
- ✅ Basic forecasting functionality
- ✅ Array input forecasting  
- ✅ DataFrame input forecasting
- ✅ Quantile forecasting for uncertainty
- ✅ CPU-based inference

## 🚀 Quick Usage Examples

### 1. Basic Forecasting
```python
import numpy as np
import timesfm

# Create sample data
data = np.sin(np.linspace(0, 4*np.pi, 100)) + 0.1 * np.random.randn(100)

# Initialize model
tfm = timesfm.TimesFm(
    hparams=timesfm.TimesFmHparams(
        backend="cpu",
        per_core_batch_size=1,
        horizon_len=32,
        context_len=512,
    ),
    checkpoint=timesfm.TimesFmCheckpoint(
        huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
    )
)

# Make forecast
forecast_input = [data]
frequency_input = [0]  # High frequency

point_forecast, quantile_forecast = tfm.forecast(
    forecast_input,
    freq=frequency_input,
)

print(f"Forecast shape: {point_forecast.shape}")
```

### 2. DataFrame Forecasting
```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'unique_id': 'series_1',
    'ds': pd.date_range('2020-01-01', periods=100, freq='D'),
    'y': your_time_series_data
})

# Forecast
forecast_df = tfm.forecast_on_df(
    inputs=df,
    freq="D",  # Daily frequency
    value_name="y"
)
```

## 📁 Available Examples

- `test_timesfm.py` - Basic installation test
- `simple_example.py` - Comprehensive functionality demo
- `timesfm_example.py` - Advanced examples (requires matplotlib)

## 🔧 Model Options

### Available Models
- **timesfm-1.0-200m-pytorch** (default, 200M parameters)
- **timesfm-2.0-500m-pytorch** (better performance, 500M parameters)

### Frequency Types
- **0**: High frequency (daily, hourly, etc.)
- **1**: Medium frequency (weekly, monthly)
- **2**: Low frequency (quarterly, yearly)

## 🎯 Next Steps

1. **Try the 2.0 model** for better performance:
   ```python
   checkpoint=timesfm.TimesFmCheckpoint(
       huggingface_repo_id="google/timesfm-2.0-500m-pytorch"
   )
   ```

2. **Explore fine-tuning** on your own data (see `notebooks/finetuning.ipynb`)

3. **Use covariates** for external features (see `notebooks/covariates.ipynb`)

4. **Check benchmarks** in the `experiments/` directory

## 📚 Resources

- [Official README](README.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Jupyter Notebooks](notebooks/)
- [Google Research Blog](https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/)

## 🆘 Need Help?

If you encounter any issues:
1. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file
2. Review the example scripts in this directory
3. Check the official documentation

---

**TimesFM is now ready to use for your time series forecasting needs!** 🎉
