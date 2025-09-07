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

# Note: Simplified version without external dependencies

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiFieldManager:
    """Enhanced field management system with multi-field support"""
    
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Setup database for multi-field management"""
        self.conn = sqlite3.connect('agriforecast_multi_field.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create tables for multi-field management
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farm_id INTEGER,
                name TEXT NOT NULL,
                crop_type TEXT,
                latitude REAL,
                longitude REAL,
                area_m2 REAL,
                area_acres REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farm_id) REFERENCES farms (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS field_zones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER,
                zone_name TEXT NOT NULL,
                zone_type TEXT,
                coordinates TEXT,
                area_m2 REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS field_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER,
                data_type TEXT,
                data_json TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS yield_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER,
                prediction_type TEXT,
                prediction_data TEXT,
                confidence_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        ''')
        
        self.conn.commit()
        logger.info("Multi-field database setup completed")
    
    def create_farm(self, name: str, description: str = "", location: str = "") -> int:
        """Create a new farm"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO farms (name, description, location) VALUES (?, ?, ?)",
            (name, description, location)
        )
        farm_id = cursor.lastrowid
        self.conn.commit()
        logger.info(f"Created farm: {name} (ID: {farm_id})")
        return farm_id
    
    def create_field(self, farm_id: int, name: str, crop_type: str, 
                    latitude: float, longitude: float, area_m2: float, 
                    description: str = "") -> int:
        """Create a new field"""
        area_acres = area_m2 * 0.000247105  # Convert m² to acres
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO fields (farm_id, name, crop_type, latitude, longitude, 
               area_m2, area_acres, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (farm_id, name, crop_type, latitude, longitude, area_m2, area_acres, description)
        )
        field_id = cursor.lastrowid
        self.conn.commit()
        logger.info(f"Created field: {name} (ID: {field_id})")
        return field_id
    
    def create_field_zone(self, field_id: int, zone_name: str, zone_type: str,
                         coordinates: str, area_m2: float, description: str = "") -> int:
        """Create a new field zone"""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO field_zones (field_id, zone_name, zone_type, coordinates, 
               area_m2, description) VALUES (?, ?, ?, ?, ?, ?)""",
            (field_id, zone_name, zone_type, coordinates, area_m2, description)
        )
        zone_id = cursor.lastrowid
        self.conn.commit()
        logger.info(f"Created zone: {zone_name} (ID: {zone_id})")
        return zone_id
    
    def get_farms(self) -> List[Dict]:
        """Get all farms"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM farms ORDER BY created_at DESC")
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_fields(self, farm_id: Optional[int] = None) -> List[Dict]:
        """Get all fields, optionally filtered by farm"""
        cursor = self.conn.cursor()
        if farm_id:
            cursor.execute("SELECT * FROM fields WHERE farm_id = ? ORDER BY created_at DESC", (farm_id,))
        else:
            cursor.execute("SELECT * FROM fields ORDER BY created_at DESC")
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_field_zones(self, field_id: int) -> List[Dict]:
        """Get all zones for a field"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM field_zones WHERE field_id = ? ORDER BY created_at DESC", (field_id,))
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_field_data(self, field_id: int, data_type: str = None) -> List[Dict]:
        """Get data for a specific field"""
        cursor = self.conn.cursor()
        if data_type:
            cursor.execute("SELECT * FROM field_data WHERE field_id = ? AND data_type = ? ORDER BY timestamp DESC", 
                         (field_id, data_type))
        else:
            cursor.execute("SELECT * FROM field_data WHERE field_id = ? ORDER BY timestamp DESC", (field_id,))
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def save_field_data(self, field_id: int, data_type: str, data: Dict) -> int:
        """Save data for a field"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO field_data (field_id, data_type, data_json) VALUES (?, ?, ?)",
            (field_id, data_type, json.dumps(data))
        )
        data_id = cursor.lastrowid
        self.conn.commit()
        logger.info(f"Saved {data_type} data for field {field_id}")
        return data_id
    
    def get_field_summary(self, field_id: int) -> Dict:
        """Get comprehensive summary for a field"""
        field_data = self.get_field_data(field_id)
        zones = self.get_field_zones(field_id)
        
        # Get latest data for each type
        latest_data = {}
        for data in field_data:
            if data['data_type'] not in latest_data or data['timestamp'] > latest_data[data['data_type']]['timestamp']:
                latest_data[data['data_type']] = data
        
        return {
            'field_id': field_id,
            'zones': zones,
            'latest_data': latest_data,
            'data_count': len(field_data)
        }

