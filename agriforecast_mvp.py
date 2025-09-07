"""
AgriForecast MVP - Hyperlocalized Field-Level Yield Prediction
Real-time weather, soil, and satellite data integration
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import time
import logging

# Import our custom modules
from field_data_integration import FieldDataIntegration
from yield_prediction_model import YieldPredictionModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgriForecastMVP:
    """MVP for hyperlocalized field-level yield prediction"""
    
    def __init__(self):
        self.field_integration = FieldDataIntegration()
        self.yield_model = YieldPredictionModel()
        
        # Initialize session state
        if 'field_data' not in st.session_state:
            st.session_state.field_data = None
        if 'yield_predictions' not in st.session_state:
            st.session_state.yield_predictions = None
        if 'last_update' not in st.session_state:
            st.session_state.last_update = None
    
    def run(self):
        """Main application runner"""
        st.set_page_config(
            page_title="AgriForecast MVP",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Header
        st.title("🌾 AgriForecast MVP")
        st.subheader("Hyperlocalized Field-Level Yield Prediction")
        
        # Sidebar for field management
        self.render_sidebar()
        
        # Main content
        if st.session_state.field_data:
            self.render_field_dashboard()
        else:
            self.render_field_setup()
    
    def render_sidebar(self):
        """Render sidebar with field management"""
        with st.sidebar:
            st.header("📍 Field Management")
            
            # Field coordinates (pre-filled with your field)
            st.subheader("Field Coordinates")
            lat = st.number_input("Latitude", value=28.368911, format="%.6f")
            lon = st.number_input("Longitude", value=77.541033, format="%.6f")
            area_m2 = st.number_input("Area (m²)", value=325.12, format="%.2f")
            
            # Crop information
            st.subheader("Crop Information")
            crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Corn", "Soybeans"])
            planting_date = st.date_input("Planting Date", value=datetime.now().date() - timedelta(days=60))
            
            # Data refresh
            st.subheader("Data Management")
            if st.button("🔄 Refresh Field Data", type="primary"):
                with st.spinner("Fetching latest field data..."):
                    self.refresh_field_data(lat, lon, area_m2, crop_type, planting_date)
            
            if st.button("📊 Generate Yield Report"):
                with st.spinner("Generating yield predictions..."):
                    self.generate_yield_report(planting_date)
            
            # Field status
            if st.session_state.field_data:
                st.success("✅ Field data loaded")
                last_update = st.session_state.last_update
                if last_update:
                    st.caption(f"Last updated: {last_update}")
            else:
                st.warning("⚠️ No field data loaded")
    
    def render_field_setup(self):
        """Render field setup page"""
        st.header("🌱 Field Setup Required")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📍 Your Field")
            st.info(f"""
            **Coordinates:** 28.368911, 77.541033  
            **Area:** 325.12 m² (0.08 acres)  
            **Crop:** Rice  
            **Location:** Delhi, India
            """)
            
            if st.button("🚀 Load This Field", type="primary"):
                with st.spinner("Loading field data..."):
                    self.refresh_field_data(28.368911, 77.541033, 325.12, "Rice", datetime.now().date() - timedelta(days=60))
        
        with col2:
            st.subheader("🛠️ Data Sources")
            st.info("""
            **Weather Data:** NOAA Weather API  
            **Soil Data:** USDA Soil Survey  
            **Satellite Data:** Sentinel-2 NDVI  
            **Prediction Model:** Multi-factor AI
            """)
    
    def refresh_field_data(self, lat, lon, area_m2, crop_type, planting_date):
        """Refresh field data from all sources"""
        try:
            # Update field integration coordinates
            self.field_integration.field_lat = lat
            self.field_integration.field_lon = lon
            self.field_integration.field_area_m2 = area_m2
            
            # Get comprehensive field data
            field_data = self.field_integration.get_field_summary()
            field_data['field_info']['crop'] = crop_type
            field_data['planting_date'] = planting_date.isoformat()
            
            # Calculate days since planting
            days_since_planting = (datetime.now().date() - planting_date).days
            field_data['days_since_planting'] = days_since_planting
            
            # Store in session state
            st.session_state.field_data = field_data
            st.session_state.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            st.success("✅ Field data refreshed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error refreshing field data: {e}")
            logger.error(f"Error refreshing field data: {e}")
    
    def generate_yield_report(self, planting_date):
        """Generate comprehensive yield report"""
        try:
            if not st.session_state.field_data:
                st.error("Please load field data first")
                return
            
            # Calculate days since planting
            days_since_planting = (datetime.now().date() - planting_date).days
            
            # Generate yield predictions
            predictions = self.yield_model.predict_yield_scenarios(
                st.session_state.field_data, 
                days_since_planting
            )
            
            # Get risk factors
            risk_factors = self.yield_model.get_risk_factors(
                st.session_state.field_data, 
                predictions
            )
            
            # Store results
            st.session_state.yield_predictions = {
                'predictions': predictions,
                'risk_factors': risk_factors,
                'days_since_planting': days_since_planting,
                'generated_at': datetime.now().isoformat()
            }
            
            st.success("✅ Yield report generated successfully!")
            
        except Exception as e:
            st.error(f"❌ Error generating yield report: {e}")
            logger.error(f"Error generating yield report: {e}")
    
    def render_field_dashboard(self):
        """Render main field dashboard"""
        field_data = st.session_state.field_data
        
        # Field overview
        self.render_field_overview(field_data)
        
        # Current conditions
        self.render_current_conditions(field_data)
        
        # Yield predictions
        if st.session_state.yield_predictions:
            self.render_yield_predictions()
        
        # Risk analysis
        if st.session_state.yield_predictions:
            self.render_risk_analysis()
        
        # Weather trends
        self.render_weather_trends(field_data)
    
    def render_field_overview(self, field_data):
        """Render field overview section"""
        st.header("📍 Field Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Area", f"{field_data['field_info']['area_acres']:.2f} acres")
        with col2:
            st.metric("Crop", field_data['field_info']['crop'])
        with col3:
            days = field_data.get('days_since_planting', 0)
            st.metric("Days Since Planting", days)
        with col4:
            data_quality = field_data.get('data_quality', {})
            available_sources = sum(data_quality.values())
            st.metric("Data Sources", f"{available_sources}/4")
    
    def render_current_conditions(self, field_data):
        """Render current conditions section"""
        st.header("🌤️ Current Conditions")
        
        col1, col2, col3 = st.columns(3)
        
        # Weather conditions
        with col1:
            st.subheader("🌤️ Weather")
            weather = field_data.get('real_time_weather', {})
            if weather:
                st.metric("Temperature", f"{weather.get('temperature_c', 'N/A')}°C")
                st.metric("Humidity", f"{weather.get('humidity', 'N/A')}%")
                st.metric("Wind Speed", f"{weather.get('wind_speed', 'N/A')} m/s")
                st.metric("Pressure", f"{weather.get('pressure', 'N/A')} hPa")
                st.metric("Visibility", f"{weather.get('visibility', 'N/A')} km")
                st.metric("Cloud Cover", f"{weather.get('cloud_cover', 'N/A')}%")
                
                # Weather description
                description = weather.get('description', 'N/A')
                weather_main = weather.get('weather_main', 'N/A')
                st.info(f"**{weather_main.title()}**: {description.title()}")
                
                # API source
                api_source = weather.get('api_source', 'Unknown')
                st.caption(f"Data source: {api_source}")
            else:
                st.warning("Weather data not available")
        
        # Soil conditions
        with col2:
            st.subheader("🌱 Soil")
            soil = field_data.get('soil_data', {})
            if soil:
                st.metric("pH", f"{soil.get('ph', 'N/A')}")
                st.metric("Organic Matter", f"{soil.get('organic_matter', 'N/A')}%")
                st.metric("Clay Content", f"{soil.get('clay_content', 'N/A')}%")
            else:
                st.warning("Soil data not available")
        
        # Vegetation health
        with col3:
            st.subheader("🛰️ Vegetation Health")
            ndvi = field_data.get('ndvi_data', {})
            if ndvi:
                st.metric("Mean NDVI", f"{ndvi.get('mean_ndvi', 0):.3f}")
                st.metric("Max NDVI", f"{ndvi.get('max_ndvi', 0):.3f}")
                st.metric("Health Status", "Good" if ndvi.get('mean_ndvi', 0) > 0.6 else "Poor")
            else:
                st.warning("NDVI data not available")
    
    def render_yield_predictions(self):
        """Render yield predictions section"""
        st.header("📊 Yield Predictions")
        
        predictions = st.session_state.yield_predictions['predictions']
        
        # Scenario comparison
        col1, col2, col3 = st.columns(3)
        
        scenarios = ['drought', 'normal', 'optimal']
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
        
        for i, scenario in enumerate(scenarios):
            with [col1, col2, col3][i]:
                data = predictions[scenario]
                st.metric(
                    f"{scenario.title()} Scenario",
                    f"{data['yield_tons_per_acre']} tons/acre",
                    delta=f"Confidence: {data['confidence']:.1%}"
                )
                
                # Show total yield for the field
                st.caption(f"Total: {data['total_yield_kg']:.1f} kg")
        
        # Yield prediction chart
        self.render_yield_chart(predictions)
        
        # Detailed breakdown
        self.render_yield_breakdown(predictions)
    
    def render_yield_chart(self, predictions):
        """Render yield prediction chart"""
        scenarios = list(predictions.keys())
        yields = [predictions[s]['yield_tons_per_acre'] for s in scenarios]
        confidences = [predictions[s]['confidence'] for s in scenarios]
        
        fig = go.Figure()
        
        # Add yield bars
        fig.add_trace(go.Bar(
            x=scenarios,
            y=yields,
            name='Yield (tons/acre)',
            marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1']
        ))
        
        # Add confidence line
        fig.add_trace(go.Scatter(
            x=scenarios,
            y=[y * c for y, c in zip(yields, confidences)],
            mode='lines+markers',
            name='Confidence Adjusted',
            line=dict(color='orange', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Yield Predictions by Scenario",
            xaxis_title="Scenario",
            yaxis_title="Yield (tons/acre)",
            yaxis2=dict(title="Confidence Adjusted Yield", overlaying="y", side="right"),
            height=400
        )
        
        st.plotly_chart(fig, width='stretch')
    
    def render_yield_breakdown(self, predictions):
        """Render detailed yield breakdown"""
        st.subheader("📈 Detailed Breakdown")
        
        # Create breakdown table
        breakdown_data = []
        for scenario, data in predictions.items():
            breakdown_data.append({
                'Scenario': scenario.title(),
                'Yield (tons/acre)': data['yield_tons_per_acre'],
                'Total Yield (kg)': data['total_yield_kg'],
                'Confidence': f"{data['confidence']:.1%}",
                'Weather Score': data['score_breakdown']['weather'],
                'Soil Score': data['score_breakdown']['soil'],
                'NDVI Score': data['score_breakdown']['ndvi'],
                'Growth Score': data['score_breakdown']['growth']
            })
        
        df = pd.DataFrame(breakdown_data)
        st.dataframe(df, width='stretch')
    
    def render_risk_analysis(self):
        """Render risk analysis section"""
        st.header("⚠️ Risk Analysis")
        
        risk_factors = st.session_state.yield_predictions['risk_factors']
        
        if risk_factors:
            # Risk severity distribution
            severity_counts = {}
            for risk in risk_factors:
                severity = risk['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk severity chart
                fig = go.Figure(data=[
                    go.Bar(x=list(severity_counts.keys()), y=list(severity_counts.values()),
                          marker_color=['#ff6b6b', '#ffa726', '#66bb6a'])
                ])
                fig.update_layout(
                    title="Risk Factors by Severity",
                    xaxis_title="Severity",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                # Top risks
                st.subheader("🔍 Top Risk Factors")
                for i, risk in enumerate(risk_factors[:5]):
                    severity_color = {
                        'High': '🔴',
                        'Medium': '🟡',
                        'Low': '🟢'
                    }.get(risk['severity'], '⚪')
                    
                    st.write(f"{severity_color} **{risk['factor']}**")
                    st.write(f"   Impact: {risk['impact']}")
                    st.write(f"   Recommendation: {risk['recommendation']}")
                    st.write("---")
        else:
            st.success("✅ No significant risk factors identified!")
    
    def render_weather_trends(self, field_data):
        """Render weather trends chart"""
        st.header("📈 Weather Trends")
        
        historical_weather = field_data.get('historical_weather')
        if historical_weather and len(historical_weather) > 0:
            # Convert to DataFrame
            df = pd.DataFrame(historical_weather)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Create weather trends chart
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)', 'Precipitation (mm)'),
                vertical_spacing=0.1
            )
            
            # Temperature
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['temperature_c'], name='Temperature', line=dict(color='red')),
                row=1, col=1
            )
            
            # Humidity
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['humidity'], name='Humidity', line=dict(color='blue')),
                row=1, col=2
            )
            
            # Wind Speed
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['wind_speed'], name='Wind Speed', line=dict(color='green')),
                row=2, col=1
            )
            
            # Precipitation
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['precipitation'], name='Precipitation', line=dict(color='purple')),
                row=2, col=2
            )
            
            fig.update_layout(height=600, showlegend=False, title_text="30-Day Weather Trends")
            st.plotly_chart(fig, width='stretch')
            
            # Weather summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg Temperature", f"{df['temperature_c'].mean():.1f}°C")
            with col2:
                st.metric("Avg Humidity", f"{df['humidity'].mean():.1f}%")
            with col3:
                st.metric("Avg Wind Speed", f"{df['wind_speed'].mean():.1f} m/s")
            with col4:
                st.metric("Total Precipitation", f"{df['precipitation'].sum():.1f} mm")
        else:
            st.info("Historical weather data not available")
    
    def render_recommendations(self):
        """Render recommendations section"""
        st.header("💡 Recommendations")
        
        # Generate recommendations based on current data
        if st.session_state.field_data and st.session_state.yield_predictions:
            recommendations = self.yield_model.generate_recommendations(
                st.session_state.field_data,
                st.session_state.yield_predictions['predictions'],
                st.session_state.yield_predictions['risk_factors']
            )
            
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.info("Generate yield predictions to see recommendations")

def main():
    """Main application entry point"""
    app = AgriForecastMVP()
    app.run()

if __name__ == "__main__":
    main()
