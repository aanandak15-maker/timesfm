# 🌾 Agricultural Datasets for TimesFM

## 📊 **Available Datasets**

I've created **5 ready-to-use agricultural datasets** that are perfectly formatted for TimesFM:

### **1. Crop Yield Data** (`crop_yield_data.csv`)
- **Records**: 730 days (2 years)
- **Data**: Daily crop yield in tons/hectare
- **Range**: 2.33 to 4.26 tons/hectare
- **Features**: Seasonal patterns, drought effects, growth trends
- **Perfect for**: Yield forecasting, harvest planning

### **2. Soil Moisture Data** (`soil_moisture_data.csv`)
- **Records**: 730 days (2 years)
- **Data**: Daily soil moisture percentage
- **Range**: 25.00% to 75.40%
- **Features**: Seasonal cycles, rainfall effects, irrigation patterns
- **Perfect for**: Irrigation scheduling, water management

### **3. Commodity Price Data** (`commodity_price_data.csv`)
- **Records**: 730 days (2 years)
- **Data**: Daily commodity prices in $/ton
- **Range**: $168.83 to $276.02
- **Features**: Market volatility, seasonal trends, supply shocks
- **Perfect for**: Price forecasting, market analysis

### **4. Weather Temperature Data** (`weather_temperature_data.csv`)
- **Records**: 730 days (2 years)
- **Data**: Daily temperature in Celsius
- **Range**: -12.70°C to 59.90°C
- **Features**: Seasonal patterns, heat waves, cold spells
- **Perfect for**: Climate forecasting, crop planning

### **5. Sample Data** (`sample_agricultural_data.csv`)
- **Records**: 100 days
- **Data**: Crop yield sample for quick testing
- **Perfect for**: Quick demos, testing the frontend

## 🚀 **How to Use These Datasets**

### **Method 1: Direct Upload to Frontend**
1. **Open the frontend**: http://localhost:8501
2. **Go to sidebar**: "📁 Upload Your Data" section
3. **Click "Browse files"**: Select any of the CSV files above
4. **Generate forecast**: Click "🚀 Generate Forecast"

### **Method 2: Using the Data Preparation Script**
If you have your own CSV data that needs formatting:

```bash
# Auto-detect columns
python prepare_csv_for_timesfm.py your_data.csv

# Specify columns manually
python prepare_csv_for_timesfm.py your_data.csv -d "Date" -v "Price" -o "formatted_data.csv"
```

## 📋 **Dataset Format Requirements**

All datasets are formatted exactly as TimesFM requires:

```csv
date,value
2022-01-01,2.55
2022-01-02,2.49
2022-01-03,2.57
```

**Requirements:**
- ✅ Column names: `date`, `value`
- ✅ Date format: `YYYY-MM-DD`
- ✅ Numeric values only
- ✅ No missing values
- ✅ Chronological order

## 🌾 **Agricultural Applications**

### **Crop Yield Forecasting**
- **Use**: `crop_yield_data.csv`
- **Applications**: 
  - Harvest planning
  - Resource allocation
  - Market supply predictions
  - Insurance risk assessment

### **Irrigation Management**
- **Use**: `soil_moisture_data.csv`
- **Applications**:
  - Automated irrigation systems
  - Water conservation
  - Crop health monitoring
  - Drought prediction

### **Market Analysis**
- **Use**: `commodity_price_data.csv`
- **Applications**:
  - Trading decisions
  - Supply chain planning
  - Risk management
  - Price optimization

### **Climate Planning**
- **Use**: `weather_temperature_data.csv`
- **Applications**:
  - Planting schedules
  - Crop selection
  - Pest management
  - Climate adaptation

## 🔧 **Data Preparation Tools**

### **Universal CSV Converter**
```bash
# Convert any CSV to TimesFM format
python prepare_csv_for_timesfm.py input.csv -o output.csv
```

**Features:**
- Auto-detects date and value columns
- Handles multiple date formats
- Removes missing values
- Sorts chronologically
- Validates data quality

### **Custom Data Generator**
```bash
# Create new agricultural datasets
python download_crop_data.py
```

**Creates:**
- Realistic seasonal patterns
- Weather effects
- Market volatility
- Agricultural trends

## 📊 **Data Quality Features**

### **Realistic Patterns**
- **Seasonal cycles**: Natural agricultural rhythms
- **Trends**: Long-term changes (climate, technology)
- **Volatility**: Real-world randomness
- **Events**: Droughts, heat waves, market shocks

### **Data Validation**
- **No missing values**: Complete time series
- **Positive values**: Realistic agricultural data
- **Chronological order**: Proper time sequence
- **Consistent frequency**: Daily intervals

## 🎯 **Quick Start Guide**

### **1. Test with Sample Data**
```bash
# Upload sample_agricultural_data.csv to frontend
# Quick 100-day test with crop yield data
```

### **2. Try Full Datasets**
```bash
# Upload crop_yield_data.csv (730 days)
# Test with 2 years of realistic data
```

### **3. Compare Different Types**
```bash
# Test all 4 main datasets:
# - crop_yield_data.csv
# - soil_moisture_data.csv  
# - commodity_price_data.csv
# - weather_temperature_data.csv
```

## 💡 **Pro Tips**

### **For Better Forecasts**
- **Use longer datasets**: 730 days vs 100 days
- **Check data quality**: No gaps or outliers
- **Understand patterns**: Seasonal vs trend vs random
- **Validate results**: Compare with known patterns

### **For Agricultural Use**
- **Crop yield**: Focus on growing seasons
- **Soil moisture**: Monitor irrigation needs
- **Commodity prices**: Watch market volatility
- **Weather**: Plan for extreme events

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Wrong column names** → Use the preparation script
2. **Date format errors** → Check YYYY-MM-DD format
3. **Missing values** → Remove or interpolate gaps
4. **Non-numeric values** → Convert to numbers

### **Data Validation**
```python
# Check your data before uploading
import pandas as pd

df = pd.read_csv('your_data.csv')
print("Columns:", df.columns.tolist())
print("Date range:", df['date'].min(), "to", df['date'].max())
print("Value range:", df['value'].min(), "to", df['value'].max())
print("Missing values:", df.isnull().sum().sum())
```

## 🎉 **Ready to Forecast!**

Your agricultural datasets are ready to use with TimesFM:

1. **Frontend**: http://localhost:8501
2. **Upload any CSV**: Point and click interface
3. **Generate forecasts**: Real-time predictions
4. **Download results**: Save for analysis

**Start with `sample_agricultural_data.csv` for a quick test!** 🌾📈

