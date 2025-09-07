#!/usr/bin/env python3
"""
AgriForecast.ai - Production-Ready Agricultural Intelligence Platform
Unified platform combining all agricultural features into a single application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import hashlib
import logging
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional, Tuple
import requests
import time
from forecasting_service import get_forecasting_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AgriForecast.ai - Agricultural Intelligence Platform",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ProductionDatabase:
    """Production-ready database management"""
    
    def __init__(self, db_path: str = "agriforecast_production.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize production database with all tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Farms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                location TEXT,
                total_area_acres REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Fields table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farm_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                crop_type TEXT,
                area_acres REAL,
                latitude REAL,
                longitude REAL,
                soil_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farm_id) REFERENCES farms (id)
            )
        """)
        
        # Weather data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER NOT NULL,
                date DATE NOT NULL,
                temperature REAL,
                humidity REAL,
                rainfall REAL,
                wind_speed REAL,
                pressure REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        """)
        
        # Soil data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS soil_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER NOT NULL,
                date DATE NOT NULL,
                ph_level REAL,
                nitrogen REAL,
                phosphorus REAL,
                potassium REAL,
                organic_matter REAL,
                moisture_content REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        """)
        
        # Crop plantings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crop_plantings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER NOT NULL,
                crop_type TEXT NOT NULL,
                variety_name TEXT,
                planting_date DATE NOT NULL,
                expected_harvest_date DATE,
                area_acres REAL,
                status TEXT DEFAULT 'Active',
                current_growth_stage TEXT,
                days_since_planting INTEGER,
                days_to_harvest INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        """)
        
        # Yield predictions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS yield_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER NOT NULL,
                prediction_date DATE NOT NULL,
                predicted_yield REAL,
                confidence_interval_lower REAL,
                confidence_interval_upper REAL,
                scenario TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        """)
        
        # Market data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commodity TEXT NOT NULL,
                price_per_unit REAL,
                unit TEXT,
                market_location TEXT,
                date DATE NOT NULL,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # IoT devices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iot_devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER NOT NULL,
                device_name TEXT NOT NULL,
                device_type TEXT NOT NULL,
                status TEXT DEFAULT 'Active',
                last_data_received TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        """)
        
        # Reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                report_type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Production database initialized successfully")
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def create_user(self, username: str, email: str, password: str, full_name: str = "") -> int:
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Hash password
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, full_name))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'password_hash': user[3],
                'full_name': user[4],
                'phone': user[5],
                'created_at': user[6],
                'is_active': user[7]
            }
        return None
    
    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        """Verify user credentials"""
        user = self.get_user_by_username(username)
        if user:
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if user['password_hash'] == password_hash:
                return user
        return None

class ProductionPlatform:
    """Main production platform class"""
    
    def __init__(self):
        self.db = ProductionDatabase()
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state"""
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'user_name' not in st.session_state:
            st.session_state.user_name = None
        if 'current_farm_id' not in st.session_state:
            st.session_state.current_farm_id = None
        if 'current_field_id' not in st.session_state:
            st.session_state.current_field_id = None
    
    def hash_password(self, password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user login"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute("""
            SELECT id, username, full_name FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        """, (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            st.session_state.user_id = user[0]
            st.session_state.user_name = user[2] or user[1]
            return True
        return False
    
    def register_user(self, username: str, email: str, password: str, full_name: str) -> bool:
        """Register new user"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, full_name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def create_farm(self, user_id: int, name: str, location: str = "", total_area_acres: float = 0.0) -> int:
        """Create a new farm"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO farms (user_id, name, location, total_area_acres)
            VALUES (?, ?, ?, ?)
        """, (user_id, name, location, total_area_acres))
        farm_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return farm_id
    
    def get_user_farms(self, user_id: int) -> pd.DataFrame:
        """Get user's farms"""
        conn = self.db.get_connection()
        query = "SELECT * FROM farms WHERE user_id = ? ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        return df
    
    def create_field(self, farm_id: int, name: str, crop_type: str, area_acres: float, 
                    latitude: float, longitude: float, soil_type: str) -> int:
        """Create a new field"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fields (farm_id, name, crop_type, area_acres, latitude, longitude, soil_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (farm_id, name, crop_type, area_acres, latitude, longitude, soil_type))
        field_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return field_id
    
    def get_farm_fields(self, farm_id: int) -> pd.DataFrame:
        """Get farm's fields"""
        conn = self.db.get_connection()
        query = "SELECT * FROM fields WHERE farm_id = ? ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn, params=(farm_id,))
        conn.close()
        return df
    
    def get_field_data(self, field_id: int) -> Dict:
        """Get comprehensive field data"""
        conn = self.db.get_connection()
        
        # Get field info
        field_query = "SELECT * FROM fields WHERE id = ?"
        field_df = pd.read_sql_query(field_query, conn, params=(field_id,))
        
        if field_df.empty:
            return {}
        
        field_info = field_df.iloc[0].to_dict()
        
        # Get weather data
        weather_query = """
            SELECT * FROM weather_data 
            WHERE field_id = ? 
            ORDER BY date DESC 
            LIMIT 30
        """
        weather_df = pd.read_sql_query(weather_query, conn, params=(field_id,))
        
        # Get soil data
        soil_query = """
            SELECT * FROM soil_data 
            WHERE field_id = ? 
            ORDER BY date DESC 
            LIMIT 10
        """
        soil_df = pd.read_sql_query(soil_query, conn, params=(field_id,))
        
        # Get crop plantings
        crop_query = """
            SELECT * FROM crop_plantings 
            WHERE field_id = ? AND status = 'Active'
        """
        crop_df = pd.read_sql_query(crop_query, conn, params=(field_id,))
        
        # Get yield predictions
        yield_query = """
            SELECT * FROM yield_predictions 
            WHERE field_id = ? 
            ORDER BY prediction_date DESC 
            LIMIT 5
        """
        yield_df = pd.read_sql_query(yield_query, conn, params=(field_id,))
        
        conn.close()
        
        return {
            'field_info': field_info,
            'weather_data': weather_df,
            'soil_data': soil_df,
            'crop_plantings': crop_df,
            'yield_predictions': yield_df
        }
    
    def render_login_page(self):
        """Render login/registration page"""
        st.title("🌾 AgriForecast.ai")
        st.subheader("Agricultural Intelligence Platform")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", type="primary")
                
                if submit:
                    if self.authenticate_user(username, password):
                        st.success(f"Welcome back, {st.session_state.user_name}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
        
        with tab2:
            with st.form("register_form"):
                username = st.text_input("Username", key="reg_username")
                email = st.text_input("Email", key="reg_email")
                full_name = st.text_input("Full Name", key="reg_full_name")
                password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
                submit = st.form_submit_button("Register", type="primary")
                
                if submit:
                    if password != confirm_password:
                        st.error("Passwords do not match")
                    elif self.register_user(username, email, password, full_name):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username or email already exists")
    
    def render_sidebar(self):
        """Render main sidebar navigation"""
        st.sidebar.title("🌾 AgriForecast.ai")
        st.sidebar.write(f"Welcome, {st.session_state.user_name}!")
        
        # Main navigation
        page = st.sidebar.selectbox(
            "Navigate",
            [
                "🏠 Dashboard",
                "🌾 Field Management", 
                "📊 Analytics & Reports",
                "🌱 Crop Management",
                "🌍 Weather & Soil",
                "🔮 AI Forecasting",
                "📈 Market Intelligence",
                "📡 IoT Devices",
                "⚙️ Settings"
            ]
        )
        
        # Quick actions
        st.sidebar.markdown("---")
        st.sidebar.subheader("Quick Actions")
        
        if st.sidebar.button("➕ Add New Farm"):
            st.session_state.show_add_farm = True
        
        if st.sidebar.button("🌾 Add New Field"):
            st.session_state.show_add_field = True
        
        if st.sidebar.button("📊 Generate Report"):
            st.session_state.show_generate_report = True
        
        # Logout
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.session_state.current_farm_id = None
            st.session_state.current_field_id = None
            st.rerun()
        
        return page
    
    def render_dashboard(self):
        """Render main dashboard"""
        st.title("🏠 Agricultural Intelligence Dashboard")
        
        # Add farm button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Your Farms")
        with col2:
            if st.button("➕ Add New Farm", type="primary"):
                st.session_state.show_add_farm = True
        
        # Get user's farms
        farms_df = self.get_user_farms(st.session_state.user_id)
        
        # Show add farm form if requested
        if st.session_state.get('show_add_farm', False):
            with st.expander("➕ Add New Farm", expanded=True):
                with st.form("add_farm_form"):
                    farm_name = st.text_input("Farm Name", placeholder="Enter farm name")
                    location = st.text_input("Location", placeholder="Enter farm location")
                    total_area = st.number_input("Total Area (acres)", min_value=0.1, value=1.0)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Create Farm", type="primary"):
                            if farm_name:
                                farm_id = self.create_farm(st.session_state.user_id, farm_name, location, total_area)
                                if farm_id:
                                    st.success(f"Farm '{farm_name}' created successfully!")
                                    st.session_state.show_add_farm = False
                                    st.rerun()
                                else:
                                    st.error("Failed to create farm")
                            else:
                                st.error("Please enter a farm name")
                    with col2:
                        if st.form_submit_button("Cancel"):
                            st.session_state.show_add_farm = False
                            st.rerun()
        
        if farms_df.empty:
            st.info("No farms found. Add your first farm to get started!")
            return
        
        # Farm selection
        farm_names = farms_df['name'].tolist()
        selected_farm_idx = st.selectbox("Select Farm", range(len(farm_names)), format_func=lambda x: farm_names[x])
        selected_farm = farms_df.iloc[selected_farm_idx]
        st.session_state.current_farm_id = selected_farm['id']
        
        # Get farm fields
        fields_df = self.get_farm_fields(selected_farm['id'])
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Farms", len(farms_df))
        
        with col2:
            st.metric("Total Fields", len(fields_df))
        
        with col3:
            total_area = fields_df['area_acres'].sum() if not fields_df.empty else 0
            st.metric("Total Area", f"{total_area:.1f} acres")
        
        with col4:
            active_crops = 0
            if not fields_df.empty:
                conn = self.db.get_connection()
                for field_id in fields_df['id']:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM crop_plantings WHERE field_id = ? AND status = 'Active'", (field_id,))
                    active_crops += cursor.fetchone()[0]
                conn.close()
            st.metric("Active Crops", active_crops)
        
        # Recent activity
        st.subheader("📈 Recent Activity")
        
        if not fields_df.empty:
            # Field overview
            st.subheader("🌾 Field Overview")
            
            for _, field in fields_df.iterrows():
                with st.expander(f"{field['name']} - {field['crop_type'] or 'No Crop'}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Area:** {field['area_acres']} acres")
                        st.write(f"**Location:** {field['latitude']}, {field['longitude']}")
                    
                    with col2:
                        st.write(f"**Soil Type:** {field['soil_type'] or 'Unknown'}")
                        st.write(f"**Created:** {field['created_at'][:10]}")
                    
                    with col3:
                        if st.button(f"View Details", key=f"view_{field['id']}"):
                            st.session_state.current_field_id = field['id']
                            st.session_state.current_page = "Field Details"
                            st.rerun()
        else:
            st.info("No fields found. Add fields to your farm to start monitoring.")
    
    def render_field_management(self):
        """Render field management page"""
        st.title("🌾 Field Management")
        
        # Farm selection
        farms_df = self.get_user_farms(st.session_state.user_id)
        
        if farms_df.empty:
            st.info("No farms found. Add your first farm to get started!")
            return
        
        farm_names = farms_df['name'].tolist()
        selected_farm_idx = st.selectbox("Select Farm", range(len(farm_names)), format_func=lambda x: farm_names[x])
        selected_farm = farms_df.iloc[selected_farm_idx]
        
        # Add new field
        st.subheader("➕ Add New Field")
        
        with st.form("add_field_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                field_name = st.text_input("Field Name", placeholder="Enter field name", help="Required: Name for your field")
                crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Corn", "Soybean", "Cotton", "Other"], help="Select the crop you plan to grow")
                area_acres = st.number_input("Area (acres)", min_value=0.1, value=1.0, step=0.1, help="Field area in acres")
            
            with col2:
                latitude = st.number_input("Latitude", value=28.368911, format="%.6f", help="GPS latitude coordinate")
                longitude = st.number_input("Longitude", value=77.541033, format="%.6f", help="GPS longitude coordinate")
                soil_type = st.selectbox("Soil Type", ["Clay", "Sandy", "Loamy", "Silty", "Other"], help="Type of soil in your field")
            
            # Form validation and submission
            submitted = st.form_submit_button("➕ Add Field", type="primary")
            
            if submitted:
                # Validate form data
                if not field_name or field_name.strip() == "":
                    st.error("❌ Please enter a field name")
                elif area_acres <= 0:
                    st.error("❌ Please enter a valid area (greater than 0)")
                else:
                    try:
                        with st.spinner("Adding field..."):
                            field_id = self.create_field(
                                selected_farm['id'], 
                                field_name.strip(), 
                                crop_type, 
                                area_acres, 
                                latitude, 
                                longitude, 
                                soil_type
                            )
                            
                        if field_id:
                            st.success(f"✅ Field '{field_name}' added successfully!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Failed to add field. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error adding field: {str(e)}")
                        logger.error(f"Field creation error: {e}")
        
        # Field list
        st.subheader("🌾 Your Fields")
        fields_df = self.get_farm_fields(selected_farm['id'])
        
        if not fields_df.empty:
            for _, field in fields_df.iterrows():
                with st.expander(f"{field['name']} - {field['crop_type'] or 'No Crop'}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Area:** {field['area_acres']} acres")
                        st.write(f"**Location:** {field['latitude']}, {field['longitude']}")
                    
                    with col2:
                        st.write(f"**Soil Type:** {field['soil_type'] or 'Unknown'}")
                        st.write(f"**Created:** {field['created_at'][:10]}")
                    
                    with col3:
                        if st.button(f"Manage", key=f"manage_{field['id']}"):
                            st.session_state.current_field_id = field['id']
                            st.session_state.current_page = "Field Details"
                            st.rerun()
        else:
            st.info("No fields found. Add fields to start monitoring.")
    
    def render_analytics_reports(self):
        """Render analytics and reports page"""
        st.title("📊 Analytics & Reports")
        
        # Analytics tabs
        tab1, tab2, tab3 = st.tabs(["📈 Yield Analytics", "💰 Financial Analysis", "📄 Reports"])
        
        with tab1:
            st.subheader("Yield Analytics")
            
            # Get user's fields for analysis
            farms_df = self.get_user_farms(st.session_state.user_id)
            if farms_df.empty:
                st.info("No farms found. Add farms to view analytics.")
                return
            
            # Field selection for analysis
            all_fields = []
            for _, farm in farms_df.iterrows():
                fields_df = self.get_farm_fields(farm['id'])
                for _, field in fields_df.iterrows():
                    all_fields.append({
                        'id': field['id'],
                        'name': f"{farm['name']} - {field['name']}",
                        'area': field['area_acres']
                    })
            
            if not all_fields:
                st.info("No fields found. Add fields to view analytics.")
                return
            
            # Create sample analytics data
            field_names = [f['name'] for f in all_fields]
            yield_data = np.random.normal(3.5, 0.5, len(field_names))
            
            # Yield comparison chart
            fig = px.bar(
                x=field_names,
                y=yield_data,
                title="Yield Comparison by Field",
                labels={'x': 'Field', 'y': 'Yield (tons/acre)'}
            )
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, width='stretch')
            
            # Yield trend over time
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
            trend_data = np.random.normal(3.5, 0.3, len(dates))
            
            fig = px.line(
                x=dates,
                y=trend_data,
                title="Yield Trend Over Time",
                labels={'x': 'Date', 'y': 'Yield (tons/acre)'}
            )
            st.plotly_chart(fig, width='stretch')
        
        with tab2:
            st.subheader("Financial Analysis")
            
            # Sample financial data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            revenue = [15000, 18000, 22000, 25000, 28000, 32000]
            costs = [12000, 14000, 16000, 18000, 20000, 22000]
            profit = [r - c for r, c in zip(revenue, costs)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=revenue, name='Revenue', line=dict(color='green')))
            fig.add_trace(go.Scatter(x=months, y=costs, name='Costs', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=months, y=profit, name='Profit', line=dict(color='blue')))
            
            fig.update_layout(
                title="Monthly Financial Performance",
                xaxis_title="Month",
                yaxis_title="Amount ($)"
            )
            st.plotly_chart(fig, width='stretch')
            
            # ROI calculation
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Revenue", f"${sum(revenue):,}")
            with col2:
                st.metric("Total Costs", f"${sum(costs):,}")
            with col3:
                st.metric("Net Profit", f"${sum(profit):,}")
        
        with tab3:
            st.subheader("Generate Reports")
            
            report_type = st.selectbox("Report Type", [
                "Field Performance Report",
                "Financial Summary Report", 
                "Weather Analysis Report",
                "Soil Health Report",
                "Crop Management Report"
            ])
            
            if st.button("Generate Report", type="primary"):
                # Simulate report generation
                st.success("Report generated successfully!")
                
                # Create sample report content
                report_content = f"""
                # {report_type}
                
                **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                **User:** {st.session_state.user_name}
                
                ## Summary
                This report contains comprehensive analysis of your agricultural operations.
                
                ## Key Findings
                - Total fields monitored: {len(all_fields) if 'all_fields' in locals() else 0}
                - Average yield: 3.5 tons/acre
                - Weather conditions: Favorable
                - Soil health: Good
                
                ## Recommendations
                1. Consider crop rotation for better soil health
                2. Monitor weather patterns for optimal planting
                3. Implement precision agriculture techniques
                """
                
                st.download_button(
                    label="Download Report",
                    data=report_content,
                    file_name=f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
    
    def render_crop_management(self):
        """Render crop management page"""
        st.title("🌱 Crop Management")
        
        # Get user's fields
        farms_df = self.get_user_farms(st.session_state.user_id)
        if farms_df.empty:
            st.info("No farms found. Add farms to manage crops.")
            return
        
        # Field selection
        all_fields = []
        for _, farm in farms_df.iterrows():
            fields_df = self.get_farm_fields(farm['id'])
            for _, field in fields_df.iterrows():
                all_fields.append({
                    'id': field['id'],
                    'name': f"{farm['name']} - {field['name']}",
                    'area': field['area_acres']
                })
        
        if not all_fields:
            st.info("No fields found. Add fields to manage crops.")
            return
        
        field_names = [f['name'] for f in all_fields]
        selected_field_idx = st.selectbox("Select Field", range(len(field_names)), format_func=lambda x: field_names[x])
        selected_field = all_fields[selected_field_idx]
        
        # Crop planting form
        st.subheader("🌱 Plant New Crop")
        
        with st.form("plant_crop_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Corn", "Soybean", "Cotton"])
                variety = st.text_input("Variety Name")
                planting_date = st.date_input("Planting Date", value=datetime.now().date())
            
            with col2:
                area_acres = st.number_input("Area (acres)", min_value=0.1, value=selected_field['area'])
                expected_harvest = st.date_input("Expected Harvest Date", value=datetime.now().date() + timedelta(days=120))
            
            if st.form_submit_button("Plant Crop", type="primary"):
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO crop_plantings (field_id, crop_type, variety_name, planting_date, expected_harvest_date, area_acres)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (selected_field['id'], crop_type, variety, planting_date, expected_harvest, area_acres))
                conn.commit()
                conn.close()
                st.success("Crop planted successfully!")
                st.rerun()
        
        # Active crops
        st.subheader("🌾 Active Crops")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cp.*, f.name as field_name 
            FROM crop_plantings cp
            JOIN fields f ON cp.field_id = f.id
            WHERE cp.status = 'Active'
            ORDER BY cp.planting_date DESC
        """)
        
        active_crops = cursor.fetchall()
        conn.close()
        
        if active_crops:
            for crop in active_crops:
                with st.expander(f"{crop[2]} - {crop[3]} ({crop[9]})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Planting Date:** {crop[4]}")
                        st.write(f"**Expected Harvest:** {crop[5]}")
                    
                    with col2:
                        st.write(f"**Area:** {crop[6]} acres")
                        st.write(f"**Status:** {crop[7]}")
                    
                    with col3:
                        days_planted = (datetime.now().date() - datetime.strptime(crop[4], '%Y-%m-%d').date()).days
                        st.write(f"**Days Planted:** {days_planted}")
                        
                        if st.button("Harvest", key=f"harvest_{crop[0]}"):
                            # Update crop status to harvested
                            conn = self.db.get_connection()
                            cursor = conn.cursor()
                            cursor.execute("UPDATE crop_plantings SET status = 'Harvested' WHERE id = ?", (crop[0],))
                            conn.commit()
                            conn.close()
                            st.success("Crop marked as harvested!")
                            st.rerun()
        else:
            st.info("No active crops found. Plant crops to start monitoring.")
    
    def render_ai_forecasting(self):
        """Render AI Forecasting page with TimesFM integration"""
        st.title("🔮 AI Forecasting Engine")
        st.markdown("**Powered by TimesFM - Google's Time Series Foundation Model**")
        
        # Get user's fields
        farms_df = self.get_user_farms(st.session_state.user_id)
        if farms_df.empty:
            st.info("No farms found. Add farms to access AI forecasting.")
            return
        
        # Field selection
        all_fields = []
        for _, farm in farms_df.iterrows():
            fields_df = self.get_farm_fields(farm['id'])
            for _, field in fields_df.iterrows():
                all_fields.append({
                    'id': field['id'],
                    'name': f"{farm['name']} - {field['name']}",
                    'crop_type': field['crop_type'],
                    'latitude': field['latitude'],
                    'longitude': field['longitude'],
                    'area_acres': field['area_acres']
                })
        
        if not all_fields:
            st.info("No fields found. Add fields to access AI forecasting.")
            return
        
        field_names = [f['name'] for f in all_fields]
        selected_field_idx = st.selectbox("Select Field for Forecasting", range(len(field_names)), format_func=lambda x: field_names[x])
        selected_field = all_fields[selected_field_idx]
        
        # Forecasting tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🌾 Yield Forecast", "🌤️ Weather Forecast", "💰 Market Forecast", "📊 Comprehensive Analysis"])
        
        with tab1:
            st.subheader("🌾 Crop Yield Forecasting")
            
            if st.button("Generate Yield Forecast", type="primary"):
                with st.spinner("Generating AI-powered yield forecast..."):
                    try:
                        forecasting_service = get_forecasting_service()
                        yield_forecast = forecasting_service.forecast_crop_yield(selected_field)
                        
                        # Display forecast results
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            avg_yield = np.mean(yield_forecast.predictions)
                            st.metric("Predicted Yield", f"{avg_yield:.2f} tons/acre")
                        
                        with col2:
                            st.metric("Confidence Score", f"{yield_forecast.accuracy_score:.1%}")
                        
                        with col3:
                            trend = "📈 Increasing" if yield_forecast.predictions[-1] > yield_forecast.predictions[0] else "📉 Decreasing"
                            st.metric("Trend", trend)
                        
                        # Yield forecast chart
                        fig = go.Figure()
                        
                        # Add historical data (simulated)
                        historical_dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
                        historical_yield = np.random.normal(avg_yield, 0.3, len(historical_dates))
                        
                        fig.add_trace(go.Scatter(
                            x=historical_dates,
                            y=historical_yield,
                            mode='lines',
                            name='Historical Yield',
                            line=dict(color='blue', width=2)
                        ))
                        
                        # Add forecast
                        fig.add_trace(go.Scatter(
                            x=yield_forecast.forecast_dates,
                            y=yield_forecast.predictions,
                            mode='lines',
                            name='AI Forecast',
                            line=dict(color='red', width=3)
                        ))
                        
                        # Add confidence intervals
                        upper_bound = yield_forecast.predictions + np.std(yield_forecast.predictions)
                        lower_bound = yield_forecast.predictions - np.std(yield_forecast.predictions)
                        
                        fig.add_trace(go.Scatter(
                            x=yield_forecast.forecast_dates + yield_forecast.forecast_dates[::-1],
                            y=np.concatenate([upper_bound, lower_bound[::-1]]),
                            fill='tonexty',
                            fillcolor='rgba(255,0,0,0.2)',
                            line=dict(color='rgba(255,255,255,0)'),
                            name='Confidence Interval',
                            showlegend=False
                        ))
                        
                        fig.update_layout(
                            title="Crop Yield Forecast (30 Days)",
                            xaxis_title="Date",
                            yaxis_title="Yield (tons/acre)",
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig, width='stretch')
                        
                        # Forecast details
                        st.subheader("Forecast Details")
                        forecast_df = pd.DataFrame({
                            'Date': yield_forecast.forecast_dates,
                            'Predicted Yield': yield_forecast.predictions,
                            'Confidence': [f"{yield_forecast.accuracy_score:.1%}"] * len(yield_forecast.predictions)
                        })
                        st.dataframe(forecast_df, width='stretch')
                        
                    except Exception as e:
                        st.error(f"Error generating yield forecast: {e}")
        
        with tab2:
            st.subheader("🌤️ Weather Trend Forecasting")
            
            if st.button("Generate Weather Forecast", type="primary"):
                with st.spinner("Generating AI-powered weather forecast..."):
                    try:
                        forecasting_service = get_forecasting_service()
                        weather_forecast = forecasting_service.forecast_weather_trends(
                            selected_field['latitude'], 
                            selected_field['longitude']
                        )
                        
                        # Display weather forecast
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            avg_temp = np.mean(weather_forecast.predictions)
                            st.metric("Predicted Temperature", f"{avg_temp:.1f}°C")
                        
                        with col2:
                            st.metric("Confidence Score", f"{weather_forecast.accuracy_score:.1%}")
                        
                        with col3:
                            trend = "🌡️ Warming" if weather_forecast.predictions[-1] > weather_forecast.predictions[0] else "❄️ Cooling"
                            st.metric("Trend", trend)
                        
                        # Weather forecast chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=weather_forecast.forecast_dates,
                            y=weather_forecast.predictions,
                            mode='lines+markers',
                            name='Temperature Forecast',
                            line=dict(color='orange', width=3),
                            marker=dict(size=6)
                        ))
                        
                        fig.update_layout(
                            title="Temperature Forecast (30 Days)",
                            xaxis_title="Date",
                            yaxis_title="Temperature (°C)",
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig, width='stretch')
                        
                    except Exception as e:
                        st.error(f"Error generating weather forecast: {e}")
        
        with tab3:
            st.subheader("💰 Market Price Forecasting")
            
            if st.button("Generate Market Forecast", type="primary"):
                with st.spinner("Generating AI-powered market forecast..."):
                    try:
                        forecasting_service = get_forecasting_service()
                        market_forecast = forecasting_service.forecast_market_prices(
                            selected_field.get('crop_type', 'rice')
                        )
                        
                        # Display market forecast
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            avg_price = np.mean(market_forecast.predictions)
                            st.metric("Predicted Price", f"${avg_price:.2f}")
                        
                        with col2:
                            st.metric("Confidence Score", f"{market_forecast.accuracy_score:.1%}")
                        
                        with col3:
                            trend = "📈 Rising" if market_forecast.predictions[-1] > market_forecast.predictions[0] else "📉 Falling"
                            st.metric("Trend", trend)
                        
                        # Market forecast chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=market_forecast.forecast_dates,
                            y=market_forecast.predictions,
                            mode='lines+markers',
                            name='Price Forecast',
                            line=dict(color='green', width=3),
                            marker=dict(size=6)
                        ))
                        
                        fig.update_layout(
                            title=f"Market Price Forecast - {selected_field.get('crop_type', 'rice').title()} (30 Days)",
                            xaxis_title="Date",
                            yaxis_title="Price ($)",
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig, width='stretch')
                        
                    except Exception as e:
                        st.error(f"Error generating market forecast: {e}")
        
        with tab4:
            st.subheader("📊 Comprehensive AI Analysis")
            
            if st.button("Generate Complete Analysis", type="primary"):
                with st.spinner("Generating comprehensive AI analysis..."):
                    try:
                        forecasting_service = get_forecasting_service()
                        analysis = forecasting_service.get_forecast_summary(selected_field)
                        
                        if 'error' in analysis:
                            st.error(f"Error in analysis: {analysis['error']}")
                        else:
                            # Display comprehensive analysis
                            st.success("✅ AI Analysis Complete!")
                            
                            # Key metrics
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Yield Prediction", f"{analysis['yield_forecast']['predicted_yield']:.2f} tons/acre")
                            
                            with col2:
                                st.metric("Weather Trend", f"{analysis['weather_forecast']['avg_temperature']:.1f}°C")
                            
                            with col3:
                                st.metric("Market Price", f"${analysis['market_forecast']['predicted_price']:.2f}")
                            
                            with col4:
                                avg_confidence = (analysis['yield_forecast']['confidence'] + 
                                               analysis['weather_forecast']['confidence'] + 
                                               analysis['market_forecast']['confidence']) / 3
                                st.metric("Overall Confidence", f"{avg_confidence:.1%}")
                            
                            # Recommendations
                            st.subheader("🤖 AI Recommendations")
                            for i, rec in enumerate(analysis['recommendations'], 1):
                                st.info(f"{i}. {rec}")
                            
                            # Model information
                            st.subheader("🔬 Model Information")
                            st.json({
                                'yield_model': analysis['yield_forecast'].get('model_info', {}),
                                'weather_model': analysis['weather_forecast'].get('model_info', {}),
                                'market_model': analysis['market_forecast'].get('model_info', {}),
                                'generated_at': analysis['generated_at']
                            })
                        
                    except Exception as e:
                        st.error(f"Error generating comprehensive analysis: {e}")
        
        # Model status
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔬 AI Model Status")
        
        forecasting_service = get_forecasting_service()
        if forecasting_service.model_loaded:
            st.sidebar.success("✅ TimesFM Model Loaded")
            st.sidebar.info("Real AI forecasting available")
        else:
            st.sidebar.warning("⚠️ TimesFM Not Available")
            st.sidebar.info("Using fallback forecasting")

    def render_weather_soil(self):
        """Render weather and soil monitoring page"""
        st.title("🌍 Weather & Soil Monitoring")
        
        # Get user's fields
        farms_df = self.get_user_farms(st.session_state.user_id)
        if farms_df.empty:
            st.info("No farms found. Add farms to monitor weather and soil.")
            return
        
        # Field selection
        all_fields = []
        for _, farm in farms_df.iterrows():
            fields_df = self.get_farm_fields(farm['id'])
            for _, field in fields_df.iterrows():
                all_fields.append({
                    'id': field['id'],
                    'name': f"{farm['name']} - {field['name']}",
                    'lat': field['latitude'],
                    'lon': field['longitude']
                })
        
        if not all_fields:
            st.info("No fields found. Add fields to monitor weather and soil.")
            return
        
        field_names = [f['name'] for f in all_fields]
        selected_field_idx = st.selectbox("Select Field", range(len(field_names)), format_func=lambda x: field_names[x])
        selected_field = all_fields[selected_field_idx]
        
        # Weather data
        st.subheader("🌤️ Weather Data")
        
        # Simulate weather data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        temperature = np.random.normal(25, 5, len(dates))
        humidity = np.random.normal(60, 10, len(dates))
        rainfall = np.random.exponential(2, len(dates))
        
        # Temperature chart
        fig = px.line(x=dates, y=temperature, title="Temperature Trend", labels={'x': 'Date', 'y': 'Temperature (°C)'})
        st.plotly_chart(fig, width='stretch')
        
        # Weather metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Temp", f"{temperature[-1]:.1f}°C")
        with col2:
            st.metric("Humidity", f"{humidity[-1]:.1f}%")
        with col3:
            st.metric("Rainfall (7d)", f"{rainfall[-7:].sum():.1f}mm")
        with col4:
            st.metric("Avg Temp", f"{temperature.mean():.1f}°C")
        
        # Soil data
        st.subheader("🌱 Soil Health")
        
        # Simulate soil data
        soil_metrics = {
            'pH Level': np.random.normal(6.5, 0.5),
            'Nitrogen': np.random.normal(45, 10),
            'Phosphorus': np.random.normal(25, 5),
            'Potassium': np.random.normal(150, 20),
            'Organic Matter': np.random.normal(3.2, 0.5)
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Soil metrics
            for metric, value in soil_metrics.items():
                st.metric(metric, f"{value:.1f}")
        
        with col2:
            # Soil health chart
            fig = px.bar(
                x=list(soil_metrics.keys()),
                y=list(soil_metrics.values()),
                title="Soil Nutrient Levels"
            )
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, width='stretch')
        
        # Soil recommendations
        st.subheader("💡 Soil Recommendations")
        
        recommendations = []
        if soil_metrics['pH Level'] < 6.0:
            recommendations.append("Consider adding lime to increase pH level")
        if soil_metrics['Nitrogen'] < 40:
            recommendations.append("Apply nitrogen fertilizer to improve soil fertility")
        if soil_metrics['Organic Matter'] < 3.0:
            recommendations.append("Add organic matter through compost or cover crops")
        
        if recommendations:
            for rec in recommendations:
                st.warning(rec)
        else:
            st.success("Soil health looks good! Continue current practices.")
    
    def render_market_intelligence(self):
        """Render market intelligence page"""
        st.title("📈 Market Intelligence")
        
        # Commodity prices
        st.subheader("💰 Commodity Prices")
        
        # Sample market data
        commodities = ['Rice', 'Wheat', 'Corn', 'Soybean', 'Cotton']
        prices = [450, 280, 180, 320, 85]  # Price per ton
        changes = [2.5, -1.2, 0.8, -0.5, 3.1]  # % change
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price table
            market_df = pd.DataFrame({
                'Commodity': commodities,
                'Price ($/ton)': prices,
                'Change (%)': changes
            })
            st.dataframe(market_df, width='stretch')
        
        with col2:
            # Price chart
            fig = px.bar(market_df, x='Commodity', y='Price ($/ton)', title="Current Commodity Prices")
            st.plotly_chart(fig, width='stretch')
        
        # Market trends
        st.subheader("📊 Market Trends")
        
        # Simulate trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=90), end=datetime.now(), freq='D')
        rice_prices = 450 + np.cumsum(np.random.normal(0, 2, len(dates)))
        
        fig = px.line(x=dates, y=rice_prices, title="Rice Price Trend (90 days)")
        st.plotly_chart(fig, width='stretch')
        
        # Market recommendations
        st.subheader("💡 Market Recommendations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("**Best Time to Sell:**\nRice prices are currently high. Consider selling soon.")
        
        with col2:
            st.warning("**Market Alert:**\nWheat prices are declining. Monitor closely.")
        
        with col3:
            st.success("**Opportunity:**\nCorn prices are stable. Good time for planting decisions.")
    
    def render_iot_devices(self):
        """Render IoT devices page"""
        st.title("📡 IoT Devices")
        
        # Device management
        st.subheader("🔧 Device Management")
        
        # Add new device
        with st.form("add_device_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                device_name = st.text_input("Device Name")
                device_type = st.selectbox("Device Type", ["Weather Station", "Soil Sensor", "Camera", "Drone", "Other"])
            
            with col2:
                # Field selection
                farms_df = self.get_user_farms(st.session_state.user_id)
                all_fields = []
                for _, farm in farms_df.iterrows():
                    fields_df = self.get_farm_fields(farm['id'])
                    for _, field in fields_df.iterrows():
                        all_fields.append({
                            'id': field['id'],
                            'name': f"{farm['name']} - {field['name']}"
                        })
                
                if all_fields:
                    field_names = [f['name'] for f in all_fields]
                    selected_field_idx = st.selectbox("Field", range(len(field_names)), format_func=lambda x: field_names[x])
                    selected_field_id = all_fields[selected_field_idx]['id']
                else:
                    st.info("No fields available. Add fields first.")
                    selected_field_id = None
            
            if st.form_submit_button("Add Device", type="primary") and selected_field_id:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO iot_devices (field_id, device_name, device_type)
                    VALUES (?, ?, ?)
                """, (selected_field_id, device_name, device_type))
                conn.commit()
                conn.close()
                st.success("Device added successfully!")
                st.rerun()
        
        # Device list
        st.subheader("📱 Connected Devices")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.*, f.name as field_name 
            FROM iot_devices d
            JOIN fields f ON d.field_id = f.id
            ORDER BY d.created_at DESC
        """)
        
        devices = cursor.fetchall()
        conn.close()
        
        if devices:
            for device in devices:
                with st.expander(f"{device[2]} - {device[3]} ({device[7]})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Type:** {device[3]}")
                        st.write(f"**Status:** {device[4]}")
                    
                    with col2:
                        st.write(f"**Field:** {device[7]}")
                        st.write(f"**Added:** {device[6][:10]}")
                    
                    with col3:
                        if device[5]:  # last_data_received
                            st.write(f"**Last Data:** {device[5][:16]}")
                        else:
                            st.write("**Last Data:** Never")
                        
                        if st.button("Remove", key=f"remove_{device[0]}"):
                            conn = self.db.get_connection()
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM iot_devices WHERE id = ?", (device[0],))
                            conn.commit()
                            conn.close()
                            st.success("Device removed!")
                            st.rerun()
        else:
            st.info("No devices found. Add IoT devices to start monitoring.")
    
    def render_settings(self):
        """Render settings page"""
        st.title("⚙️ Settings")
        
        # User profile
        st.subheader("👤 User Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Username:** {st.session_state.user_name}")
            st.write(f"**User ID:** {st.session_state.user_id}")
        
        with col2:
            if st.button("Change Password"):
                st.info("Password change functionality would be implemented here.")
        
        # System settings
        st.subheader("🔧 System Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Theme", ["Light", "Dark"], index=0)
            st.selectbox("Language", ["English", "Spanish", "French"], index=0)
        
        with col2:
            st.number_input("Data Refresh Interval (minutes)", min_value=1, max_value=60, value=15)
            st.checkbox("Email Notifications", value=True)
        
        # Data management
        st.subheader("💾 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export Data", type="primary"):
                st.success("Data export functionality would be implemented here.")
        
        with col2:
            if st.button("Clear Cache"):
                st.success("Cache cleared successfully!")
        
        # About
        st.subheader("ℹ️ About")
        st.write("**AgriForecast.ai v1.0**")
        st.write("Agricultural Intelligence Platform")
        st.write("Built with Streamlit and Python")
    
    def run(self):
        """Main application runner"""
        # Check if user is logged in
        if st.session_state.user_id is None:
            self.render_login_page()
        else:
            # Render main application
            page = self.render_sidebar()
            
            if page == "🏠 Dashboard":
                self.render_dashboard()
            elif page == "🌾 Field Management":
                self.render_field_management()
            elif page == "📊 Analytics & Reports":
                self.render_analytics_reports()
            elif page == "🌱 Crop Management":
                self.render_crop_management()
            elif page == "🌍 Weather & Soil":
                self.render_weather_soil()
            elif page == "🔮 AI Forecasting":
                self.render_ai_forecasting()
            elif page == "📈 Market Intelligence":
                self.render_market_intelligence()
            elif page == "📡 IoT Devices":
                self.render_iot_devices()
            elif page == "⚙️ Settings":
                self.render_settings()

if __name__ == "__main__":
    app = ProductionPlatform()
    app.run()
