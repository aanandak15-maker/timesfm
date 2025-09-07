"""
Modern UI Components for AgriForecast.ai
Professional Agricultural Platform Components
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

class ModernUIComponents:
    """Modern UI Components for the agricultural platform"""
    
    @staticmethod
    def load_css():
        """Load the modern CSS framework"""
        with open('agriforecast_modern.css', 'r') as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    
    @staticmethod
    def render_header(user_name: str = "User"):
        """Render modern header with branding and navigation"""
        header_html = f"""
        <div class="ag-header">
            <div class="ag-header-content">
                <button class="ag-mobile-toggle" onclick="toggleMobileMenu()">☰</button>
                <a href="#" class="ag-logo">
                    🌾 AgriForecast.ai
                </a>
                <div class="ag-nav">
                    <a href="#" class="ag-nav-item">📊 Dashboard</a>
                    <a href="#" class="ag-nav-item">🌾 Fields</a>
                    <a href="#" class="ag-nav-item">🔮 AI Forecast</a>
                    <a href="#" class="ag-nav-item">📈 Analytics</a>
                </div>
                <div class="ag-user-menu">
                    <span>👤</span>
                    <span>{user_name}</span>
                    <span>▼</span>
                </div>
            </div>
        </div>
        <div class="ag-mobile-overlay" id="mobileOverlay" onclick="closeMobileMenu()"></div>
        <script>
        function toggleMobileMenu() {{
            const sidebar = document.querySelector('.ag-sidebar');
            const overlay = document.getElementById('mobileOverlay');
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
        }}
        function closeMobileMenu() {{
            const sidebar = document.querySelector('.ag-sidebar');
            const overlay = document.getElementById('mobileOverlay');
            sidebar.classList.remove('open');
            overlay.classList.remove('open');
        }}
        </script>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_sidebar(navigation_items: List[Dict[str, str]], active_item: str = "Dashboard"):
        """Render modern sidebar navigation"""
        sidebar_html = '<div class="ag-sidebar"><div class="ag-sidebar-nav">'
        
        for item in navigation_items:
            icon = item.get('icon', '📊')
            title = item.get('title', 'Item')
            key = item.get('key', title.lower().replace(' ', '_'))
            is_active = 'active' if key == active_item else ''
            
            sidebar_html += f'''
            <a href="#" class="ag-sidebar-item {is_active}" data-key="{key}">
                <span>{icon}</span>
                <span>{title}</span>
            </a>
            '''
        
        sidebar_html += '</div></div>'
        st.markdown(sidebar_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_metric_card(title: str, value: str, change: Optional[str] = None, 
                          change_type: str = "neutral", icon: str = "📊"):
        """Render a modern metric card"""
        change_html = ""
        if change:
            change_class = f"ag-metric-change {change_type}"
            change_html = f'<div class="{change_class}">{change}</div>'
        
        card_html = f"""
        <div class="ag-metric ag-fade-in">
            <div class="ag-metric-value">{value}</div>
            <div class="ag-metric-label">{title}</div>
            {change_html}
        </div>
        """
        return card_html
    
    @staticmethod
    def render_dashboard_metrics(metrics: List[Dict[str, Any]]):
        """Render dashboard metrics grid"""
        st.markdown('<div class="ag-grid ag-grid-4">', unsafe_allow_html=True)
        
        for metric in metrics:
            title = metric.get('title', 'Metric')
            value = metric.get('value', '0')
            change = metric.get('change')
            change_type = metric.get('change_type', 'neutral')
            icon = metric.get('icon', '📊')
            
            card_html = ModernUIComponents.render_metric_card(
                title, value, change, change_type, icon
            )
            st.markdown(card_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_card(title: str, content: str, icon: str = "📊", 
                   subtitle: Optional[str] = None, actions: Optional[List[Dict]] = None):
        """Render a modern card component"""
        subtitle_html = f'<div class="ag-card-subtitle">{subtitle}</div>' if subtitle else ''
        
        actions_html = ""
        if actions:
            actions_html = '<div class="ag-card-actions">'
            for action in actions:
                label = action.get('label', 'Action')
                action_type = action.get('type', 'primary')
                actions_html += f'<button class="ag-btn ag-btn-{action_type}">{label}</button>'
            actions_html += '</div>'
        
        card_html = f"""
        <div class="ag-card ag-slide-up">
            <div class="ag-card-header">
                <div>
                    <h3 class="ag-card-title">
                        <span>{icon}</span>
                        {title}
                    </h3>
                    {subtitle_html}
                </div>
                {actions_html}
            </div>
            <div class="ag-card-content">
                {content}
            </div>
        </div>
        """
        return card_html
    
    @staticmethod
    def render_alert(message: str, alert_type: str = "info", icon: str = "ℹ️"):
        """Render modern alert component"""
        alert_html = f"""
        <div class="ag-alert ag-alert-{alert_type} ag-fade-in">
            <span>{icon}</span>
            <span>{message}</span>
        </div>
        """
        st.markdown(alert_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_status_indicator(status: str, label: str = ""):
        """Render status indicator"""
        status_html = f"""
        <div class="ag-status ag-status-{status}">
            <span>●</span>
            <span>{label or status.title()}</span>
        </div>
        """
        return status_html
    
    @staticmethod
    def render_loading_spinner(message: str = "Loading..."):
        """Render loading spinner"""
        loading_html = f"""
        <div class="ag-loading">
            <div class="ag-spinner"></div>
            <div class="ag-mt-md">{message}</div>
        </div>
        """
        st.markdown(loading_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_api_status(api_name: str, status: str, message: str = ""):
        """Render API status indicator"""
        status_icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'loading': '🔄'
        }
        
        status_colors = {
            'success': 'ag-alert-success',
            'error': 'ag-alert-error',
            'warning': 'ag-alert-warning',
            'loading': 'ag-alert-info'
        }
        
        icon = status_icons.get(status, 'ℹ️')
        color_class = status_colors.get(status, 'ag-alert-info')
        
        status_html = f"""
        <div class="ag-alert {color_class}">
            <span>{icon}</span>
            <span><strong>{api_name}:</strong> {message or status.title()}</span>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_error_message(error: str, context: str = ""):
        """Render user-friendly error message"""
        error_html = f"""
        <div class="ag-alert ag-alert-error">
            <span>❌</span>
            <div>
                <strong>Error:</strong> {error}<br>
                {f'<small>Context: {context}</small>' if context else ''}
            </div>
        </div>
        """
        st.markdown(error_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_success_message(message: str):
        """Render success message"""
        success_html = f"""
        <div class="ag-alert ag-alert-success">
            <span>✅</span>
            <span>{message}</span>
        </div>
        """
        st.markdown(success_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_modern_chart(fig, title: str, height: int = 400):
        """Render chart with modern styling"""
        # Update chart styling
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=12),
            title=dict(
                font=dict(size=16, color='#212121'),
                x=0.05,
                xanchor='left'
            ),
            xaxis=dict(
                gridcolor='#E0E0E0',
                linecolor='#E0E0E0',
                tickfont=dict(color='#757575')
            ),
            yaxis=dict(
                gridcolor='#E0E0E0',
                linecolor='#E0E0E0',
                tickfont=dict(color='#757575')
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#E0E0E0',
                borderwidth=1
            )
        )
        
        # Render in modern container
        chart_html = f"""
        <div class="ag-chart-container ag-slide-up">
            <div class="ag-chart-title">
                <span>📊</span>
                <span>{title}</span>
            </div>
        </div>
        """
        st.markdown(chart_html, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, height=height)
    
    @staticmethod
    def render_modern_form(form_title: str, fields: List[Dict], submit_label: str = "Submit"):
        """Render modern form"""
        form_html = f"""
        <div class="ag-card ag-slide-up">
            <div class="ag-card-header">
                <h3 class="ag-card-title">
                    <span>📝</span>
                    {form_title}
                </h3>
            </div>
            <div class="ag-card-content">
        """
        
        for field in fields:
            field_type = field.get('type', 'text')
            field_name = field.get('name', 'field')
            field_label = field.get('label', field_name.title())
            field_placeholder = field.get('placeholder', f'Enter {field_label.lower()}')
            field_required = field.get('required', False)
            
            if field_type == 'select':
                options = field.get('options', [])
                options_html = ""
                for option in options:
                    options_html += f'<option value="{option}">{option}</option>'
                
                form_html += f"""
                <div class="ag-form-group">
                    <label class="ag-label">{field_label}</label>
                    <select class="ag-select" name="{field_name}" {"required" if field_required else ""}>
                        <option value="">Select {field_label}</option>
                        {options_html}
                    </select>
                </div>
                """
            else:
                form_html += f"""
                <div class="ag-form-group">
                    <label class="ag-label">{field_label}</label>
                    <input type="{field_type}" class="ag-input" name="{field_name}" 
                           placeholder="{field_placeholder}" {"required" if field_required else ""}>
                </div>
                """
        
        form_html += f"""
                <div class="ag-form-group">
                    <button type="submit" class="ag-btn ag-btn-primary">
                        <span>✓</span>
                        <span>{submit_label}</span>
                    </button>
                </div>
            </div>
        </div>
        """
        
        return form_html
    
    @staticmethod
    def render_data_table(data: pd.DataFrame, title: str = "Data Table"):
        """Render modern data table"""
        table_html = f"""
        <div class="ag-card ag-slide-up">
            <div class="ag-card-header">
                <h3 class="ag-card-title">
                    <span>📋</span>
                    {title}
                </h3>
            </div>
            <div class="ag-card-content">
                <table class="ag-table">
                    <thead>
                        <tr>
        """
        
        # Add headers
        for col in data.columns:
            table_html += f'<th>{col}</th>'
        
        table_html += '</tr></thead><tbody>'
        
        # Add data rows
        for _, row in data.head(10).iterrows():  # Limit to 10 rows for performance
            table_html += '<tr>'
            for value in row:
                table_html += f'<td>{value}</td>'
            table_html += '</tr>'
        
        table_html += '</tbody></table></div></div>'
        
        return table_html
    
    @staticmethod
    def render_weather_card(weather_data: Dict):
        """Render weather information card"""
        temp = weather_data.get('temperature', 'N/A')
        humidity = weather_data.get('humidity', 'N/A')
        condition = weather_data.get('condition', 'N/A')
        wind = weather_data.get('wind_speed', 'N/A')
        
        weather_html = f"""
        <div class="ag-card ag-slide-up">
            <div class="ag-card-header">
                <h3 class="ag-card-title">
                    <span>🌤️</span>
                    Current Weather
                </h3>
            </div>
            <div class="ag-card-content">
                <div class="ag-grid ag-grid-2">
                    <div class="ag-metric">
                        <div class="ag-metric-value">{temp}°C</div>
                        <div class="ag-metric-label">Temperature</div>
                    </div>
                    <div class="ag-metric">
                        <div class="ag-metric-value">{humidity}%</div>
                        <div class="ag-metric-label">Humidity</div>
                    </div>
                    <div class="ag-metric">
                        <div class="ag-metric-value">{condition}</div>
                        <div class="ag-metric-label">Condition</div>
                    </div>
                    <div class="ag-metric">
                        <div class="ag-metric-value">{wind} km/h</div>
                        <div class="ag-metric-label">Wind Speed</div>
                    </div>
                </div>
            </div>
        </div>
        """
        return weather_html
    
    @staticmethod
    def render_field_card(field_data: Dict):
        """Render field information card"""
        name = field_data.get('name', 'Unknown Field')
        crop = field_data.get('crop', 'Unknown Crop')
        area = field_data.get('area_acres', 0)
        status = field_data.get('status', 'active')
        yield_estimate = field_data.get('yield_estimate', 'N/A')
        
        status_indicator = ModernUIComponents.render_status_indicator(status)
        
        field_html = f"""
        <div class="ag-card ag-slide-up">
            <div class="ag-card-header">
                <h3 class="ag-card-title">
                    <span>🌾</span>
                    {name}
                </h3>
                {status_indicator}
            </div>
            <div class="ag-card-content">
                <div class="ag-grid ag-grid-2">
                    <div>
                        <strong>Crop:</strong> {crop}<br>
                        <strong>Area:</strong> {area} acres<br>
                        <strong>Yield Estimate:</strong> {yield_estimate}
                    </div>
                    <div class="ag-text-right">
                        <button class="ag-btn ag-btn-outline ag-mb-sm">View Details</button><br>
                        <button class="ag-btn ag-btn-ghost">Edit Field</button>
                    </div>
                </div>
            </div>
        </div>
        """
        return field_html

# Navigation items for the sidebar
NAVIGATION_ITEMS = [
    {"icon": "🏠", "title": "Dashboard", "key": "dashboard"},
    {"icon": "🌾", "title": "Field Management", "key": "fields"},
    {"icon": "🔮", "title": "AI Forecasting", "key": "forecasting"},
    {"icon": "🌤️", "title": "Weather", "key": "weather"},
    {"icon": "🌱", "title": "Crop Management", "key": "crops"},
    {"icon": "📊", "title": "Analytics", "key": "analytics"},
    {"icon": "📈", "title": "Market Intelligence", "key": "market"},
    {"icon": "🌐", "title": "IoT Integration", "key": "iot"},
    {"icon": "📋", "title": "Reports", "key": "reports"},
    {"icon": "⚙️", "title": "Settings", "key": "settings"}
]

# Sample dashboard metrics
SAMPLE_METRICS = [
    {"title": "Total Fields", "value": "4", "change": "+1 this month", "change_type": "positive", "icon": "🌾"},
    {"title": "Active Crops", "value": "3", "change": "2 planted", "change_type": "positive", "icon": "🌱"},
    {"title": "Avg Yield", "value": "3.2t/ha", "change": "+0.3t/ha", "change_type": "positive", "icon": "📈"},
    {"title": "Market Price", "value": "$4.17", "change": "+$0.12", "change_type": "positive", "icon": "💰"}
]
