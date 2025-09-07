#!/usr/bin/env python3
"""
IoT Integration System for AgriForecast.ai
Phase 3: Advanced Agricultural Features
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

class IoTDeviceType(Enum):
    WEATHER_STATION = "Weather Station"
    SOIL_SENSOR = "Soil Sensor"
    DRONE = "Drone"
    CAMERA = "Camera"
    IRRIGATION_CONTROLLER = "Irrigation Controller"
    FERTILIZER_SPREADER = "Fertilizer Spreader"

class IoTIntegrationSystem:
    """IoT device integration and data collection system"""
    
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Setup IoT integration database"""
        self.conn = sqlite3.connect('agriforecast_iot_integration.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create IoT integration tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS iot_devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                device_name TEXT NOT NULL,
                device_type TEXT NOT NULL,
                device_id TEXT UNIQUE NOT NULL,
                location_lat REAL,
                location_lon REAL,
                status TEXT DEFAULT 'Active',
                last_seen TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                data_type TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                quality_score REAL DEFAULT 1.0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_station_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                pressure REAL NOT NULL,
                wind_speed REAL NOT NULL,
                wind_direction REAL NOT NULL,
                rainfall REAL NOT NULL,
                solar_radiation REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS soil_sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                soil_moisture REAL NOT NULL,
                soil_temperature REAL NOT NULL,
                ph_level REAL NOT NULL,
                electrical_conductivity REAL NOT NULL,
                nitrogen_level REAL NOT NULL,
                phosphorus_level REAL NOT NULL,
                potassium_level REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drone_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                flight_date DATE NOT NULL,
                ndvi_value REAL NOT NULL,
                crop_health_score REAL NOT NULL,
                coverage_area REAL NOT NULL,
                image_count INTEGER NOT NULL,
                flight_duration REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                alert_data TEXT,
                status TEXT DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("IoT integration database setup completed")
    
    def register_device(self, user_id: int, field_id: int, device_name: str, 
                       device_type: str, location_lat: float = None, 
                       location_lon: float = None) -> str:
        """Register a new IoT device"""
        try:
            cursor = self.conn.cursor()
            
            # Generate unique device ID
            device_id = f"{device_type}_{user_id}_{field_id}_{int(datetime.now().timestamp())}"
            
            cursor.execute('''
                INSERT INTO iot_devices (user_id, field_id, device_name, device_type, 
                                       device_id, location_lat, location_lon)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, field_id, device_name, device_type, device_id, 
                  location_lat, location_lon))
            
            self.conn.commit()
            
            logger.info(f"Registered device: {device_name} ({device_id})")
            return device_id
            
        except Exception as e:
            logger.error(f"Error registering device: {e}")
            return ""
    
    def get_devices(self, user_id: int, field_id: int = None) -> pd.DataFrame:
        """Get IoT devices for user"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT * FROM iot_devices 
                    WHERE user_id = ? AND field_id = ? 
                    ORDER BY created_at DESC
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT * FROM iot_devices 
                    WHERE user_id = ? 
                    ORDER BY created_at DESC
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting devices: {e}")
            return pd.DataFrame()
    
    def simulate_weather_station_data(self, device_id: str) -> Dict:
        """Simulate weather station data"""
        try:
            # Simulate realistic weather data
            base_temp = 25.0 + np.random.normal(0, 5)  # Base temperature around 25°C
            humidity = max(0, min(100, 60 + np.random.normal(0, 15)))
            pressure = 1013.25 + np.random.normal(0, 10)
            wind_speed = max(0, np.random.exponential(5))
            wind_direction = np.random.uniform(0, 360)
            rainfall = max(0, np.random.exponential(2))
            solar_radiation = max(0, np.random.uniform(0, 1000))
            
            # Save to database
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO weather_station_data (device_id, temperature, humidity, pressure,
                                                wind_speed, wind_direction, rainfall, solar_radiation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (device_id, base_temp, humidity, pressure, wind_speed, 
                  wind_direction, rainfall, solar_radiation))
            
            self.conn.commit()
            
            return {
                'temperature': round(base_temp, 1),
                'humidity': round(humidity, 1),
                'pressure': round(pressure, 1),
                'wind_speed': round(wind_speed, 1),
                'wind_direction': round(wind_direction, 1),
                'rainfall': round(rainfall, 1),
                'solar_radiation': round(solar_radiation, 1)
            }
            
        except Exception as e:
            logger.error(f"Error simulating weather station data: {e}")
            return {}
    
    def simulate_soil_sensor_data(self, device_id: str) -> Dict:
        """Simulate soil sensor data"""
        try:
            # Simulate realistic soil data
            soil_moisture = max(0, min(100, 40 + np.random.normal(0, 10)))
            soil_temp = 20.0 + np.random.normal(0, 3)
            ph_level = 6.5 + np.random.normal(0, 0.5)
            electrical_conductivity = max(0, 0.5 + np.random.normal(0, 0.2))
            nitrogen = max(0, 50 + np.random.normal(0, 15))
            phosphorus = max(0, 25 + np.random.normal(0, 8))
            potassium = max(0, 150 + np.random.normal(0, 30))
            
            # Save to database
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO soil_sensor_data (device_id, soil_moisture, soil_temperature,
                                            ph_level, electrical_conductivity, nitrogen_level,
                                            phosphorus_level, potassium_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (device_id, soil_moisture, soil_temp, ph_level, electrical_conductivity,
                  nitrogen, phosphorus, potassium))
            
            self.conn.commit()
            
            return {
                'soil_moisture': round(soil_moisture, 1),
                'soil_temperature': round(soil_temp, 1),
                'ph_level': round(ph_level, 1),
                'electrical_conductivity': round(electrical_conductivity, 2),
                'nitrogen': round(nitrogen, 1),
                'phosphorus': round(phosphorus, 1),
                'potassium': round(potassium, 1)
            }
            
        except Exception as e:
            logger.error(f"Error simulating soil sensor data: {e}")
            return {}
    
    def simulate_drone_data(self, device_id: str) -> Dict:
        """Simulate drone data"""
        try:
            # Simulate drone flight data
            ndvi_value = max(0, min(1, 0.6 + np.random.normal(0, 0.2)))
            crop_health_score = max(0, min(100, 75 + np.random.normal(0, 15)))
            coverage_area = np.random.uniform(10, 50)  # acres
            image_count = np.random.randint(50, 200)
            flight_duration = np.random.uniform(15, 45)  # minutes
            
            # Save to database
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO drone_data (device_id, flight_date, ndvi_value, crop_health_score,
                                      coverage_area, image_count, flight_duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (device_id, datetime.now().date(), ndvi_value, crop_health_score,
                  coverage_area, image_count, flight_duration))
            
            self.conn.commit()
            
            return {
                'ndvi_value': round(ndvi_value, 3),
                'crop_health_score': round(crop_health_score, 1),
                'coverage_area': round(coverage_area, 1),
                'image_count': image_count,
                'flight_duration': round(flight_duration, 1)
            }
            
        except Exception as e:
            logger.error(f"Error simulating drone data: {e}")
            return {}
    
    def get_device_data(self, device_id: str, data_type: str = None) -> pd.DataFrame:
        """Get data from a specific device"""
        try:
            cursor = self.conn.cursor()
            
            if data_type == "weather":
                query = '''
                    SELECT * FROM weather_station_data 
                    WHERE device_id = ? 
                    ORDER BY timestamp DESC
                '''
            elif data_type == "soil":
                query = '''
                    SELECT * FROM soil_sensor_data 
                    WHERE device_id = ? 
                    ORDER BY timestamp DESC
                '''
            elif data_type == "drone":
                query = '''
                    SELECT * FROM drone_data 
                    WHERE device_id = ? 
                    ORDER BY timestamp DESC
                '''
            else:
                query = '''
                    SELECT * FROM device_data 
                    WHERE device_id = ? 
                    ORDER BY timestamp DESC
                '''
            
            cursor.execute(query, (device_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting device data: {e}")
            return pd.DataFrame()
    
    def create_device_alert(self, device_id: str, alert_type: str, severity: str, 
                           message: str, alert_data: str = "") -> int:
        """Create a device alert"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT INTO device_alerts (device_id, alert_type, severity, message, alert_data)
                VALUES (?, ?, ?, ?, ?)
            ''', (device_id, alert_type, severity, message, alert_data))
            
            alert_id = cursor.lastrowid
            self.conn.commit()
            
            logger.info(f"Created alert for device {device_id}: {message}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Error creating device alert: {e}")
            return 0

class IoTIntegrationFrontend:
    """IoT integration frontend"""
    
    def __init__(self):
        self.iot_system = IoTIntegrationSystem()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast IoT Integration",
            page_icon="📡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render IoT integration sidebar"""
        st.sidebar.title("📡 IoT Integration")
        
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
    
    def render_device_management(self, user_id: int, field_id: int):
        """Render device management interface"""
        st.subheader("📱 Device Management")
        
        # Add new device
        with st.expander("Register New Device"):
            col1, col2 = st.columns(2)
            
            with col1:
                device_name = st.text_input(
                    "Device Name",
                    placeholder="e.g., Weather Station 1",
                    key="device_name"
                )
                
                device_type = st.selectbox(
                    "Device Type",
                    options=[device.value for device in IoTDeviceType],
                    key="device_type"
                )
            
            with col2:
                location_lat = st.number_input(
                    "Latitude",
                    min_value=-90.0,
                    max_value=90.0,
                    value=28.368911,
                    step=0.000001,
                    key="location_lat"
                )
                
                location_lon = st.number_input(
                    "Longitude",
                    min_value=-180.0,
                    max_value=180.0,
                    value=77.541033,
                    step=0.000001,
                    key="location_lon"
                )
            
            if st.button("Register Device", type="primary"):
                if device_name and field_id:
                    device_id = self.iot_system.register_device(
                        user_id, field_id, device_name, device_type,
                        location_lat, location_lon
                    )
                    
                    if device_id:
                        st.success(f"Device registered successfully! Device ID: {device_id}")
                        st.rerun()
                    else:
                        st.error("Failed to register device")
                else:
                    st.warning("Please provide device name and select a field")
        
        # Display devices
        devices_df = self.iot_system.get_devices(user_id, field_id)
        
        if not devices_df.empty:
            st.subheader("📱 Registered Devices")
            st.dataframe(
                devices_df[['device_name', 'device_type', 'device_id', 'status', 'created_at']],
                width='stretch'
            )
        else:
            st.info("No devices registered. Register a device to get started.")
    
    def render_data_collection(self, user_id: int, field_id: int):
        """Render data collection interface"""
        st.subheader("📊 Data Collection")
        
        # Get devices
        devices_df = self.iot_system.get_devices(user_id, field_id)
        
        if devices_df.empty:
            st.info("No devices available. Register a device first.")
            return
        
        # Device selection
        device_options = devices_df['device_name'].tolist()
        selected_device = st.selectbox("Select Device", device_options)
        
        if selected_device:
            device_info = devices_df[devices_df['device_name'] == selected_device].iloc[0]
            device_id = device_info['device_id']
            device_type = device_info['device_type']
            
            st.subheader(f"📡 {selected_device} - {device_type}")
            
            # Collect data based on device type
            if device_type == "Weather Station":
                if st.button("Collect Weather Data", type="primary"):
                    data = self.iot_system.simulate_weather_station_data(device_id)
                    
                    if data:
                        st.success("Weather data collected successfully!")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Temperature", f"{data['temperature']}°C")
                            st.metric("Humidity", f"{data['humidity']}%")
                        
                        with col2:
                            st.metric("Pressure", f"{data['pressure']} hPa")
                            st.metric("Wind Speed", f"{data['wind_speed']} m/s")
                        
                        with col3:
                            st.metric("Wind Direction", f"{data['wind_direction']}°")
                            st.metric("Rainfall", f"{data['rainfall']} mm")
                        
                        with col4:
                            st.metric("Solar Radiation", f"{data['solar_radiation']} W/m²")
                    else:
                        st.error("Failed to collect weather data")
            
            elif device_type == "Soil Sensor":
                if st.button("Collect Soil Data", type="primary"):
                    data = self.iot_system.simulate_soil_sensor_data(device_id)
                    
                    if data:
                        st.success("Soil data collected successfully!")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Soil Moisture", f"{data['soil_moisture']}%")
                            st.metric("Soil Temperature", f"{data['soil_temperature']}°C")
                        
                        with col2:
                            st.metric("pH Level", f"{data['ph_level']}")
                            st.metric("EC", f"{data['electrical_conductivity']} mS/cm")
                        
                        with col3:
                            st.metric("Nitrogen", f"{data['nitrogen']} ppm")
                            st.metric("Phosphorus", f"{data['phosphorus']} ppm")
                        
                        with col4:
                            st.metric("Potassium", f"{data['potassium']} ppm")
                    else:
                        st.error("Failed to collect soil data")
            
            elif device_type == "Drone":
                if st.button("Collect Drone Data", type="primary"):
                    data = self.iot_system.simulate_drone_data(device_id)
                    
                    if data:
                        st.success("Drone data collected successfully!")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("NDVI Value", f"{data['ndvi_value']}")
                            st.metric("Crop Health Score", f"{data['crop_health_score']}%")
                        
                        with col2:
                            st.metric("Coverage Area", f"{data['coverage_area']} acres")
                            st.metric("Image Count", f"{data['image_count']}")
                        
                        with col3:
                            st.metric("Flight Duration", f"{data['flight_duration']} min")
                    else:
                        st.error("Failed to collect drone data")
            
            else:
                st.info(f"Data collection for {device_type} devices will be implemented soon.")
    
    def render_data_visualization(self, user_id: int, field_id: int):
        """Render data visualization"""
        st.subheader("📊 Data Visualization")
        
        # Get devices
        devices_df = self.iot_system.get_devices(user_id, field_id)
        
        if devices_df.empty:
            st.info("No devices available. Register a device first.")
            return
        
        # Device selection
        device_options = devices_df['device_name'].tolist()
        selected_device = st.selectbox("Select Device for Visualization", device_options)
        
        if selected_device:
            device_info = devices_df[devices_df['device_name'] == selected_device].iloc[0]
            device_id = device_info['device_id']
            device_type = device_info['device_type']
            
            # Get historical data
            if device_type == "Weather Station":
                data_df = self.iot_system.get_device_data(device_id, "weather")
                
                if not data_df.empty:
                    st.subheader("🌤️ Weather Data Trends")
                    
                    # Temperature and humidity chart
                    fig = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=('Temperature', 'Humidity', 'Pressure', 'Wind Speed'),
                        vertical_spacing=0.1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=data_df['timestamp'], y=data_df['temperature'], 
                                 name='Temperature', line=dict(color='red')),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=data_df['timestamp'], y=data_df['humidity'], 
                                 name='Humidity', line=dict(color='blue')),
                        row=1, col=2
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=data_df['timestamp'], y=data_df['pressure'], 
                                 name='Pressure', line=dict(color='green')),
                        row=2, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=data_df['timestamp'], y=data_df['wind_speed'], 
                                 name='Wind Speed', line=dict(color='orange')),
                        row=2, col=2
                    )
                    
                    fig.update_layout(height=600, showlegend=False)
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("No weather data available. Collect some data first.")
            
            elif device_type == "Soil Sensor":
                data_df = self.iot_system.get_device_data(device_id, "soil")
                
                if not data_df.empty:
                    st.subheader("🌱 Soil Data Trends")
                    
                    # Soil parameters chart
                    fig = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=('Soil Moisture', 'pH Level', 'Nitrogen', 'Phosphorus'),
                        vertical_spacing=0.1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=data_df['timestamp'], y=data_df['soil_moisture'], 
                                 name='Soil Moisture', line=dict(color='blue')),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=data_df['timestamp'], y=data_df['ph_level'], 
                                 name='pH Level', line=dict(color='green')),
                        row=1, col=2
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=data_df['timestamp'], y=data_df['nitrogen_level'], 
                                 name='Nitrogen', line=dict(color='red')),
                        row=2, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=data_df['timestamp'], y=data_df['phosphorus_level'], 
                                 name='Phosphorus', line=dict(color='orange')),
                        row=2, col=2
                    )
                    
                    fig.update_layout(height=600, showlegend=False)
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("No soil data available. Collect some data first.")
            
            else:
                st.info(f"Visualization for {device_type} devices will be implemented soon.")
    
    def run(self):
        """Main IoT integration runner"""
        st.title("📡 AgriForecast.ai - IoT Integration")
        st.markdown("**Smart Device Integration & Data Collection**")
        
        # Render sidebar
        user_id, field_id = self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs([
            "📱 Device Management", "📊 Data Collection", "📈 Data Visualization"
        ])
        
        with tab1:
            self.render_device_management(user_id, field_id)
        
        with tab2:
            self.render_data_collection(user_id, field_id)
        
        with tab3:
            self.render_data_visualization(user_id, field_id)
        
        # Footer
        st.markdown("---")
        st.markdown("**📡 IoT Integration System - Phase 3 Advanced Features**")
        st.markdown("*Smart device integration and automated data collection*")

def main():
    """Main IoT integration entry point"""
    try:
        app = IoTIntegrationFrontend()
        app.run()
    except Exception as e:
        st.error(f"IoT integration error: {e}")
        logger.error(f"IoT integration error: {e}")

if __name__ == "__main__":
    main()
