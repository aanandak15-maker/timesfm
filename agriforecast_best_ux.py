"""
AgriForecast.ai - Market-Leading Agricultural Platform
Best-in-Class UI/UX for Farmers and Students
Mobile-First, Farmer-Centric Design
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import hashlib
import json
import os
from typing import Dict, List, Optional, Any
import requests
import numpy as np

# Import existing services
try:
    from real_data_service import real_data_service
    from forecasting_service import ForecastingService
    FORECASTING_AVAILABLE = True
except ImportError:
    real_data_service = None
    FORECASTING_AVAILABLE = False

class BestUXPlatform:
    """Market-Leading Agricultural Platform with Best-in-Class UX"""
    
    def __init__(self):
        self.db_path = "agriforecast_best_ux.db"
        self.init_database()
        self.load_best_css()
        
        # Initialize services
        if FORECASTING_AVAILABLE:
            try:
                self.forecasting_service = ForecastingService()
            except:
                self.forecasting_service = None
        else:
            self.forecasting_service = None
    
    def load_best_css(self):
        """Load best-in-class CSS for farmers and students"""
        css = """
        <style>
        /* ========================================
           AGRIFORECAST.AI - BEST UX FRAMEWORK
           Market-Leading Agricultural Platform
           ======================================== */
        
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* CSS Variables - Farmer-Friendly Design System */
        :root {
          /* Primary Colors - Nature Inspired */
          --primary: #2E7D32;
          --primary-light: #4CAF50;
          --primary-dark: #1B5E20;
          --accent: #FF9800;
          --accent-light: #FFB74D;
          
          /* Status Colors - Clear Visual Communication */
          --success: #4CAF50;
          --warning: #FF9800;
          --danger: #F44336;
          --info: #2196F3;
          --neutral: #9E9E9E;
          
          /* Background Colors */
          --bg-primary: #FAFAFA;
          --bg-surface: #FFFFFF;
          --bg-card: #FFFFFF;
          --bg-hover: #F5F5F5;
          
          /* Text Colors - High Contrast for Accessibility */
          --text-primary: #212121;
          --text-secondary: #757575;
          --text-disabled: #BDBDBD;
          --text-inverse: #FFFFFF;
          
          /* Spacing - Touch-Friendly */
          --space-xs: 4px;
          --space-sm: 8px;
          --space-md: 16px;
          --space-lg: 24px;
          --space-xl: 32px;
          --space-2xl: 48px;
          
          /* Touch Targets - Mobile First */
          --touch-target: 48px;
          --touch-target-lg: 56px;
          
          /* Border Radius */
          --radius-sm: 8px;
          --radius-md: 12px;
          --radius-lg: 16px;
          --radius-xl: 24px;
          
          /* Shadows - Subtle Depth */
          --shadow-sm: 0 2px 8px rgba(0,0,0,0.1);
          --shadow-md: 0 4px 16px rgba(0,0,0,0.12);
          --shadow-lg: 0 8px 32px rgba(0,0,0,0.15);
          
          /* Typography */
          --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          --font-size-sm: 14px;
          --font-size-base: 16px;
          --font-size-lg: 18px;
          --font-size-xl: 20px;
          --font-size-2xl: 24px;
          --font-size-3xl: 32px;
          
          /* Transitions */
          --transition: 0.2s ease-in-out;
        }
        
        /* Global Styles */
        * {
          box-sizing: border-box;
        }
        
        .stApp {
          font-family: var(--font-family);
          background-color: var(--bg-primary);
        }
        
        /* Hide Streamlit Elements for Clean UI */
        #MainMenu {visibility: hidden;}
        .stDeployButton {display: none;}
        footer {visibility: hidden;}
        .stAppHeader {display: none;}
        
        /* ========================================
           MOBILE-FIRST RESPONSIVE DESIGN
           ======================================== */
        
        /* Mobile Bottom Navigation */
        .mobile-bottom-nav {
          position: fixed;
          bottom: 0;
          left: 0;
          right: 0;
          background: var(--bg-surface);
          border-top: 1px solid #E0E0E0;
          padding: var(--space-sm) 0;
          display: flex;
          justify-content: space-around;
          align-items: center;
          z-index: 1000;
          box-shadow: var(--shadow-lg);
        }
        
        .mobile-nav-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: var(--space-sm);
          text-decoration: none;
          color: var(--text-secondary);
          min-width: var(--touch-target);
          min-height: var(--touch-target);
          border-radius: var(--radius-sm);
          transition: var(--transition);
          font-size: var(--font-size-sm);
          font-weight: 500;
        }
        
        .mobile-nav-item.active {
          color: var(--primary);
          background-color: var(--bg-hover);
        }
        
        .mobile-nav-item:hover {
          color: var(--primary);
          background-color: var(--bg-hover);
        }
        
        .mobile-nav-icon {
          font-size: 24px;
          margin-bottom: 2px;
        }
        
        /* Desktop Navigation */
        .desktop-nav {
          background: var(--bg-surface);
          border-right: 1px solid #E0E0E0;
          height: 100vh;
          width: 280px;
          position: fixed;
          left: 0;
          top: 0;
          padding: var(--space-lg);
          box-shadow: var(--shadow-sm);
          overflow-y: auto;
        }
        
        .nav-logo {
          display: flex;
          align-items: center;
          gap: var(--space-sm);
          font-size: var(--font-size-xl);
          font-weight: 700;
          color: var(--primary);
          margin-bottom: var(--space-xl);
          padding: var(--space-md);
        }
        
        .nav-section {
          margin-bottom: var(--space-lg);
        }
        
        .nav-section-title {
          font-size: var(--font-size-sm);
          font-weight: 600;
          color: var(--text-secondary);
          text-transform: uppercase;
          letter-spacing: 0.5px;
          margin-bottom: var(--space-md);
          padding: 0 var(--space-md);
        }
        
        .nav-item {
          display: flex;
          align-items: center;
          gap: var(--space-md);
          padding: var(--space-md);
          margin-bottom: var(--space-sm);
          border-radius: var(--radius-md);
          text-decoration: none;
          color: var(--text-primary);
          transition: var(--transition);
          font-weight: 500;
          min-height: var(--touch-target);
        }
        
        .nav-item:hover {
          background-color: var(--bg-hover);
          color: var(--primary);
          transform: translateX(4px);
        }
        
        .nav-item.active {
          background-color: var(--primary);
          color: var(--text-inverse);
        }
        
        .nav-icon {
          font-size: 20px;
          width: 24px;
          text-align: center;
        }
        
        /* ========================================
           CONTENT LAYOUT
           ======================================== */
        
        .main-content {
          margin-left: 0;
          padding: var(--space-lg);
          padding-bottom: 100px; /* Space for mobile nav */
          min-height: 100vh;
        }
        
        @media (min-width: 768px) {
          .main-content {
            margin-left: 280px;
            padding-bottom: var(--space-lg);
          }
          
          .mobile-bottom-nav {
            display: none;
          }
        }
        
        @media (max-width: 767px) {
          .desktop-nav {
            display: none;
          }
        }
        
        /* ========================================
           CARDS AND COMPONENTS
           ======================================== */
        
        .insight-card {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--space-lg);
          margin-bottom: var(--space-lg);
          box-shadow: var(--shadow-sm);
          border: 1px solid #F0F0F0;
          transition: var(--transition);
        }
        
        .insight-card:hover {
          box-shadow: var(--shadow-md);
          transform: translateY(-2px);
        }
        
        .insight-header {
          display: flex;
          align-items: center;
          gap: var(--space-md);
          margin-bottom: var(--space-md);
        }
        
        .insight-icon {
          width: 48px;
          height: 48px;
          border-radius: var(--radius-md);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;
          font-weight: bold;
        }
        
        .insight-icon.success {
          background-color: #E8F5E8;
          color: var(--success);
        }
        
        .insight-icon.warning {
          background-color: #FFF8E1;
          color: var(--warning);
        }
        
        .insight-icon.danger {
          background-color: #FFEBEE;
          color: var(--danger);
        }
        
        .insight-icon.info {
          background-color: #E3F2FD;
          color: var(--info);
        }
        
        .insight-title {
          font-size: var(--font-size-lg);
          font-weight: 600;
          color: var(--text-primary);
          margin: 0;
        }
        
        .insight-subtitle {
          font-size: var(--font-size-base);
          color: var(--text-secondary);
          margin: 0;
        }
        
        .insight-content {
          font-size: var(--font-size-base);
          color: var(--text-primary);
          line-height: 1.6;
        }
        
        .insight-action {
          margin-top: var(--space-md);
          padding-top: var(--space-md);
          border-top: 1px solid #F0F0F0;
        }
        
        /* ========================================
           BUTTONS - TOUCH FRIENDLY
           ======================================== */
        
        .btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: var(--space-sm);
          padding: var(--space-md) var(--space-lg);
          min-height: var(--touch-target);
          border: none;
          border-radius: var(--radius-md);
          font-family: var(--font-family);
          font-size: var(--font-size-base);
          font-weight: 500;
          text-decoration: none;
          cursor: pointer;
          transition: var(--transition);
          outline: none;
        }
        
        .btn-primary {
          background-color: var(--primary);
          color: var(--text-inverse);
        }
        
        .btn-primary:hover {
          background-color: var(--primary-dark);
          transform: translateY(-1px);
        }
        
        .btn-secondary {
          background-color: var(--bg-surface);
          color: var(--text-primary);
          border: 1px solid #E0E0E0;
        }
        
        .btn-secondary:hover {
          background-color: var(--bg-hover);
          border-color: var(--primary);
        }
        
        .btn-success {
          background-color: var(--success);
          color: var(--text-inverse);
        }
        
        .btn-warning {
          background-color: var(--warning);
          color: var(--text-inverse);
        }
        
        .btn-danger {
          background-color: var(--danger);
          color: var(--text-inverse);
        }
        
        .btn-lg {
          padding: var(--space-lg) var(--space-xl);
          min-height: var(--touch-target-lg);
          font-size: var(--font-size-lg);
        }
        
        .btn-full {
          width: 100%;
        }
        
        /* ========================================
           METRICS AND STATUS
           ======================================== */
        
        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: var(--space-lg);
          margin-bottom: var(--space-xl);
        }
        
        .metric-card {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--space-lg);
          box-shadow: var(--shadow-sm);
          border: 1px solid #F0F0F0;
          text-align: center;
        }
        
        .metric-value {
          font-size: var(--font-size-3xl);
          font-weight: 700;
          margin-bottom: var(--space-sm);
        }
        
        .metric-value.success {
          color: var(--success);
        }
        
        .metric-value.warning {
          color: var(--warning);
        }
        
        .metric-value.danger {
          color: var(--danger);
        }
        
        .metric-label {
          font-size: var(--font-size-base);
          color: var(--text-secondary);
          font-weight: 500;
        }
        
        .metric-change {
          font-size: var(--font-size-sm);
          font-weight: 500;
          margin-top: var(--space-sm);
        }
        
        .metric-change.positive {
          color: var(--success);
        }
        
        .metric-change.negative {
          color: var(--danger);
        }
        
        /* ========================================
           FORMS - MOBILE OPTIMIZED
           ======================================== */
        
        .form-group {
          margin-bottom: var(--space-lg);
        }
        
        .form-label {
          display: block;
          font-size: var(--font-size-base);
          font-weight: 500;
          color: var(--text-primary);
          margin-bottom: var(--space-sm);
        }
        
        .form-input {
          width: 100%;
          min-height: var(--touch-target);
          padding: var(--space-md);
          border: 2px solid #E0E0E0;
          border-radius: var(--radius-md);
          font-family: var(--font-family);
          font-size: var(--font-size-base);
          background-color: var(--bg-surface);
          transition: var(--transition);
        }
        
        .form-input:focus {
          outline: none;
          border-color: var(--primary);
          box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
        }
        
        .form-help {
          font-size: var(--font-size-sm);
          color: var(--text-secondary);
          margin-top: var(--space-sm);
        }
        
        /* ========================================
           RESPONSIVE UTILITIES
           ======================================== */
        
        .hide-mobile {
          display: block;
        }
        
        .show-mobile {
          display: none;
        }
        
        @media (max-width: 767px) {
          .hide-mobile {
            display: none;
          }
          
          .show-mobile {
            display: block;
          }
          
          .metrics-grid {
            grid-template-columns: 1fr;
            gap: var(--space-md);
          }
          
          .main-content {
            padding: var(--space-md);
          }
        }
        
        /* ========================================
           ACCESSIBILITY IMPROVEMENTS
           ======================================== */
        
        /* Focus indicators */
        .btn:focus,
        .nav-item:focus,
        .mobile-nav-item:focus {
          outline: 2px solid var(--primary);
          outline-offset: 2px;
        }
        
        /* High contrast mode support */
        @media (prefers-contrast: high) {
          :root {
            --text-primary: #000000;
            --text-secondary: #444444;
            --border: #000000;
          }
        }
        
        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
          * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
        }
        
        /* ========================================
           LOADING STATES
           ======================================== */
        
        .loading-spinner {
          display: inline-block;
          width: 20px;
          height: 20px;
          border: 2px solid #f3f3f3;
          border-top: 2px solid var(--primary);
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        .skeleton {
          background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
          background-size: 200% 100%;
          animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
          0% {
            background-position: 200% 0;
          }
          100% {
            background-position: -200% 0;
          }
        }
        
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    def init_database(self):
        """Initialize database with optimized schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                user_type TEXT DEFAULT 'farmer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                preferences TEXT
            )
        ''')
        
        # Farms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                location TEXT,
                total_area_acres REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Fields table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farm_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                crop_type TEXT,
                area_acres REAL NOT NULL,
                latitude REAL,
                longitude REAL,
                soil_type TEXT,
                planting_date DATE,
                expected_harvest_date DATE,
                status TEXT DEFAULT 'active',
                health_score REAL DEFAULT 85.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farm_id) REFERENCES farms (id)
            )
        ''')
        
        # Insights table - for storing AI-generated insights
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER NOT NULL,
                insight_type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                action_required BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (field_id) REFERENCES fields (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def render_mobile_navigation(self, active_page="home"):
        """Render mobile bottom navigation"""
        nav_items = [
            {"key": "home", "icon": "🏠", "label": "Home"},
            {"key": "fields", "icon": "🌾", "label": "Fields"},
            {"key": "insights", "icon": "🔮", "label": "Insights"},
            {"key": "more", "icon": "⚙️", "label": "More"}
        ]
        
        nav_html = '<div class="mobile-bottom-nav">'
        for item in nav_items:
            active_class = "active" if item["key"] == active_page else ""
            nav_html += f'''
            <a href="#{item["key"]}" class="mobile-nav-item {active_class}" onclick="setPage('{item["key"]}')">
                <div class="mobile-nav-icon">{item["icon"]}</div>
                <div>{item["label"]}</div>
            </a>
            '''
        nav_html += '</div>'
        
        # JavaScript for page navigation
        nav_html += '''
        <script>
        function setPage(page) {
            // This would typically trigger a Streamlit rerun with the selected page
            // For now, we'll use session state
            console.log('Navigate to:', page);
        }
        </script>
        '''
        
        st.markdown(nav_html, unsafe_allow_html=True)
    
    def render_desktop_navigation(self, active_page="home"):
        """Render desktop sidebar navigation"""
        nav_html = '''
        <div class="desktop-nav">
            <div class="nav-logo">
                🌾 AgriForecast.ai
            </div>
            
            <div class="nav-section">
                <div class="nav-section-title">Main</div>
        '''
        
        main_items = [
            {"key": "home", "icon": "🏠", "label": "Dashboard"},
            {"key": "fields", "icon": "🌾", "label": "My Fields"},
            {"key": "insights", "icon": "🔮", "label": "Insights & Forecast"},
        ]
        
        for item in main_items:
            active_class = "active" if item["key"] == active_page else ""
            nav_html += f'''
            <a href="#{item["key"]}" class="nav-item {active_class}">
                <div class="nav-icon">{item["icon"]}</div>
                <div>{item["label"]}</div>
            </a>
            '''
        
        nav_html += '''
            </div>
            
            <div class="nav-section">
                <div class="nav-section-title">Tools</div>
        '''
        
        tool_items = [
            {"key": "weather", "icon": "🌤️", "label": "Weather"},
            {"key": "market", "icon": "📈", "label": "Market Prices"},
            {"key": "analytics", "icon": "📊", "label": "Analytics"},
        ]
        
        for item in tool_items:
            active_class = "active" if item["key"] == active_page else ""
            nav_html += f'''
            <a href="#{item["key"]}" class="nav-item {active_class}">
                <div class="nav-icon">{item["icon"]}</div>
                <div>{item["label"]}</div>
            </a>
            '''
        
        nav_html += '''
            </div>
            
            <div class="nav-section">
                <div class="nav-section-title">Account</div>
        '''
        
        account_items = [
            {"key": "profile", "icon": "👤", "label": "Profile"},
            {"key": "settings", "icon": "⚙️", "label": "Settings"},
            {"key": "help", "icon": "❓", "label": "Help & Support"},
        ]
        
        for item in account_items:
            active_class = "active" if item["key"] == active_page else ""
            nav_html += f'''
            <a href="#{item["key"]}" class="nav-item {active_class}">
                <div class="nav-icon">{item["icon"]}</div>
                <div>{item["label"]}</div>
            </a>
            '''
        
        nav_html += '''
            </div>
        </div>
        '''
        
        st.markdown(nav_html, unsafe_allow_html=True)
    
    def render_insights_dashboard(self):
        """Render farmer-first insights dashboard"""
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Welcome header
        user_name = st.session_state.get('user', {}).get('full_name', 'Farmer')
        current_time = datetime.now()
        if current_time.hour < 12:
            greeting = "Good morning"
        elif current_time.hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        st.markdown(f"""
        <h1 style="color: var(--text-primary); margin-bottom: var(--space-md); font-size: var(--font-size-3xl);">
            {greeting}, {user_name}! 🌾
        </h1>
        <p style="color: var(--text-secondary); font-size: var(--font-size-lg); margin-bottom: var(--space-xl);">
            Here's what's happening with your crops today
        </p>
        """, unsafe_allow_html=True)
        
        # Critical insights (3 max)
        self.render_critical_insights()
        
        # Quick metrics
        self.render_quick_metrics()
        
        # Quick actions
        self.render_quick_actions()
        
        # Recent activity
        self.render_recent_activity()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_critical_insights(self):
        """Render 3 critical insights for immediate attention"""
        insights = [
            {
                "type": "warning",
                "title": "Irrigation Needed",
                "subtitle": "Rice Field A",
                "message": "Soil moisture is below optimal level. Water your rice field today for best growth.",
                "action": "Schedule irrigation for this afternoon"
            },
            {
                "type": "success",
                "title": "Perfect Weather",
                "subtitle": "Next 3 days",
                "message": "Sunny weather with light rain expected. Great conditions for crop growth.",
                "action": "Good time for field maintenance"
            },
            {
                "type": "info",
                "title": "Market Opportunity",
                "subtitle": "Wheat prices up 8%",
                "message": "Wheat prices have increased significantly. Consider timing your harvest sales.",
                "action": "Check market trends"
            }
        ]
        
        for insight in insights:
            icon_class = insight["type"]
            if insight["type"] == "warning":
                icon = "💧"
            elif insight["type"] == "success":
                icon = "☀️"
            else:
                icon = "📈"
            
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-header">
                    <div class="insight-icon {icon_class}">{icon}</div>
                    <div>
                        <h3 class="insight-title">{insight["title"]}</h3>
                        <p class="insight-subtitle">{insight["subtitle"]}</p>
                    </div>
                </div>
                <div class="insight-content">
                    {insight["message"]}
                </div>
                <div class="insight-action">
                    <button class="btn btn-primary">
                        {insight["action"]} →
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_quick_metrics(self):
        """Render key metrics in farmer-friendly format"""
        st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
        
        metrics = [
            {
                "value": "4",
                "label": "Active Fields",
                "change": "+1 this month",
                "type": "success"
            },
            {
                "value": "89%",
                "label": "Avg. Field Health",
                "change": "+5% this week",
                "type": "success"
            },
            {
                "value": "25°C",
                "label": "Temperature Today",
                "change": "Perfect for crops",
                "type": "success"
            },
            {
                "value": "$2,340",
                "label": "Est. Revenue",
                "change": "+12% vs last season",
                "type": "success"
            }
        ]
        
        for metric in metrics:
            change_class = "positive" if "+" in metric["change"] else "neutral"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value {metric["type"]}">{metric["value"]}</div>
                <div class="metric-label">{metric["label"]}</div>
                <div class="metric-change {change_class}">{metric["change"]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_quick_actions(self):
        """Render quick action buttons"""
        st.markdown("""
        <h2 style="color: var(--text-primary); margin: var(--space-xl) 0 var(--space-lg) 0;">
            Quick Actions
        </h2>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <button class="btn btn-primary btn-full btn-lg">
                🌾 Add Field Data
            </button>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <button class="btn btn-secondary btn-full btn-lg">
                🌤️ Check Weather
            </button>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <button class="btn btn-secondary btn-full btn-lg">
                📈 View Markets
            </button>
            """, unsafe_allow_html=True)
    
    def render_recent_activity(self):
        """Render recent activity feed"""
        st.markdown("""
        <h2 style="color: var(--text-primary); margin: var(--space-xl) 0 var(--space-lg) 0;">
            Recent Activity
        </h2>
        """, unsafe_allow_html=True)
        
        activities = [
            {
                "icon": "💧",
                "title": "Field watered",
                "subtitle": "Rice Field A • 2 hours ago",
                "description": "Automated irrigation completed successfully"
            },
            {
                "icon": "📊",
                "title": "Yield prediction updated",
                "subtitle": "Wheat Field B • 1 day ago", 
                "description": "Expected yield increased by 15% based on recent weather"
            },
            {
                "icon": "🌡️",
                "title": "Temperature alert",
                "subtitle": "All fields • 2 days ago",
                "description": "High temperature warning - extra irrigation recommended"
            }
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-header">
                    <div class="insight-icon info">{activity["icon"]}</div>
                    <div>
                        <h4 class="insight-title" style="font-size: var(--font-size-base);">{activity["title"]}</h4>
                        <p class="insight-subtitle">{activity["subtitle"]}</p>
                    </div>
                </div>
                <div class="insight-content" style="font-size: var(--font-size-sm);">
                    {activity["description"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def create_sample_user(self):
        """Create sample user for testing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE username = ?", ("farmer",))
            if cursor.fetchone():
                conn.close()
                return
            
            # Create sample user
            password_hash = hashlib.sha256("password123".encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, user_type)
                VALUES (?, ?, ?, ?, ?)
            ''', ("farmer", "farmer@example.com", password_hash, "John Farmer", "farmer"))
            
            user_id = cursor.lastrowid
            
            # Create sample farm
            cursor.execute('''
                INSERT INTO farms (user_id, name, location, total_area_acres, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, "Green Valley Farm", "Punjab, India", 25.5, "Organic farming operation"))
            
            farm_id = cursor.lastrowid
            
            # Create sample fields
            fields = [
                ("Rice Field A", "Rice", 5.0, 30.7046, 76.7179, "Clay", 85.0),
                ("Wheat Field B", "Wheat", 8.0, 30.7056, 76.7189, "Loamy", 92.0),
                ("Corn Field C", "Corn", 6.5, 30.7066, 76.7199, "Sandy", 78.0),
                ("Soybean Field D", "Soybean", 6.0, 30.7076, 76.7209, "Silty", 88.0),
            ]
            
            for field in fields:
                cursor.execute('''
                    INSERT INTO fields (farm_id, name, crop_type, area_acres, latitude, longitude, soil_type, health_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (farm_id, *field))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            st.error(f"Error creating sample data: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        """Verify user credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, username, email, full_name, user_type FROM users
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, password_hash))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'user_type': user[4]
            }
        return None
    
    def render_login_page(self):
        """Render beautiful login page"""
        st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        ">
            <div style="
                background: white;
                padding: var(--space-2xl);
                border-radius: var(--radius-xl);
                box-shadow: var(--shadow-lg);
                width: 100%;
                max-width: 400px;
                margin: var(--space-lg);
            ">
                <div style="text-align: center; margin-bottom: var(--space-xl);">
                    <h1 style="color: var(--primary); font-size: var(--font-size-3xl); margin-bottom: var(--space-sm);">
                        🌾 AgriForecast.ai
                    </h1>
                    <p style="color: var(--text-secondary); font-size: var(--font-size-lg);">
                        Smart farming for better yields
                    </p>
                </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_clicked = st.form_submit_button("Login", use_container_width=True)
            with col2:
                demo_clicked = st.form_submit_button("Demo Login", use_container_width=True)
            
            if login_clicked:
                user = self.verify_user(username, password)
                if user:
                    st.session_state.user = user
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            
            if demo_clicked:
                # Use demo credentials
                user = self.verify_user("farmer", "password123")
                if user:
                    st.session_state.user = user
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Demo user not found")
        
        st.markdown("""
                <div style="text-align: center; margin-top: var(--space-lg); padding-top: var(--space-lg); border-top: 1px solid #E0E0E0;">
                    <p style="color: var(--text-secondary); font-size: var(--font-size-sm);">
                        Demo credentials: <strong>farmer</strong> / <strong>password123</strong>
                    </p>
                    <p style="color: var(--text-secondary); font-size: var(--font-size-sm);">
                        Built for farmers, students, and agricultural professionals
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Main application entry point"""
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        
        # Create sample data if needed
        self.create_sample_user()
        
        # Check authentication
        if not st.session_state.authenticated:
            self.render_login_page()
            return
        
        # Render navigation
        self.render_desktop_navigation(st.session_state.current_page)
        self.render_mobile_navigation(st.session_state.current_page)
        
        # Render main content based on current page
        if st.session_state.current_page == 'home':
            self.render_insights_dashboard()
        else:
            # Placeholder for other pages
            st.markdown('<div class="main-content">', unsafe_allow_html=True)
            st.title(f"🚧 {st.session_state.current_page.title()} Page")
            st.info("This page is coming soon in Phase 2 of the implementation!")
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Initialize and run the best UX platform"""
    st.set_page_config(
        page_title="AgriForecast.ai - Best Agricultural Platform",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    platform = BestUXPlatform()
    platform.run()

if __name__ == "__main__":
    main()
