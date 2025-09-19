#!/usr/bin/env python3
"""
Market Intelligence System for AgriForecast.ai
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
import requests
import hashlib
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketIntelligenceSystem:
    """Market intelligence and commodity price tracking system"""
    
    def __init__(self):
        self.setup_database()
        self.setup_api_keys()
        
    def setup_database(self):
        """Setup market intelligence database"""
        self.conn = sqlite3.connect('agriforecast_market_intelligence.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create market intelligence tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commodity_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commodity_name TEXT NOT NULL,
                price REAL NOT NULL,
                unit TEXT NOT NULL,
                market_location TEXT NOT NULL,
                price_date DATE NOT NULL,
                price_source TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commodity_name TEXT NOT NULL,
                trend_direction TEXT NOT NULL,
                trend_strength REAL NOT NULL,
                price_change_percent REAL NOT NULL,
                analysis_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selling_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                crop_type TEXT NOT NULL,
                recommendation_type TEXT NOT NULL,
                current_price REAL NOT NULL,
                recommended_price REAL NOT NULL,
                confidence_score REAL NOT NULL,
                reasoning TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS supply_chain_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commodity_name TEXT NOT NULL,
                supply_level TEXT NOT NULL,
                demand_level TEXT NOT NULL,
                inventory_level TEXT NOT NULL,
                logistics_cost REAL NOT NULL,
                analysis_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("Market intelligence database setup completed")
    
    def setup_api_keys(self):
        """Setup API keys for market data"""
        self.alpha_vantage_key = "KJRXQKB09I13GUPP"  # Your existing key
        self.alpha_vantage_base_url = "https://www.alphavantage.co/query"
    
    def fetch_commodity_prices(self, commodity: str) -> Dict:
        """Fetch commodity prices from Alpha Vantage"""
        try:
            # For demo purposes, we'll simulate commodity prices
            # In production, you would use real API calls
            
            base_prices = {
                "Rice": 400.0,
                "Wheat": 250.0,
                "Corn": 200.0,
                "Soybean": 500.0,
                "Cotton": 80.0,
                "Sugarcane": 30.0
            }
            
            base_price = base_prices.get(commodity, 300.0)
            
            # Simulate price variations
            price_variation = np.random.uniform(-0.1, 0.1)  # ±10% variation
            current_price = base_price * (1 + price_variation)
            
            # Generate historical prices for trend analysis
            historical_prices = []
            for i in range(30):
                date = datetime.now().date() - timedelta(days=i)
                price_variation = np.random.uniform(-0.05, 0.05)
                price = base_price * (1 + price_variation)
                historical_prices.append({
                    'date': date,
                    'price': round(price, 2)
                })
            
            return {
                'current_price': round(current_price, 2),
                'historical_prices': historical_prices,
                'price_change': round(price_variation * 100, 2),
                'source': 'Alpha Vantage (Simulated)'
            }
            
        except Exception as e:
            logger.error(f"Error fetching commodity prices: {e}")
            return {}
    
    def analyze_market_trends(self, commodity: str) -> Dict:
        """Analyze market trends for a commodity"""
        try:
            price_data = self.fetch_commodity_prices(commodity)
            
            if not price_data or 'historical_prices' not in price_data:
                return {}
            
            historical_prices = price_data['historical_prices']
            prices = [p['price'] for p in historical_prices]
            
            # Calculate trend
            recent_avg = np.mean(prices[:7])  # Last 7 days
            older_avg = np.mean(prices[7:14])  # Previous 7 days
            
            trend_direction = "Rising" if recent_avg > older_avg else "Falling"
            trend_strength = abs(recent_avg - older_avg) / older_avg * 100
            price_change_percent = price_data.get('price_change', 0)
            
            return {
                'trend_direction': trend_direction,
                'trend_strength': round(trend_strength, 2),
                'price_change_percent': price_change_percent,
                'recent_avg_price': round(recent_avg, 2),
                'older_avg_price': round(older_avg, 2)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {e}")
            return {}
    
    def generate_selling_recommendations(self, user_id: int, field_id: int, 
                                       crop_type: str, current_price: float) -> Dict:
        """Generate selling recommendations based on market analysis"""
        try:
            trend_data = self.analyze_market_trends(crop_type)
            
            if not trend_data:
                return {}
            
            # Generate recommendation based on trend
            if trend_data['trend_direction'] == "Rising" and trend_data['trend_strength'] > 5:
                recommendation = "Hold - Prices are rising strongly"
                recommended_price = current_price * 1.1  # 10% higher
                confidence = 0.8
            elif trend_data['trend_direction'] == "Falling" and trend_data['trend_strength'] > 5:
                recommendation = "Sell Now - Prices are falling"
                recommended_price = current_price * 0.95  # 5% lower
                confidence = 0.7
            else:
                recommendation = "Monitor - Market is stable"
                recommended_price = current_price
                confidence = 0.5
            
            reasoning = f"""
            Market Analysis for {crop_type}:
            - Trend: {trend_data['trend_direction']} ({trend_data['trend_strength']:.1f}% strength)
            - Price Change: {trend_data['price_change_percent']:.1f}%
            - Recent Average: ${trend_data['recent_avg_price']}
            - Recommendation: {recommendation}
            """
            
            return {
                'recommendation_type': recommendation,
                'current_price': current_price,
                'recommended_price': round(recommended_price, 2),
                'confidence_score': confidence,
                'reasoning': reasoning
            }
            
        except Exception as e:
            logger.error(f"Error generating selling recommendations: {e}")
            return {}
    
    def get_supply_chain_analysis(self, commodity: str) -> Dict:
        """Get supply chain analysis for a commodity"""
        try:
            # Simulate supply chain data
            supply_levels = ["Low", "Normal", "High"]
            demand_levels = ["Low", "Normal", "High"]
            inventory_levels = ["Low", "Normal", "High"]
            
            return {
                'supply_level': np.random.choice(supply_levels),
                'demand_level': np.random.choice(demand_levels),
                'inventory_level': np.random.choice(inventory_levels),
                'logistics_cost': round(np.random.uniform(10, 50), 2),
                'analysis_date': datetime.now().date()
            }
            
        except Exception as e:
            logger.error(f"Error getting supply chain analysis: {e}")
            return {}
    
    def save_commodity_price(self, commodity_name: str, price: float, unit: str, 
                           market_location: str, price_source: str) -> int:
        """Save commodity price to database"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT INTO commodity_prices (commodity_name, price, unit, market_location, 
                                           price_date, price_source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (commodity_name, price, unit, market_location, datetime.now().date(), price_source))
            
            price_id = cursor.lastrowid
            self.conn.commit()
            
            return price_id
            
        except Exception as e:
            logger.error(f"Error saving commodity price: {e}")
            return 0
    
    def get_commodity_prices(self, commodity_name: str = None) -> pd.DataFrame:
        """Get commodity prices from database"""
        try:
            cursor = self.conn.cursor()
            
            if commodity_name:
                query = '''
                    SELECT * FROM commodity_prices 
                    WHERE commodity_name = ? 
                    ORDER BY price_date DESC
                '''
                cursor.execute(query, (commodity_name,))
            else:
                query = '''
                    SELECT * FROM commodity_prices 
                    ORDER BY price_date DESC
                '''
                cursor.execute(query)
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting commodity prices: {e}")
            return pd.DataFrame()

