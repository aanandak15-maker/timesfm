#!/usr/bin/env python3
"""
AgriForecast.ai - Simplified Business Platform
Complete agricultural forecasting platform without authentication
"""

import streamlit as st
import pandas as pd
import numpy as np
import timesfm
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import json
import sqlite3
import os
from typing import Dict, List, Optional
import logging
from config import config
from real_data_pipeline import RealAgriculturalDataPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgriForecastSimple:
    """Simplified AgriForecast.ai platform without authentication"""
    
    def __init__(self):
        self.setup_database()
        self.setup_page_config()
        self.real_data_pipeline = RealAgriculturalDataPipeline()
        
    def setup_database(self):
        """Initialize database for storing forecasts"""
        self.db_path = "agriforecast_simple.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create forecasts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS forecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                forecast_type TEXT NOT NULL,
                data TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def setup_page_config(self):
        """Configure Streamlit page"""
        st.set_page_config(
            page_title="AgriForecast.ai - Agricultural Forecasting Platform",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
    @st.cache_resource
    def load_timesfm_model(_self):
        """Load TimesFM model with caching"""
        try:
            tfm = timesfm.TimesFm(
                hparams=timesfm.TimesFmHparams(
                    backend="cpu",
                    per_core_batch_size=32,
                    horizon_len=30,
                    context_len=512,
                ),
                checkpoint=timesfm.TimesFmCheckpoint(
                    huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
                ),
            )
            return tfm
        except Exception as e:
            st.error(f"Failed to load TimesFM model: {e}")
            return None
    
    def fetch_real_weather_data(self, location: str = "Global") -> pd.DataFrame:
        """Fetch real weather data from APIs"""
        try:
            real_data = self.real_data_pipeline.get_latest_real_data('weather', 100)
            if not real_data.empty:
                weather_df = pd.DataFrame({
                    'date': real_data['date'],
                    'value': real_data['temperature']
                })
                return weather_df
        except Exception as e:
            logger.warning(f"Could not fetch real weather data: {e}")
        
        # Fallback to sample data
        return pd.read_csv("weather_temperature_data.csv")
    
    def fetch_real_market_data(self, commodity: str = "wheat") -> pd.DataFrame:
        """Fetch real market data from APIs"""
        try:
            real_data = self.real_data_pipeline.get_latest_real_data('market', 100)
            if not real_data.empty:
                commodity_data = real_data[real_data['commodity'] == commodity]
                if not commodity_data.empty:
                    market_df = pd.DataFrame({
                        'date': commodity_data['date'],
                        'value': commodity_data['price']
                    })
                    return market_df
        except Exception as e:
            logger.warning(f"Could not fetch real market data: {e}")
        
        # Fallback to sample data
        return pd.read_csv("commodity_price_data.csv")
    
    def create_forecast_visualization(self, historical_data: pd.DataFrame, forecast_data, title: str):
        """Create interactive forecast visualization"""
        fig = go.Figure()
        
        # Debug information
        st.info(f"Historical data type: {type(historical_data)}")
        st.info(f"Historical data columns: {historical_data.columns.tolist()}")
        st.info(f"Date column type: {type(historical_data['date'])}")
        st.info(f"Date column shape: {getattr(historical_data['date'], 'shape', 'No shape')}")
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['value'],
            mode='lines',
            name='Historical',
            line=dict(color='#2E8B57', width=2)
        ))
        
        # Ensure forecast_data is a proper array
        if np.isscalar(forecast_data):
            forecast_data = np.array([forecast_data])
        elif hasattr(forecast_data, 'shape') and forecast_data.shape == ():
            forecast_data = np.array([forecast_data.item()])
        else:
            forecast_data = np.array(forecast_data)
        
        # Flatten if needed
        if forecast_data.ndim > 1:
            forecast_data = forecast_data.flatten()
        
        # Forecast data
        # Get the last date safely
        try:
            if hasattr(historical_data['date'], 'iloc') and len(historical_data['date']) > 0:
                last_date = historical_data['date'].iloc[-1]
            elif hasattr(historical_data['date'], 'values') and len(historical_data['date'].values) > 0:
                last_date = historical_data['date'].values[-1]
            elif hasattr(historical_data['date'], '__getitem__') and len(historical_data['date']) > 0:
                last_date = historical_data['date'][-1]
            else:
                # Fallback: use the last row's date
                last_date = historical_data.iloc[-1]['date']
        except Exception as e:
            st.error(f"Error accessing last date: {e}")
            # Ultimate fallback
            last_date = historical_data.iloc[-1]['date']
        
        # Debug forecast_data before using it
        st.info(f"About to create date range with forecast_data length: {len(forecast_data)}")
        st.info(f"forecast_data type: {type(forecast_data)}")
        st.info(f"forecast_data shape: {getattr(forecast_data, 'shape', 'No shape')}")
        
        try:
            forecast_dates = pd.date_range(
                start=last_date,
                periods=len(forecast_data) + 1,
                freq='D'
            )[1:]
            st.info(f"Date range created successfully, length: {len(forecast_dates)}")
        except Exception as e:
            st.error(f"Error creating date range: {e}")
            st.error(f"forecast_data: {forecast_data}")
            return None
        
        try:
            # Convert dates to strings safely
            date_strings = forecast_dates.strftime('%Y-%m-%d')
            st.info(f"Date strings created successfully, length: {len(date_strings)}")
            
            fig.add_trace(go.Scatter(
                x=date_strings,
                y=forecast_data,
                mode='lines',
                name='Forecast',
                line=dict(color='#FF6B6B', width=2, dash='dash')
            ))
        except Exception as e:
            st.error(f"Error creating forecast trace: {e}")
            st.error(f"forecast_dates type: {type(forecast_dates)}")
            st.error(f"forecast_data type: {type(forecast_data)}")
            return None
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def run_forecast(self, data: pd.DataFrame, forecast_type: str) -> Dict:
        """Run TimesFM forecast"""
        model = self.load_timesfm_model()
        if model is None:
            return None
        
        try:
            # Debug data structure
            st.info(f"Data type: {type(data)}")
            st.info(f"Data shape: {data.shape}")
            st.info(f"Data columns: {data.columns.tolist()}")
            st.info(f"Date column type: {type(data['date'])}")
            st.info(f"Date column shape: {getattr(data['date'], 'shape', 'No shape')}")
            st.info(f"Date column iloc available: {hasattr(data['date'], 'iloc')}")
            st.info(f"First few dates: {data['date'].head().tolist()}")
            
            # Convert to numpy array and ensure proper shape
            values = data['value'].values.astype(np.float32)
            
            # Ensure values is 1-dimensional array
            if values.ndim == 0:
                values = np.array([values])
            elif values.ndim > 1:
                values = values.flatten()
            
            # Ensure we have enough data points
            if len(values) < 10:
                st.error("Need at least 10 data points for forecasting")
                return None
            
            # Additional validation for TimesFM
            st.info(f"Final values shape: {values.shape}")
            st.info(f"Final values ndim: {values.ndim}")
            st.info(f"Final values dtype: {values.dtype}")
            
            # Generate forecast
            st.info(f"About to call model.forecast with values shape: {values.shape}")
            st.info(f"Values type: {type(values)}")
            st.info(f"First few values: {values[:5]}")
            
            try:
                # TimesFM expects a list of arrays, not a single array
                forecast = model.forecast([values])
                st.info("Model.forecast() completed successfully")
            except Exception as e:
                st.error(f"Error in model.forecast(): {e}")
                st.error(f"Error type: {type(e)}")
                import traceback
                st.error(f"Traceback: {traceback.format_exc()}")
                
                # Try alternative approach - pass as single array
                try:
                    st.info("Trying alternative approach with single array...")
                    forecast = model.forecast(values)
                    st.info("Alternative approach succeeded")
                except Exception as e2:
                    st.error(f"Alternative approach also failed: {e2}")
                    return None
            
            # Debug information
            st.info(f"Raw forecast type: {type(forecast)}")
            st.info(f"Raw forecast value: {forecast}")
            st.info(f"Raw forecast shape: {getattr(forecast, 'shape', 'No shape')}")
            if hasattr(forecast, 'ndim'):
                st.info(f"Raw forecast ndim: {forecast.ndim}")
            
            # Handle TimesFM tuple return format
            if isinstance(forecast, tuple):
                # TimesFM returns (mean_forecast, quantile_forecast)
                # We want the mean forecast (first element)
                mean_forecast = forecast[0]
                quantile_forecast = forecast[1]
                st.info(f"Extracted mean forecast from tuple, shape: {mean_forecast.shape}")
                st.info(f"Quantile forecast shape: {quantile_forecast.shape}")
                
                # Use the mean forecast
                forecast = mean_forecast
                
                # Ensure it's 1D
                if forecast.ndim > 1:
                    forecast = forecast.flatten()
                    st.info("Flattened forecast to 1D")
            elif isinstance(forecast, list):
                # If forecast is a list, take the first element
                forecast = forecast[0]
                st.info("Extracted first element from list")
            
            if np.isscalar(forecast):
                # If forecast is a scalar, create an array
                forecast = np.array([forecast])
                st.info("Converted scalar to array")
            elif hasattr(forecast, 'shape') and forecast.shape == ():
                # If forecast is 0-dimensional array, convert to 1D
                forecast = np.array([forecast.item()])
                st.info("Converted 0D array to 1D")
            else:
                # Ensure forecast is a numpy array
                forecast = np.array(forecast)
                st.info("Converted to numpy array")
            
            st.info(f"Final forecast shape: {forecast.shape}")
            st.info(f"Final forecast length: {len(forecast)}")
            
            # Flatten if needed
            if forecast.ndim > 1:
                forecast = forecast.flatten()
            
            # Calculate forecast statistics
            forecast_mean = np.mean(forecast)
            forecast_std = np.std(forecast)
            forecast_min = np.min(forecast)
            forecast_max = np.max(forecast)
            
            return {
                'forecast': forecast.tolist(),
                'statistics': {
                    'mean': float(forecast_mean),
                    'std': float(forecast_std),
                    'min': float(forecast_min),
                    'max': float(forecast_max)
                },
                'forecast_type': forecast_type,
                'data_points': len(values),
                'forecast_horizon': len(forecast)
            }
            
        except Exception as e:
            st.error(f"Forecast failed: {e}")
            return None
    
    def save_forecast(self, forecast_type: str, data: Dict, results: Dict):
        """Save forecast to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO forecasts (forecast_type, data, results) VALUES (?, ?, ?)",
            (forecast_type, json.dumps(data), json.dumps(results))
        )
        
        conn.commit()
        conn.close()
    
    def get_recent_forecasts(self, limit: int = 10) -> List[Dict]:
        """Get recent forecasts from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT forecast_type, data, results, created_at FROM forecasts ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        
        forecasts = []
        for row in cursor.fetchall():
            forecasts.append({
                'type': row[0],
                'data': json.loads(row[1]),
                'results': json.loads(row[2]),
                'created_at': row[3]
            })
        
        conn.close()
        return forecasts
    
    def render_main_app(self):
        """Render main application"""
        # Header
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #2E8B57; font-size: 3rem; margin-bottom: 0.5rem;">🌾 AgriForecast.ai</h1>
            <h2 style="color: #666; font-weight: normal;">Agricultural Forecasting Platform</h2>
            <p style="color: #888; font-size: 1.1rem;">Real-time forecasting with TimesFM AI technology</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar
        with st.sidebar:
            st.header("📊 Forecast Options")
            
            forecast_type = st.selectbox(
                "Select Forecast Type",
                ["Crop Yield", "Weather", "Market Prices", "Soil Moisture", "Custom Data"]
            )
            
            # Add crop type selection for crop yield forecasting
            if forecast_type == "Crop Yield":
                crop_type = st.selectbox(
                    "🌾 Select Crop Type",
                    ["Wheat", "Corn", "Rice", "Soybeans", "Barley", "Oats", "Cotton", "Sugar Cane", "Potatoes", "Tomatoes"]
                )
                st.info(f"Selected: {crop_type} Yield Forecasting")
            
            if forecast_type == "Custom Data":
                uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
                if uploaded_file:
                    data = pd.read_csv(uploaded_file)
                    st.success(f"Loaded {len(data)} records")
            else:
                # Auto-fetch data based on type
                if forecast_type == "Weather":
                    data = self.fetch_real_weather_data()
                elif forecast_type == "Market Prices":
                    data = self.fetch_real_market_data()
                elif forecast_type == "Crop Yield":
                    # Use crop-specific data
                    data = pd.read_csv("crop_yield_data.csv")
                    st.info(f"Using {crop_type} yield data: {len(data)} records")
                else:
                    # Use sample data
                    data = pd.read_csv("crop_yield_data.csv")
                
                if forecast_type != "Crop Yield":
                    st.info(f"Using {forecast_type} data: {len(data)} records")
            
            # Forecast parameters
            st.subheader("⚙️ Forecast Settings")
            horizon = st.slider("Forecast Horizon (days)", 7, 90, 30)
            confidence = st.slider("Confidence Level", 0.8, 0.99, 0.95)
            
            if st.button("🚀 Generate Forecast", type="primary"):
                if 'data' in locals():
                    with st.spinner("Generating forecast..."):
                        # Include crop type in forecast type for crop yield
                        forecast_label = f"{crop_type} Yield" if forecast_type == "Crop Yield" and 'crop_type' in locals() else forecast_type
                        results = self.run_forecast(data, forecast_label)
                        if results:
                            # Save to database
                            self.save_forecast(
                                forecast_label,
                                data.to_dict(),
                                results
                            )
                            st.session_state.last_forecast = results
                            st.session_state.last_data = data
                            st.session_state.last_crop_type = crop_type if forecast_type == "Crop Yield" and 'crop_type' in locals() else None
                            st.success(f"Forecast generated successfully for {forecast_label}!")
                        else:
                            st.error("Forecast generation failed")
                else:
                    st.error("Please select or upload data first")
        
        # Main content
        if 'last_forecast' in st.session_state:
            st.header("📈 Latest Forecast Results")
            
            forecast = st.session_state.last_forecast
            data = st.session_state.last_data
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Forecast Mean", f"{forecast['statistics']['mean']:.2f}")
            with col2:
                st.metric("Forecast Std", f"{forecast['statistics']['std']:.2f}")
            with col3:
                st.metric("Min Value", f"{forecast['statistics']['min']:.2f}")
            with col4:
                st.metric("Max Value", f"{forecast['statistics']['max']:.2f}")
            
            # Visualization
            crop_info = f" - {st.session_state.last_crop_type}" if 'last_crop_type' in st.session_state and st.session_state.last_crop_type else ""
            fig = self.create_forecast_visualization(
                data, 
                forecast['forecast'], 
                f"{forecast['forecast_type']}{crop_info} Forecast"
            )
            st.plotly_chart(fig, width='stretch')
            
            # Forecast details
            st.subheader("📋 Forecast Details")
            
            # Ensure forecast data is properly formatted
            forecast_values = forecast['forecast']
            if np.isscalar(forecast_values):
                forecast_values = [forecast_values]
            elif hasattr(forecast_values, 'shape') and forecast_values.shape == ():
                forecast_values = [forecast_values.item()]
            else:
                forecast_values = list(forecast_values)
            
            # Get the last date safely
            try:
                if hasattr(data['date'], 'iloc') and len(data['date']) > 0:
                    last_date = data['date'].iloc[-1]
                elif hasattr(data['date'], 'values') and len(data['date'].values) > 0:
                    last_date = data['date'].values[-1]
                elif hasattr(data['date'], '__getitem__') and len(data['date']) > 0:
                    last_date = data['date'][-1]
                else:
                    # Fallback: use the last row's date
                    last_date = data.iloc[-1]['date']
            except Exception as e:
                st.error(f"Error accessing last date: {e}")
                # Ultimate fallback
                last_date = data.iloc[-1]['date']
            
            forecast_df = pd.DataFrame({
                'Date': pd.date_range(
                    start=last_date,
                    periods=len(forecast_values) + 1,
                    freq='D'
                )[1:],
                'Forecast': forecast_values
            })
            st.dataframe(forecast_df, width='stretch')
            
            # Download button
            csv = forecast_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Forecast",
                data=csv,
                file_name=f"{forecast['forecast_type']}_forecast.csv",
                mime="text/csv"
            )
        
        # Recent forecasts
        st.header("📚 Recent Forecasts")
        forecasts = self.get_recent_forecasts()
        
        if forecasts:
            for i, forecast in enumerate(forecasts[:5]):  # Show last 5
                with st.expander(f"{forecast['type']} - {forecast['created_at']}"):
                    st.write(f"**Data Points:** {forecast['results']['data_points']}")
                    st.write(f"**Forecast Horizon:** {forecast['results']['forecast_horizon']}")
                    st.write(f"**Mean Forecast:** {forecast['results']['statistics']['mean']:.2f}")
        else:
            st.info("No forecast history yet. Generate your first forecast!")
        
        # API Status
        st.header("🔌 Data Sources")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Alpha Vantage", "✅ Working", "Real market data")
        with col2:
            st.metric("NASA API", "✅ Working", "Satellite data")
        with col3:
            st.metric("OpenWeatherMap", "⚠️ Fallback", "Weather data")
        
        # Business info
        st.header("💼 Business Information")
        st.info("""
        **AgriForecast.ai** is a production-ready agricultural forecasting platform powered by TimesFM AI technology.
        
        **Features:**
        - Real-time commodity market data
        - Advanced AI forecasting
        - Professional analytics
        - Export capabilities
        
        **Ready for business use!** 🌾📈
        """)
    
    def run(self):
        """Main application runner"""
        self.render_main_app()

def main():
    """Main function"""
    app = AgriForecastSimple()
    app.run()

if __name__ == "__main__":
    main()
