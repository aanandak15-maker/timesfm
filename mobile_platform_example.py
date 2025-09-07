"""
Mobile-Optimized AgriForecast.ai Platform Example
Integration of mobile navigation and PWA features with existing platform
"""

import streamlit as st
import sys
import os

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mobile_navigation import MobileNavigation, render_mobile_navigation, MOBILE_NAVIGATION_ITEMS
from pwa_integration import setup_pwa

class MobileAgriForecastPlatform:
    """Mobile-optimized version of AgriForecast.ai platform"""
    
    def __init__(self):
        self.mobile_nav = MobileNavigation()
        self.setup_page_config()
        self.setup_pwa()
    
    def setup_page_config(self):
        """Configure Streamlit page for mobile optimization"""
        st.set_page_config(
            page_title="AgriForecast.ai",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="collapsed",  # Start collapsed on mobile
            menu_items={
                'Get Help': 'https://agriforecast.ai/help',
                'Report a bug': 'https://agriforecast.ai/bugs',
                'About': '''
                # AgriForecast.ai - Agricultural Intelligence Platform
                
                AI-powered forecasting and farm management with real-time data.
                
                **Features:**
                - 🌾 Field Management
                - 🔮 AI Forecasting  
                - 🌤️ Weather Integration
                - 📊 Analytics & Reports
                - 📱 Mobile-First Design
                - 🔄 Offline Capabilities
                '''
            }
        )
    
    def setup_pwa(self):
        """Setup PWA features"""
        # Setup PWA integration
        self.pwa = setup_pwa("AgriForecast.ai")
        
        # Hide Streamlit default elements on mobile
        hide_streamlit_style = """
        <style>
        /* Hide Streamlit elements on mobile */
        @media (max-width: 768px) {
            .stDeployButton {
                display: none !important;
            }
            
            #MainMenu {
                display: none !important;
            }
            
            header {
                display: none !important;
            }
            
            .stToolbar {
                display: none !important;
            }
            
            /* Adjust main content for mobile */
            .main .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
                max-width: 100%;
            }
        }
        
        /* Desktop view adjustments */
        @media (min-width: 769px) {
            .mobile-nav-container {
                display: none !important;
            }
        }
        </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    def detect_mobile_device(self):
        """Detect if user is on mobile device"""
        # This is a simple detection - in production you might want to use
        # more sophisticated user agent detection
        mobile_detection = """
        <script>
        // Simple mobile detection
        const isMobile = window.innerWidth <= 768 || 
                        /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        // Store in session storage
        sessionStorage.setItem('isMobile', isMobile);
        
        // Add class to body
        if (isMobile) {
            document.body.classList.add('mobile-device');
        }
        
        console.log('Mobile device detected:', isMobile);
        </script>
        """
        st.markdown(mobile_detection, unsafe_allow_html=True)
        
        # You can also set this in session state for Python access
        if 'is_mobile' not in st.session_state:
            st.session_state.is_mobile = True  # Default to mobile-first
    
    def render_mobile_header_nav(self):
        """Render mobile header and navigation"""
        # Get current user info (replace with your user system)
        user_info = st.session_state.get('user', {
            'username': 'demo_user',
            'full_name': 'Demo User',
            'role': 'Farmer'
        })
        
        # Get current page
        current_page = st.session_state.get('page', 'dashboard')
        
        # Render mobile navigation
        render_mobile_navigation(
            navigation_items=MOBILE_NAVIGATION_ITEMS,
            active_page=current_page,
            user_info=user_info
        )
    
    def handle_navigation(self):
        """Handle page navigation from URL params or session state"""
        # Check URL parameters
        query_params = st.experimental_get_query_params()
        
        if 'page' in query_params:
            st.session_state.page = query_params['page'][0]
        elif 'page' not in st.session_state:
            st.session_state.page = 'dashboard'
        
        # Handle actions
        if 'action' in query_params:
            action = query_params['action'][0]
            if action == 'add_field':
                st.session_state.show_add_field = True
            elif action == 'logout':
                self.handle_logout()
    
    def handle_logout(self):
        """Handle user logout"""
        # Clear session state
        for key in list(st.session_state.keys()):
            if key.startswith('user') or key in ['authenticated', 'page']:
                del st.session_state[key]
        
        # Redirect to login
        st.experimental_set_query_params()
        st.rerun()
    
    def render_dashboard_mobile(self):
        """Render mobile-optimized dashboard"""
        st.markdown("""
        <div class="mobile-content">
            <div class="mobile-card mobile-fade-in-up">
                <div class="mobile-card-header">
                    <h2 class="mobile-card-title">🌾 Welcome to AgriForecast.ai</h2>
                </div>
                <p>AI-powered agricultural intelligence at your fingertips</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="mobile-card">
                <div class="mobile-card-header">
                    <h3 class="mobile-card-title">🏡 Farms</h3>
                </div>
                <div style="font-size: 2rem; color: #2E7D32; font-weight: bold;">3</div>
                <div style="color: #666; font-size: 0.9rem;">Active farms</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="mobile-card">
                <div class="mobile-card-header">
                    <h3 class="mobile-card-title">🌾 Fields</h3>
                </div>
                <div style="font-size: 2rem; color: #2E7D32; font-weight: bold;">12</div>
                <div style="color: #666; font-size: 0.9rem;">Total fields</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌾 Add Field", use_container_width=True, key="mobile_add_field"):
                st.session_state.page = "fields"
                st.experimental_set_query_params(page="fields", action="add_field")
                st.rerun()
        
        with col2:
            if st.button("🔮 AI Forecast", use_container_width=True, key="mobile_forecast"):
                st.session_state.page = "forecasting"
                st.experimental_set_query_params(page="forecasting")
                st.rerun()
        
        # Recent activity
        st.markdown("### 📈 Recent Activity")
        
        activities = [
            {"icon": "🌱", "text": "Field 'Rice Field 1' updated", "time": "2 hours ago"},
            {"icon": "🌤️", "text": "Weather alert received", "time": "4 hours ago"},
            {"icon": "📊", "text": "New yield prediction", "time": "6 hours ago"},
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div class="mobile-card" style="padding: 12px; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.2rem;">{activity['icon']}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: 500;">{activity['text']}</div>
                        <div style="font-size: 0.8rem; color: #666;">{activity['time']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_fields_mobile(self):
        """Render mobile-optimized fields page"""
        st.markdown("""
        <div class="mobile-content">
            <div class="mobile-card">
                <div class="mobile-card-header">
                    <h2 class="mobile-card-title">🌾 My Fields</h2>
                    <button class="mobile-card-action">➕</button>
                </div>
                <p>Manage your agricultural fields</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add field form in expander
        with st.expander("➕ Add New Field", expanded=st.session_state.get('show_add_field', False)):
            with st.form("mobile_add_field_form", clear_on_submit=True):
                st.markdown("#### Field Information")
                
                field_name = st.text_input("Field Name", placeholder="e.g., North Rice Field")
                
                col1, col2 = st.columns(2)
                with col1:
                    crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Corn", "Soybean", "Cotton"])
                    area = st.number_input("Area (acres)", min_value=0.1, value=1.0, step=0.1)
                
                with col2:
                    soil_type = st.selectbox("Soil Type", ["Loamy", "Clay", "Sandy", "Silty"])
                    irrigation = st.selectbox("Irrigation", ["Rainfed", "Drip", "Sprinkler", "Flood"])
                
                submitted = st.form_submit_button("Add Field", use_container_width=True)
                
                if submitted and field_name:
                    st.success(f"✅ Field '{field_name}' added successfully!")
                    st.balloons()
                    st.session_state.show_add_field = False
                    st.rerun()
        
        # Display existing fields
        st.markdown("### 🏡 Your Fields")
        
        fields = [
            {"name": "Rice Field 1", "crop": "Rice", "area": "5.0", "status": "Active"},
            {"name": "Wheat Field A", "crop": "Wheat", "area": "3.2", "status": "Active"},
            {"name": "Corn Field North", "crop": "Corn", "area": "4.5", "status": "Planted"},
        ]
        
        for field in fields:
            st.markdown(f"""
            <div class="mobile-card touch-feedback">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #2E7D32;">{field['name']}</h4>
                        <p style="margin: 4px 0; color: #666;">
                            {field['crop']} • {field['area']} acres
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <span style="
                            background: #e8f5e8; 
                            color: #2E7D32; 
                            padding: 4px 8px; 
                            border-radius: 12px; 
                            font-size: 0.8rem;
                            font-weight: 500;
                        ">{field['status']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_page_content(self):
        """Render content based on current page"""
        current_page = st.session_state.get('page', 'dashboard')
        
        if current_page == 'dashboard':
            self.render_dashboard_mobile()
        elif current_page == 'fields':
            self.render_fields_mobile()
        elif current_page == 'forecasting':
            st.markdown("## 🔮 AI Forecasting")
            st.info("AI forecasting features coming soon...")
        elif current_page == 'analytics':
            st.markdown("## 📊 Analytics")
            st.info("Analytics dashboard coming soon...")
        elif current_page == 'weather':
            st.markdown("## 🌤️ Weather")
            st.info("Weather data coming soon...")
        elif current_page == 'settings':
            st.markdown("## ⚙️ Settings")
            st.info("Settings page coming soon...")
        else:
            st.error("Page not found")
    
    def run(self):
        """Main application runner"""
        # Detect mobile device
        self.detect_mobile_device()
        
        # Handle navigation
        self.handle_navigation()
        
        # Render mobile header and navigation
        self.render_mobile_header_nav()
        
        # Render page content
        self.render_page_content()
        
        # Add mobile-specific JavaScript
        mobile_js = """
        <script>
        // Handle mobile-specific interactions
        document.addEventListener('DOMContentLoaded', function() {
            // Add touch feedback to cards
            const cards = document.querySelectorAll('.mobile-card.touch-feedback');
            cards.forEach(card => {
                card.addEventListener('touchstart', function() {
                    this.style.transform = 'scale(0.98)';
                    this.style.transition = 'transform 0.1s ease';
                });
                
                card.addEventListener('touchend', function() {
                    this.style.transform = 'scale(1)';
                });
            });
            
            // Handle pull-to-refresh
            let startY = 0;
            let currentY = 0;
            let pullDistance = 0;
            
            document.addEventListener('touchstart', function(e) {
                startY = e.touches[0].clientY;
            });
            
            document.addEventListener('touchmove', function(e) {
                currentY = e.touches[0].clientY;
                pullDistance = currentY - startY;
                
                if (pullDistance > 0 && window.scrollY === 0) {
                    e.preventDefault();
                    // Add pull-to-refresh indicator
                    if (pullDistance > 100) {
                        console.log('Pull to refresh triggered');
                    }
                }
            });
            
            document.addEventListener('touchend', function(e) {
                if (pullDistance > 100 && window.scrollY === 0) {
                    // Trigger refresh
                    window.location.reload();
                }
                pullDistance = 0;
            });
        });
        </script>
        """
        
        st.markdown(mobile_js, unsafe_allow_html=True)

def main():
    """Main function to run the mobile platform"""
    platform = MobileAgriForecastPlatform()
    platform.run()

if __name__ == "__main__":
    main()
