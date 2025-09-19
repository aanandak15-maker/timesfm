# 🌾 TimesFM Web Frontend

A beautiful, interactive web interface for testing TimesFM forecasting capabilities with agricultural data.

## 🚀 Quick Start

### Option 1: Run with Script
```bash
./run_frontend.sh
```

### Option 2: Run Directly
```bash
streamlit run timesfm_frontend.py
```

The web interface will open at: **http://localhost:8501**

## ✨ Features

### 🎯 **Interactive Dashboard**
- **Real-time forecasting** with TimesFM
- **Multiple data types** (Crop Yield, Soil Moisture, Milk Production, etc.)
- **Customizable parameters** (forecast horizon, frequency, data points)
- **Beautiful visualizations** with Plotly charts

### 📊 **Data Management**
- **Sample data generation** for different agricultural scenarios
- **CSV file upload** for your own time series data
- **Data preview** and statistics
- **Export forecast results** to CSV

### 🌾 **Agricultural Focus**
- **Pre-configured scenarios** for common agricultural use cases
- **Agricultural insights** and recommendations
- **Uncertainty quantification** for risk management
- **Trend analysis** for decision making

## 📋 How to Use

### 1. **Select Data Type**
Choose from predefined agricultural scenarios:
- **Crop Yield**: Wheat, corn, rice production forecasting
- **Soil Moisture**: Irrigation planning and water management
- **Milk Production**: Dairy farm production forecasting
- **Commodity Price**: Market price prediction for selling decisions
- **Temperature**: Weather forecasting for crop protection
- **Custom**: Upload your own data

### 2. **Configure Parameters**
- **Number of Historical Points**: 50-500 data points
- **Forecast Horizon**: 7-90 days ahead
- **Data Frequency**: Daily, Weekly, or Monthly
- **Upload CSV**: Use your own time series data

### 3. **Generate Forecast**
Click "🚀 Generate Forecast" to:
- Load TimesFM model
- Process your data
- Generate predictions with uncertainty
- Display interactive charts

### 4. **Analyze Results**
- **Interactive plots** with historical data and forecasts
- **Uncertainty bands** for risk assessment
- **Agricultural insights** and recommendations
- **Download results** as CSV

## 📁 File Upload Format

Upload CSV files with this format:
```csv
date,value
2023-01-01,3.2
2023-01-02,3.1
2023-01-03,3.3
...
```

**Required columns:**
- `date`: Date in YYYY-MM-DD format
- `value`: Numeric time series values

## 🎨 Interface Overview

### **Main Dashboard**
- **Header**: TimesFM branding and title
- **Sidebar**: Configuration controls and file upload
- **Main Area**: Data visualization and results
- **Footer**: Information and credits

### **Key Components**
1. **Data Configuration Panel**: Select data type and parameters
2. **File Upload Area**: Upload your own CSV data
3. **Forecast Results**: Interactive charts and metrics
4. **Agricultural Insights**: Domain-specific recommendations
5. **Download Section**: Export forecast results

## 🔧 Technical Details

### **Backend**
- **TimesFM Model**: Google's time series foundation model
- **Backend**: CPU-based inference (no GPU required)
- **Model**: timesfm-1.0-200m-pytorch (200M parameters)

### **Frontend**
- **Framework**: Streamlit web application
- **Visualization**: Plotly interactive charts
- **Styling**: Custom CSS for agricultural theme
- **Caching**: Model loading and data processing

### **Performance**
- **Model Loading**: ~2-3 seconds (cached after first load)
- **Forecast Generation**: <1 second for typical data
- **Memory Usage**: ~2GB RAM recommended
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari)

## 📊 Sample Data Types

### **Crop Yield Data**
- **Pattern**: Seasonal growth with trend
- **Range**: 1.0 - 4.8 tons/hectare
- **Use Case**: Harvest planning and storage

### **Soil Moisture Data**
- **Pattern**: Seasonal variation with irrigation cycles
- **Range**: 10% - 80% moisture
- **Use Case**: Smart irrigation scheduling

### **Milk Production Data**
- **Pattern**: Seasonal production with feed effects
- **Range**: 300 - 600 liters/day
- **Use Case**: Feed planning and production scheduling

### **Commodity Price Data**
- **Pattern**: Volatile price movements with trend
- **Range**: $150 - $250/ton
- **Use Case**: Market timing and selling decisions

## 🌾 Agricultural Applications

### **Crop Management**
- **Yield Forecasting**: Predict harvest quantities
- **Irrigation Planning**: Optimize water usage
- **Pest Management**: Forecast disease risks
- **Harvest Timing**: Optimize collection schedules

### **Livestock Management**
- **Production Forecasting**: Predict milk/meat output
- **Feed Planning**: Optimize feed requirements
- **Health Monitoring**: Predict production changes
- **Resource Allocation**: Plan equipment and labor

### **Market Analysis**
- **Price Forecasting**: Predict commodity prices
- **Selling Decisions**: Optimize market timing
- **Risk Management**: Hedge against price volatility
- **Profit Optimization**: Maximize revenue

## 🛠️ Troubleshooting

### **Common Issues**

1. **Model Loading Error**
   - Ensure TimesFM is properly installed
   - Check internet connection for model download
   - Restart the application

2. **File Upload Issues**
   - Verify CSV format (date, value columns)
   - Check date format (YYYY-MM-DD)
   - Ensure numeric values in 'value' column

3. **Forecast Errors**
   - Verify data has sufficient points (minimum 50)
   - Check for missing or invalid values
   - Try different frequency settings

4. **Performance Issues**
   - Reduce number of data points
   - Use shorter forecast horizon
   - Close other applications to free memory

### **Browser Compatibility**
- **Chrome**: Recommended (best performance)
- **Firefox**: Supported
- **Safari**: Supported
- **Edge**: Supported

## 📈 Best Practices

### **Data Preparation**
1. **Clean Data**: Remove outliers and missing values
2. **Consistent Frequency**: Use regular time intervals
3. **Sufficient History**: Provide 100+ data points for best results
4. **Relevant Context**: Include seasonal patterns and trends

### **Forecast Interpretation**
1. **Use Uncertainty**: Consider confidence intervals
2. **Monitor Trends**: Watch for trend changes
3. **Validate Results**: Compare with historical patterns
4. **Update Regularly**: Refresh forecasts with new data

### **Agricultural Decision Making**
1. **Risk Management**: Use uncertainty estimates
2. **Seasonal Planning**: Consider seasonal patterns
3. **Resource Optimization**: Plan based on forecasts
4. **Market Timing**: Use price forecasts for selling

## 🎯 Next Steps

1. **Try Different Data Types**: Experiment with various agricultural scenarios
2. **Upload Your Data**: Use your own time series data
3. **Adjust Parameters**: Test different forecast horizons and frequencies
4. **Export Results**: Download forecasts for further analysis
5. **Integrate Workflows**: Use forecasts in your agricultural planning

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the TimesFM documentation
3. Check the agricultural applications guide
4. Verify your data format and parameters

---

## 🎉 Ready to Forecast!

Your TimesFM web frontend is ready to use! Start with sample data to explore the interface, then upload your own agricultural time series for personalized forecasting.

**Happy Forecasting!** 🌾📈




