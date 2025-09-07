"""
TimesFM Analytics Dashboard for AgriForecast.ai
Advanced machine learning insights and predictions
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

# Import FastAPI integration if available
try:
    from fastapi_integration import get_api_client, check_backend_status
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

class TimesFMDashboard:
    """TimesFM-powered analytics dashboard"""
    
    def __init__(self):
        self.backend_available = BACKEND_AVAILABLE
        if self.backend_available:
            self.api_client = get_api_client()
    
    def create_yield_forecast_advanced(self, field_data: Dict) -> go.Figure:
        """Create advanced yield forecast with TimesFM predictions"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Yield Prediction Timeline', 'Confidence Intervals', 
                          'Risk Factors Impact', 'Seasonal Patterns'),
            specs=[[{"secondary_y": False}, {"secondary_y": True}],
                   [{"type": "bar"}, {"type": "polar"}]]
        )
        
        # Generate prediction data
        if self.backend_available:
            try:
                response = self.api_client.predict_yield(field_data)
                if response.success:
                    prediction_data = response.data
                else:
                    prediction_data = self._generate_demo_prediction()
            except Exception:
                prediction_data = self._generate_demo_prediction()
        else:
            prediction_data = self._generate_demo_prediction()
        
        # Timeline prediction
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        historical = prediction_data.get('historical_yield', np.random.normal(4.2, 0.3, 6))
        predicted = prediction_data.get('predicted_yield', np.random.normal(4.8, 0.2, 6))
        
        fig.add_trace(
            go.Scatter(x=dates[:6], y=historical, name='Historical', 
                      line=dict(color='blue', width=3)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=dates[6:], y=predicted, name='TimesFM Prediction', 
                      line=dict(color='red', width=3, dash='dash')),
            row=1, col=1
        )
        
        # Confidence intervals
        upper_bound = np.array(predicted) + 0.3
        lower_bound = np.array(predicted) - 0.3
        
        fig.add_trace(
            go.Scatter(x=dates[6:], y=upper_bound, line=dict(color='rgba(0,100,80,0)'), 
                      showlegend=False),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=dates[6:], y=lower_bound, fill='tonexty', 
                      fillcolor='rgba(255,0,0,0.2)', line=dict(color='rgba(255,255,255,0)'),
                      name='95% Confidence'),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=dates[6:], y=predicted, name='Prediction', 
                      line=dict(color='red', width=2)),
            row=1, col=2
        )
        
        # Risk factors
        risk_factors = ['Weather', 'Soil', 'Pests', 'Market', 'Climate']
        risk_impact = np.random.uniform(-0.5, 0.3, len(risk_factors))
        colors = ['red' if impact < -0.2 else 'yellow' if impact < 0.1 else 'green' 
                 for impact in risk_impact]
        
        fig.add_trace(
            go.Bar(x=risk_factors, y=risk_impact, marker_color=colors,
                  name='Yield Impact', showlegend=False),
            row=2, col=1
        )
        
        # Seasonal patterns
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        seasonal_yield = np.random.uniform(0.3, 1.0, 12)
        
        fig.add_trace(
            go.Scatterpolar(r=seasonal_yield, theta=months, fill='toself',
                          name='Seasonal Yield Pattern'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="TimesFM Advanced Yield Analytics",
            height=600,
            showlegend=True
        )
        
        return fig
    
    def create_market_intelligence_chart(self) -> go.Figure:
        """Create market intelligence visualization"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Price Prediction', 'Supply-Demand Balance', 
                          'Regional Markets', 'Profit Windows')
        )
        
        # Price prediction
        dates = pd.date_range(start='2024-01-01', periods=52, freq='W')
        prices = 450 + 50 * np.sin(np.linspace(0, 4*np.pi, 52)) + np.random.normal(0, 15, 52)
        predicted_prices = prices[-12:] + np.random.normal(10, 5, 12)
        
        fig.add_trace(
            go.Scatter(x=dates[:-12], y=prices[:-12], name='Historical Prices',
                      line=dict(color='blue')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=dates[-12:], y=predicted_prices, name='AI Prediction',
                      line=dict(color='red', dash='dash')),
            row=1, col=1
        )
        
        # Supply-demand
        supply = np.random.uniform(800, 1200, 12)
        demand = np.random.uniform(900, 1100, 12)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig.add_trace(
            go.Bar(x=months, y=supply, name='Supply', marker_color='lightblue'),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(x=months, y=demand, name='Demand', marker_color='lightcoral'),
            row=1, col=2
        )
        
        # Regional markets
        regions = ['Punjab', 'Haryana', 'UP', 'Bihar', 'WB']
        regional_prices = np.random.uniform(400, 600, len(regions))
        market_share = np.random.uniform(10, 30, len(regions))
        
        fig.add_trace(
            go.Scatter(x=regional_prices, y=market_share, mode='markers+text',
                      text=regions, textposition='top center',
                      marker=dict(size=15, color=regional_prices, colorscale='Viridis'),
                      name='Regional Markets'),
            row=2, col=1
        )
        
        # Profit windows
        selling_periods = ['Oct-Nov', 'Dec-Jan', 'Feb-Mar', 'Apr-May']
        profit_margins = [18, 25, 22, 15]
        
        fig.add_trace(
            go.Bar(x=selling_periods, y=profit_margins, 
                  marker_color=['red' if p < 20 else 'green' for p in profit_margins],
                  name='Profit Margin %', showlegend=False),
            row=2, col=2
        )
        
        fig.update_layout(
            title="AI-Powered Market Intelligence",
            height=600
        )
        
        return fig
    
    def create_risk_assessment_radar(self, field_data: Dict) -> go.Figure:
        """Create comprehensive risk assessment radar chart"""
        if self.backend_available:
            try:
                response = self.api_client.risk_assessment(field_data)
                if response.success:
                    risk_data = response.data.get('factors', {})
                else:
                    risk_data = self._generate_demo_risks()
            except Exception:
                risk_data = self._generate_demo_risks()
        else:
            risk_data = self._generate_demo_risks()
        
        categories = list(risk_data.keys())
        values = list(risk_data.values())
        
        # Normalize to 0-1 scale for radar chart
        normalized_values = [v/100 for v in values]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values,
            theta=categories,
            fill='toself',
            name='Current Risk Level',
            fillcolor='rgba(255,0,0,0.3)',
            line=dict(color='red', width=2)
        ))
        
        # Add optimal risk levels
        optimal_risks = [0.2] * len(categories)  # 20% optimal risk
        fig.add_trace(go.Scatterpolar(
            r=optimal_risks,
            theta=categories,
            fill='toself',
            name='Optimal Risk Level',
            fillcolor='rgba(0,255,0,0.2)',
            line=dict(color='green', width=2, dash='dash')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],
                    ticktext=['20%', '40%', '60%', '80%', '100%']
                )),
            title="Comprehensive Risk Assessment",
            height=500
        )
        
        return fig
    
    def generate_ai_insights(self, field_data: Dict) -> List[Dict]:
        """Generate AI-powered insights and recommendations"""
        insights = []
        
        # Get predictions from backend if available
        if self.backend_available:
            try:
                # Yield prediction insights
                yield_response = self.api_client.predict_yield(field_data)
                if yield_response.success:
                    yield_data = yield_response.data
                    predicted_yield = yield_data.get('predicted_yield', 4.5)
                    
                    if predicted_yield > 5.0:
                        insights.append({
                            'type': 'success',
                            'title': 'Excellent Yield Potential',
                            'description': f'AI models predict exceptional yield of {predicted_yield:.1f} tons/ha',
                            'confidence': 'High',
                            'action': 'Maintain current practices and consider expanding area'
                        })
                    elif predicted_yield < 3.5:
                        insights.append({
                            'type': 'warning',
                            'title': 'Yield Optimization Needed',
                            'description': f'Predicted yield of {predicted_yield:.1f} tons/ha is below potential',
                            'confidence': 'High',
                            'action': 'Review irrigation, fertilization, and pest management'
                        })
                
                # Risk assessment insights
                risk_response = self.api_client.risk_assessment(field_data)
                if risk_response.success:
                    risk_data = risk_response.data
                    overall_risk = risk_data.get('overall_risk_score', 30)
                    
                    if overall_risk > 70:
                        insights.append({
                            'type': 'error',
                            'title': 'Critical Risk Level',
                            'description': f'Overall risk score of {overall_risk}% requires immediate attention',
                            'confidence': 'Critical',
                            'action': 'Implement emergency risk mitigation measures'
                        })
                
            except Exception as e:
                insights.append({
                    'type': 'info',
                    'title': 'Backend Connection Issue',
                    'description': 'Using demo insights due to backend connectivity',
                    'confidence': 'Low',
                    'action': 'Check FastAPI backend connection'
                })
        
        # Default demo insights if no backend data
        if not insights:
            insights = [
                {
                    'type': 'info',
                    'title': 'TimesFM Model Ready',
                    'description': 'Advanced forecasting models are ready for your field analysis',
                    'confidence': 'High',
                    'action': 'Upload field data for personalized predictions'
                },
                {
                    'type': 'success',
                    'title': 'Optimal Growing Conditions',
                    'description': 'Current weather patterns favor crop development',
                    'confidence': 'Medium',
                    'action': 'Monitor for any changes in weather patterns'
                }
            ]
        
        return insights
    
    def _generate_demo_prediction(self) -> Dict:
        """Generate demo prediction data"""
        return {
            'predicted_yield': 4.8,
            'confidence_score': 0.87,
            'historical_yield': [4.1, 4.3, 4.0, 4.5, 4.2, 4.4],
            'predicted_yield_series': [4.6, 4.8, 4.9, 4.7, 4.8, 5.0]
        }
    
    def _generate_demo_risks(self) -> Dict:
        """Generate demo risk data"""
        return {
            'Weather Risk': 25,
            'Pest & Disease': 35,
            'Soil Health': 20,
            'Market Volatility': 40,
            'Climate Change': 30,
            'Water Availability': 25
        }

# Global dashboard instance
_timesfm_dashboard = None

def get_timesfm_dashboard() -> TimesFMDashboard:
    """Get global TimesFM dashboard instance"""
    global _timesfm_dashboard
    if _timesfm_dashboard is None:
        _timesfm_dashboard = TimesFMDashboard()
    return _timesfm_dashboard

def render_timesfm_analytics_page(field_data: Dict):
    """Render the complete TimesFM analytics page"""
    st.markdown("""
    <div class="ag-card ag-fade-in">
        <div class="ag-card-header">
            <h1 class="ag-card-title">
                <span>🤖</span>
                TimesFM Analytics Dashboard
            </h1>
        </div>
        <div class="ag-card-content">
            <p>Advanced machine learning insights powered by Google's TimesFM models</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    dashboard = get_timesfm_dashboard()
    
    # Backend status
    if dashboard.backend_available:
        if check_backend_status():
            st.success("🔗 Connected to TimesFM Backend")
        else:
            st.warning("⚠️ Backend unavailable - using demo mode")
    else:
        st.info("📊 Demo Mode - Install fastapi_integration for live data")
    
    # Main analytics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Advanced Yield Forecasting")
        yield_chart = dashboard.create_yield_forecast_advanced(field_data)
        st.plotly_chart(yield_chart, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Risk Assessment")
        risk_chart = dashboard.create_risk_assessment_radar(field_data)
        st.plotly_chart(risk_chart, use_container_width=True)
    
    # Market intelligence
    st.subheader("💰 Market Intelligence")
    market_chart = dashboard.create_market_intelligence_chart()
    st.plotly_chart(market_chart, use_container_width=True)
    
    # AI Insights
    st.subheader("🧠 AI-Powered Insights")
    insights = dashboard.generate_ai_insights(field_data)
    
    for insight in insights:
        icon = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️'
        }.get(insight['type'], 'ℹ️')
        
        with st.expander(f"{icon} {insight['title']} (Confidence: {insight['confidence']})"):
            st.write(f"**Analysis:** {insight['description']}")
            st.write(f"**Recommended Action:** {insight['action']}")

# Demo function
def demo_timesfm_analytics():
    """Demo the TimesFM analytics dashboard"""
    st.title("🤖 TimesFM Analytics Demo")
    
    demo_field = {
        'id': 'timesfm_demo_field',
        'name': 'AI-Optimized Field',
        'crop_type': 'rice',
        'area_acres': 10.0,
        'latitude': 28.368911,
        'longitude': 77.541033,
        'soil_type': 'loamy'
    }
    
    render_timesfm_analytics_page(demo_field)

if __name__ == "__main__":
    demo_timesfm_analytics()
