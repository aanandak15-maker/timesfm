#!/usr/bin/env python3
"""
Advanced Analytics Dashboard for AgriForecast.ai
Phase 2: Business Intelligence and Analytics
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsDataManager:
    """Advanced analytics data management system"""
    
    def __init__(self):
        self.setup_analytics_database()
        
    def setup_analytics_database(self):
        """Setup database for analytics and reporting"""
        self.conn = sqlite3.connect('agriforecast_analytics.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create analytics tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS yield_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                crop_type TEXT,
                season TEXT,
                year INTEGER,
                predicted_yield REAL,
                actual_yield REAL,
                yield_variance REAL,
                confidence_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cost_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                cost_type TEXT,
                cost_category TEXT,
                amount REAL,
                unit TEXT,
                season TEXT,
                year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS revenue_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                crop_type TEXT,
                quantity REAL,
                unit_price REAL,
                total_revenue REAL,
                season TEXT,
                year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS field_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                field_name TEXT,
                crop_type TEXT,
                area_acres REAL,
                yield_per_acre REAL,
                revenue_per_acre REAL,
                cost_per_acre REAL,
                profit_per_acre REAL,
                roi_percentage REAL,
                season TEXT,
                year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_id INTEGER NOT NULL,
                date DATE,
                temperature REAL,
                humidity REAL,
                precipitation REAL,
                wind_speed REAL,
                weather_impact_score REAL,
                season TEXT,
                year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("Analytics database setup completed")
    
    def generate_sample_analytics_data(self, user_id: int):
        """Generate sample analytics data for demonstration"""
        try:
            cursor = self.conn.cursor()
            
            # Generate yield analytics data
            crops = ['Rice', 'Wheat', 'Corn', 'Soybean']
            seasons = ['Kharif', 'Rabi', 'Summer']
            years = [2022, 2023, 2024, 2025]
            
            for year in years:
                for season in seasons:
                    for i, crop in enumerate(crops):
                        # Simulate yield data
                        base_yield = np.random.normal(3.5, 0.8)  # Base yield in tons/acre
                        predicted_yield = max(0, base_yield + np.random.normal(0, 0.3))
                        actual_yield = max(0, predicted_yield + np.random.normal(0, 0.4))
                        yield_variance = actual_yield - predicted_yield
                        confidence_score = np.random.uniform(0.6, 0.95)
                        
                        cursor.execute('''
                            INSERT INTO yield_analytics (user_id, field_id, crop_type, season, year, 
                                                       predicted_yield, actual_yield, yield_variance, confidence_score)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (user_id, i+1, crop, season, year, predicted_yield, actual_yield, yield_variance, confidence_score))
            
            # Generate cost analytics data
            cost_types = ['Seeds', 'Fertilizer', 'Pesticides', 'Labor', 'Irrigation', 'Machinery', 'Fuel', 'Other']
            cost_categories = ['Input', 'Labor', 'Equipment', 'Utilities', 'Other']
            
            for year in years:
                for season in seasons:
                    for i, crop in enumerate(crops):
                        for cost_type in cost_types:
                            amount = np.random.uniform(50, 500)
                            cursor.execute('''
                                INSERT INTO cost_analytics (user_id, field_id, cost_type, cost_category, 
                                                          amount, unit, season, year)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (user_id, i+1, cost_type, np.random.choice(cost_categories), 
                                 amount, 'USD', season, year))
            
            # Generate revenue analytics data
            for year in years:
                for season in seasons:
                    for i, crop in enumerate(crops):
                        quantity = np.random.uniform(100, 1000)  # tons
                        unit_price = np.random.uniform(200, 800)  # USD per ton
                        total_revenue = quantity * unit_price
                        
                        cursor.execute('''
                            INSERT INTO revenue_analytics (user_id, field_id, crop_type, quantity, 
                                                         unit_price, total_revenue, season, year)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (user_id, i+1, crop, quantity, unit_price, total_revenue, season, year))
            
            # Generate field performance data
            for year in years:
                for season in seasons:
                    for i, crop in enumerate(crops):
                        area_acres = np.random.uniform(1, 10)
                        yield_per_acre = np.random.uniform(2, 6)
                        revenue_per_acre = yield_per_acre * np.random.uniform(300, 600)
                        cost_per_acre = np.random.uniform(200, 400)
                        profit_per_acre = revenue_per_acre - cost_per_acre
                        roi_percentage = (profit_per_acre / cost_per_acre) * 100
                        
                        cursor.execute('''
                            INSERT INTO field_performance (user_id, field_id, field_name, crop_type, 
                                                         area_acres, yield_per_acre, revenue_per_acre, 
                                                         cost_per_acre, profit_per_acre, roi_percentage, season, year)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (user_id, i+1, f"Field {i+1}", crop, area_acres, yield_per_acre, 
                             revenue_per_acre, cost_per_acre, profit_per_acre, roi_percentage, season, year))
            
            self.conn.commit()
            logger.info(f"Generated sample analytics data for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error generating sample analytics data: {e}")
    
    def get_yield_trends(self, user_id: int, field_id: Optional[int] = None) -> pd.DataFrame:
        """Get yield trend data for analysis"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT crop_type, season, year, predicted_yield, actual_yield, yield_variance, confidence_score
                    FROM yield_analytics 
                    WHERE user_id = ? AND field_id = ?
                    ORDER BY year, season
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT crop_type, season, year, predicted_yield, actual_yield, yield_variance, confidence_score
                    FROM yield_analytics 
                    WHERE user_id = ?
                    ORDER BY year, season
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting yield trends: {e}")
            return pd.DataFrame()
    
    def get_cost_analysis(self, user_id: int, field_id: Optional[int] = None) -> pd.DataFrame:
        """Get cost analysis data"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT cost_type, cost_category, amount, season, year
                    FROM cost_analytics 
                    WHERE user_id = ? AND field_id = ?
                    ORDER BY year, season
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT cost_type, cost_category, amount, season, year
                    FROM cost_analytics 
                    WHERE user_id = ?
                    ORDER BY year, season
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting cost analysis: {e}")
            return pd.DataFrame()
    
    def get_revenue_analysis(self, user_id: int, field_id: Optional[int] = None) -> pd.DataFrame:
        """Get revenue analysis data"""
        try:
            cursor = self.conn.cursor()
            
            if field_id:
                query = '''
                    SELECT crop_type, quantity, unit_price, total_revenue, season, year
                    FROM revenue_analytics 
                    WHERE user_id = ? AND field_id = ?
                    ORDER BY year, season
                '''
                cursor.execute(query, (user_id, field_id))
            else:
                query = '''
                    SELECT crop_type, quantity, unit_price, total_revenue, season, year
                    FROM revenue_analytics 
                    WHERE user_id = ?
                    ORDER BY year, season
                '''
                cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting revenue analysis: {e}")
            return pd.DataFrame()
    
    def get_field_performance(self, user_id: int) -> pd.DataFrame:
        """Get field performance comparison data"""
        try:
            cursor = self.conn.cursor()
            
            query = '''
                SELECT field_name, crop_type, area_acres, yield_per_acre, revenue_per_acre, 
                       cost_per_acre, profit_per_acre, roi_percentage, season, year
                FROM field_performance 
                WHERE user_id = ?
                ORDER BY year DESC, roi_percentage DESC
            '''
            cursor.execute(query, (user_id,))
            
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting field performance: {e}")
            return pd.DataFrame()
    
    def calculate_roi_metrics(self, user_id: int) -> Dict:
        """Calculate ROI and profitability metrics"""
        try:
            # Get field performance data
            df = self.get_field_performance(user_id)
            
            if df.empty:
                return {}
            
            # Calculate overall metrics
            total_investment = df['cost_per_acre'].sum()
            total_revenue = df['revenue_per_acre'].sum()
            total_profit = df['profit_per_acre'].sum()
            
            overall_roi = (total_profit / total_investment * 100) if total_investment > 0 else 0
            
            # Calculate by crop type
            crop_metrics = df.groupby('crop_type').agg({
                'cost_per_acre': 'mean',
                'revenue_per_acre': 'mean',
                'profit_per_acre': 'mean',
                'roi_percentage': 'mean'
            }).round(2)
            
            # Calculate by season
            season_metrics = df.groupby('season').agg({
                'cost_per_acre': 'mean',
                'revenue_per_acre': 'mean',
                'profit_per_acre': 'mean',
                'roi_percentage': 'mean'
            }).round(2)
            
            return {
                'overall_roi': round(overall_roi, 2),
                'total_investment': round(total_investment, 2),
                'total_revenue': round(total_revenue, 2),
                'total_profit': round(total_profit, 2),
                'crop_metrics': crop_metrics.to_dict(),
                'season_metrics': season_metrics.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error calculating ROI metrics: {e}")
            return {}

class AdvancedAnalyticsDashboard:
    """Advanced analytics dashboard frontend"""
    
    def __init__(self):
        self.analytics_manager = AnalyticsDataManager()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast Analytics",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render analytics sidebar"""
        st.sidebar.title("📊 Analytics Dashboard")
        
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
        
        # Time period selection
        time_period = st.sidebar.selectbox(
            "Time Period",
            ["Last 2 Years", "Last 3 Years", "All Time"]
        )
        
        # Generate sample data button
        if st.sidebar.button("Generate Sample Data"):
            self.analytics_manager.generate_sample_analytics_data(user_id)
            st.sidebar.success("Sample data generated!")
            st.rerun()
        
        return user_id, field_id, time_period
    
    def render_yield_trends(self, user_id: int, field_id: Optional[int]):
        """Render yield trend analysis"""
        st.subheader("🌾 Yield Trend Analysis")
        
        # Get yield data
        df = self.analytics_manager.get_yield_trends(user_id, field_id)
        
        if df.empty:
            st.info("No yield data available. Generate sample data to see trends.")
            return
        
        # Create yield trend chart
        fig = go.Figure()
        
        for crop in df['crop_type'].unique():
            crop_data = df[df['crop_type'] == crop]
            
            fig.add_trace(go.Scatter(
                x=crop_data['year'],
                y=crop_data['actual_yield'],
                mode='lines+markers',
                name=f'{crop} (Actual)',
                line=dict(dash='solid')
            ))
            
            fig.add_trace(go.Scatter(
                x=crop_data['year'],
                y=crop_data['predicted_yield'],
                mode='lines+markers',
                name=f'{crop} (Predicted)',
                line=dict(dash='dash')
            ))
        
        fig.update_layout(
            title="Yield Trends: Actual vs Predicted",
            xaxis_title="Year",
            yaxis_title="Yield (tons/acre)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # Yield variance analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Average Yield Variance", f"{df['yield_variance'].mean():.2f} tons/acre")
            st.metric("Prediction Accuracy", f"{df['confidence_score'].mean():.1%}")
        
        with col2:
            st.metric("Best Performing Crop", df.groupby('crop_type')['actual_yield'].mean().idxmax())
            st.metric("Highest Yield", f"{df['actual_yield'].max():.2f} tons/acre")
    
    def render_cost_benefit_analysis(self, user_id: int, field_id: Optional[int]):
        """Render cost-benefit analysis"""
        st.subheader("💰 Cost-Benefit Analysis")
        
        # Get cost and revenue data
        cost_df = self.analytics_manager.get_cost_analysis(user_id, field_id)
        revenue_df = self.analytics_manager.get_revenue_analysis(user_id, field_id)
        
        if cost_df.empty or revenue_df.empty:
            st.info("No cost/revenue data available. Generate sample data to see analysis.")
            return
        
        # Cost breakdown by category
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Cost Breakdown by Category")
            cost_by_category = cost_df.groupby('cost_category')['amount'].sum()
            
            fig_pie = px.pie(
                values=cost_by_category.values,
                names=cost_by_category.index,
                title="Cost Distribution"
            )
            st.plotly_chart(fig_pie, width='stretch')
        
        with col2:
            st.subheader("📈 Revenue vs Costs")
            
            # Aggregate data by year
            yearly_costs = cost_df.groupby('year')['amount'].sum()
            yearly_revenue = revenue_df.groupby('year')['total_revenue'].sum()
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(name='Costs', x=yearly_costs.index, y=yearly_costs.values))
            fig_bar.add_trace(go.Bar(name='Revenue', x=yearly_revenue.index, y=yearly_revenue.values))
            
            fig_bar.update_layout(
                title="Yearly Costs vs Revenue",
                xaxis_title="Year",
                yaxis_title="Amount (USD)",
                barmode='group'
            )
            
            st.plotly_chart(fig_bar, width='stretch')
        
        # Profitability metrics
        st.subheader("💵 Profitability Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_costs = cost_df['amount'].sum()
        total_revenue = revenue_df['total_revenue'].sum()
        total_profit = total_revenue - total_costs
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        with col1:
            st.metric("Total Costs", f"${total_costs:,.2f}")
        with col2:
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        with col3:
            st.metric("Total Profit", f"${total_profit:,.2f}")
        with col4:
            st.metric("Profit Margin", f"{profit_margin:.1f}%")
    
    def render_roi_analysis(self, user_id: int):
        """Render ROI analysis"""
        st.subheader("📈 Return on Investment (ROI) Analysis")
        
        # Get ROI metrics
        roi_metrics = self.analytics_manager.calculate_roi_metrics(user_id)
        
        if not roi_metrics:
            st.info("No ROI data available. Generate sample data to see analysis.")
            return
        
        # Overall ROI metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Overall ROI", f"{roi_metrics['overall_roi']:.1f}%")
        with col2:
            st.metric("Total Investment", f"${roi_metrics['total_investment']:,.2f}")
        with col3:
            st.metric("Total Revenue", f"${roi_metrics['total_revenue']:,.2f}")
        with col4:
            st.metric("Total Profit", f"${roi_metrics['total_profit']:,.2f}")
        
        # ROI by crop type
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌾 ROI by Crop Type")
            crop_roi = pd.DataFrame(roi_metrics['crop_metrics'])
            
            fig_crop = px.bar(
                x=crop_roi.index,
                y=crop_roi['roi_percentage'],
                title="ROI by Crop Type",
                labels={'x': 'Crop Type', 'y': 'ROI (%)'}
            )
            st.plotly_chart(fig_crop, width='stretch')
        
        with col2:
            st.subheader("📅 ROI by Season")
            season_roi = pd.DataFrame(roi_metrics['season_metrics'])
            
            fig_season = px.bar(
                x=season_roi.index,
                y=season_roi['roi_percentage'],
                title="ROI by Season",
                labels={'x': 'Season', 'y': 'ROI (%)'}
            )
            st.plotly_chart(fig_season, width='stretch')
    
    def render_field_performance_comparison(self, user_id: int):
        """Render field performance comparison"""
        st.subheader("🏆 Field Performance Comparison")
        
        # Get field performance data
        df = self.analytics_manager.get_field_performance(user_id)
        
        if df.empty:
            st.info("No field performance data available. Generate sample data to see comparison.")
            return
        
        # Performance metrics table
        st.subheader("📊 Field Performance Metrics")
        
        # Sort by ROI
        df_sorted = df.sort_values('roi_percentage', ascending=False)
        
        # Display metrics
        st.dataframe(
            df_sorted[['field_name', 'crop_type', 'area_acres', 'yield_per_acre', 
                      'revenue_per_acre', 'cost_per_acre', 'profit_per_acre', 'roi_percentage']].round(2),
            width='stretch'
        )
        
        # Performance comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌾 Yield per Acre by Field")
            fig_yield = px.bar(
                df_sorted,
                x='field_name',
                y='yield_per_acre',
                title="Yield per Acre Comparison",
                labels={'field_name': 'Field Name', 'yield_per_acre': 'Yield (tons/acre)'}
            )
            fig_yield.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_yield, width='stretch')
        
        with col2:
            st.subheader("💰 Profit per Acre by Field")
            fig_profit = px.bar(
                df_sorted,
                x='field_name',
                y='profit_per_acre',
                title="Profit per Acre Comparison",
                labels={'field_name': 'Field Name', 'profit_per_acre': 'Profit ($/acre)'}
            )
            fig_profit.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_profit, width='stretch')
    
    def render_seasonal_analysis(self, user_id: int):
        """Render seasonal analysis"""
        st.subheader("📅 Seasonal Analysis")
        
        # Get field performance data
        df = self.analytics_manager.get_field_performance(user_id)
        
        if df.empty:
            st.info("No seasonal data available. Generate sample data to see analysis.")
            return
        
        # Seasonal yield analysis
        seasonal_yield = df.groupby('season')['yield_per_acre'].mean()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌾 Average Yield by Season")
            fig_seasonal = px.bar(
                x=seasonal_yield.index,
                y=seasonal_yield.values,
                title="Average Yield by Season",
                labels={'x': 'Season', 'y': 'Yield (tons/acre)'}
            )
            st.plotly_chart(fig_seasonal, width='stretch')
        
        with col2:
            st.subheader("💰 Average Profit by Season")
            seasonal_profit = df.groupby('season')['profit_per_acre'].mean()
            
            fig_profit_seasonal = px.bar(
                x=seasonal_profit.index,
                y=seasonal_profit.values,
                title="Average Profit by Season",
                labels={'x': 'Season', 'y': 'Profit ($/acre)'}
            )
            st.plotly_chart(fig_profit_seasonal, width='stretch')
    
    def run(self):
        """Main analytics dashboard runner"""
        st.title("📊 AgriForecast.ai - Advanced Analytics Dashboard")
        st.markdown("**Business Intelligence for Agricultural Operations**")
        
        # Render sidebar and get parameters
        user_id, field_id, time_period = self.render_sidebar()
        
        # Main analytics sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🌾 Yield Trends", "💰 Cost-Benefit", "📈 ROI Analysis", 
            "🏆 Field Comparison", "📅 Seasonal Analysis"
        ])
        
        with tab1:
            self.render_yield_trends(user_id, field_id)
        
        with tab2:
            self.render_cost_benefit_analysis(user_id, field_id)
        
        with tab3:
            self.render_roi_analysis(user_id)
        
        with tab4:
            self.render_field_performance_comparison(user_id)
        
        with tab5:
            self.render_seasonal_analysis(user_id)
        
        # Footer
        st.markdown("---")
        st.markdown("**📊 Advanced Analytics Dashboard - Phase 2 Complete**")
        st.markdown("*Business intelligence features for data-driven agricultural decisions*")

def main():
    """Main analytics dashboard entry point"""
    try:
        app = AdvancedAnalyticsDashboard()
        app.run()
    except Exception as e:
        st.error(f"Analytics dashboard error: {e}")
        logger.error(f"Analytics dashboard error: {e}")

if __name__ == "__main__":
    main()
