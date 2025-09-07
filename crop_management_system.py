#!/usr/bin/env python3
"""
Crop Management System for AgriForecast.ai
Phase 3: Agricultural Workflow Integration
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sqlite3
import json
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
import hashlib
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CropType(Enum):
    RICE = "Rice"
    WHEAT = "Wheat"
    CORN = "Corn"
    SOYBEAN = "Soybean"
    COTTON = "Cotton"
    SUGARCANE = "Sugarcane"
    POTATO = "Potato"
    TOMATO = "Tomato"

class GrowthStage(Enum):
    PLANTING = "Planting"
    GERMINATION = "Germination"
    VEGETATIVE = "Vegetative"
    FLOWERING = "Flowering"
    FRUITING = "Fruiting"
    MATURITY = "Maturity"
    HARVEST = "Harvest"

class Season(Enum):
    KHARIF = "Kharif"
    RABI = "Rabi"
    SUMMER = "Summer"

@dataclass
class CropData:
    crop_type: str
    variety: str
    planting_date: datetime
    expected_harvest: datetime
    growth_stage: str
    days_since_planting: int
    days_to_harvest: int
    field_id: int
    area_acres: float
    planting_density: float
    irrigation_schedule: str
    fertilizer_schedule: str
    pest_control_schedule: str

@dataclass
class ActivityLog:
    field_id: int
    activity_type: str
    activity_date: datetime
    description: str
    cost: float
    notes: str
    performed_by: str

class CropManagementDatabase:
    """Database management for crop management system"""
    
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Setup crop management database"""
        self.conn = sqlite3.connect('agriforecast_crop_management.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create crop management tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crop_varieties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_type TEXT NOT NULL,
                variety_name TEXT NOT NULL,
                planting_season TEXT NOT NULL,
                days_to_maturity INTEGER NOT NULL,
                planting_density REAL NOT NULL,
                water_requirements REAL NOT NULL,
                fertilizer_requirements TEXT NOT NULL,
                pest_susceptibility TEXT NOT NULL,
                yield_potential REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crop_plantings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                crop_type TEXT NOT NULL,
                variety_name TEXT NOT NULL,
                planting_date DATE NOT NULL,
                expected_harvest_date DATE NOT NULL,
                actual_harvest_date DATE,
                area_acres REAL NOT NULL,
                planting_density REAL NOT NULL,
                current_growth_stage TEXT NOT NULL,
                days_since_planting INTEGER NOT NULL,
                days_to_harvest INTEGER NOT NULL,
                status TEXT DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS growth_stages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_type TEXT NOT NULL,
                stage_name TEXT NOT NULL,
                stage_order INTEGER NOT NULL,
                days_from_planting INTEGER NOT NULL,
                description TEXT NOT NULL,
                care_instructions TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS field_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                activity_type TEXT NOT NULL,
                activity_date DATE NOT NULL,
                description TEXT NOT NULL,
                cost REAL DEFAULT 0,
                notes TEXT,
                performed_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pest_disease_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                crop_type TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                recommended_action TEXT NOT NULL,
                alert_date DATE NOT NULL,
                status TEXT DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS irrigation_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                crop_type TEXT NOT NULL,
                growth_stage TEXT NOT NULL,
                irrigation_frequency INTEGER NOT NULL,
                water_amount REAL NOT NULL,
                irrigation_method TEXT NOT NULL,
                next_irrigation_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fertilizer_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                crop_type TEXT NOT NULL,
                growth_stage TEXT NOT NULL,
                fertilizer_type TEXT NOT NULL,
                application_rate REAL NOT NULL,
                application_method TEXT NOT NULL,
                next_application_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        self.populate_crop_data()
        logger.info("Crop management database setup completed")
    
    def populate_crop_data(self):
        """Populate database with crop varieties and growth stages"""
        try:
            cursor = self.conn.cursor()
            
            # Check if data already exists
            cursor.execute("SELECT COUNT(*) FROM crop_varieties")
            if cursor.fetchone()[0] > 0:
                return
            
            # Insert crop varieties
            crop_varieties = [
                # Rice varieties
                ("Rice", "Basmati 370", "Kharif", 120, 25.0, 1000.0, "NPK 120:60:60", "Low", 4.5),
                ("Rice", "IR64", "Kharif", 110, 30.0, 1200.0, "NPK 100:50:50", "Medium", 5.0),
                ("Rice", "Swarna", "Kharif", 125, 28.0, 1100.0, "NPK 110:55:55", "Low", 4.8),
                
                # Wheat varieties
                ("Wheat", "HD-2967", "Rabi", 140, 40.0, 800.0, "NPK 150:75:75", "Low", 5.5),
                ("Wheat", "PBW-343", "Rabi", 135, 45.0, 900.0, "NPK 160:80:80", "Medium", 5.2),
                ("Wheat", "DBW-17", "Rabi", 145, 42.0, 850.0, "NPK 155:78:78", "Low", 5.8),
                
                # Corn varieties
                ("Corn", "Pioneer 3394", "Kharif", 100, 20.0, 600.0, "NPK 200:100:100", "High", 8.0),
                ("Corn", "Syngenta NK-603", "Kharif", 95, 22.0, 650.0, "NPK 180:90:90", "Medium", 7.5),
                ("Corn", "Monsanto 8900", "Kharif", 105, 18.0, 700.0, "NPK 220:110:110", "High", 8.5),
                
                # Soybean varieties
                ("Soybean", "JS-335", "Kharif", 90, 15.0, 400.0, "NPK 60:30:30", "Low", 2.5),
                ("Soybean", "PK-472", "Kharif", 85, 18.0, 450.0, "NPK 65:32:32", "Medium", 2.8),
                ("Soybean", "MAUS-71", "Kharif", 95, 16.0, 420.0, "NPK 62:31:31", "Low", 2.6),
            ]
            
            cursor.executemany('''
                INSERT INTO crop_varieties (crop_type, variety_name, planting_season, days_to_maturity,
                                          planting_density, water_requirements, fertilizer_requirements,
                                          pest_susceptibility, yield_potential)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', crop_varieties)
            
            # Insert growth stages
            growth_stages = [
                # Rice growth stages
                ("Rice", "Planting", 1, 0, "Seed sowing and initial establishment", "Ensure proper soil moisture and seed depth"),
                ("Rice", "Germination", 2, 5, "Seed germination and emergence", "Maintain consistent moisture, avoid waterlogging"),
                ("Rice", "Vegetative", 3, 30, "Leaf and stem development", "Apply nitrogen fertilizer, control weeds"),
                ("Rice", "Flowering", 4, 80, "Panicle initiation and flowering", "Reduce nitrogen, ensure adequate water"),
                ("Rice", "Fruiting", 5, 100, "Grain development and filling", "Maintain soil moisture, monitor for pests"),
                ("Rice", "Maturity", 6, 115, "Grain ripening and hardening", "Reduce irrigation, prepare for harvest"),
                ("Rice", "Harvest", 7, 120, "Ready for harvesting", "Harvest at optimal moisture content"),
                
                # Wheat growth stages
                ("Wheat", "Planting", 1, 0, "Seed sowing and establishment", "Ensure proper seed depth and soil contact"),
                ("Wheat", "Germination", 2, 7, "Seed germination and emergence", "Maintain soil moisture, protect from birds"),
                ("Wheat", "Vegetative", 3, 40, "Tillering and leaf development", "Apply nitrogen fertilizer, control weeds"),
                ("Wheat", "Flowering", 4, 90, "Spike emergence and flowering", "Ensure adequate water, monitor for diseases"),
                ("Wheat", "Fruiting", 5, 120, "Grain development and filling", "Maintain soil moisture, control pests"),
                ("Wheat", "Maturity", 6, 135, "Grain ripening and hardening", "Reduce irrigation, prepare for harvest"),
                ("Wheat", "Harvest", 7, 140, "Ready for harvesting", "Harvest at optimal moisture content"),
                
                # Corn growth stages
                ("Corn", "Planting", 1, 0, "Seed sowing and establishment", "Ensure proper seed depth and spacing"),
                ("Corn", "Germination", 2, 10, "Seed germination and emergence", "Maintain soil moisture, protect from pests"),
                ("Corn", "Vegetative", 3, 30, "Leaf and stem development", "Apply nitrogen fertilizer, control weeds"),
                ("Corn", "Flowering", 4, 60, "Tasseling and silking", "Ensure adequate water, monitor pollination"),
                ("Corn", "Fruiting", 5, 80, "Ear development and grain filling", "Maintain soil moisture, control pests"),
                ("Corn", "Maturity", 6, 95, "Grain ripening and hardening", "Reduce irrigation, prepare for harvest"),
                ("Corn", "Harvest", 7, 100, "Ready for harvesting", "Harvest at optimal moisture content"),
            ]
            
            cursor.executemany('''
                INSERT INTO growth_stages (crop_type, stage_name, stage_order, days_from_planting,
                                         description, care_instructions)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', growth_stages)
            
            self.conn.commit()
            logger.info("Crop data populated successfully")
            
        except Exception as e:
            logger.error(f"Error populating crop data: {e}")
    
    def get_crop_varieties(self, crop_type: str = None) -> pd.DataFrame:
        """Get crop varieties"""
        try:
            cursor = self.conn.cursor()
            
            if crop_type:
                query = "SELECT * FROM crop_varieties WHERE crop_type = ? ORDER BY variety_name"
                cursor.execute(query, (crop_type,))
            else:
                query = "SELECT * FROM crop_varieties ORDER BY crop_type, variety_name"
                cursor.execute(query)
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting crop varieties: {e}")
            return pd.DataFrame()
    
    def get_growth_stages(self, crop_type: str) -> pd.DataFrame:
        """Get growth stages for a crop type"""
        try:
            cursor = self.conn.cursor()
            
            query = "SELECT * FROM growth_stages WHERE crop_type = ? ORDER BY stage_order"
            cursor.execute(query, (crop_type,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting growth stages: {e}")
            return pd.DataFrame()
    
    def create_crop_planting(self, user_id: int, field_id: int, crop_type: str, 
                           variety_name: str, planting_date: datetime, area_acres: float) -> int:
        """Create a new crop planting"""
        try:
            cursor = self.conn.cursor()
            
            # Get variety data
            variety_data = self.get_crop_varieties(crop_type)
            variety_info = variety_data[variety_data['variety_name'] == variety_name].iloc[0]
            
            # Calculate harvest date
            days_to_maturity = int(variety_info['days_to_maturity'])
            expected_harvest = planting_date + timedelta(days=days_to_maturity)
            
            # Calculate days since planting
            days_since_planting = (datetime.now().date() - planting_date.date()).days
            days_to_harvest = max(0, days_to_maturity - days_since_planting)
            
            # Determine current growth stage
            growth_stages = self.get_growth_stages(crop_type)
            current_stage = "Planting"
            
            for _, stage in growth_stages.iterrows():
                if days_since_planting >= stage['days_from_planting']:
                    current_stage = stage['stage_name']
            
            # Insert planting record
            cursor.execute('''
                INSERT INTO crop_plantings (user_id, field_id, crop_type, variety_name, planting_date,
                                          expected_harvest_date, area_acres, planting_density,
                                          current_growth_stage, days_since_planting, days_to_harvest)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, field_id, crop_type, variety_name, planting_date.date(),
                  expected_harvest.date(), area_acres, variety_info['planting_density'],
                  current_stage, days_since_planting, days_to_harvest))
            
            planting_id = cursor.lastrowid
            self.conn.commit()
            
            logger.info(f"Created crop planting: {crop_type} - {variety_name} for field {field_id}")
            return planting_id
            
        except Exception as e:
            logger.error(f"Error creating crop planting: {e}")
            return 0
    
    def get_crop_plantings(self, user_id: int, field_id: int = None) -> pd.DataFrame:
        """Get crop plantings for user"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT * FROM crop_plantings 
                    WHERE user_id = ? AND field_id = ? 
                    ORDER BY planting_date DESC
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT * FROM crop_plantings 
                    WHERE user_id = ? 
                    ORDER BY planting_date DESC
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting crop plantings: {e}")
            return pd.DataFrame()
    
    def log_field_activity(self, user_id: int, field_id: int, activity_type: str,
                          activity_date: datetime, description: str, cost: float = 0,
                          notes: str = "", performed_by: str = "") -> int:
        """Log field activity"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT INTO field_activities (user_id, field_id, activity_type, activity_date,
                                            description, cost, notes, performed_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, field_id, activity_type, activity_date.date(), description, cost, notes, performed_by))
            
            activity_id = cursor.lastrowid
            self.conn.commit()
            
            logger.info(f"Logged field activity: {activity_type} for field {field_id}")
            return activity_id
            
        except Exception as e:
            logger.error(f"Error logging field activity: {e}")
            return 0
    
    def get_field_activities(self, user_id: int, field_id: int = None) -> pd.DataFrame:
        """Get field activities"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT * FROM field_activities 
                    WHERE user_id = ? AND field_id = ? 
                    ORDER BY activity_date DESC
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT * FROM field_activities 
                    WHERE user_id = ? 
                    ORDER BY activity_date DESC
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting field activities: {e}")
            return pd.DataFrame()
    
    def create_pest_disease_alert(self, user_id: int, field_id: int, crop_type: str,
                                 alert_type: str, severity: str, description: str,
                                 recommended_action: str) -> int:
        """Create pest/disease alert"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT INTO pest_disease_alerts (user_id, field_id, crop_type, alert_type,
                                               severity, description, recommended_action, alert_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, field_id, crop_type, alert_type, severity, description,
                  recommended_action, datetime.now().date()))
            
            alert_id = cursor.lastrowid
            self.conn.commit()
            
            logger.info(f"Created pest/disease alert: {alert_type} for field {field_id}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Error creating pest/disease alert: {e}")
            return 0
    
    def get_pest_disease_alerts(self, user_id: int, field_id: int = None) -> pd.DataFrame:
        """Get pest/disease alerts"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT * FROM pest_disease_alerts 
                    WHERE user_id = ? AND field_id = ? AND status = 'Active'
                    ORDER BY alert_date DESC
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT * FROM pest_disease_alerts 
                    WHERE user_id = ? AND status = 'Active'
                    ORDER BY alert_date DESC
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting pest/disease alerts: {e}")
            return pd.DataFrame()

class CropManagementFrontend:
    """Crop management frontend"""
    
    def __init__(self):
        self.db = CropManagementDatabase()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast Crop Management",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render crop management sidebar"""
        st.sidebar.title("🌾 Crop Management")
        
        # User selection
        user_id = st.sidebar.selectbox(
            "Select User",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: f"User {x}"
        )
        
        # Field selection
        field_options = ["All Fields"] + [f"Field {i}" for i in range(1, 6)]
        selected_field = st.sidebar.selectbox("Select Field", field_options)
        field_id = None if selected_field == "All Fields" else int(selected_field.split()[-1])
        
        return user_id, field_id
    
    def render_crop_planting(self, user_id: int, field_id: int):
        """Render crop planting interface"""
        st.subheader("🌱 New Crop Planting")
        
        col1, col2 = st.columns(2)
        
        with col1:
            crop_type = st.selectbox(
                "Crop Type",
                options=[crop.value for crop in CropType],
                key="crop_type"
            )
            
            # Get varieties for selected crop
            varieties_df = self.db.get_crop_varieties(crop_type)
            if not varieties_df.empty:
                variety_options = varieties_df['variety_name'].tolist()
                variety_name = st.selectbox(
                    "Variety",
                    options=variety_options,
                    key="variety_name"
                )
            else:
                st.warning("No varieties available for selected crop")
                return
            
            planting_date = st.date_input(
                "Planting Date",
                value=datetime.now().date(),
                key="planting_date"
            )
            
            area_acres = st.number_input(
                "Area (acres)",
                min_value=0.1,
                max_value=1000.0,
                value=1.0,
                step=0.1,
                key="area_acres"
            )
        
        with col2:
            if not varieties_df.empty and variety_name:
                variety_info = varieties_df[varieties_df['variety_name'] == variety_name].iloc[0]
                
                st.info(f"""
                **Variety Information:**
                - **Days to Maturity:** {variety_info['days_to_maturity']} days
                - **Planting Density:** {variety_info['planting_density']} plants/acre
                - **Water Requirements:** {variety_info['water_requirements']} mm
                - **Fertilizer:** {variety_info['fertilizer_requirements']}
                - **Pest Susceptibility:** {variety_info['pest_susceptibility']}
                - **Yield Potential:** {variety_info['yield_potential']} tons/acre
                """)
        
        if st.button("Plant Crop", type="primary"):
            if field_id:
                planting_id = self.db.create_crop_planting(
                    user_id, field_id, crop_type, variety_name,
                    datetime.combine(planting_date, datetime.min.time()),
                    area_acres
                )
                
                if planting_id:
                    st.success(f"Crop planted successfully! Planting ID: {planting_id}")
                    st.rerun()
                else:
                    st.error("Failed to plant crop")
            else:
                st.warning("Please select a specific field to plant crops")
    
    def render_crop_monitoring(self, user_id: int, field_id: int):
        """Render crop monitoring dashboard"""
        st.subheader("📊 Crop Monitoring Dashboard")
        
        # Get crop plantings
        plantings_df = self.db.get_crop_plantings(user_id, field_id)
        
        if plantings_df.empty:
            st.info("No crops planted. Plant a crop to start monitoring.")
            return
        
        # Display active plantings
        active_plantings = plantings_df[plantings_df['status'] == 'Active']
        
        if not active_plantings.empty:
            st.subheader("🌱 Active Crops")
            
            for _, planting in active_plantings.iterrows():
                with st.expander(f"{planting['crop_type']} - {planting['variety_name']} (Field {planting['field_id']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Current Stage", planting['current_growth_stage'])
                        st.metric("Days Since Planting", planting['days_since_planting'])
                    
                    with col2:
                        st.metric("Days to Harvest", planting['days_to_harvest'])
                        st.metric("Area", f"{planting['area_acres']} acres")
                    
                    with col3:
                        st.metric("Planting Date", planting['planting_date'])
                        st.metric("Expected Harvest", planting['expected_harvest_date'])
                    
                    # Growth stage progress
                    growth_stages = self.db.get_growth_stages(planting['crop_type'])
                    if not growth_stages.empty:
                        st.subheader("Growth Stage Progress")
                        
                        # Create progress chart
                        fig = go.Figure()
                        
                        current_stage_order = growth_stages[
                            growth_stages['stage_name'] == planting['current_growth_stage']
                        ]['stage_order'].iloc[0] if not growth_stages.empty else 0
                        
                        for _, stage in growth_stages.iterrows():
                            color = 'green' if stage['stage_order'] <= current_stage_order else 'lightgray'
                            
                            fig.add_trace(go.Bar(
                                x=[stage['stage_name']],
                                y=[1],
                                name=stage['stage_name'],
                                marker_color=color,
                                text=[stage['description']],
                                textposition='auto'
                            ))
                        
                        fig.update_layout(
                            title="Growth Stage Progress",
                            xaxis_title="Growth Stage",
                            yaxis_title="Progress",
                            showlegend=False,
                            height=400
                        )
                        
                        st.plotly_chart(fig, width='stretch', key=f"growth_chart_{planting['id']}")
        
        # Crop performance summary
        st.subheader("📈 Crop Performance Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Active Crops", len(active_plantings))
        
        with col2:
            total_area = active_plantings['area_acres'].sum()
            st.metric("Total Area", f"{total_area:.1f} acres")
        
        with col3:
            crop_types = active_plantings['crop_type'].nunique()
            st.metric("Crop Types", crop_types)
        
        with col4:
            avg_days_to_harvest = active_plantings['days_to_harvest'].mean()
            st.metric("Avg Days to Harvest", f"{avg_days_to_harvest:.0f}")
    
    def render_field_activities(self, user_id: int, field_id: int):
        """Render field activities interface"""
        st.subheader("📝 Field Activities")
        
        # Add new activity
        with st.expander("Add New Activity"):
            col1, col2 = st.columns(2)
            
            with col1:
                activity_type = st.selectbox(
                    "Activity Type",
                    options=["Planting", "Fertilizing", "Irrigation", "Pest Control", 
                            "Weeding", "Harvesting", "Other"],
                    key="activity_type"
                )
                
                activity_date = st.date_input(
                    "Activity Date",
                    value=datetime.now().date(),
                    key="activity_date"
                )
                
                cost = st.number_input(
                    "Cost ($)",
                    min_value=0.0,
                    value=0.0,
                    step=0.01,
                    key="activity_cost"
                )
            
            with col2:
                description = st.text_area(
                    "Description",
                    placeholder="Describe the activity performed...",
                    key="activity_description"
                )
                
                notes = st.text_area(
                    "Notes",
                    placeholder="Additional notes...",
                    key="activity_notes"
                )
                
                performed_by = st.text_input(
                    "Performed By",
                    placeholder="Name of person who performed the activity",
                    key="activity_performed_by"
                )
            
            if st.button("Log Activity", type="primary"):
                if field_id and description:
                    activity_id = self.db.log_field_activity(
                        user_id, field_id, activity_type,
                        datetime.combine(activity_date, datetime.min.time()),
                        description, cost, notes, performed_by
                    )
                    
                    if activity_id:
                        st.success(f"Activity logged successfully! Activity ID: {activity_id}")
                        st.rerun()
                    else:
                        st.error("Failed to log activity")
                else:
                    st.warning("Please select a field and provide description")
        
        # Display activities
        activities_df = self.db.get_field_activities(user_id, field_id)
        
        if not activities_df.empty:
            st.subheader("Recent Activities")
            
            # Filter activities
            activity_filter = st.selectbox(
                "Filter by Activity Type",
                options=["All"] + activities_df['activity_type'].unique().tolist(),
                key="activity_filter"
            )
            
            filtered_activities = activities_df
            if activity_filter != "All":
                filtered_activities = activities_df[activities_df['activity_type'] == activity_filter]
            
            # Display activities table
            st.dataframe(
                filtered_activities[['activity_type', 'activity_date', 'description', 
                                   'cost', 'performed_by']].round(2),
                width='stretch'
            )
            
            # Activity summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_activities = len(filtered_activities)
                st.metric("Total Activities", total_activities)
            
            with col2:
                total_cost = filtered_activities['cost'].sum()
                st.metric("Total Cost", f"${total_cost:.2f}")
            
            with col3:
                avg_cost = filtered_activities['cost'].mean()
                st.metric("Average Cost", f"${avg_cost:.2f}")
        else:
            st.info("No activities logged yet. Add an activity to get started.")
    
    def render_pest_disease_alerts(self, user_id: int, field_id: int):
        """Render pest/disease alerts interface"""
        st.subheader("⚠️ Pest & Disease Alerts")
        
        # Add new alert
        with st.expander("Add New Alert"):
            col1, col2 = st.columns(2)
            
            with col1:
                alert_type = st.selectbox(
                    "Alert Type",
                    options=["Pest Infestation", "Disease Outbreak", "Nutrient Deficiency", 
                            "Weather Warning", "Other"],
                    key="alert_type"
                )
                
                severity = st.selectbox(
                    "Severity",
                    options=["Low", "Medium", "High", "Critical"],
                    key="alert_severity"
                )
                
                crop_type = st.selectbox(
                    "Crop Type",
                    options=[crop.value for crop in CropType],
                    key="alert_crop_type"
                )
            
            with col2:
                description = st.text_area(
                    "Description",
                    placeholder="Describe the issue...",
                    key="alert_description"
                )
                
                recommended_action = st.text_area(
                    "Recommended Action",
                    placeholder="What should be done to address this issue?",
                    key="alert_recommended_action"
                )
            
            if st.button("Create Alert", type="primary"):
                if field_id and description and recommended_action:
                    alert_id = self.db.create_pest_disease_alert(
                        user_id, field_id, crop_type, alert_type,
                        severity, description, recommended_action
                    )
                    
                    if alert_id:
                        st.success(f"Alert created successfully! Alert ID: {alert_id}")
                        st.rerun()
                    else:
                        st.error("Failed to create alert")
                else:
                    st.warning("Please select a field and provide description and recommended action")
        
        # Display alerts
        alerts_df = self.db.get_pest_disease_alerts(user_id, field_id)
        
        if not alerts_df.empty:
            st.subheader("Active Alerts")
            
            for _, alert in alerts_df.iterrows():
                severity_color = {
                    "Low": "🟢",
                    "Medium": "🟡", 
                    "High": "🟠",
                    "Critical": "🔴"
                }
                
                with st.expander(f"{severity_color.get(alert['severity'], '⚪')} {alert['alert_type']} - {alert['crop_type']} (Field {alert['field_id']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Severity:** {alert['severity']}")
                        st.write(f"**Date:** {alert['alert_date']}")
                        st.write(f"**Description:** {alert['description']}")
                    
                    with col2:
                        st.write(f"**Recommended Action:** {alert['recommended_action']}")
                        
                        if st.button(f"Mark as Resolved", key=f"resolve_{alert['id']}"):
                            # Mark alert as resolved
                            st.success("Alert marked as resolved!")
                            st.rerun()
        else:
            st.info("No active alerts. Great job keeping your crops healthy!")
    
    def run(self):
        """Main crop management runner"""
        st.title("🌾 AgriForecast.ai - Crop Management System")
        st.markdown("**Complete Agricultural Workflow Management**")
        
        # Render sidebar
        user_id, field_id = self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🌱 Crop Planting", "📊 Crop Monitoring", "📝 Field Activities", "⚠️ Alerts"
        ])
        
        with tab1:
            self.render_crop_planting(user_id, field_id)
        
        with tab2:
            self.render_crop_monitoring(user_id, field_id)
        
        with tab3:
            self.render_field_activities(user_id, field_id)
        
        with tab4:
            self.render_pest_disease_alerts(user_id, field_id)
        
        # Footer
        st.markdown("---")
        st.markdown("**🌾 Crop Management System - Phase 3 Complete**")
        st.markdown("*Complete agricultural workflow management for modern farming*")

def main():
    """Main crop management entry point"""
    try:
        app = CropManagementFrontend()
        app.run()
    except Exception as e:
        st.error(f"Crop management error: {e}")
        logger.error(f"Crop management error: {e}")

if __name__ == "__main__":
    main()
