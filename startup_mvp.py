#!/usr/bin/env python3
"""
AgriForecast.ai MVP - Production-Ready Agricultural Forecasting Platform
Built on TimesFM with automated data collection and user management
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
import hashlib
import os
from typing import Dict, List, Optional
import logging
from config import config
from real_data_pipeline import RealAgriculturalDataPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgriForecastMVP:
    """Main application class for AgriForecast.ai MVP"""
    
    def __init__(self):
        self.setup_database()
        self.setup_page_config()
        self.real_data_pipeline = RealAgriculturalDataPipeline()
        
    def setup_database(self):
        """Initialize SQLite database for user management"""
        self.db_path = "agriforecast.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                plan TEXT DEFAULT 'free',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create forecasts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS forecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                forecast_type TEXT NOT NULL,
                data TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
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
                    huggingface_repo_id="google/timesfm-2.0-500m-pytorch"
                ),
            )
            return tfm
        except Exception as e:
            st.error(f"Failed to load TimesFM model: {e}")
            return None
    
    def hash_password(self, password: str) -> str:
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, email: str, password: str) -> bool:
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id, plan FROM users WHERE email = ? AND password_hash = ?",
            (email, password_hash)
        )
        
        result = cursor.fetchone()
        if result:
            user_id, plan = result
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user_id,)
            )
            conn.commit()
            st.session_state.user_id = user_id
            st.session_state.user_plan = plan
            st.session_state.authenticated = True
            conn.close()
            return True
        
        conn.close()
        return False
    
    def register_user(self, email: str, password: str) -> bool:
        """Register new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def get_user_forecasts(self, user_id: int) -> List[Dict]:
        """Get user's forecast history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT forecast_type, data, results, created_at FROM forecasts WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
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
    
    def save_forecast(self, user_id: int, forecast_type: str, data: Dict, results: Dict):
        """Save forecast to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO forecasts (user_id, forecast_type, data, results) VALUES (?, ?, ?, ?)",
            (user_id, forecast_type, json.dumps(data), json.dumps(results))
        )
        
        conn.commit()
        conn.close()
    
    def fetch_weather_data(self, location: str = "Global") -> pd.DataFrame:
        """Fetch real-time weather data from APIs"""
        try:
            # Try to get real data first
            real_data = self.real_data_pipeline.get_latest_real_data('weather', 100)
            if not real_data.empty:
                # Convert to TimesFM format
                weather_df = pd.DataFrame({
                    'date': real_data['date'],
                    'value': real_data['temperature']
                })
                return weather_df
        except Exception as e:
            logger.warning(f"Could not fetch real weather data: {e}")
        
        # Fallback to sample data
        return pd.read_csv("weather_temperature_data.csv")
    
    def fetch_market_data(self, commodity: str = "wheat") -> pd.DataFrame:
        """Fetch real-time market data from APIs"""
        try:
            # Try to get real data first
            real_data = self.real_data_pipeline.get_latest_real_data('market', 100)
            if not real_data.empty:
                # Filter for specific commodity
                commodity_data = real_data[real_data['commodity'] == commodity]
                if not commodity_data.empty:
                    # Convert to TimesFM format
                    market_df = pd.DataFrame({
                        'date': commodity_data['date'],
                        'value': commodity_data['price']
                    })
                    return market_df
        except Exception as e:
            logger.warning(f"Could not fetch real market data: {e}")
        
        # Fallback to sample data
        return pd.read_csv("commodity_price_data.csv")
    
    def create_forecast_visualization(self, historical_data: pd.DataFrame, forecast_data: np.ndarray, title: str):
        """Create interactive forecast visualization"""
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['value'],
            mode='lines',
            name='Historical',
            line=dict(color='blue', width=2)
        ))
        
        # Forecast data
        forecast_dates = pd.date_range(
            start=historical_data['date'].iloc[-1],
            periods=len(forecast_data) + 1,
            freq='D'
        )[1:]
        
        fig.add_trace(go.Scatter(
            x=forecast_dates.strftime('%Y-%m-%d'),
            y=forecast_data,
            mode='lines',
            name='Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            height=500
        )
        
        return fig
    
    def run_forecast(self, data: pd.DataFrame, forecast_type: str) -> Dict:
        """Run TimesFM forecast"""
        model = self.load_timesfm_model()
        if model is None:
            return None
        
        try:
            # Convert to numpy array
            values = data['value'].values.astype(np.float32)
            
            # Generate forecast
            forecast = model.forecast(values)
            
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
    
    def render_login_page(self):
        """Render login/register page"""
        st.title("🌾 AgriForecast.ai")
        st.subheader("Agricultural Forecasting Platform")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login to Your Account")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", key="login_btn"):
                if self.authenticate_user(email, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
        
        with tab2:
            st.subheader("Create New Account")
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            if st.button("Register", key="register_btn"):
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif self.register_user(email, password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Email already exists")
    
    def render_main_app(self):
        """Render main application"""
        # Header
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.title("🌾 AgriForecast.ai")
        with col2:
            st.metric("Plan", st.session_state.user_plan.title())
        with col3:
            if st.button("Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        # Sidebar
        with st.sidebar:
            st.header("📊 Forecast Options")
            
            forecast_type = st.selectbox(
                "Select Forecast Type",
                ["Crop Yield", "Weather", "Market Prices", "Soil Moisture", "Custom Data"]
            )
            
            if forecast_type == "Custom Data":
                uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
                if uploaded_file:
                    data = pd.read_csv(uploaded_file)
                    st.success(f"Loaded {len(data)} records")
            else:
                # Auto-fetch data based on type
                if forecast_type == "Weather":
                    data = self.fetch_weather_data()
                elif forecast_type == "Market Prices":
                    data = self.fetch_market_data()
                else:
                    # Use sample data
                    data = pd.read_csv("crop_yield_data.csv")
                
                st.info(f"Using {forecast_type} data: {len(data)} records")
            
            # Forecast parameters
            st.subheader("⚙️ Forecast Settings")
            horizon = st.slider("Forecast Horizon (days)", 7, 90, 30)
            confidence = st.slider("Confidence Level", 0.8, 0.99, 0.95)
            
            if st.button("🚀 Generate Forecast", type="primary"):
                if 'data' in locals():
                    with st.spinner("Generating forecast..."):
                        results = self.run_forecast(data, forecast_type)
                        if results:
                            # Save to database
                            self.save_forecast(
                                st.session_state.user_id,
                                forecast_type,
                                data.to_dict(),
                                results
                            )
                            st.session_state.last_forecast = results
                            st.session_state.last_data = data
                            st.success("Forecast generated successfully!")
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
            fig = self.create_forecast_visualization(
                data, 
                np.array(forecast['forecast']), 
                f"{forecast['forecast_type']} Forecast"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast details
            st.subheader("📋 Forecast Details")
            forecast_df = pd.DataFrame({
                'Date': pd.date_range(
                    start=data['date'].iloc[-1],
                    periods=len(forecast['forecast']) + 1,
                    freq='D'
                )[1:],
                'Forecast': forecast['forecast']
            })
            st.dataframe(forecast_df, use_container_width=True)
            
            # Download button
            csv = forecast_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Forecast",
                data=csv,
                file_name=f"{forecast['forecast_type']}_forecast.csv",
                mime="text/csv"
            )
        
        # Forecast history
        st.header("📚 Forecast History")
        forecasts = self.get_user_forecasts(st.session_state.user_id)
        
        if forecasts:
            for i, forecast in enumerate(forecasts[:5]):  # Show last 5
                with st.expander(f"{forecast['type']} - {forecast['created_at']}"):
                    st.write(f"**Data Points:** {forecast['results']['data_points']}")
                    st.write(f"**Forecast Horizon:** {forecast['results']['forecast_horizon']}")
                    st.write(f"**Mean Forecast:** {forecast['results']['statistics']['mean']:.2f}")
        else:
            st.info("No forecast history yet. Generate your first forecast!")
    
    def run(self):
        """Main application runner"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        
        if st.session_state.authenticated:
            self.render_main_app()
        else:
            self.render_login_page()

def main():
    """Main function"""
    app = AgriForecastMVP()
    app.run()

if __name__ == "__main__":
    main()
