#!/usr/bin/env python3
"""
AgriForecast.ai - Mobile-Optimized Agricultural Platform
Responsive design for mobile devices and field work
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MobileUserManager:
    """Mobile-optimized user management system"""
    
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Setup database for mobile users"""
        self.conn = sqlite3.connect('agriforecast_mobile.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                phone TEXT,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create farms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                location TEXT,
                latitude REAL,
                longitude REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create fields table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farm_id INTEGER,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                crop_type TEXT,
                latitude REAL,
                longitude REAL,
                area_m2 REAL,
                area_acres REAL,
                description TEXT,
                planting_date DATE,
                expected_harvest DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farm_id) REFERENCES farms (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create field_observations table for mobile data collection
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS field_observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER,
                user_id INTEGER NOT NULL,
                observation_type TEXT,
                data_json TEXT,
                latitude REAL,
                longitude REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
        logger.info("Mobile database setup completed")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str, 
                   full_name: str = "", phone: str = "", location: str = "") -> int:
        """Create a new mobile user"""
        try:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute(
                """INSERT INTO users (username, email, password_hash, full_name, phone, location) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (username, email, password_hash, full_name, phone, location)
            )
            user_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Created mobile user: {username} (ID: {user_id})")
            return user_id
        except sqlite3.IntegrityError:
            raise ValueError("Username or email already exists")
        except Exception as e:
            logger.error(f"Error creating mobile user: {e}")
            raise e
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate mobile user login"""
        try:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute(
                "SELECT id, username, email, full_name, phone, location FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            user = cursor.fetchone()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'full_name': user[3],
                    'phone': user[4],
                    'location': user[5]
                }
            return None
        except Exception as e:
            logger.error(f"Error authenticating mobile user: {e}")
            return None
    
    def get_user_farms(self, user_id: int) -> List[Dict]:
        """Get all farms for a mobile user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM farms WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting farms: {e}")
            return []
    
    def get_user_fields(self, user_id: int, farm_id: Optional[int] = None) -> List[Dict]:
        """Get all fields for a mobile user"""
        try:
            cursor = self.conn.cursor()
            if farm_id:
                cursor.execute("SELECT * FROM fields WHERE user_id = ? AND farm_id = ? ORDER BY created_at DESC", 
                             (user_id, farm_id))
            else:
                cursor.execute("SELECT * FROM fields WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting fields: {e}")
            return []
    
    def create_farm(self, user_id: int, name: str, description: str = "", 
                   location: str = "", latitude: float = None, longitude: float = None) -> int:
        """Create a new farm for mobile user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO farms (user_id, name, description, location, latitude, longitude) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, name, description, location, latitude, longitude)
            )
            farm_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Created mobile farm: {name} for user {user_id} (Farm ID: {farm_id})")
            return farm_id
        except Exception as e:
            logger.error(f"Error creating mobile farm: {e}")
            raise e
    
    def create_field(self, user_id: int, farm_id: int, name: str, crop_type: str, 
                    latitude: float, longitude: float, area_m2: float, 
                    description: str = "", planting_date: str = None, 
                    expected_harvest: str = None) -> int:
        """Create a new field for mobile user"""
        try:
            area_acres = area_m2 * 0.000247105  # Convert m² to acres
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO fields (user_id, farm_id, name, crop_type, latitude, longitude, 
                   area_m2, area_acres, description, planting_date, expected_harvest) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, farm_id, name, crop_type, latitude, longitude, area_m2, area_acres, 
                 description, planting_date, expected_harvest)
            )
            field_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Created mobile field: {name} for user {user_id} (Field ID: {field_id})")
            return field_id
        except Exception as e:
            logger.error(f"Error creating mobile field: {e}")
            raise e
    
    def add_field_observation(self, user_id: int, field_id: int, observation_type: str, 
                            data: Dict, latitude: float = None, longitude: float = None) -> int:
        """Add field observation from mobile device"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO field_observations (user_id, field_id, observation_type, data_json, latitude, longitude) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, field_id, observation_type, json.dumps(data), latitude, longitude)
            )
            observation_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Added field observation: {observation_type} for field {field_id}")
            return observation_id
        except Exception as e:
            logger.error(f"Error adding field observation: {e}")
            raise e

class MobileFrontend:
    """Mobile-optimized frontend"""
    
    def __init__(self):
        self.user_manager = MobileUserManager()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration for mobile"""
        st.set_page_config(
            page_title="AgriForecast Mobile",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="collapsed"  # Collapsed for mobile
        )
    
    def render_mobile_header(self):
        """Render mobile-optimized header"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("☰", key="mobile_menu"):
                st.session_state.show_mobile_menu = not st.session_state.get('show_mobile_menu', False)
        
        with col2:
            st.markdown("### 🌾 AgriForecast Mobile")
        
        with col3:
            if st.session_state.get('logged_in', False):
                if st.button("👤", key="mobile_profile"):
                    st.session_state.show_mobile_profile = not st.session_state.get('show_mobile_profile', False)
    
    def render_mobile_menu(self):
        """Render mobile menu"""
        if st.session_state.get('show_mobile_menu', False):
            st.sidebar.title("🌾 Menu")
            
            if st.session_state.get('logged_in', False):
                user = st.session_state.user
                st.sidebar.markdown(f"**👤 {user['full_name'] or user['username']}**")
                st.sidebar.markdown(f"📧 {user['email']}")
                
                if st.sidebar.button("🏠 Dashboard", width='stretch'):
                    st.session_state.mobile_page = "dashboard"
                    st.rerun()
                
                if st.sidebar.button("🌾 My Fields", width='stretch'):
                    st.session_state.mobile_page = "fields"
                
                if st.sidebar.button("📊 Quick Stats", width='stretch'):
                    st.session_state.mobile_page = "stats"
                
                if st.sidebar.button("➕ Add Field", width='stretch'):
                    st.session_state.mobile_page = "add_field"
                
                if st.sidebar.button("📱 Field Work", width='stretch'):
                    st.session_state.mobile_page = "field_work"
                
                st.sidebar.markdown("---")
                if st.sidebar.button("🚪 Logout", width='stretch'):
                    st.session_state.logged_in = False
                    st.session_state.user = None
                    st.rerun()
            else:
                if st.sidebar.button("🔐 Login", width='stretch'):
                    st.session_state.mobile_page = "login"
                
                if st.sidebar.button("📝 Register", width='stretch'):
                    st.session_state.mobile_page = "register"
    
    def render_mobile_dashboard(self):
        """Render mobile-optimized dashboard"""
        user = st.session_state.user
        
        # Quick stats in mobile-friendly format
        col1, col2 = st.columns(2)
        
        with col1:
            farms = self.user_manager.get_user_farms(user['id'])
            st.metric("🏡 Farms", len(farms))
        
        with col2:
            fields = self.user_manager.get_user_fields(user['id'])
            st.metric("🌾 Fields", len(fields))
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Farm", width='stretch'):
                st.session_state.mobile_page = "add_farm"
                st.rerun()
        
        with col2:
            if st.button("🌾 Add Field", width='stretch'):
                st.session_state.mobile_page = "add_field"
                st.rerun()
        
        # Recent fields
        if fields:
            st.subheader("🌾 Recent Fields")
            for field in fields[:3]:  # Show only 3 for mobile
                with st.container():
                    st.write(f"**{field['name']}**")
                    st.write(f"*{field['crop_type']}* - {field['area_acres']:.2f} acres")
                    st.write(f"📍 {field['latitude']:.4f}, {field['longitude']:.4f}")
                    st.divider()
    
    def render_mobile_fields(self):
        """Render mobile-optimized fields view"""
        user = st.session_state.user
        fields = self.user_manager.get_user_fields(user['id'])
        
        if not fields:
            st.info("No fields found. Add your first field!")
            return
        
        st.subheader("🌾 Your Fields")
        
        for field in fields:
            with st.expander(f"🌾 {field['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Crop:** {field['crop_type']}")
                    st.write(f"**Area:** {field['area_acres']:.2f} acres")
                
                with col2:
                    st.write(f"**Location:** {field['latitude']:.4f}, {field['longitude']:.4f}")
                    st.write(f"**Created:** {field['created_at'][:10]}")
                
                if st.button("📱 Field Work", key=f"field_work_{field['id']}"):
                    st.session_state.selected_field = field['id']
                    st.session_state.mobile_page = "field_work"
                    st.rerun()
    
    def render_mobile_field_work(self):
        """Render mobile field work interface"""
        st.subheader("📱 Field Work")
        
        user = st.session_state.user
        field_id = st.session_state.get('selected_field')
        
        if not field_id:
            st.warning("Please select a field first")
            return
        
        # Get field details
        fields = self.user_manager.get_user_fields(user['id'])
        field = next((f for f in fields if f['id'] == field_id), None)
        
        if not field:
            st.error("Field not found")
            return
        
        st.write(f"**Working on: {field['name']}**")
        st.write(f"*{field['crop_type']} - {field['area_acres']:.2f} acres*")
        
        # Field work options
        st.subheader("📝 Record Observations")
        
        # Weather observation
        with st.expander("🌤️ Weather Observation"):
            with st.form("weather_obs"):
                temperature = st.number_input("Temperature (°C)", value=25.0)
                humidity = st.number_input("Humidity (%)", value=60.0)
                precipitation = st.number_input("Precipitation (mm)", value=0.0)
                wind_speed = st.number_input("Wind Speed (m/s)", value=3.0)
                description = st.text_input("Weather Description", placeholder="Clear, cloudy, etc.")
                
                if st.form_submit_button("Record Weather"):
                    observation_data = {
                        'temperature': temperature,
                        'humidity': humidity,
                        'precipitation': precipitation,
                        'wind_speed': wind_speed,
                        'description': description,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self.user_manager.add_field_observation(
                        user['id'], field_id, 'weather', observation_data
                    )
                    st.success("Weather observation recorded!")
        
        # Crop observation
        with st.expander("🌱 Crop Observation"):
            with st.form("crop_obs"):
                growth_stage = st.selectbox("Growth Stage", 
                    ["Planting", "Germination", "Vegetative", "Flowering", "Fruiting", "Harvest"])
                health_status = st.selectbox("Health Status", 
                    ["Excellent", "Good", "Fair", "Poor", "Critical"])
                pest_damage = st.number_input("Pest Damage (%)", value=0.0, max_value=100.0)
                disease_presence = st.checkbox("Disease Present")
                notes = st.text_area("Notes", placeholder="Additional observations...")
                
                if st.form_submit_button("Record Crop Status"):
                    observation_data = {
                        'growth_stage': growth_stage,
                        'health_status': health_status,
                        'pest_damage': pest_damage,
                        'disease_presence': disease_presence,
                        'notes': notes,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self.user_manager.add_field_observation(
                        user['id'], field_id, 'crop', observation_data
                    )
                    st.success("Crop observation recorded!")
        
        # Soil observation
        with st.expander("🌍 Soil Observation"):
            with st.form("soil_obs"):
                soil_moisture = st.selectbox("Soil Moisture", 
                    ["Very Dry", "Dry", "Moist", "Wet", "Very Wet"])
                soil_condition = st.selectbox("Soil Condition", 
                    ["Excellent", "Good", "Fair", "Poor"])
                ph_level = st.number_input("pH Level", value=6.5, min_value=4.0, max_value=9.0)
                fertilizer_applied = st.checkbox("Fertilizer Applied Today")
                irrigation_applied = st.checkbox("Irrigation Applied Today")
                
                if st.form_submit_button("Record Soil Status"):
                    observation_data = {
                        'soil_moisture': soil_moisture,
                        'soil_condition': soil_condition,
                        'ph_level': ph_level,
                        'fertilizer_applied': fertilizer_applied,
                        'irrigation_applied': irrigation_applied,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self.user_manager.add_field_observation(
                        user['id'], field_id, 'soil', observation_data
                    )
                    st.success("Soil observation recorded!")
    
    def render_mobile_login(self):
        """Render mobile login form"""
        st.subheader("🔐 Login")
        
        with st.form("mobile_login"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            if st.form_submit_button("Login", width='stretch'):
                if username and password:
                    try:
                        user = self.user_manager.authenticate_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.logged_in = True
                            st.session_state.mobile_page = "dashboard"
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    except Exception as e:
                        st.error(f"Login error: {e}")
                else:
                    st.error("Please enter both username and password")
    
    def render_mobile_register(self):
        """Render mobile registration form"""
        st.subheader("📝 Register")
        
        with st.form("mobile_register"):
            username = st.text_input("Username", placeholder="Choose username")
            email = st.text_input("Email", placeholder="Enter email")
            full_name = st.text_input("Full Name", placeholder="Enter full name")
            phone = st.text_input("Phone", placeholder="Enter phone number")
            location = st.text_input("Location", placeholder="Enter location")
            password = st.text_input("Password", type="password", placeholder="Choose password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            
            if st.form_submit_button("Register", width='stretch'):
                if username and email and password and confirm_password:
                    if password == confirm_password:
                        try:
                            user_id = self.user_manager.create_user(
                                username, email, password, full_name, phone, location
                            )
                            st.success("Registration successful! Please login.")
                            st.session_state.mobile_page = "login"
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
                        except Exception as e:
                            st.error(f"Registration error: {e}")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all required fields")
    
    def run(self):
        """Main mobile application runner"""
        # Initialize session state
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'mobile_page' not in st.session_state:
            st.session_state.mobile_page = "dashboard"
        if 'show_mobile_menu' not in st.session_state:
            st.session_state.show_mobile_menu = False
        if 'show_mobile_profile' not in st.session_state:
            st.session_state.show_mobile_profile = False
        
        # Render mobile header
        self.render_mobile_header()
        
        # Render mobile menu
        self.render_mobile_menu()
        
        # Render main content based on page
        if not st.session_state.logged_in:
            if st.session_state.mobile_page == "login":
                self.render_mobile_login()
            else:
                self.render_mobile_register()
        else:
            if st.session_state.mobile_page == "dashboard":
                self.render_mobile_dashboard()
            elif st.session_state.mobile_page == "fields":
                self.render_mobile_fields()
            elif st.session_state.mobile_page == "field_work":
                self.render_mobile_field_work()
            elif st.session_state.mobile_page == "add_farm":
                st.info("Add Farm form coming soon!")
            elif st.session_state.mobile_page == "add_field":
                st.info("Add Field form coming soon!")
            elif st.session_state.mobile_page == "stats":
                st.info("Quick Stats coming soon!")

def main():
    """Main mobile application entry point"""
    try:
        app = MobileFrontend()
        app.run()
    except Exception as e:
        st.error(f"Mobile application error: {e}")
        logger.error(f"Mobile application error: {e}")

if __name__ == "__main__":
    main()




