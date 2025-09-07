"""
AgriForecast.ai - Love at First Sight Platform
Designed for instant user engagement and clarity
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import hashlib
import numpy as np
from typing import Dict, List, Optional

# Import real data service
from real_data_service import real_data_service

class LoveAtFirstSightPlatform:
    """Platform designed for instant user love and engagement"""
    
    def __init__(self):
        self.db_path = "agriforecast_love.db"
        self.init_database()
        
    def init_database(self):
        """Initialize simple database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Fields table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                crop_type TEXT,
                area_acres REAL NOT NULL,
                latitude REAL,
                longitude REAL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str, full_name: str = "") -> bool:
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, full_name))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        """Verify user credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, username, email, full_name FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3]
            }
        return None
    
    def get_user_fields(self, user_id: int) -> List[Dict]:
        """Get all fields for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, crop_type, area_acres, latitude, longitude, status, created_at
            FROM fields WHERE user_id = ?
        ''', (user_id,))
        fields = []
        for row in cursor.fetchall():
            fields.append({
                'id': row[0],
                'name': row[1],
                'crop_type': row[2],
                'area_acres': row[3],
                'latitude': row[4],
                'longitude': row[5],
                'status': row[6],
                'created_at': row[7]
            })
        conn.close()
        return fields
    
    def create_field(self, user_id: int, name: str, crop_type: str, area_acres: float, 
                    latitude: float = None, longitude: float = None) -> int:
        """Create a new field"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO fields (user_id, name, crop_type, area_acres, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, name, crop_type, area_acres, latitude, longitude))
        field_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return field_id
    
    def load_modern_css(self):
        """Load modern CSS for love at first sight"""
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Main container */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
            color: white;
            padding: 60px 40px;
            border-radius: 20px;
            margin: 20px 0;
            text-align: center;
            box-shadow: 0 20px 60px rgba(46, 125, 50, 0.3);
        }
        
        .hero-title {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 20px;
            line-height: 1.2;
        }
        
        .hero-subtitle {
            font-size: 20px;
            font-weight: 400;
            margin-bottom: 40px;
            opacity: 0.9;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .hero-metrics {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }
        
        .hero-metric {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .hero-metric-value {
            font-size: 32px;
            font-weight: 700;
            display: block;
        }
        
        .hero-metric-label {
            font-size: 14px;
            opacity: 0.8;
            margin-top: 5px;
        }
        
        .hero-cta {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        /* Navigation */
        .nav-container {
            background: white;
            border-radius: 15px;
            padding: 15px 30px;
            margin: 20px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 20px;
            text-decoration: none;
            color: #333;
            border-radius: 10px;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .nav-item:hover {
            background: #f0f9f0;
            color: #2E7D32;
            transform: translateY(-2px);
        }
        
        .nav-item.active {
            background: #2E7D32;
            color: white;
        }
        
        .nav-icon {
            font-size: 20px;
        }
        
        /* Dashboard Cards */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .dashboard-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            border: 1px solid #f0f0f0;
            transition: all 0.3s ease;
        }
        
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .card-icon {
            font-size: 32px;
            padding: 15px;
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            border-radius: 12px;
            color: white;
        }
        
        .card-title {
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin: 0;
        }
        
        .card-subtitle {
            font-size: 14px;
            color: #666;
            margin: 5px 0 0 0;
        }
        
        /* Alert Cards */
        .alert-card {
            background: linear-gradient(135deg, #fff3e0, #ffe0b2);
            border-left: 5px solid #FF9800;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .alert-urgent {
            background: linear-gradient(135deg, #ffebee, #ffcdd2);
            border-left-color: #f44336;
        }
        
        .alert-success {
            background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
            border-left-color: #4caf50;
        }
        
        .alert-icon {
            font-size: 24px;
        }
        
        .alert-content {
            flex: 1;
        }
        
        .alert-title {
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .alert-message {
            color: #666;
            font-size: 14px;
        }
        
        /* Quick Actions */
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .quick-action {
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .quick-action:hover {
            transform: translateY(-5px);
            border-color: #2E7D32;
            box-shadow: 0 8px 30px rgba(46, 125, 50, 0.2);
        }
        
        .quick-action-icon {
            font-size: 48px;
            margin-bottom: 15px;
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .quick-action-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }
        
        .quick-action-desc {
            font-size: 14px;
            color: #666;
        }
        
        /* Buttons */
        .btn-primary {
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(46, 125, 50, 0.3);
        }
        
        .btn-secondary {
            background: transparent;
            color: white;
            border: 2px solid white;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn-secondary:hover {
            background: white;
            color: #2E7D32;
            transform: translateY(-2px);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 32px;
            }
            
            .hero-subtitle {
                font-size: 16px;
            }
            
            .hero-metrics {
                gap: 20px;
            }
            
            .nav-container {
                gap: 20px;
            }
            
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .quick-actions {
                grid-template-columns: 1fr;
            }
        }
        
        /* Loading Animation */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #2E7D32;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Success Animation */
        .success-message {
            background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
            color: #2e7d32;
            padding: 15px 20px;
            border-radius: 10px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_hero_section(self):
        """Render compelling hero section"""
        st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">🌾 Your Farm's Future is Clear</h1>
            <p class="hero-subtitle">Get weather alerts, yield predictions, and market insights in one simple dashboard</p>
            
            <div class="hero-metrics">
                <div class="hero-metric">
                    <span class="hero-metric-value">📈 25%</span>
                    <span class="hero-metric-label">Higher Yields</span>
                </div>
                <div class="hero-metric">
                    <span class="hero-metric-value">💰 $2,500</span>
                    <span class="hero-metric-label">Saved per Season</span>
                </div>
                <div class="hero-metric">
                    <span class="hero-metric-value">⚡ 2 min</span>
                    <span class="hero-metric-label">Daily Check</span>
                </div>
            </div>
            
            <div class="hero-cta">
                <a href="#" class="btn-primary">🚀 Start Free Trial</a>
                <a href="#" class="btn-secondary">📺 See How It Works</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_simple_navigation(self, active_page="home"):
        """Render simplified 4-item navigation"""
        nav_items = [
            {"key": "home", "icon": "🏠", "label": "Home", "desc": "Overview & alerts"},
            {"key": "fields", "icon": "🌾", "label": "My Fields", "desc": "Field management"},
            {"key": "predictions", "icon": "🔮", "label": "Predictions", "desc": "Weather & forecasts"},
            {"key": "insights", "icon": "📊", "label": "Insights", "desc": "Reports & analytics"}
        ]
        
        nav_html = '<div class="nav-container">'
        for item in nav_items:
            active_class = "active" if item["key"] == active_page else ""
            nav_html += f'''
            <div class="nav-item {active_class}" onclick="window.location.href='?page={item["key"]}'">
                <span class="nav-icon">{item["icon"]}</span>
                <div>
                    <div>{item["label"]}</div>
                    <small style="opacity: 0.7;">{item["desc"]}</small>
                </div>
            </div>
            '''
        nav_html += '</div>'
        
        st.markdown(nav_html, unsafe_allow_html=True)
        
        # Handle page navigation
        query_params = st.query_params
        if "page" in query_params:
            return query_params["page"]
        return active_page
    
    def render_key_alerts(self):
        """Render top 3 key alerts"""
        # Get sample alerts (in real app, these would be dynamic)
        alerts = [
            {
                "type": "urgent",
                "icon": "🌧️",
                "title": "Rain Expected Tomorrow",
                "message": "Delay irrigation for Field 1. 15mm rainfall predicted.",
                "action": "View Weather"
            },
            {
                "type": "success", 
                "icon": "📈",
                "title": "Rice Prices Rising",
                "message": "Market price up 5% this week. Good time to consider selling.",
                "action": "Check Market"
            },
            {
                "type": "normal",
                "icon": "🌱",
                "title": "Fertilizer Reminder",
                "message": "Field 2 (Corn) is due for nitrogen fertilizer application.",
                "action": "View Field"
            }
        ]
        
        st.markdown("### 🚨 Today's Key Alerts")
        
        for alert in alerts:
            alert_class = f"alert-{alert['type']}" if alert['type'] != 'normal' else ''
            st.markdown(f"""
            <div class="alert-card {alert_class}">
                <div class="alert-icon">{alert['icon']}</div>
                <div class="alert-content">
                    <div class="alert-title">{alert['title']}</div>
                    <div class="alert-message">{alert['message']}</div>
                </div>
                <button class="btn-primary" style="padding: 8px 16px; font-size: 14px;">{alert['action']}</button>
            </div>
            """, unsafe_allow_html=True)
    
    def render_quick_actions(self):
        """Render 3 main quick actions"""
        st.markdown("### ⚡ Quick Actions")
        
        actions = [
            {
                "icon": "➕",
                "title": "Add New Field",
                "desc": "Monitor your crops and get insights",
                "action": "add_field"
            },
            {
                "icon": "🔮",
                "title": "Check Predictions",
                "desc": "Weather forecasts and yield estimates",
                "action": "predictions"
            },
            {
                "icon": "📊",
                "title": "View Insights",
                "desc": "Farm performance and analytics",
                "action": "insights"
            }
        ]
        
        st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, action in enumerate(actions):
            with cols[i]:
                if st.button(f"{action['icon']}\n{action['title']}\n{action['desc']}", key=f"action_{i}"):
                    if action['action'] == 'add_field':
                        st.session_state.show_add_field = True
                    elif action['action'] == 'predictions':
                        st.session_state.page = 'predictions'
                    elif action['action'] == 'insights':
                        st.session_state.page = 'insights'
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_field_overview(self, user_id: int):
        """Render simple field overview"""
        fields = self.get_user_fields(user_id)
        
        st.markdown("### 🌾 Your Fields")
        
        if not fields:
            st.markdown("""
            <div class="dashboard-card" style="text-align: center; padding: 40px;">
                <div style="font-size: 48px; margin-bottom: 20px;">🌾</div>
                <h3>No Fields Yet</h3>
                <p style="color: #666;">Add your first field to start getting insights and predictions.</p>
                <button class="btn-primary" onclick="document.querySelector('[data-testid=\"add-field-btn\"]').click()">
                    ➕ Add Your First Field
                </button>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Display fields in a clean grid
        cols = st.columns(min(len(fields), 3))
        
        for i, field in enumerate(fields):
            with cols[i % 3]:
                # Get weather data for field
                lat = field.get('latitude', 28.368911)
                lon = field.get('longitude', 77.541033)
                weather = real_data_service.get_real_weather(lat, lon)
                
                st.markdown(f"""
                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-icon">🌾</div>
                        <div>
                            <div class="card-title">{field['name']}</div>
                            <div class="card-subtitle">{field['crop_type']} • {field['area_acres']} acres</div>
                        </div>
                    </div>
                    <div style="margin-top: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span>🌡️ Temperature</span>
                            <strong>{weather['temperature']}°C</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span>💧 Humidity</span>
                            <strong>{weather['humidity']}%</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                            <span>🌤️ Condition</span>
                            <strong>{weather['condition']}</strong>
                        </div>
                        <button class="btn-primary" style="width: 100%; padding: 10px; font-size: 14px;">
                            View Details
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    def render_add_field_form(self, user_id: int):
        """Render simplified add field form"""
        st.markdown("### ➕ Add New Field")
        
        with st.form("add_field_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                field_name = st.text_input("Field Name", placeholder="e.g., North Field")
                crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Corn", "Soybean", "Cotton", "Other"])
                area_acres = st.number_input("Area (acres)", min_value=0.1, value=1.0, step=0.1)
            
            with col2:
                latitude = st.number_input("Latitude", value=28.368911, format="%.6f")
                longitude = st.number_input("Longitude", value=77.541033, format="%.6f")
                st.info("💡 Use your field's GPS coordinates for accurate weather data")
            
            col_submit, col_cancel = st.columns([1, 1])
            
            with col_submit:
                if st.form_submit_button("🌾 Add Field", use_container_width=True):
                    if field_name and area_acres:
                        field_id = self.create_field(user_id, field_name, crop_type, area_acres, latitude, longitude)
                        st.success(f"✅ Field '{field_name}' added successfully!")
                        st.balloons()
                        st.session_state.show_add_field = False
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields")
            
            with col_cancel:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.show_add_field = False
                    st.rerun()
    
    def render_home_page(self, user: Dict):
        """Render the main home page"""
        # Key alerts
        self.render_key_alerts()
        
        # Quick actions
        self.render_quick_actions()
        
        # Field overview
        self.render_field_overview(user['id'])
        
        # Add field form (if requested)
        if st.session_state.get('show_add_field', False):
            self.render_add_field_form(user['id'])
    
    def render_predictions_page(self, user: Dict):
        """Render predictions page"""
        st.markdown("### 🔮 Predictions & Forecasts")
        
        fields = self.get_user_fields(user['id'])
        
        if not fields:
            st.info("Add fields to see predictions")
            return
        
        # Field selection
        field_names = [f"{field['name']} ({field['crop_type']})" for field in fields]
        selected_idx = st.selectbox("Select Field", range(len(field_names)), format_func=lambda x: field_names[x])
        
        if selected_idx is not None:
            selected_field = fields[selected_idx]
            lat = selected_field.get('latitude', 28.368911)
            lon = selected_field.get('longitude', 77.541033)
            
            # Get weather forecast
            forecast = real_data_service.get_weather_forecast(lat, lon, 5)
            
            # Weather forecast chart
            dates = [f["date"] for f in forecast]
            temps = [f["temperature"] for f in forecast]
            humidity = [f["humidity"] for f in forecast]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=temps, mode='lines+markers', name='Temperature (°C)', line=dict(color='#FF6B6B', width=3)))
            fig.add_trace(go.Scatter(x=dates, y=humidity, mode='lines+markers', name='Humidity (%)', yaxis='y2', line=dict(color='#4ECDC4', width=3)))
            
            fig.update_layout(
                title="5-Day Weather Forecast",
                xaxis_title="Date",
                yaxis_title="Temperature (°C)",
                yaxis2=dict(title="Humidity (%)", overlaying='y', side='right'),
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Market prices
            st.markdown("### 💰 Market Insights")
            
            crop_type = selected_field['crop_type'].upper()
            market_data = real_data_service.get_market_prices(crop_type)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"${market_data['price']:.2f}", f"{market_data['change']:+.2f}")
            with col2:
                st.metric("Change %", f"{market_data['change_percent']:+.1f}%")
            with col3:
                st.metric("Recommendation", "HOLD" if abs(market_data['change_percent']) < 3 else ("SELL" if market_data['change_percent'] > 0 else "WAIT"))
    
    def render_insights_page(self, user: Dict):
        """Render insights page"""
        st.markdown("### 📊 Farm Insights")
        
        fields = self.get_user_fields(user['id'])
        
        if not fields:
            st.info("Add fields to see insights")
            return
        
        # Farm overview metrics
        total_acres = sum(f['area_acres'] for f in fields)
        active_fields = len([f for f in fields if f['status'] == 'active'])
        crop_types = len(set(f['crop_type'] for f in fields))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Acres", f"{total_acres:.1f}")
        with col2:
            st.metric("Active Fields", active_fields)
        with col3:
            st.metric("Crop Types", crop_types)
        
        # Crop distribution chart
        crop_counts = {}
        for field in fields:
            crop = field['crop_type']
            crop_counts[crop] = crop_counts.get(crop, 0) + field['area_acres']
        
        if crop_counts:
            fig = go.Figure(data=[go.Pie(
                labels=list(crop_counts.keys()),
                values=list(crop_counts.values()),
                hole=0.4,
                marker_colors=['#2E7D32', '#4CAF50', '#8BC34A', '#CDDC39', '#FFC107']
            )])
            
            fig.update_layout(
                title="Crop Distribution by Area",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_login_page(self):
        """Render simple login page"""
        st.markdown("""
        <div style="max-width: 400px; margin: 100px auto; padding: 40px; background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2E7D32; margin: 0; font-size: 32px;">🌾 AgriForecast.ai</h1>
                <p style="color: #666; margin: 10px 0 0 0;">Your Smart Farming Assistant</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.form_submit_button("🚀 Sign In", use_container_width=True):
                    if username and password:
                        user = self.verify_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.authenticated = True
                            st.success("Welcome back!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    else:
                        st.error("Please enter username and password")
            
            with col2:
                if st.form_submit_button("📝 Register", use_container_width=True):
                    if username and password:
                        if self.create_user(username, f"{username}@farm.com", password, username.title()):
                            st.success("Account created! Please login.")
                        else:
                            st.error("Username already exists")
                    else:
                        st.error("Please enter username and password")
        
        # Quick login hint
        st.info("💡 Quick test: Username: 'demo', Password: 'demo'")
    
    def run(self):
        """Run the love at first sight platform"""
        # Page config
        st.set_page_config(
            page_title="AgriForecast.ai - Smart Farming",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Load modern CSS
        self.load_modern_css()
        
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'page' not in st.session_state:
            st.session_state.page = 'home'
        
        # Check authentication
        if not st.session_state.authenticated:
            self.render_login_page()
            return
        
        # Main app
        user = st.session_state.user
        
        # Hero section (only on home page)
        if st.session_state.page == 'home':
            self.render_hero_section()
        
        # Navigation
        active_page = self.render_simple_navigation(st.session_state.page)
        st.session_state.page = active_page
        
        # Main content
        if st.session_state.page == 'home':
            self.render_home_page(user)
        elif st.session_state.page == 'fields':
            self.render_home_page(user)  # Same as home for now
        elif st.session_state.page == 'predictions':
            self.render_predictions_page(user)
        elif st.session_state.page == 'insights':
            self.render_insights_page(user)
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 50px; padding: 20px; color: #666; border-top: 1px solid #eee;">
            <p>🌾 AgriForecast.ai - Making farming smarter, one field at a time</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main function"""
    platform = LoveAtFirstSightPlatform()
    platform.run()

if __name__ == "__main__":
    main()
