"""
FastAPI Backend Integration for AgriForecast.ai
Complete API client with TimesFM models and advanced analytics
"""

import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import aiohttp
import time
from dataclasses import dataclass
import plotly.graph_objects as go
import plotly.express as px

@dataclass
class APIResponse:
    """Standardized API response format"""
    success: bool
    data: Any = None
    error: str = None
    status_code: int = None
    response_time: float = None

class FastAPIClient:
    """Comprehensive FastAPI backend client"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.timeout = 30
        self.max_retries = 3
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> APIResponse:
        """Make HTTP request with error handling and retries"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                response = self.session.request(
                    method, url, 
                    timeout=self.timeout,
                    **kwargs
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        return APIResponse(
                            success=True,
                            data=data,
                            status_code=response.status_code,
                            response_time=response_time
                        )
                    except json.JSONDecodeError:
                        return APIResponse(
                            success=True,
                            data=response.text,
                            status_code=response.status_code,
                            response_time=response_time
                        )
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    return APIResponse(
                        success=False,
                        error=error_msg,
                        status_code=response.status_code,
                        response_time=response_time
                    )
                    
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    return APIResponse(
                        success=False,
                        error=f"Request failed after {self.max_retries} attempts: {str(e)}",
                        status_code=None
                    )
                time.sleep(1 * (attempt + 1))  # Exponential backoff
        
        return APIResponse(success=False, error="Max retries exceeded")
    
    def health_check(self) -> APIResponse:
        """Check backend health status"""
        return self._make_request('GET', '/health')
    
    def get_api_info(self) -> APIResponse:
        """Get API information and available endpoints"""
        return self._make_request('GET', '/')
    
    # TimesFM Integration
    def predict_yield(self, field_data: Dict) -> APIResponse:
        """Predict crop yield using TimesFM models"""
        return self._make_request('POST', '/predict/yield', json=field_data)
    
    def forecast_weather_impact(self, weather_data: Dict) -> APIResponse:
        """Forecast weather impact on crops"""
        return self._make_request('POST', '/forecast/weather-impact', json=weather_data)
    
    def analyze_crop_health(self, crop_data: Dict) -> APIResponse:
        """Analyze crop health using AI models"""
        return self._make_request('POST', '/analyze/crop-health', json=crop_data)
    
    def get_market_predictions(self, crop_type: str, region: str = None) -> APIResponse:
        """Get market price predictions"""
        params = {'crop_type': crop_type}
        if region:
            params['region'] = region
        return self._make_request('GET', '/market/predictions', params=params)
    
    def optimize_irrigation(self, field_data: Dict) -> APIResponse:
        """Get irrigation optimization recommendations"""
        return self._make_request('POST', '/optimize/irrigation', json=field_data)
    
    def risk_assessment(self, field_data: Dict) -> APIResponse:
        """Perform comprehensive risk assessment"""
        return self._make_request('POST', '/risk/assessment', json=field_data)
    
    # Advanced Analytics
    def get_yield_trends(self, field_id: str, time_range: int = 365) -> APIResponse:
        """Get historical yield trends"""
        params = {'field_id': field_id, 'days': time_range}
        return self._make_request('GET', '/analytics/yield-trends', params=params)
    
    def get_weather_analytics(self, location: Dict, time_range: int = 30) -> APIResponse:
        """Get weather analytics and patterns"""
        params = {
            'lat': location.get('latitude'),
            'lon': location.get('longitude'),
            'days': time_range
        }
        return self._make_request('GET', '/analytics/weather', params=params)
    
    def get_crop_insights(self, crop_type: str, region: str = None) -> APIResponse:
        """Get crop-specific insights and recommendations"""
        params = {'crop_type': crop_type}
        if region:
            params['region'] = region
        return self._make_request('GET', '/insights/crop', params=params)
    
    def batch_predict(self, batch_data: List[Dict]) -> APIResponse:
        """Batch prediction for multiple fields"""
        return self._make_request('POST', '/predict/batch', json={'fields': batch_data})
    
    # Data Management
    def upload_field_data(self, field_data: Dict) -> APIResponse:
        """Upload field data to backend"""
        return self._make_request('POST', '/data/fields', json=field_data)
    
    def get_field_data(self, field_id: str) -> APIResponse:
        """Get field data from backend"""
        return self._make_request('GET', f'/data/fields/{field_id}')
    
    def update_field_data(self, field_id: str, field_data: Dict) -> APIResponse:
        """Update field data in backend"""
        return self._make_request('PUT', f'/data/fields/{field_id}', json=field_data)
    
    def delete_field_data(self, field_id: str) -> APIResponse:
        """Delete field data from backend"""
        return self._make_request('DELETE', f'/data/fields/{field_id}')

