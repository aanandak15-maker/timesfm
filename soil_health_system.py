#!/usr/bin/env python3
"""
Soil Health Monitoring System for AgriForecast.ai
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

class SoilHealthSystem:
    """Soil health monitoring and management system"""
    
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Setup soil health database"""
        self.conn = sqlite3.connect('agriforecast_soil_health.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create soil health tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS soil_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                test_date DATE NOT NULL,
                ph_level REAL NOT NULL,
                nitrogen_level REAL NOT NULL,
                phosphorus_level REAL NOT NULL,
                potassium_level REAL NOT NULL,
                organic_matter REAL NOT NULL,
                soil_texture TEXT NOT NULL,
                moisture_content REAL NOT NULL,
                test_lab TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fertilizer_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                crop_type TEXT NOT NULL,
                growth_stage TEXT NOT NULL,
                fertilizer_type TEXT NOT NULL,
                application_rate REAL NOT NULL,
                application_method TEXT NOT NULL,
                application_date DATE NOT NULL,
                cost_per_acre REAL NOT NULL,
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
        
        self.conn.commit()
        logger.info("Soil health database setup completed")
    
    def add_soil_test(self, user_id: int, field_id: int, test_date: datetime,
                     ph_level: float, nitrogen: float, phosphorus: float, 
                     potassium: float, organic_matter: float, soil_texture: str,
                     moisture_content: float, test_lab: str = "", notes: str = "") -> int:
        """Add soil test results"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT INTO soil_tests (user_id, field_id, test_date, ph_level, nitrogen_level,
                                      phosphorus_level, potassium_level, organic_matter,
                                      soil_texture, moisture_content, test_lab, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, field_id, test_date.date(), ph_level, nitrogen, phosphorus,
                  potassium, organic_matter, soil_texture, moisture_content, test_lab, notes))
            
            test_id = cursor.lastrowid
            self.conn.commit()
            
            logger.info(f"Added soil test for field {field_id}")
            return test_id
            
        except Exception as e:
            logger.error(f"Error adding soil test: {e}")
            return 0
    
    def get_soil_tests(self, user_id: int, field_id: int = None) -> pd.DataFrame:
        """Get soil test results"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT * FROM soil_tests 
                    WHERE user_id = ? AND field_id = ? 
                    ORDER BY test_date DESC
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT * FROM soil_tests 
                    WHERE user_id = ? 
                    ORDER BY test_date DESC
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting soil tests: {e}")
            return pd.DataFrame()
    
    def generate_fertilizer_recommendations(self, user_id: int, field_id: int, 
                                          crop_type: str, growth_stage: str) -> List[Dict]:
        """Generate fertilizer recommendations based on soil test"""
        try:
            # Get latest soil test
            soil_tests = self.get_soil_tests(user_id, field_id)
            
            if soil_tests.empty:
                return []
            
            latest_test = soil_tests.iloc[0]
            
            recommendations = []
            
            # Nitrogen recommendations
            if latest_test['nitrogen_level'] < 50:
                recommendations.append({
                    'fertilizer_type': 'Urea (46-0-0)',
                    'application_rate': 100.0,
                    'application_method': 'Broadcast',
                    'cost_per_acre': 25.0
                })
            elif latest_test['nitrogen_level'] < 75:
                recommendations.append({
                    'fertilizer_type': 'Urea (46-0-0)',
                    'application_rate': 75.0,
                    'application_method': 'Broadcast',
                    'cost_per_acre': 18.75
                })
            
            # Phosphorus recommendations
            if latest_test['phosphorus_level'] < 20:
                recommendations.append({
                    'fertilizer_type': 'DAP (18-46-0)',
                    'application_rate': 50.0,
                    'application_method': 'Band placement',
                    'cost_per_acre': 30.0
                })
            elif latest_test['phosphorus_level'] < 35:
                recommendations.append({
                    'fertilizer_type': 'DAP (18-46-0)',
                    'application_rate': 35.0,
                    'application_method': 'Band placement',
                    'cost_per_acre': 21.0
                })
            
            # Potassium recommendations
            if latest_test['potassium_level'] < 150:
                recommendations.append({
                    'fertilizer_type': 'MOP (0-0-60)',
                    'application_rate': 40.0,
                    'application_method': 'Broadcast',
                    'cost_per_acre': 20.0
                })
            elif latest_test['potassium_level'] < 200:
                recommendations.append({
                    'fertilizer_type': 'MOP (0-0-60)',
                    'application_rate': 25.0,
                    'application_method': 'Broadcast',
                    'cost_per_acre': 12.5
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating fertilizer recommendations: {e}")
            return []

class SoilHealthFrontend:
    """Soil health frontend"""
    
    def __init__(self):
        self.db = SoilHealthSystem()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast Soil Health",
            page_icon="🌱",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render soil health sidebar"""
        st.sidebar.title("🌱 Soil Health")
        
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
    
    def render_soil_testing(self, user_id: int, field_id: int):
        """Render soil testing interface"""
        st.subheader("🧪 Soil Testing")
        
        with st.expander("Add New Soil Test"):
            col1, col2 = st.columns(2)
            
            with col1:
                test_date = st.date_input(
                    "Test Date",
                    value=datetime.now().date(),
                    key="test_date"
                )
                
                ph_level = st.slider(
                    "pH Level",
                    min_value=4.0,
                    max_value=9.0,
                    value=6.5,
                    step=0.1,
                    key="ph_level"
                )
                
                nitrogen = st.number_input(
                    "Nitrogen (ppm)",
                    min_value=0.0,
                    max_value=200.0,
                    value=50.0,
                    step=1.0,
                    key="nitrogen"
                )
                
                phosphorus = st.number_input(
                    "Phosphorus (ppm)",
                    min_value=0.0,
                    max_value=100.0,
                    value=25.0,
                    step=1.0,
                    key="phosphorus"
                )
            
            with col2:
                potassium = st.number_input(
                    "Potassium (ppm)",
                    min_value=0.0,
                    max_value=500.0,
                    value=150.0,
                    step=1.0,
                    key="potassium"
                )
                
                organic_matter = st.number_input(
                    "Organic Matter (%)",
                    min_value=0.0,
                    max_value=10.0,
                    value=2.5,
                    step=0.1,
                    key="organic_matter"
                )
                
                soil_texture = st.selectbox(
                    "Soil Texture",
                    options=["Clay", "Sandy Clay", "Silty Clay", "Sandy Clay Loam", 
                            "Clay Loam", "Silty Clay Loam", "Sandy Loam", "Loam", 
                            "Silty Loam", "Sandy", "Silty"],
                    key="soil_texture"
                )
                
                moisture_content = st.number_input(
                    "Moisture Content (%)",
                    min_value=0.0,
                    max_value=50.0,
                    value=15.0,
                    step=0.1,
                    key="moisture_content"
                )
            
            test_lab = st.text_input(
                "Test Lab",
                placeholder="Name of testing laboratory",
                key="test_lab"
            )
            
            notes = st.text_area(
                "Notes",
                placeholder="Additional notes about the soil test...",
                key="test_notes"
            )
            
            if st.button("Add Soil Test", type="primary"):
                if field_id:
                    test_id = self.db.add_soil_test(
                        user_id, field_id, datetime.combine(test_date, datetime.min.time()),
                        ph_level, nitrogen, phosphorus, potassium, organic_matter,
                        soil_texture, moisture_content, test_lab, notes
                    )
                    
                    if test_id:
                        st.success(f"Soil test added successfully! Test ID: {test_id}")
                        st.rerun()
                    else:
                        st.error("Failed to add soil test")
                else:
                    st.warning("Please select a specific field to add soil test")
        
        # Display soil tests
        soil_tests = self.db.get_soil_tests(user_id, field_id)
        
        if not soil_tests.empty:
            st.subheader("📊 Soil Test History")
            st.dataframe(
                soil_tests[['test_date', 'ph_level', 'nitrogen_level', 'phosphorus_level',
                           'potassium_level', 'organic_matter', 'soil_texture']].round(2),
                width='stretch'
            )
        else:
            st.info("No soil tests available. Add a soil test to get started.")
    
    def render_fertilizer_recommendations(self, user_id: int, field_id: int):
        """Render fertilizer recommendations"""
        st.subheader("💊 Fertilizer Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            crop_type = st.selectbox(
                "Crop Type",
                options=["Rice", "Wheat", "Corn", "Soybean", "Cotton", "Sugarcane"],
                key="fertilizer_crop_type"
            )
        
        with col2:
            growth_stage = st.selectbox(
                "Growth Stage",
                options=["Planting", "Vegetative", "Flowering", "Fruiting", "Maturity"],
                key="fertilizer_growth_stage"
            )
        
        if st.button("Generate Recommendations", type="primary"):
            if field_id:
                recommendations = self.db.generate_fertilizer_recommendations(
                    user_id, field_id, crop_type, growth_stage
                )
                
                if recommendations:
                    st.success("Fertilizer recommendations generated!")
                    
                    for i, rec in enumerate(recommendations):
                        with st.expander(f"Recommendation {i+1}: {rec['fertilizer_type']}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Application Rate", f"{rec['application_rate']} kg/acre")
                                st.metric("Application Method", rec['application_method'])
                            
                            with col2:
                                st.metric("Cost per Acre", f"${rec['cost_per_acre']}")
                            
                            with col3:
                                if st.button(f"Apply Recommendation", key=f"apply_{i}"):
                                    st.success("Recommendation applied!")
                else:
                    st.warning("No recommendations available. Add soil test data first.")
            else:
                st.warning("Please select a specific field to generate recommendations")
    
    def run(self):
        """Main soil health runner"""
        st.title("🌱 AgriForecast.ai - Soil Health Monitoring")
        st.markdown("**Comprehensive Soil Health Management**")
        
        # Render sidebar
        user_id, field_id = self.render_sidebar()
        
        # Main content tabs
        tab1, tab2 = st.tabs(["🧪 Soil Testing", "💊 Fertilizer Recommendations"])
        
        with tab1:
            self.render_soil_testing(user_id, field_id)
        
        with tab2:
            self.render_fertilizer_recommendations(user_id, field_id)
        
        # Footer
        st.markdown("---")
        st.markdown("**🌱 Soil Health System - Phase 3 Complete**")
        st.markdown("*Precision soil health management for optimal crop production*")

def main():
    """Main soil health entry point"""
    try:
        app = SoilHealthFrontend()
        app.run()
    except Exception as e:
        st.error(f"Soil health error: {e}")
        logger.error(f"Soil health error: {e}")

if __name__ == "__main__":
    main()