class MultiFieldFrontend:
    """Enhanced frontend for multi-field management"""
    
    def __init__(self):
        self.field_manager = MultiFieldManager()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast.ai - Multi-Field Management",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render the sidebar with navigation"""
        st.sidebar.title("🌾 AgriForecast.ai")
        st.sidebar.markdown("**Multi-Field Management System**")
        
        # Navigation
        page = st.sidebar.selectbox(
            "Navigate",
            ["🏠 Dashboard", "🌾 Fields", "📊 Compare Fields", "📈 Analytics", "⚙️ Settings"]
        )
        
        # Quick stats
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Quick Stats")
        
        farms = self.field_manager.get_farms()
        fields = self.field_manager.get_fields()
        
        st.sidebar.metric("Farms", len(farms))
        st.sidebar.metric("Fields", len(fields))
        
        if fields:
            total_area = sum(float(field['area_acres']) for field in fields)
            st.sidebar.metric("Total Area", f"{total_area:.2f} acres")
        
        # Quick actions in sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Quick Actions")
        
        if st.sidebar.button("➕ Add Farm", width='stretch'):
            st.session_state.show_add_farm = True
            st.rerun()
        
        if st.sidebar.button("🌾 Add Field", width='stretch'):
            st.session_state.show_add_field = True
            st.rerun()
        
        return page
    
    def render_dashboard(self):
        """Render the main dashboard"""
        st.title("🌾 AgriForecast.ai Multi-Field Dashboard")
        st.markdown("**Comprehensive Agricultural Intelligence Platform**")
        
        # Add Farm button at the top
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➕ Add New Farm", type="primary", width='stretch'):
                st.session_state.show_add_farm = True
                st.rerun()
        
        # Get data
        farms = self.field_manager.get_farms()
        fields = self.field_manager.get_fields()
        
        if not farms:
            st.info("👋 Welcome! Start by creating your first farm and field.")
        else:
            st.success(f"✅ You have {len(farms)} farms and {len(fields)} fields!")
        
        # Farm overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Farms", len(farms))
        with col2:
            st.metric("Total Fields", len(fields))
        with col3:
            if fields:
                total_area = sum(float(field['area_acres']) for field in fields)
                st.metric("Total Area", f"{total_area:.2f} acres")
        
        # Recent activity
        st.subheader("📈 Recent Activity")
        if fields:
            recent_fields = fields[:5]  # Show 5 most recent
            for field in recent_fields:
                with st.expander(f"🌾 {field['name']} - {field['crop_type']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Location:** {field['latitude']:.4f}, {field['longitude']:.4f}")
                    with col2:
                        st.write(f"**Area:** {field['area_acres']:.2f} acres")
                    with col3:
                        st.write(f"**Created:** {field['created_at'][:10]}")
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Add New Farm", width='stretch'):
                st.session_state.show_add_farm = True
        
        with col2:
            if st.button("🌾 Add New Field", width='stretch'):
                st.session_state.show_add_field = True
        
        with col3:
            if st.button("📊 View All Fields", width='stretch'):
                st.session_state.page = "🌾 Fields"
                st.rerun()
    
    def render_fields_page(self):
        """Render the fields management page"""
        st.title("🌾 Field Management")
        
        # Add new field button
        if st.button("➕ Add New Field", type="primary"):
            st.session_state.show_add_field = True
        
        # Get fields
        fields = self.field_manager.get_fields()
        
        if not fields:
            st.info("No fields found. Create your first field to get started!")
            return
        
        # Fields table
        st.subheader("Your Fields")
        
        # Create a DataFrame for better display
        df = pd.DataFrame(fields)
        df['area_acres'] = df['area_acres'].round(2)
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d')
        
        # Display fields in a nice format
        for idx, field in enumerate(fields):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{field['name']}**")
                    st.write(f"*{field['crop_type']}*")
                    if field['description']:
                        st.write(f"_{field['description']}_")
                
                with col2:
                    st.write(f"📍 {field['latitude']:.4f}, {field['longitude']:.4f}")
                    st.write(f"📏 {field['area_acres']:.2f} acres")
                
                with col3:
                    st.write(f"📅 {field['created_at'][:10]}")
                    zones = self.field_manager.get_field_zones(field['id'])
                    st.write(f"🏘️ {len(zones)} zones")
                
                with col4:
                    if st.button("View", key=f"view_{field['id']}"):
                        st.session_state.selected_field = field['id']
                        st.session_state.page = "📊 Compare Fields"
                        st.rerun()
                
                st.divider()
    
    def render_compare_fields(self):
        """Render the field comparison page"""
        st.title("📊 Field Comparison")
        
        fields = self.field_manager.get_fields()
        
        if not fields:
            st.info("No fields to compare. Create some fields first!")
            return
        
        # Field selection
        col1, col2 = st.columns(2)
        
        with col1:
            field1_id = st.selectbox(
                "Select Field 1",
                options=[f['id'] for f in fields],
                format_func=lambda x: next(f['name'] for f in fields if f['id'] == x)
            )
        
        with col2:
            field2_id = st.selectbox(
                "Select Field 2",
                options=[f['id'] for f in fields],
                format_func=lambda x: next(f['name'] for f in fields if f['id'] == x)
            )
        
        if field1_id == field2_id:
            st.warning("Please select two different fields for comparison.")
            return
        
        # Get field details
        field1 = next(f for f in fields if f['id'] == field1_id)
        field2 = next(f for f in fields if f['id'] == field2_id)
        
        # Comparison metrics
        st.subheader("📊 Field Comparison")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Field 1 Area", f"{field1['area_acres']:.2f} acres")
            st.metric("Field 1 Crop", field1['crop_type'])
        
        with col2:
            st.metric("Field 2 Area", f"{field2['area_acres']:.2f} acres")
            st.metric("Field 2 Crop", field2['crop_type'])
        
        with col3:
            area_diff = field1['area_acres'] - field2['area_acres']
            st.metric("Area Difference", f"{area_diff:+.2f} acres")
        
        # Detailed comparison
        st.subheader("🔍 Detailed Comparison")
        
        comparison_data = {
            'Metric': ['Name', 'Crop Type', 'Area (acres)', 'Latitude', 'Longitude', 'Created'],
            'Field 1': [
                field1['name'],
                field1['crop_type'],
                f"{field1['area_acres']:.2f}",
                f"{field1['latitude']:.4f}",
                f"{field1['longitude']:.4f}",
                field1['created_at'][:10]
            ],
            'Field 2': [
                field2['name'],
                field2['crop_type'],
                f"{field2['area_acres']:.2f}",
                f"{field2['latitude']:.4f}",
                f"{field2['longitude']:.4f}",
                field2['created_at'][:10]
            ]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, width='stretch')
        
        # Zones comparison
        zones1 = self.field_manager.get_field_zones(field1_id)
        zones2 = self.field_manager.get_field_zones(field2_id)
        
        if zones1 or zones2:
            st.subheader("🏘️ Zones Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{field1['name']} Zones:**")
                if zones1:
                    for zone in zones1:
                        st.write(f"• {zone['zone_name']} ({zone['zone_type']})")
                else:
                    st.write("No zones defined")
            
            with col2:
                st.write(f"**{field2['name']} Zones:**")
                if zones2:
                    for zone in zones2:
                        st.write(f"• {zone['zone_name']} ({zone['zone_type']})")
                else:
                    st.write("No zones defined")
    
    def render_analytics(self):
        """Render the analytics page"""
        st.title("📈 Analytics & Insights")
        
        fields = self.field_manager.get_fields()
        
        if not fields:
            st.info("No fields available for analytics. Create some fields first!")
            return
        
        # Field distribution
        st.subheader("🌾 Field Distribution")
        
        # Crop type distribution
        crop_counts = {}
        for field in fields:
            crop = field['crop_type']
            crop_counts[crop] = crop_counts.get(crop, 0) + 1
        
        if crop_counts:
            fig_crops = px.pie(
                values=list(crop_counts.values()),
                names=list(crop_counts.keys()),
                title="Crop Type Distribution"
            )
            st.plotly_chart(fig_crops, width='stretch')
        
        # Area distribution
        st.subheader("📏 Area Distribution")
        
        area_data = [float(field['area_acres']) for field in fields]
        if area_data:
            fig_area = px.histogram(
                x=area_data,
                title="Field Area Distribution",
                labels={'x': 'Area (acres)', 'y': 'Number of Fields'}
            )
            st.plotly_chart(fig_area, width='stretch')
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        
        if area_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Fields", len(fields))
            with col2:
                st.metric("Total Area", f"{sum(area_data):.2f} acres")
            with col3:
                st.metric("Average Area", f"{np.mean(area_data):.2f} acres")
            with col4:
                st.metric("Largest Field", f"{max(area_data):.2f} acres")
    
    def render_settings(self):
        """Render the settings page"""
        st.title("⚙️ Settings")
        
        st.subheader("🌾 Field Management Settings")
        
        # Database management
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.session_state.get('confirm_clear', False):
                # Clear all data
                cursor = self.field_manager.conn.cursor()
                cursor.execute("DELETE FROM field_data")
                cursor.execute("DELETE FROM yield_predictions")
                cursor.execute("DELETE FROM field_zones")
                cursor.execute("DELETE FROM fields")
                cursor.execute("DELETE FROM farms")
                self.field_manager.conn.commit()
                st.success("All data cleared!")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm clearing all data")
        
        # Export data
        if st.button("📤 Export Data"):
            # Export all data to JSON
            farms = self.field_manager.get_farms()
            fields = self.field_manager.get_fields()
            
            export_data = {
                'farms': farms,
                'fields': fields,
                'exported_at': datetime.now().isoformat()
            }
            
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"agriforecast_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Import data
        st.subheader("📥 Import Data")
        uploaded_file = st.file_uploader("Upload JSON file", type=['json'])
        
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                
                if 'farms' in data and 'fields' in data:
                    # Import farms
                    for farm in data['farms']:
                        self.field_manager.create_farm(
                            farm['name'],
                            farm.get('description', ''),
                            farm.get('location', '')
                        )
                    
                    # Import fields
                    for field in data['fields']:
                        self.field_manager.create_field(
                            field['farm_id'],
                            field['name'],
                            field['crop_type'],
                            field['latitude'],
                            field['longitude'],
                            field['area_m2'],
                            field.get('description', '')
                        )
                    
                    st.success("Data imported successfully!")
                    st.rerun()
                else:
                    st.error("Invalid file format. Please upload a valid JSON file.")
            except Exception as e:
                st.error(f"Error importing data: {e}")
    
    def render_add_farm_form(self):
        """Render the add farm form"""
        st.subheader("➕ Add New Farm")
        
        with st.form("add_farm_form"):
            name = st.text_input("Farm Name", placeholder="Enter farm name")
            description = st.text_area("Description", placeholder="Enter farm description")
            location = st.text_input("Location", placeholder="Enter farm location")
            
            submitted = st.form_submit_button("Create Farm", type="primary")
            
            if submitted:
                if name:
                    farm_id = self.field_manager.create_farm(name, description, location)
                    st.success(f"Farm '{name}' created successfully!")
                    st.session_state.show_add_farm = False
                    st.rerun()
                else:
                    st.error("Please enter a farm name")
    
    def render_add_field_form(self):
        """Render the add field form"""
        st.subheader("🌾 Add New Field")
        
        farms = self.field_manager.get_farms()
        
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
                    field_id = self.field_manager.create_field(
                        farm_id, name, crop_type, latitude, longitude, area_m2, description
                    )
                    st.success(f"Field '{name}' created successfully!")
                    st.session_state.show_add_field = False
                    st.rerun()
                else:
                    st.error("Please enter a field name")
    
    def run(self):
        """Main application runner"""
        # Initialize session state
        if 'page' not in st.session_state:
            st.session_state.page = "🏠 Dashboard"
        if 'show_add_farm' not in st.session_state:
            st.session_state.show_add_farm = False
        if 'show_add_field' not in st.session_state:
            st.session_state.show_add_field = False
        
        # Render sidebar and get current page
        page = self.render_sidebar()
        
        # Render main content based on page
        if page == "🏠 Dashboard":
            self.render_dashboard()
        elif page == "🌾 Fields":
            self.render_fields_page()
        elif page == "📊 Compare Fields":
            self.render_compare_fields()
        elif page == "📈 Analytics":
            self.render_analytics()
        elif page == "⚙️ Settings":
            self.render_settings()
        
        # Render forms if needed
        if st.session_state.show_add_farm:
            self.render_add_farm_form()
        
        if st.session_state.show_add_field:
            self.render_add_field_form()

def main():
    """Main application entry point"""
    try:
        app = MultiFieldFrontend()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()
