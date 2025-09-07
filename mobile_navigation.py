"""
Mobile-Responsive Navigation Component for AgriForecast.ai
Enhanced navigation with touch-optimized components
"""

import streamlit as st
from typing import List, Dict, Optional

class MobileNavigation:
    """Mobile-first navigation component with touch optimization"""
    
    def __init__(self):
        self.load_mobile_css()
    
    def load_mobile_css(self):
        """Load mobile-specific CSS"""
        mobile_css = """
        <style>
        /* Mobile Navigation Styles */
        .mobile-nav-container {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
            z-index: 1000;
            box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        }
        
        .mobile-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            min-height: 56px;
        }
        
        .mobile-logo {
            display: flex;
            align-items: center;
            gap: 8px;
            color: white;
            font-size: 20px;
            font-weight: 700;
            text-decoration: none;
        }
        
        .mobile-menu-button {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 8px;
            border-radius: 8px;
            transition: background-color 0.2s ease;
            min-height: 44px;
            min-width: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .mobile-menu-button:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .mobile-sidebar {
            position: fixed;
            top: 0;
            left: -300px;
            width: 280px;
            height: 100vh;
            background: white;
            box-shadow: 2px 0 12px rgba(0,0,0,0.15);
            transition: left 0.3s ease;
            z-index: 1001;
            overflow-y: auto;
        }
        
        .mobile-sidebar.open {
            left: 0;
        }
        
        .mobile-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }
        
        .mobile-overlay.open {
            opacity: 1;
            visibility: visible;
        }
        
        .mobile-sidebar-header {
            background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .mobile-close-button {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 8px;
            min-height: 44px;
            min-width: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
        }
        
        .mobile-nav-items {
            padding: 20px 0;
        }
        
        .mobile-nav-item {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 16px 20px;
            color: #333;
            text-decoration: none;
            font-weight: 500;
            border-bottom: 1px solid #f0f0f0;
            min-height: 56px;
            transition: background-color 0.2s ease;
        }
        
        .mobile-nav-item:hover {
            background: #f8f9fa;
        }
        
        .mobile-nav-item.active {
            background: rgba(46, 125, 50, 0.1);
            color: #2E7D32;
            border-left: 4px solid #2E7D32;
        }
        
        .mobile-nav-icon {
            font-size: 20px;
            width: 24px;
            text-align: center;
        }
        
        .mobile-nav-section {
            padding: 20px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .mobile-nav-section-title {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        .mobile-user-info {
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .mobile-user-name {
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }
        
        .mobile-user-role {
            font-size: 14px;
            color: #666;
        }
        
        .mobile-quick-actions {
            padding: 16px 20px;
        }
        
        .mobile-quick-action {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 8px;
            color: #333;
            text-decoration: none;
            font-weight: 500;
            min-height: 48px;
            transition: all 0.2s ease;
        }
        
        .mobile-quick-action:hover {
            background: #e8f5e8;
            border-color: #2E7D32;
            transform: translateY(-1px);
        }
        
        .mobile-logout {
            background: #dc3545;
            color: white;
            border: none;
            margin-top: 8px;
        }
        
        .mobile-logout:hover {
            background: #c82333;
        }
        
        /* Touch-optimized improvements */
        .touch-target {
            min-height: 44px;
            min-width: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Main content adjustment for mobile */
        .mobile-content {
            padding-top: 70px;
            min-height: 100vh;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .stSidebar {
                display: none !important;
            }
            
            .main .block-container {
                padding-top: 0;
                max-width: 100%;
            }
        }
        
        @media (min-width: 769px) {
            .mobile-nav-container {
                display: none;
            }
            
            .mobile-content {
                padding-top: 0;
            }
        }
        </style>
        """
        st.markdown(mobile_css, unsafe_allow_html=True)
    
    def render_mobile_header(self, user_name: str = "User", logo_text: str = "🌾 AgriForecast.ai"):
        """Render mobile header with hamburger menu"""
        header_html = f"""
        <div class="mobile-nav-container">
            <div class="mobile-header">
                <div class="mobile-logo">{logo_text}</div>
                <button class="mobile-menu-button touch-target" onclick="toggleMobileMenu()">
                    ☰
                </button>
            </div>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    
    def render_mobile_sidebar(self, navigation_items: List[Dict], active_page: str, user_info: Dict):
        """Render mobile sidebar navigation"""
        user_name = user_info.get('full_name', user_info.get('username', 'User'))
        user_role = user_info.get('role', 'Farmer')
        
        # Group navigation items
        main_items = [item for item in navigation_items if item.get('group') == 'main']
        tool_items = [item for item in navigation_items if item.get('group') == 'tools']
        
        sidebar_html = f"""
        <div class="mobile-overlay" onclick="closeMobileMenu()"></div>
        <div class="mobile-sidebar">
            <div class="mobile-sidebar-header">
                <div class="mobile-logo">🌾 AgriForecast.ai</div>
                <button class="mobile-close-button touch-target" onclick="closeMobileMenu()">
                    ×
                </button>
            </div>
            
            <div class="mobile-user-info">
                <div class="mobile-user-name">{user_name}</div>
                <div class="mobile-user-role">{user_role}</div>
            </div>
            
            <div class="mobile-nav-items">
                <div class="mobile-nav-section-title">Navigation</div>
        """
        
        # Add main navigation items
        for item in main_items:
            active_class = "active" if item['key'] == active_page else ""
            sidebar_html += f"""
                <a href="#" class="mobile-nav-item {active_class}" onclick="navigateToPage('{item['key']}')">
                    <span class="mobile-nav-icon">{item['icon']}</span>
                    <span>{item['title']}</span>
                </a>
            """
        
        # Add tools section if exists
        if tool_items:
            sidebar_html += """
                <div class="mobile-nav-section">
                    <div class="mobile-nav-section-title">Tools</div>
                </div>
            """
            
            for item in tool_items:
                active_class = "active" if item['key'] == active_page else ""
                sidebar_html += f"""
                    <a href="#" class="mobile-nav-item {active_class}" onclick="navigateToPage('{item['key']}')">
                        <span class="mobile-nav-icon">{item['icon']}</span>
                        <span>{item['title']}</span>
                    </a>
                """
        
        # Quick actions
        sidebar_html += """
            </div>
            
            <div class="mobile-quick-actions">
                <div class="mobile-nav-section-title">Quick Actions</div>
                <a href="#" class="mobile-quick-action" onclick="quickAction('add_field')">
                    <span>🌾</span>
                    <span>Add Field</span>
                </a>
                <a href="#" class="mobile-quick-action" onclick="quickAction('ai_forecast')">
                    <span>🔮</span>
                    <span>AI Forecast</span>
                </a>
                <a href="#" class="mobile-quick-action" onclick="quickAction('weather')">
                    <span>🌤️</span>
                    <span>Weather</span>
                </a>
                <button class="mobile-quick-action mobile-logout" onclick="logout()">
                    <span>🚪</span>
                    <span>Logout</span>
                </button>
            </div>
        </div>
        """
        
        st.markdown(sidebar_html, unsafe_allow_html=True)
    
    def add_mobile_javascript(self):
        """Add JavaScript for mobile navigation functionality"""
        js_code = """
        <script>
        // Mobile navigation JavaScript
        function toggleMobileMenu() {
            const sidebar = document.querySelector('.mobile-sidebar');
            const overlay = document.querySelector('.mobile-overlay');
            
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
        }
        
        function closeMobileMenu() {
            const sidebar = document.querySelector('.mobile-sidebar');
            const overlay = document.querySelector('.mobile-overlay');
            
            sidebar.classList.remove('open');
            overlay.classList.remove('open');
        }
        
        function navigateToPage(pageKey) {
            // Close mobile menu
            closeMobileMenu();
            
            // Set the session state for page navigation
            window.location.href = window.location.href.split('?')[0] + '?page=' + pageKey;
            
            // Alternative: Use Streamlit's session state
            if (window.streamlitSetComponentValue) {
                window.streamlitSetComponentValue('current_page', pageKey);
            }
        }
        
        function quickAction(action) {
            closeMobileMenu();
            
            switch(action) {
                case 'add_field':
                    // Trigger add field action
                    window.location.href = window.location.href.split('?')[0] + '?action=add_field';
                    break;
                case 'ai_forecast':
                    window.location.href = window.location.href.split('?')[0] + '?page=forecasting';
                    break;
                case 'weather':
                    window.location.href = window.location.href.split('?')[0] + '?page=weather';
                    break;
            }
        }
        
        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                // Clear session and redirect
                window.location.href = window.location.href.split('?')[0] + '?action=logout';
            }
        }
        
        // Handle page visibility for mobile optimization
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                // Page is hidden - can pause animations, etc.
                console.log('App hidden');
            } else {
                // Page is visible
                console.log('App visible');
            }
        });
        
        // Touch optimization
        document.addEventListener('DOMContentLoaded', function() {
            // Add touch feedback to buttons
            const touchTargets = document.querySelectorAll('.touch-target, .mobile-nav-item, .mobile-quick-action');
            
            touchTargets.forEach(target => {
                target.addEventListener('touchstart', function() {
                    this.style.opacity = '0.7';
                });
                
                target.addEventListener('touchend', function() {
                    this.style.opacity = '1';
                });
                
                target.addEventListener('touchcancel', function() {
                    this.style.opacity = '1';
                });
            });
        });
        
        // Prevent zoom on input focus for iOS
        document.addEventListener('touchstart', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') {
                e.target.style.fontSize = '16px';
            }
        });
        </script>
        """
        st.markdown(js_code, unsafe_allow_html=True)

# Usage example function
def render_mobile_navigation(navigation_items: List[Dict], active_page: str, user_info: Dict):
    """
    Main function to render complete mobile navigation
    
    Args:
        navigation_items: List of navigation items with 'key', 'title', 'icon', 'group'
        active_page: Current active page key
        user_info: User information dictionary
    """
    mobile_nav = MobileNavigation()
    
    # Check if mobile device or small screen
    is_mobile = st.session_state.get('is_mobile', True)  # You can set this based on user agent
    
    if is_mobile:
        # Render mobile header
        mobile_nav.render_mobile_header(user_info.get('username', 'User'))
        
        # Render mobile sidebar
        mobile_nav.render_mobile_sidebar(navigation_items, active_page, user_info)
        
        # Add JavaScript functionality
        mobile_nav.add_mobile_javascript()
        
        # Add mobile content wrapper
        st.markdown('<div class="mobile-content">', unsafe_allow_html=True)

# Sample navigation items for testing
MOBILE_NAVIGATION_ITEMS = [
    {"key": "dashboard", "title": "Dashboard", "icon": "🏠", "group": "main"},
    {"key": "fields", "title": "My Fields", "icon": "🌾", "group": "main"},
    {"key": "forecasting", "title": "AI Forecasting", "icon": "🔮", "group": "main"},
    {"key": "analytics", "title": "Analytics", "icon": "📊", "group": "tools"},
    {"key": "weather", "title": "Weather", "icon": "🌤️", "group": "tools"},
    {"key": "market", "title": "Market", "icon": "💰", "group": "tools"},
    {"key": "settings", "title": "Settings", "icon": "⚙️", "group": "main"},
]