class MarketIntelligenceFrontend:
    """Market intelligence frontend"""
    
    def __init__(self):
        self.market_system = MarketIntelligenceSystem()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast Market Intelligence",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render market intelligence sidebar"""
        st.sidebar.title("📈 Market Intelligence")
        
        # User selection
        user_id = st.sidebar.selectbox(
            "Select User",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: f"User {x}"
        )
        
        # Commodity selection
        commodity_options = ["Rice", "Wheat", "Corn", "Soybean", "Cotton", "Sugarcane"]
        selected_commodity = st.sidebar.selectbox("Select Commodity", commodity_options)
        
        return user_id, selected_commodity
    
    def render_commodity_prices(self, commodity: str):
        """Render commodity price tracking"""
        st.subheader(f"💰 {commodity} Price Tracking")
        
        # Fetch current prices
        price_data = self.market_system.fetch_commodity_prices(commodity)
        
        if price_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"${price_data['current_price']}/ton")
            
            with col2:
                st.metric("Price Change", f"{price_data['price_change']:.1f}%")
            
            with col3:
                st.metric("Data Source", price_data['source'])
            
            with col4:
                if st.button("Refresh Prices"):
                    st.rerun()
            
            # Price trend chart
            if 'historical_prices' in price_data:
                st.subheader("📊 Price Trend (Last 30 Days)")
                
                df = pd.DataFrame(price_data['historical_prices'])
                df['date'] = pd.to_datetime(df['date'])
                
                fig = px.line(df, x='date', y='price', title=f"{commodity} Price Trend")
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Price ($/ton)",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, width='stretch')
                
                # Save price to database
                self.market_system.save_commodity_price(
                    commodity, price_data['current_price'], "ton", 
                    "Global Market", price_data['source']
                )
        else:
            st.error("Failed to fetch price data")
    
    def render_market_analysis(self, commodity: str):
        """Render market trend analysis"""
        st.subheader(f"📊 Market Analysis - {commodity}")
        
        # Get market trends
        trend_data = self.market_system.analyze_market_trends(commodity)
        
        if trend_data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                trend_color = "green" if trend_data['trend_direction'] == "Rising" else "red"
                st.metric(
                    "Market Trend", 
                    trend_data['trend_direction'],
                    delta=f"{trend_data['trend_strength']:.1f}% strength"
                )
            
            with col2:
                st.metric(
                    "Price Change", 
                    f"{trend_data['price_change_percent']:.1f}%"
                )
            
            with col3:
                st.metric(
                    "Recent Average", 
                    f"${trend_data['recent_avg_price']}"
                )
            
            # Trend visualization
            st.subheader("📈 Trend Analysis")
            
            # Create trend chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=["Older Period", "Recent Period"],
                y=[trend_data['older_avg_price'], trend_data['recent_avg_price']],
                mode='lines+markers',
                name='Average Price',
                line=dict(color='blue', width=3),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                title=f"{commodity} Market Trend Analysis",
                xaxis_title="Time Period",
                yaxis_title="Average Price ($/ton)",
                height=400
            )
            
            st.plotly_chart(fig, width='stretch')
        else:
            st.error("Failed to analyze market trends")
    
    def render_selling_recommendations(self, user_id: int, commodity: str):
        """Render selling recommendations"""
        st.subheader(f"💡 Selling Recommendations - {commodity}")
        
        # Get current price
        price_data = self.market_system.fetch_commodity_prices(commodity)
        
        if price_data:
            current_price = price_data['current_price']
            
            # Generate recommendations
            recommendations = self.market_system.generate_selling_recommendations(
                user_id, 1, commodity, current_price
            )
            
            if recommendations:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Current Price", f"${current_price}/ton")
                    st.metric("Recommended Price", f"${recommendations['recommended_price']}/ton")
                
                with col2:
                    confidence_color = "green" if recommendations['confidence_score'] > 0.7 else "orange"
                    st.metric(
                        "Confidence Score", 
                        f"{recommendations['confidence_score']:.1%}",
                        delta=recommendations['recommendation_type']
                    )
                
                # Recommendation details
                st.subheader("📋 Recommendation Details")
                
                with st.expander("View Analysis"):
                    st.write(recommendations['reasoning'])
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Accept Recommendation", type="primary"):
                        st.success("Recommendation accepted! Consider selling at recommended price.")
                
                with col2:
                    if st.button("Hold Position"):
                        st.info("Position held. Monitor market conditions.")
                
                with col3:
                    if st.button("Get More Analysis"):
                        st.rerun()
            else:
                st.warning("No recommendations available at this time.")
        else:
            st.error("Failed to generate recommendations")
    
    def render_supply_chain_analysis(self, commodity: str):
        """Render supply chain analysis"""
        st.subheader(f"🚚 Supply Chain Analysis - {commodity}")
        
        # Get supply chain data
        supply_data = self.market_system.get_supply_chain_analysis(commodity)
        
        if supply_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                supply_color = "red" if supply_data['supply_level'] == "Low" else "green" if supply_data['supply_level'] == "High" else "orange"
                st.metric("Supply Level", supply_data['supply_level'])
            
            with col2:
                demand_color = "red" if supply_data['demand_level'] == "Low" else "green" if supply_data['demand_level'] == "High" else "orange"
                st.metric("Demand Level", supply_data['demand_level'])
            
            with col3:
                inventory_color = "red" if supply_data['inventory_level'] == "Low" else "green" if supply_data['inventory_level'] == "High" else "orange"
                st.metric("Inventory Level", supply_data['inventory_level'])
            
            with col4:
                st.metric("Logistics Cost", f"${supply_data['logistics_cost']}/ton")
            
            # Supply chain visualization
            st.subheader("📊 Supply Chain Overview")
            
            # Create supply chain chart
            fig = go.Figure()
            
            categories = ['Supply', 'Demand', 'Inventory']
            values = [
                1 if supply_data['supply_level'] == "High" else 0.5 if supply_data['supply_level'] == "Normal" else 0,
                1 if supply_data['demand_level'] == "High" else 0.5 if supply_data['demand_level'] == "Normal" else 0,
                1 if supply_data['inventory_level'] == "High" else 0.5 if supply_data['inventory_level'] == "Normal" else 0
            ]
            
            fig.add_trace(go.Bar(
                x=categories,
                y=values,
                marker_color=['green', 'blue', 'orange'],
                text=[supply_data['supply_level'], supply_data['demand_level'], supply_data['inventory_level']],
                textposition='auto'
            ))
            
            fig.update_layout(
                title=f"{commodity} Supply Chain Analysis",
                yaxis_title="Level (0=Low, 0.5=Normal, 1=High)",
                height=400
            )
            
            st.plotly_chart(fig, width='stretch')
        else:
            st.error("Failed to get supply chain analysis")
    
    def run(self):
        """Main market intelligence runner"""
        st.title("📈 AgriForecast.ai - Market Intelligence")
        st.markdown("**Commodity Price Tracking & Market Analysis**")
        
        # Render sidebar
        user_id, selected_commodity = self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "💰 Price Tracking", "📊 Market Analysis", "💡 Recommendations", "🚚 Supply Chain"
        ])
        
        with tab1:
            self.render_commodity_prices(selected_commodity)
        
        with tab2:
            self.render_market_analysis(selected_commodity)
        
        with tab3:
            self.render_selling_recommendations(user_id, selected_commodity)
        
        with tab4:
            self.render_supply_chain_analysis(selected_commodity)
        
        # Footer
        st.markdown("---")
        st.markdown("**📈 Market Intelligence System - Phase 3 Advanced Features**")
        st.markdown("*Comprehensive market analysis and commodity price tracking*")

def main():
    """Main market intelligence entry point"""
    try:
        app = MarketIntelligenceFrontend()
        app.run()
    except Exception as e:
        st.error(f"Market intelligence error: {e}")
        logger.error(f"Market intelligence error: {e}")

if __name__ == "__main__":
    main()