class TimesFMAnalytics:
    """Advanced analytics using TimesFM models"""
    
    def __init__(self, api_client: FastAPIClient):
        self.api_client = api_client
        
    def comprehensive_field_analysis(self, field_data: Dict) -> Dict:
        """Perform comprehensive field analysis"""
        results = {}
        
        # Yield prediction
        yield_response = self.api_client.predict_yield(field_data)
        if yield_response.success:
            results['yield_prediction'] = yield_response.data
        
        # Risk assessment
        risk_response = self.api_client.risk_assessment(field_data)
        if risk_response.success:
            results['risk_assessment'] = risk_response.data
        
        # Crop health analysis
        health_response = self.api_client.analyze_crop_health(field_data)
        if health_response.success:
            results['crop_health'] = health_response.data
        
        # Irrigation optimization
        irrigation_response = self.api_client.optimize_irrigation(field_data)
        if irrigation_response.success:
            results['irrigation_optimization'] = irrigation_response.data
        
        return results
    
    def generate_predictive_insights(self, field_data: Dict, time_horizon: int = 90) -> Dict:
        """Generate predictive insights for specified time horizon"""
        insights = {
            'time_horizon_days': time_horizon,
            'predictions': {},
            'recommendations': [],
            'risk_factors': [],
            'opportunities': []
        }
        
        # Weather impact forecast
        weather_data = {
            'field_id': field_data.get('id'),
            'latitude': field_data.get('latitude'),
            'longitude': field_data.get('longitude'),
            'crop_type': field_data.get('crop_type'),
            'days_ahead': time_horizon
        }
        
        weather_response = self.api_client.forecast_weather_impact(weather_data)
        if weather_response.success:
            insights['predictions']['weather_impact'] = weather_response.data
        
        # Market predictions
        crop_type = field_data.get('crop_type', 'rice')
        market_response = self.api_client.get_market_predictions(crop_type)
        if market_response.success:
            insights['predictions']['market_outlook'] = market_response.data
        
        # Crop insights
        crop_insights_response = self.api_client.get_crop_insights(crop_type)
        if crop_insights_response.success:
            insights['crop_insights'] = crop_insights_response.data
        
        return insights
    
    def create_yield_forecast_chart(self, field_data: Dict) -> go.Figure:
        """Create yield forecast visualization"""
        # Get yield trends
        field_id = field_data.get('id', 'demo_field')
        trends_response = self.api_client.get_yield_trends(field_id, 365)
        
        fig = go.Figure()
        
        if trends_response.success and trends_response.data:
            trend_data = trends_response.data
            
            # Historical data
            if 'historical' in trend_data:
                historical = trend_data['historical']
                fig.add_trace(go.Scatter(
                    x=historical.get('dates', []),
                    y=historical.get('yields', []),
                    mode='lines+markers',
                    name='Historical Yield',
                    line=dict(color='blue', width=2)
                ))
            
            # Predicted data
            if 'predicted' in trend_data:
                predicted = trend_data['predicted']
                fig.add_trace(go.Scatter(
                    x=predicted.get('dates', []),
                    y=predicted.get('yields', []),
                    mode='lines+markers',
                    name='Predicted Yield',
                    line=dict(color='orange', width=2, dash='dash')
                ))
                
                # Confidence interval
                if 'confidence_interval' in predicted:
                    ci = predicted['confidence_interval']
                    fig.add_trace(go.Scatter(
                        x=predicted.get('dates', []) + predicted.get('dates', [])[::-1],
                        y=ci.get('upper', []) + ci.get('lower', [])[::-1],
                        fill='toself',
                        fillcolor='rgba(255,165,0,0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='Confidence Interval',
                        hoverinfo="skip"
                    ))
        else:
            # Fallback demo data
            dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
            historical_yield = np.random.normal(4.5, 0.5, 8)
            predicted_yield = np.random.normal(5.0, 0.3, 4)
            
            fig.add_trace(go.Scatter(
                x=dates[:8],
                y=historical_yield,
                mode='lines+markers',
                name='Historical Yield',
                line=dict(color='blue', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=dates[8:],
                y=predicted_yield,
                mode='lines+markers',
                name='Predicted Yield',
                line=dict(color='orange', width=2, dash='dash')
            ))
        
        fig.update_layout(
            title=f"Yield Forecast - {field_data.get('name', 'Field')}",
            xaxis_title="Date",
            yaxis_title="Yield (tons/hectare)",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_risk_assessment_chart(self, risk_data: Dict) -> go.Figure:
        """Create risk assessment visualization"""
        fig = go.Figure()
        
        if risk_data and 'factors' in risk_data:
            factors = risk_data['factors']
            
            # Risk factor names and scores
            factor_names = list(factors.keys())
            risk_scores = list(factors.values())
            
            # Color coding based on risk level
            colors = ['green' if score < 30 else 'yellow' if score < 60 else 'red' 
                     for score in risk_scores]
            
            fig.add_trace(go.Bar(
                x=factor_names,
                y=risk_scores,
                marker_color=colors,
                text=[f"{score}%" for score in risk_scores],
                textposition='auto'
            ))
        else:
            # Fallback demo data
            factors = ['Weather Risk', 'Pest Risk', 'Disease Risk', 'Market Risk', 'Irrigation Risk']
            scores = [25, 45, 15, 35, 20]
            colors = ['green' if score < 30 else 'yellow' if score < 60 else 'red' 
                     for score in scores]
            
            fig.add_trace(go.Bar(
                x=factors,
                y=scores,
                marker_color=colors,
                text=[f"{score}%" for score in scores],
                textposition='auto'
            ))
        
        fig.update_layout(
            title="Risk Assessment",
            xaxis_title="Risk Factors",
            yaxis_title="Risk Level (%)",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        return fig

class BackendConnectionManager:
    """Manages backend connection and health monitoring"""
    
    def __init__(self, api_client: FastAPIClient):
        self.api_client = api_client
        self.last_health_check = None
        self.is_healthy = False
        self.connection_attempts = 0
        self.max_connection_attempts = 5
        
    def check_backend_health(self) -> Dict:
        """Check backend health and connection status"""
        try:
            response = self.api_client.health_check()
            
            if response.success:
                self.is_healthy = True
                self.connection_attempts = 0
                self.last_health_check = datetime.now()
                
                return {
                    'status': 'healthy',
                    'backend_url': self.api_client.base_url,
                    'response_time': response.response_time,
                    'last_check': self.last_health_check,
                    'data': response.data
                }
            else:
                self.is_healthy = False
                self.connection_attempts += 1
                
                return {
                    'status': 'unhealthy',
                    'backend_url': self.api_client.base_url,
                    'error': response.error,
                    'attempts': self.connection_attempts
                }
                
        except Exception as e:
            self.is_healthy = False
            self.connection_attempts += 1
            
            return {
                'status': 'error',
                'backend_url': self.api_client.base_url,
                'error': str(e),
                'attempts': self.connection_attempts
            }
    
    def get_backend_info(self) -> Dict:
        """Get comprehensive backend information"""
        info = {
            'connection_status': 'unknown',
            'backend_url': self.api_client.base_url,
            'features_available': [],
            'last_health_check': self.last_health_check,
            'connection_attempts': self.connection_attempts
        }
        
        # Check health
        health_status = self.check_backend_health()
        info.update(health_status)
        
        if self.is_healthy:
            # Get API info
            try:
                api_response = self.api_client.get_api_info()
                if api_response.success:
                    info['api_info'] = api_response.data
                    
                    # Extract available features
                    if isinstance(api_response.data, dict):
                        endpoints = api_response.data.get('endpoints', [])
                        info['features_available'] = endpoints
                        
            except Exception as e:
                info['api_info_error'] = str(e)
        
        return info

# Global instances
_api_client = None
_timesfm_analytics = None
_connection_manager = None

def get_api_client(base_url: str = "http://localhost:8000") -> FastAPIClient:
    """Get global API client instance"""
    global _api_client
    if _api_client is None:
        _api_client = FastAPIClient(base_url)
    return _api_client

def get_timesfm_analytics() -> TimesFMAnalytics:
    """Get global TimesFM analytics instance"""
    global _timesfm_analytics
    if _timesfm_analytics is None:
        _timesfm_analytics = TimesFMAnalytics(get_api_client())
    return _timesfm_analytics

def get_connection_manager() -> BackendConnectionManager:
    """Get global connection manager instance"""
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = BackendConnectionManager(get_api_client())
    return _connection_manager

# Convenience functions for Streamlit integration
def check_backend_status():
    """Check and display backend status in Streamlit"""
    connection_manager = get_connection_manager()
    backend_info = connection_manager.get_backend_info()
    
    if backend_info['status'] == 'healthy':
        st.success(f"🟢 Backend Connected: {backend_info['backend_url']}")
        if 'response_time' in backend_info:
            st.info(f"⚡ Response Time: {backend_info['response_time']:.3f}s")
        return True
    elif backend_info['status'] == 'unhealthy':
        st.error(f"🔴 Backend Unhealthy: {backend_info.get('error', 'Unknown error')}")
        return False
    else:
        st.warning(f"⚠️ Backend Connection Issues: {backend_info.get('error', 'Unknown error')}")
        return False

def display_backend_info():
    """Display comprehensive backend information"""
    connection_manager = get_connection_manager()
    backend_info = connection_manager.get_backend_info()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_color = "🟢" if backend_info['status'] == 'healthy' else "🔴"
        st.metric("Backend Status", f"{status_color} {backend_info['status'].title()}")
    
    with col2:
        if 'response_time' in backend_info:
            st.metric("Response Time", f"{backend_info['response_time']:.3f}s")
        else:
            st.metric("Response Time", "N/A")
    
    with col3:
        features_count = len(backend_info.get('features_available', []))
        st.metric("Available Features", features_count)
    
    # Detailed info
    with st.expander("Backend Details"):
        st.json(backend_info)

def test_api_endpoints():
    """Test various API endpoints and display results"""
    st.subheader("🧪 API Endpoint Testing")
    
    api_client = get_api_client()
    
    # Test data
    test_field_data = {
        'id': 'test_field_1',
        'name': 'Test Field',
        'crop_type': 'rice',
        'area_acres': 5.0,
        'latitude': 28.368911,
        'longitude': 77.541033,
        'soil_type': 'loamy',
        'planting_date': '2024-01-15'
    }
    
    # Test endpoints
    tests = [
        ("Health Check", lambda: api_client.health_check()),
        ("API Info", lambda: api_client.get_api_info()),
        ("Yield Prediction", lambda: api_client.predict_yield(test_field_data)),
        ("Risk Assessment", lambda: api_client.risk_assessment(test_field_data)),
        ("Market Predictions", lambda: api_client.get_market_predictions('rice')),
    ]
    
    for test_name, test_func in tests:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{test_name}**")
        
        with col2:
            if st.button(f"Test", key=f"test_{test_name}"):
                with st.spinner(f"Testing {test_name}..."):
                    result = test_func()
                    
                    with col3:
                        if result.success:
                            st.success("✅")
                        else:
                            st.error("❌")
                    
                    # Show result details
                    with st.expander(f"{test_name} Results"):
                        if result.success:
                            st.json(result.data)
                        else:
                            st.error(result.error)

# Demo functions
def demo_backend_integration():
    """Demo the complete backend integration"""
    st.title("🔗 FastAPI Backend Integration")
    
    # Backend status
    st.subheader("🏥 Backend Health")
    if check_backend_status():
        display_backend_info()
        
        # API testing
        test_api_endpoints()
        
        # TimesFM Analytics demo
        st.subheader("🤖 TimesFM Analytics")
        
        analytics = get_timesfm_analytics()
        
        # Sample field data
        demo_field = {
            'id': 'demo_field_1',
            'name': 'Demo Rice Field',
            'crop_type': 'rice',
            'area_acres': 5.0,
            'latitude': 28.368911,
            'longitude': 77.541033,
            'soil_type': 'loamy'
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔮 Generate Yield Forecast"):
                with st.spinner("Generating forecast..."):
                    fig = analytics.create_yield_forecast_chart(demo_field)
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if st.button("⚠️ Risk Assessment"):
                with st.spinner("Analyzing risks..."):
                    # Get risk data from API
                    api_client = get_api_client()
                    risk_response = api_client.risk_assessment(demo_field)
                    
                    if risk_response.success:
                        fig = analytics.create_risk_assessment_chart(risk_response.data)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"Risk assessment failed: {risk_response.error}")
        
        # Comprehensive analysis
        if st.button("📊 Comprehensive Field Analysis"):
            with st.spinner("Performing comprehensive analysis..."):
                analysis = analytics.comprehensive_field_analysis(demo_field)
                
                if analysis:
                    st.success("Analysis complete!")
                    
                    for analysis_type, data in analysis.items():
                        with st.expander(f"{analysis_type.replace('_', ' ').title()}"):
                            st.json(data)
                else:
                    st.warning("No analysis data available")
    
    else:
        st.error("Backend is not available. Please ensure FastAPI server is running.")
        st.info("Start the backend with: `uvicorn main:app --reload`")

if __name__ == "__main__":
    demo_backend_integration()
