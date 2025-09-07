#!/usr/bin/env python3
"""
TimesFM Web Frontend - Easy Testing Interface
A Streamlit web application for testing TimesFM forecasting capabilities.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import timesfm
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(
    page_title="TimesFM Forecasting Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_timesfm_model():
    """Load TimesFM model with caching."""
    try:
        tfm = timesfm.TimesFm(
            hparams=timesfm.TimesFmHparams(
                backend="cpu",
                per_core_batch_size=1,
                horizon_len=50,
                context_len=512,
                num_layers=20,
                use_positional_embedding=False,
            ),
            checkpoint=timesfm.TimesFmCheckpoint(
                huggingface_repo_id="google/timesfm-1.0-200m-pytorch"
            )
        )
        return tfm, None
    except Exception as e:
        return None, str(e)

def create_sample_data(data_type, n_points=100):
    """Create sample data for different agricultural scenarios."""
    np.random.seed(42)
    
    if data_type == "Crop Yield":
        # Crop yield with seasonal pattern
        trend = np.linspace(3.0, 3.5, n_points)
        seasonal = 0.5 * np.sin(2 * np.pi * np.arange(n_points) / 365.25)
        noise = 0.1 * np.random.randn(n_points)
        data = trend + seasonal + noise
        data = np.maximum(data, 1.0)  # Ensure positive yields
        
    elif data_type == "Soil Moisture":
        # Soil moisture with irrigation pattern
        base = 40
        seasonal = 15 * np.sin(2 * np.pi * np.arange(n_points) / 365.25 + np.pi/2)
        weekly = 5 * np.sin(2 * np.pi * np.arange(n_points) / 7)
        noise = 3 * np.random.randn(n_points)
        data = base + seasonal + weekly + noise
        data = np.clip(data, 10, 80)  # Keep within realistic bounds
        
    elif data_type == "Milk Production":
        # Milk production with seasonal pattern
        base = 500
        seasonal = 50 * np.sin(2 * np.pi * np.arange(n_points) / 365.25 - np.pi/2)
        feed_effect = 20 * np.sin(2 * np.pi * np.arange(n_points) / 30)
        noise = 15 * np.random.randn(n_points)
        data = base + seasonal + feed_effect + noise
        data = np.maximum(data, 300)  # Ensure minimum production
        
    elif data_type == "Commodity Price":
        # Commodity price with volatility
        price_changes = np.random.randn(n_points) * 0.02
        data = 200 * np.exp(np.cumsum(price_changes))
        
    elif data_type == "Temperature":
        # Temperature with seasonal pattern
        base = 15
        seasonal = 10 * np.sin(2 * np.pi * np.arange(n_points) / 365.25 - np.pi/2)
        trend = np.linspace(0, 1, n_points)  # Climate change
        noise = 3 * np.random.randn(n_points)
        data = base + seasonal + trend + noise
        
    else:  # Custom
        # Random walk
        data = np.cumsum(np.random.randn(n_points) * 0.1) + 100
    
    return data

def plot_forecast(historical_data, forecast_data, quantile_data, title, unit=""):
    """Create interactive forecast plot."""
    n_hist = len(historical_data)
    n_forecast = len(forecast_data)
    
    # Create date range
    dates_hist = pd.date_range(start='2023-01-01', periods=n_hist, freq='D')
    dates_forecast = pd.date_range(start=dates_hist[-1] + timedelta(days=1), periods=n_forecast, freq='D')
    
    # Create plot
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=dates_hist,
        y=historical_data,
        mode='lines',
        name='Historical Data',
        line=dict(color='#2E8B57', width=2)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=dates_forecast,
        y=forecast_data,
        mode='lines',
        name='Forecast',
        line=dict(color='#FF6B6B', width=2, dash='dash')
    ))
    
    # Uncertainty bands
    if quantile_data is not None:
        q10 = quantile_data[:, 0]  # 10th percentile
        q90 = quantile_data[:, 8]  # 90th percentile
        
        fig.add_trace(go.Scatter(
            x=dates_forecast,
            y=q90,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates_forecast,
            y=q10,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(255, 107, 107, 0.2)',
            name='80% Confidence Interval',
            hoverinfo='skip'
        ))
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=f'Value {unit}',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🌾 TimesFM Forecasting Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Time Series Forecasting for Agriculture")
    
    # Sidebar
    st.sidebar.header("🔧 Configuration")
    
    # Model loading
    with st.spinner("Loading TimesFM model..."):
        model, error = load_timesfm_model()
    
    if error:
        st.error(f"Failed to load model: {error}")
        st.stop()
    
    st.success("✅ TimesFM model loaded successfully!")
    
    # Sidebar controls
    st.sidebar.subheader("📊 Data Configuration")
    
    data_type = st.sidebar.selectbox(
        "Select Data Type",
        ["Crop Yield", "Soil Moisture", "Milk Production", "Commodity Price", "Temperature", "Custom"]
    )
    
    n_points = st.sidebar.slider("Number of Historical Points", 50, 500, 100)
    forecast_horizon = st.sidebar.slider("Forecast Horizon (days)", 7, 90, 30)
    frequency = st.sidebar.selectbox("Data Frequency", ["Daily (0)", "Weekly (1)", "Monthly (2)"])
    freq_value = int(frequency.split("(")[1].split(")")[0])
    
    # File upload
    st.sidebar.subheader("📁 Upload Your Data")
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=['csv'],
        help="Upload a CSV file with your time series data. Should have columns: 'date' and 'value'"
    )
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Time Series Data")
        
        # Generate or load data
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'date' in df.columns and 'value' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                    data = df['value'].values[-n_points:]  # Use last n_points
                    st.success("✅ Data loaded successfully!")
                else:
                    st.error("❌ CSV must have 'date' and 'value' columns")
                    data = create_sample_data(data_type, n_points)
            except Exception as e:
                st.error(f"❌ Error loading file: {e}")
                data = create_sample_data(data_type, n_points)
        else:
            data = create_sample_data(data_type, n_points)
        
        # Display data info
        st.write(f"**Data Type:** {data_type}")
        st.write(f"**Data Points:** {len(data)}")
        st.write(f"**Mean:** {np.mean(data):.2f}")
        st.write(f"**Std:** {np.std(data):.2f}")
        st.write(f"**Range:** {np.min(data):.2f} - {np.max(data):.2f}")
        
        # Show data table
        if st.checkbox("Show Data Table"):
            df_display = pd.DataFrame({
                'Date': pd.date_range(start='2023-01-01', periods=len(data), freq='D'),
                'Value': data
            })
            st.dataframe(df_display, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Forecast Settings")
        
        # Model parameters
        st.write("**Model:** TimesFM 1.0-200m")
        st.write("**Backend:** CPU")
        st.write(f"**Context Length:** 512")
        st.write(f"**Forecast Horizon:** {forecast_horizon} days")
        st.write(f"**Frequency:** {frequency}")
        
        # Forecast button
        if st.button("🚀 Generate Forecast", type="primary"):
            with st.spinner("Generating forecast..."):
                try:
                    # Prepare data
                    context = data.astype(np.float32)
                    
                    # Make forecast
                    point_forecast, quantile_forecast = model.forecast(
                        [context],
                        freq=[freq_value]
                    )
                    
                    forecast = point_forecast[0][:forecast_horizon]
                    quantiles = quantile_forecast[0][:forecast_horizon]
                    
                    # Store in session state
                    st.session_state['forecast'] = forecast
                    st.session_state['quantiles'] = quantiles
                    st.session_state['historical'] = data
                    
                    st.success("✅ Forecast generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Forecast failed: {e}")
    
    # Display results
    if 'forecast' in st.session_state:
        st.subheader("📊 Forecast Results")
        
        forecast = st.session_state['forecast']
        quantiles = st.session_state['quantiles']
        historical = st.session_state['historical']
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Forecast Mean", f"{np.mean(forecast):.2f}")
        
        with col2:
            st.metric("Forecast Std", f"{np.std(forecast):.2f}")
        
        with col3:
            trend = np.polyfit(range(len(forecast)), forecast, 1)[0]
            st.metric("Trend", f"{trend:+.3f}/day")
        
        with col4:
            uncertainty = np.mean(quantiles[:, 8] - quantiles[:, 0])
            st.metric("Uncertainty", f"{uncertainty:.2f}")
        
        # Plot
        unit_map = {
            "Crop Yield": "(tons/hectare)",
            "Soil Moisture": "(%)",
            "Milk Production": "(liters/day)",
            "Commodity Price": "($/ton)",
            "Temperature": "(°C)",
            "Custom": ""
        }
        
        unit = unit_map.get(data_type, "")
        fig = plot_forecast(historical, forecast, quantiles, f"{data_type} Forecast", unit)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed results
        st.subheader("📋 Detailed Forecast")
        
        # Create forecast dataframe
        forecast_dates = pd.date_range(
            start=pd.Timestamp('2023-01-01') + timedelta(days=len(historical)),
            periods=len(forecast),
            freq='D'
        )
        
        forecast_df = pd.DataFrame({
            'Date': forecast_dates,
            'Forecast': forecast,
            'Lower_80%': quantiles[:, 0],
            'Upper_80%': quantiles[:, 8],
            'Lower_50%': quantiles[:, 2],
            'Upper_50%': quantiles[:, 6]
        })
        
        st.dataframe(forecast_df, use_container_width=True)
        
        # Download button
        csv = forecast_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Forecast CSV",
            data=csv,
            file_name=f"{data_type.lower().replace(' ', '_')}_forecast.csv",
            mime="text/csv"
        )
        
        # Agricultural insights
        if data_type in ["Crop Yield", "Soil Moisture", "Milk Production", "Commodity Price"]:
            st.subheader("🌾 Agricultural Insights")
            
            if data_type == "Crop Yield":
                avg_yield = np.mean(forecast)
                if avg_yield > 3.5:
                    st.success("🌱 **Excellent yield forecast!** Consider optimizing storage and logistics.")
                elif avg_yield > 3.0:
                    st.info("🌾 **Good yield forecast.** Monitor weather conditions closely.")
                else:
                    st.warning("⚠️ **Lower yield forecast.** Consider additional inputs or irrigation.")
            
            elif data_type == "Soil Moisture":
                avg_moisture = np.mean(forecast)
                if avg_moisture < 30:
                    st.warning("🚨 **Irrigation needed!** Soil moisture below 30% threshold.")
                elif avg_moisture < 40:
                    st.info("💧 **Monitor closely.** Soil moisture approaching irrigation threshold.")
                else:
                    st.success("✅ **Adequate moisture.** No immediate irrigation needed.")
            
            elif data_type == "Milk Production":
                avg_production = np.mean(forecast)
                total_production = np.sum(forecast)
                st.info(f"🐄 **Production forecast:** {avg_production:.0f} liters/day average")
                st.info(f"📊 **Total forecast:** {total_production:.0f} liters over {len(forecast)} days")
            
            elif data_type == "Commodity Price":
                current_price = historical[-1]
                forecast_price = np.mean(forecast)
                price_change = ((forecast_price - current_price) / current_price) * 100
                
                if price_change > 5:
                    st.success(f"📈 **Bullish trend:** +{price_change:.1f}% expected. Consider holding or buying.")
                elif price_change < -5:
                    st.warning(f"📉 **Bearish trend:** {price_change:.1f}% expected. Consider selling or hedging.")
                else:
                    st.info(f"➡️ **Neutral trend:** {price_change:+.1f}% expected. Monitor market conditions.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🌾 TimesFM Forecasting Dashboard | Powered by Google Research</p>
        <p>Built with Streamlit and TimesFM for Agricultural Time Series Forecasting</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
