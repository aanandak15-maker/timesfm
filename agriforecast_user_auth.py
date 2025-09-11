#!/usr/bin/env python3
"""
AgriForecast.ai - User Authentication & Farm Management System
Real users can manage their own farms with proper data isolation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import sqlite3
import hashlib
import requests
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
import time
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserManager:
    """User authentication and management system"""
    
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Setup database with user authentication"""
        self.conn = sqlite3.connect('agriforecast_user_auth.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create farms table with user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                location TEXT,
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farm_id) REFERENCES farms (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create field_zones table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS field_zones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER,
                user_id INTEGER NOT NULL,
                zone_name TEXT NOT NULL,
                zone_type TEXT,
                coordinates TEXT,
                area_m2 REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create field_data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS field_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER,
                user_id INTEGER NOT NULL,
                data_type TEXT,
                data_json TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create yield_predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS yield_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER,
                user_id INTEGER NOT NULL,
                prediction_type TEXT,
                prediction_data TEXT,
                confidence_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
        logger.info("User authentication database setup completed")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str, full_name: str = "") -> int:
        """Create a new user"""
        cursor = self.conn.cursor()
        password_hash = self.hash_password(password)
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, full_name)
            )
            user_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Created user: {username} (ID: {user_id})")
            return user_id
        except sqlite3.IntegrityError:
            raise ValueError("Username or email already exists")
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        cursor = self.conn.cursor()
        password_hash = self.hash_password(password)
        
        cursor.execute(
            "SELECT id, username, email, full_name FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user[0],)
            )
            self.conn.commit()
            
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3]
            }
        return None
    
    def get_user_farms(self, user_id: int) -> List[Dict]:
        """Get all farms for a specific user"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM farms WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_user_fields(self, user_id: int, farm_id: Optional[int] = None) -> List[Dict]:
        """Get all fields for a specific user"""
        cursor = self.conn.cursor()
        if farm_id:
            cursor.execute("SELECT * FROM fields WHERE user_id = ? AND farm_id = ? ORDER BY created_at DESC", 
                         (user_id, farm_id))
        else:
            cursor.execute("SELECT * FROM fields WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def create_farm(self, user_id: int, name: str, description: str = "", location: str = "") -> int:
        """Create a new farm for a user"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO farms (user_id, name, description, location) VALUES (?, ?, ?, ?)",
            (user_id, name, description, location)
        )
        farm_id = cursor.lastrowid
        self.conn.commit()
        logger.info(f"Created farm: {name} for user {user_id} (Farm ID: {farm_id})")
        return farm_id
    
    def create_field(self, user_id: int, farm_id: int, name: str, crop_type: str, 
                    latitude: float, longitude: float, area_m2: float, 
                    description: str = "") -> int:
        """Create a new field for a user"""
        area_acres = area_m2 * 0.000247105  # Convert m² to acres
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO fields (user_id, farm_id, name, crop_type, latitude, longitude, 
               area_m2, area_acres, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, farm_id, name, crop_type, latitude, longitude, area_m2, area_acres, description)
        )
        field_id = cursor.lastrowid
        self.conn.commit()
        logger.info(f"Created field: {name} for user {user_id} (Field ID: {field_id})")
        return field_id

