#!/usr/bin/env python3
"""
AgriForecast.ai - Simplified User Authentication System
Fixed version that works properly
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

class SimpleUserManager:
    """Simplified user management system"""
    
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Setup database with user authentication"""
        try:
            self.conn = sqlite3.connect('agriforecast_user_simple.db', check_same_thread=False)
            cursor = self.conn.cursor()
            
            # Create users table
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
            
            self.conn.commit()
            logger.info("Simple user database setup completed")
            
        except Exception as e:
            logger.error(f"Database setup error: {e}")
            st.error(f"Database error: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str, full_name: str = "") -> int:
        """Create a new user"""
        try:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)
            
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
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise e
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        try:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute(
                "SELECT id, username, email, full_name FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            user = cursor.fetchone()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'full_name': user[3]
                }
            return None
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    def get_user_farms(self, user_id: int) -> List[Dict]:
        """Get all farms for a specific user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM farms WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting farms: {e}")
            return []
    
    def get_user_fields(self, user_id: int, farm_id: Optional[int] = None) -> List[Dict]:
        """Get all fields for a specific user"""
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
    
    def create_farm(self, user_id: int, name: str, description: str = "", location: str = "") -> int:
        """Create a new farm for a user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO farms (user_id, name, description, location) VALUES (?, ?, ?, ?)",
                (user_id, name, description, location)
            )
            farm_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Created farm: {name} for user {user_id} (Farm ID: {farm_id})")
            return farm_id
        except Exception as e:
            logger.error(f"Error creating farm: {e}")
            raise e
    
    def create_field(self, user_id: int, farm_id: int, name: str, crop_type: str, 
                    latitude: float, longitude: float, area_m2: float, 
                    description: str = "") -> int:
        """Create a new field for a user"""
        try:
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
        except Exception as e:
            logger.error(f"Error creating field: {e}")
            raise e

class SimpleUserFrontend:
    """Simplified frontend with user authentication"""
    
    def __init__(self):
        self.user_manager = SimpleUserManager()
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
                        try:
                            user = self.user_manager.authenticate_user(username, password)
                            if user:
                                st.session_state.user = user
                                st.session_state.logged_in = True
                                st.success(f"Welcome back, {user['full_name'] or user['username']}!")
                                st.rerun()
                            else:
                                st.error("Invalid username or password")
                        except Exception as e:
                            st.error(f"Login error: {e}")
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
                            except Exception as e:
                                st.error(f"Registration error: {e}")
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
        try:
            farms = self.user_manager.get_user_farms(user['id'])
            fields = self.user_manager.get_user_fields(user['id'])
        except Exception as e:
            st.error(f"Error loading data: {e}")
            farms = []
            fields = []
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Your Farms", len(farms))
        with col2:
            st.metric("Your Fields", len(fields))
        with col3:
            if fields:
                try:
                    total_area = sum(float(field['area_acres']) for field in fields)
                    st.metric("Total Area", f"{total_area:.2f} acres")
                except:
                    st.metric("Total Area", "N/A")
            else:
                st.metric("Total Area", "0 acres")
        
        # Add Farm button
        if st.button("➕ Add New Farm", type="primary", width='stretch'):
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
                    try:
                        farm_fields = self.user_manager.get_user_fields(user['id'], farm['id'])
                        if farm_fields:
                            st.write(f"**Fields:** {len(farm_fields)}")
                            for field in farm_fields:
                                st.write(f"  • {field['name']} ({field['crop_type']}) - {field['area_acres']:.2f} acres")
                        else:
                            st.write("No fields yet. Add your first field!")
                    except Exception as e:
                        st.write(f"Error loading fields: {e}")
        
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
                    try:
                        user_id = st.session_state.user['id']
                        farm_id = self.user_manager.create_farm(user_id, name, description, location)
                        st.success(f"Farm '{name}' created successfully!")
                        st.session_state.show_add_farm = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating farm: {e}")
                else:
                    st.error("Please enter a farm name")
    
    def render_add_field_form(self):
        """Render the add field form"""
        st.subheader("🌾 Add New Field")
        
        user_id = st.session_state.user['id']
        try:
            farms = self.user_manager.get_user_farms(user_id)
        except Exception as e:
            st.error(f"Error loading farms: {e}")
            farms = []
        
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
                    try:
                        field_id = self.user_manager.create_field(
                            user_id, farm_id, name, crop_type, latitude, longitude, area_m2, description
                        )
                        st.success(f"Field '{name}' created successfully!")
                        st.session_state.show_add_field = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating field: {e}")
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
            
            if st.sidebar.button("➕ Add Farm", width='stretch'):
                st.session_state.show_add_farm = True
                st.rerun()
            
            if st.sidebar.button("🌾 Add Field", width='stretch'):
                st.session_state.show_add_field = True
                st.rerun()
            
            # Logout
            st.sidebar.markdown("---")
            if st.sidebar.button("🚪 Logout", width='stretch'):
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
        app = SimpleUserFrontend()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()

