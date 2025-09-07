#!/usr/bin/env python3
"""
Offline Capability System for AgriForecast.ai
Critical Feature: Field work without internet connection
"""

import streamlit as st
import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import hashlib
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OfflineCapabilitySystem:
    """Offline data collection and synchronization system"""
    
    def __init__(self):
        self.setup_offline_database()
        
    def setup_offline_database(self):
        """Setup offline data storage"""
        self.conn = sqlite3.connect('agriforecast_offline.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create offline data tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_field_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                data_type TEXT NOT NULL,
                data_json TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                synced BOOLEAN DEFAULT FALSE,
                sync_timestamp TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                activity_type TEXT NOT NULL,
                activity_data TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                synced BOOLEAN DEFAULT FALSE,
                sync_timestamp TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                photo_data BLOB NOT NULL,
                photo_metadata TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                synced BOOLEAN DEFAULT FALSE,
                sync_timestamp TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                record_id INTEGER NOT NULL,
                operation TEXT NOT NULL,
                data_json TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                retry_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        self.conn.commit()
        logger.info("Offline capability database setup completed")
    
    def save_offline_data(self, user_id: int, field_id: int, data_type: str, data: Dict) -> int:
        """Save data for offline synchronization"""
        try:
            cursor = self.conn.cursor()
            
            data_json = json.dumps(data)
            
            cursor.execute('''
                INSERT INTO offline_field_data (user_id, field_id, data_type, data_json)
                VALUES (?, ?, ?, ?)
            ''', (user_id, field_id, data_type, data_json))
            
            record_id = cursor.lastrowid
            
            # Add to sync queue
            cursor.execute('''
                INSERT INTO sync_queue (table_name, record_id, operation, data_json)
                VALUES (?, ?, ?, ?)
            ''', ('offline_field_data', record_id, 'INSERT', data_json))
            
            self.conn.commit()
            
            logger.info(f"Saved offline data: {data_type} for field {field_id}")
            return record_id
            
        except Exception as e:
            logger.error(f"Error saving offline data: {e}")
            return 0
    
    def save_offline_activity(self, user_id: int, field_id: int, activity_type: str, activity_data: Dict) -> int:
        """Save field activity for offline synchronization"""
        try:
            cursor = self.conn.cursor()
            
            activity_json = json.dumps(activity_data)
            
            cursor.execute('''
                INSERT INTO offline_activities (user_id, field_id, activity_type, activity_data)
                VALUES (?, ?, ?, ?)
            ''', (user_id, field_id, activity_type, activity_json))
            
            record_id = cursor.lastrowid
            
            # Add to sync queue
            cursor.execute('''
                INSERT INTO sync_queue (table_name, record_id, operation, data_json)
                VALUES (?, ?, ?, ?)
            ''', ('offline_activities', record_id, 'INSERT', activity_json))
            
            self.conn.commit()
            
            logger.info(f"Saved offline activity: {activity_type} for field {field_id}")
            return record_id
            
        except Exception as e:
            logger.error(f"Error saving offline activity: {e}")
            return 0
    
    def save_offline_photo(self, user_id: int, field_id: int, photo_data: bytes, metadata: Dict) -> int:
        """Save photo for offline synchronization"""
        try:
            cursor = self.conn.cursor()
            
            metadata_json = json.dumps(metadata)
            
            cursor.execute('''
                INSERT INTO offline_photos (user_id, field_id, photo_data, photo_metadata)
                VALUES (?, ?, ?, ?)
            ''', (user_id, field_id, photo_data, metadata_json))
            
            record_id = cursor.lastrowid
            
            # Add to sync queue
            cursor.execute('''
                INSERT INTO sync_queue (table_name, record_id, operation, data_json)
                VALUES (?, ?, ?, ?)
            ''', ('offline_photos', record_id, 'INSERT', metadata_json))
            
            self.conn.commit()
            
            logger.info(f"Saved offline photo for field {field_id}")
            return record_id
            
        except Exception as e:
            logger.error(f"Error saving offline photo: {e}")
            return 0
    
    def get_offline_data(self, user_id: int, field_id: int = None) -> pd.DataFrame:
        """Get offline data for synchronization"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT * FROM offline_field_data 
                    WHERE user_id = ? AND field_id = ? AND synced = FALSE
                    ORDER BY timestamp DESC
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT * FROM offline_field_data 
                    WHERE user_id = ? AND synced = FALSE
                    ORDER BY timestamp DESC
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting offline data: {e}")
            return pd.DataFrame()
    
    def get_sync_queue(self) -> pd.DataFrame:
        """Get items in sync queue"""
        try:
            cursor = self.conn.cursor()
            
            query = '''
                SELECT * FROM sync_queue 
                WHERE status = 'pending'
                ORDER BY timestamp ASC
            '''
            cursor.execute(query)
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting sync queue: {e}")
            return pd.DataFrame()
    
    def mark_as_synced(self, table_name: str, record_id: int) -> bool:
        """Mark record as synced"""
        try:
            cursor = self.conn.cursor()
            
            # Update the specific table
            if table_name == 'offline_field_data':
                cursor.execute('''
                    UPDATE offline_field_data 
                    SET synced = TRUE, sync_timestamp = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (record_id,))
            elif table_name == 'offline_activities':
                cursor.execute('''
                    UPDATE offline_activities 
                    SET synced = TRUE, sync_timestamp = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (record_id,))
            elif table_name == 'offline_photos':
                cursor.execute('''
                    UPDATE offline_photos 
                    SET synced = TRUE, sync_timestamp = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (record_id,))
            
            # Update sync queue
            cursor.execute('''
                UPDATE sync_queue 
                SET status = 'synced'
                WHERE table_name = ? AND record_id = ?
            ''', (table_name, record_id))
            
            self.conn.commit()
            
            logger.info(f"Marked {table_name} record {record_id} as synced")
            return True
            
        except Exception as e:
            logger.error(f"Error marking as synced: {e}")
            return False
    
    def check_connection_status(self) -> bool:
        """Check if internet connection is available"""
        try:
            import requests
            response = requests.get('https://www.google.com', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def sync_offline_data(self) -> Dict:
        """Sync offline data when connection is available"""
        try:
            if not self.check_connection_status():
                return {
                    'status': 'offline',
                    'message': 'No internet connection available',
                    'synced_count': 0
                }
            
            sync_queue = self.get_sync_queue()
            synced_count = 0
            
            for _, item in sync_queue.iterrows():
                # Simulate sync process
                # In production, this would make API calls to sync data
                
                if self.mark_as_synced(item['table_name'], item['record_id']):
                    synced_count += 1
            
            return {
                'status': 'success',
                'message': f'Successfully synced {synced_count} items',
                'synced_count': synced_count
            }
            
        except Exception as e:
            logger.error(f"Error syncing offline data: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'synced_count': 0
            }

class OfflineCapabilityFrontend:
    """Offline capability frontend"""
    
    def __init__(self):
        self.offline_system = OfflineCapabilitySystem()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast Offline Mode",
            page_icon="📱",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render offline capability sidebar"""
        st.sidebar.title("📱 Offline Mode")
        
        # Connection status
        connection_status = self.offline_system.check_connection_status()
        if connection_status:
            st.sidebar.success("🟢 Online")
        else:
            st.sidebar.warning("🔴 Offline")
        
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
        
        return user_id, field_id, connection_status
    
    def render_offline_data_collection(self, user_id: int, field_id: int):
        """Render offline data collection interface"""
        st.subheader("📊 Offline Data Collection")
        
        if not field_id:
            st.warning("Please select a specific field to collect data")
            return
        
        # Data collection forms
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌱 Field Observations")
            
            with st.form("field_observations"):
                observation_type = st.selectbox(
                    "Observation Type",
                    options=["Crop Growth", "Pest Damage", "Disease", "Weather", "Soil Condition", "Other"]
                )
                
                observation_notes = st.text_area(
                    "Observation Notes",
                    placeholder="Describe what you observed..."
                )
                
                severity = st.slider(
                    "Severity Level",
                    min_value=1,
                    max_value=5,
                    value=1,
                    help="1 = Low, 5 = High"
                )
                
                if st.form_submit_button("Save Observation", type="primary"):
                    observation_data = {
                        'type': observation_type,
                        'notes': observation_notes,
                        'severity': severity,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    record_id = self.offline_system.save_offline_data(
                        user_id, field_id, 'field_observation', observation_data
                    )
                    
                    if record_id:
                        st.success(f"Observation saved! Record ID: {record_id}")
                        st.rerun()
                    else:
                        st.error("Failed to save observation")
        
        with col2:
            st.subheader("📸 Photo Upload")
            
            uploaded_file = st.file_uploader(
                "Upload Field Photo",
                type=['png', 'jpg', 'jpeg'],
                help="Upload photos of field conditions, crops, or issues"
            )
            
            if uploaded_file is not None:
                # Display uploaded image
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                
                photo_metadata = {
                    'filename': uploaded_file.name,
                    'size': uploaded_file.size,
                    'type': uploaded_file.type,
                    'timestamp': datetime.now().isoformat()
                }
                
                if st.button("Save Photo", type="primary"):
                    photo_data = uploaded_file.read()
                    
                    record_id = self.offline_system.save_offline_photo(
                        user_id, field_id, photo_data, photo_metadata
                    )
                    
                    if record_id:
                        st.success(f"Photo saved! Record ID: {record_id}")
                        st.rerun()
                    else:
                        st.error("Failed to save photo")
    
    def render_offline_activities(self, user_id: int, field_id: int):
        """Render offline activity logging"""
        st.subheader("🌾 Field Activities")
        
        if not field_id:
            st.warning("Please select a specific field to log activities")
            return
        
        with st.form("field_activities"):
            col1, col2 = st.columns(2)
            
            with col1:
                activity_type = st.selectbox(
                    "Activity Type",
                    options=["Planting", "Fertilizing", "Irrigation", "Pest Control", "Harvest", "Other"]
                )
                
                activity_description = st.text_area(
                    "Activity Description",
                    placeholder="Describe the activity performed..."
                )
            
            with col2:
                cost = st.number_input(
                    "Cost ($)",
                    min_value=0.0,
                    value=0.0,
                    step=0.01
                )
                
                duration = st.number_input(
                    "Duration (hours)",
                    min_value=0.0,
                    value=1.0,
                    step=0.1
                )
            
            if st.form_submit_button("Log Activity", type="primary"):
                activity_data = {
                    'type': activity_type,
                    'description': activity_description,
                    'cost': cost,
                    'duration': duration,
                    'timestamp': datetime.now().isoformat()
                }
                
                record_id = self.offline_system.save_offline_activity(
                    user_id, field_id, activity_type, activity_data
                )
                
                if record_id:
                    st.success(f"Activity logged! Record ID: {record_id}")
                    st.rerun()
                else:
                    st.error("Failed to log activity")
    
    def render_sync_status(self, user_id: int):
        """Render synchronization status"""
        st.subheader("🔄 Synchronization Status")
        
        # Get offline data
        offline_data = self.offline_system.get_offline_data(user_id)
        sync_queue = self.offline_system.get_sync_queue()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Pending Sync", len(sync_queue))
        
        with col2:
            st.metric("Offline Records", len(offline_data))
        
        with col3:
            connection_status = self.offline_system.check_connection_status()
            if connection_status:
                st.metric("Connection", "🟢 Online")
            else:
                st.metric("Connection", "🔴 Offline")
        
        # Sync button
        if st.button("🔄 Sync Now", type="primary"):
            if connection_status:
                sync_result = self.offline_system.sync_offline_data()
                
                if sync_result['status'] == 'success':
                    st.success(sync_result['message'])
                else:
                    st.error(sync_result['message'])
                
                st.rerun()
            else:
                st.warning("No internet connection available for sync")
        
        # Show pending items
        if not sync_queue.empty:
            st.subheader("📋 Pending Sync Items")
            st.dataframe(
                sync_queue[['table_name', 'operation', 'timestamp', 'status']],
                use_container_width=True
            )
    
    def run(self):
        """Main offline capability runner"""
        st.title("📱 AgriForecast.ai - Offline Mode")
        st.markdown("**Field work without internet connection**")
        
        # Render sidebar
        user_id, field_id, connection_status = self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs([
            "📊 Data Collection", "🌾 Activities", "🔄 Sync Status"
        ])
        
        with tab1:
            self.render_offline_data_collection(user_id, field_id)
        
        with tab2:
            self.render_offline_activities(user_id, field_id)
        
        with tab3:
            self.render_sync_status(user_id)
        
        # Footer
        st.markdown("---")
        st.markdown("**📱 Offline Capability System - Critical Feature**")
        st.markdown("*Work in the field without internet connection*")

def main():
    """Main offline capability entry point"""
    try:
        app = OfflineCapabilityFrontend()
        app.run()
    except Exception as e:
        st.error(f"Offline capability error: {e}")
        logger.error(f"Offline capability error: {e}")

if __name__ == "__main__":
    main()