class UserAuthFrontend:
    """Frontend with user authentication"""
    
    def __init__(self):
        self.user_manager = UserManager()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast.ai - Your Farms",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_login_page(self):
        """Render the login/register page"""
        st.title("🌾 AgriForecast.ai")
        st.markdown("**Your Personal Agricultural Intelligence Platform**")
        
        # Create tabs for login and register
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.subheader("Login to Your Account")
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Login", type="primary")
                
                if submitted:
                    if username and password:
                        user = self.user_manager.authenticate_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.logged_in = True
                            st.success(f"Welcome back, {user['full_name'] or user['username']}!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Please enter both username and password")
        
        with tab2:
            st.subheader("Create New Account")
            
            with st.form("register_form"):
                username = st.text_input("Username", placeholder="Choose a username")
                email = st.text_input("Email", placeholder="Enter your email")
                full_name = st.text_input("Full Name", placeholder="Enter your full name")
                password = st.text_input("Password", type="password", placeholder="Choose a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                submitted = st.form_submit_button("Register", type="primary")
                
                if submitted:
                    if username and email and password and confirm_password:
                        if password == confirm_password:
                            try:
                                user_id = self.user_manager.create_user(username, email, password, full_name)
                                st.success(f"Account created successfully! Welcome, {full_name or username}!")
                                st.info("Please login with your new credentials.")
                            except ValueError as e:
                                st.error(str(e))
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.error("Please fill in all fields")
    
    def render_user_dashboard(self):
        """Render the user's personal dashboard"""
        user = st.session_state.user
        
        st.title(f"🌾 Welcome, {user['full_name'] or user['username']}!")
        st.markdown("**Your Personal Agricultural Intelligence Platform**")
        
        # User info in sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**👤 {user['full_name'] or user['username']}**")
        st.sidebar.markdown(f"📧 {user['email']}")
        
        # Get user's farms and fields
        farms = self.user_manager.get_user_farms(user['id'])
        fields = self.user_manager.get_user_fields(user['id'])
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Your Farms", len(farms))
        with col2:
            st.metric("Your Fields", len(fields))
        with col3:
            if fields:
                total_area = sum(float(field['area_acres']) for field in fields)
                st.metric("Total Area", f"{total_area:.2f} acres")
        
        # Add Farm button
        if st.button("➕ Add New Farm", type="primary", use_container_width=True):
            st.session_state.show_add_farm = True
            st.rerun()
        
        # Show farms
        if not farms:
            st.info("👋 Welcome! Start by creating your first farm.")
        else:
            st.subheader("🏡 Your Farms")
            for farm in farms:
                with st.expander(f"🏡 {farm['name']}"):
                    st.write(f"**Location:** {farm['location']}")
                    st.write(f"**Description:** {farm['description']}")
                    st.write(f"**Created:** {farm['created_at'][:10]}")
                    
                    # Show fields for this farm
                    farm_fields = self.user_manager.get_user_fields(user['id'], farm['id'])
                    if farm_fields:
                        st.write(f"**Fields:** {len(farm_fields)}")
                        for field in farm_fields:
                            st.write(f"  • {field['name']} ({field['crop_type']}) - {field['area_acres']:.2f} acres")
                    else:
                        st.write("No fields yet. Add your first field!")
        
        # Show all fields
        if fields:
            st.subheader("🌾 Your Fields")
            for field in fields:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.write(f"**{field['name']}**")
                        st.write(f"*{field['crop_type']}*")
                        if field['description']:
                            st.write(f"_{field['description']}_")
                    
                    with col2:
                        st.write(f"📍 {field['latitude']:.4f}, {field['longitude']:.4f}")
                        st.write(f"📏 {field['area_acres']:.2f} acres")
                        st.write(f"📅 {field['created_at'][:10]}")
                    
                    with col3:
                        if st.button("View Details", key=f"view_{field['id']}"):
                            st.session_state.selected_field = field['id']
                            st.rerun()
    
    def render_add_farm_form(self):
        """Render the add farm form"""
        st.subheader("➕ Add New Farm")
        
        with st.form("add_farm_form"):
            name = st.text_input("Farm Name", placeholder="Enter your farm name")
            description = st.text_area("Description", placeholder="Describe your farm")
            location = st.text_input("Location", placeholder="City, State, Country")
            
            submitted = st.form_submit_button("Create Farm", type="primary")
            
            if submitted:
                if name:
                    user_id = st.session_state.user['id']
                    farm_id = self.user_manager.create_farm(user_id, name, description, location)
                    st.success(f"Farm '{name}' created successfully!")
                    st.session_state.show_add_farm = False
                    st.rerun()
                else:
                    st.error("Please enter a farm name")
    
    def render_add_field_form(self):
        """Render the add field form"""
        st.subheader("🌾 Add New Field")
        
        user_id = st.session_state.user['id']
        farms = self.user_manager.get_user_farms(user_id)
        
        if not farms:
            st.warning("Please create a farm first before adding fields.")
            return
        
        with st.form("add_field_form"):
            farm_id = st.selectbox(
                "Select Farm",
                options=[f['id'] for f in farms],
                format_func=lambda x: next(f['name'] for f in farms if f['id'] == x)
            )
            
            name = st.text_input("Field Name", placeholder="Enter field name")
            crop_type = st.selectbox(
                "Crop Type",
                ["Rice", "Wheat", "Corn", "Soybean", "Cotton", "Sugarcane", "Other"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", value=28.368911, format="%.6f")
            with col2:
                longitude = st.number_input("Longitude", value=77.541033, format="%.6f")
            
            area_m2 = st.number_input("Area (m²)", value=325.12, min_value=0.01)
            description = st.text_area("Description", placeholder="Enter field description")
            
            submitted = st.form_submit_button("Create Field", type="primary")
            
            if submitted:
                if name:
                    field_id = self.user_manager.create_field(
                        user_id, farm_id, name, crop_type, latitude, longitude, area_m2, description
                    )
                    st.success(f"Field '{name}' created successfully!")
                    st.session_state.show_add_field = False
                    st.rerun()
                else:
                    st.error("Please enter a field name")
    
    def render_sidebar(self):
        """Render the sidebar with navigation"""
        if st.session_state.get('logged_in', False):
            user = st.session_state.user
            
            st.sidebar.title("🌾 AgriForecast.ai")
            st.sidebar.markdown(f"**Welcome, {user['full_name'] or user['username']}!**")
            
            # Navigation
            page = st.sidebar.selectbox(
                "Navigate",
                ["🏠 My Dashboard", "🌾 My Fields", "📊 Analytics", "⚙️ Settings"]
            )
            
            # Quick actions
            st.sidebar.markdown("---")
            st.sidebar.markdown("### Quick Actions")
            
            if st.sidebar.button("➕ Add Farm", use_container_width=True):
                st.session_state.show_add_farm = True
                st.rerun()
            
            if st.sidebar.button("🌾 Add Field", use_container_width=True):
                st.session_state.show_add_field = True
                st.rerun()
            
            # Logout
            st.sidebar.markdown("---")
            if st.sidebar.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
            
            return page
        return None
    
    def run(self):
        """Main application runner"""
        # Initialize session state
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'show_add_farm' not in st.session_state:
            st.session_state.show_add_farm = False
        if 'show_add_field' not in st.session_state:
            st.session_state.show_add_field = False
        
        if not st.session_state.logged_in:
            self.render_login_page()
        else:
            # Render sidebar and get current page
            page = self.render_sidebar()
            
            # Render main content based on page
            if page == "🏠 My Dashboard":
                self.render_user_dashboard()
            elif page == "🌾 My Fields":
                self.render_user_dashboard()  # Same as dashboard for now
            elif page == "📊 Analytics":
                st.title("📊 Analytics")
                st.info("Analytics features coming soon!")
            elif page == "⚙️ Settings":
                st.title("⚙️ Settings")
                st.info("Settings features coming soon!")
            
            # Render forms if needed
            if st.session_state.show_add_farm:
                self.render_add_farm_form()
            
            if st.session_state.show_add_field:
                self.render_add_field_form()

def main():
    """Main application entry point"""
    try:
        app = UserAuthFrontend()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()

