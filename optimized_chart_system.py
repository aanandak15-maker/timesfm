"""
Optimized Chart Rendering System for AgriForecast.ai
High-performance chart rendering with data virtualization and smart caching
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Callable, Union
import time
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
from dataclasses import dataclass
import json

@dataclass
class ChartConfig:
    """Configuration for optimized charts"""
    max_points: int = 1000
    decimation_factor: int = 10
    cache_enabled: bool = True
    lazy_render: bool = True
    animation_enabled: bool = True
    responsive: bool = True
    height: int = 400
    margin: dict = None

class DataProcessor:
    """Intelligent data processing for large datasets"""
    
    def __init__(self):
        self.cache = {}
    
    def decimate_data(self, data: pd.DataFrame, target_points: int, x_col: str = None) -> pd.DataFrame:
        """
        Intelligently reduce data points while preserving trends
        
        Args:
            data: Input DataFrame
            target_points: Target number of points
            x_col: X-axis column name for time-based decimation
        
        Returns:
            Decimated DataFrame
        """
        if len(data) <= target_points:
            return data
        
        if x_col and x_col in data.columns:
            # Time-based decimation
            return self._time_based_decimation(data, target_points, x_col)
        else:
            # Simple interval-based decimation
            step = len(data) // target_points
            return data.iloc[::max(1, step)].copy()
    
    def _time_based_decimation(self, data: pd.DataFrame, target_points: int, time_col: str) -> pd.DataFrame:
        """Decimate based on time intervals"""
        if pd.api.types.is_datetime64_any_dtype(data[time_col]):
            # Already datetime
            time_data = data[time_col]
        else:
            # Convert to datetime
            time_data = pd.to_datetime(data[time_col])
        
        # Calculate time intervals
        time_span = time_data.max() - time_data.min()
        interval = time_span / target_points
        
        # Group by time intervals and take representative points
        data_copy = data.copy()
        data_copy['time_group'] = (time_data - time_data.min()) // interval
        
        # Take first, last, min, max from each group to preserve trends
        result_frames = []
        for group_id, group in data_copy.groupby('time_group'):
            if len(group) <= 4:
                result_frames.append(group)
            else:
                # Take representative points
                indices = []
                indices.append(group.index[0])  # First
                indices.append(group.index[-1])  # Last
                
                # Add extreme points for numeric columns
                for col in group.select_dtypes(include=[np.number]).columns:
                    if col != 'time_group':
                        indices.append(group[col].idxmin())  # Min
                        indices.append(group[col].idxmax())  # Max
                
                # Remove duplicates and sort
                indices = sorted(list(set(indices)))
                result_frames.append(group.loc[indices])
        
        result = pd.concat(result_frames).drop('time_group', axis=1)
        return result.sort_values(time_col).reset_index(drop=True)
    
    def aggregate_data(self, data: pd.DataFrame, time_col: str, 
                      value_cols: List[str], interval: str = 'H') -> pd.DataFrame:
        """
        Aggregate data for better performance
        
        Args:
            data: Input DataFrame
            time_col: Time column name
            value_cols: Columns to aggregate
            interval: Aggregation interval ('H', 'D', 'W', 'M')
        
        Returns:
            Aggregated DataFrame
        """
        data_copy = data.copy()
        data_copy[time_col] = pd.to_datetime(data_copy[time_col])
        data_copy.set_index(time_col, inplace=True)
        
        agg_funcs = {}
        for col in value_cols:
            if col in data_copy.columns:
                agg_funcs[col] = ['mean', 'min', 'max', 'std']
        
        aggregated = data_copy.resample(interval).agg(agg_funcs)
        aggregated.columns = [f"{col[0]}_{col[1]}" for col in aggregated.columns]
        
        return aggregated.reset_index()
    
    def detect_outliers(self, data: pd.Series, method: str = 'iqr') -> pd.Series:
        """Detect outliers in data"""
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (data < lower_bound) | (data > upper_bound)
        elif method == 'zscore':
            z_scores = np.abs((data - data.mean()) / data.std())
            return z_scores > 3
        else:
            return pd.Series([False] * len(data), index=data.index)

class OptimizedChart:
    """High-performance chart with intelligent optimizations"""
    
    def __init__(self, config: ChartConfig = None):
        self.config = config or ChartConfig()
        self.data_processor = DataProcessor()
        self.render_cache = {}
        
    def _get_cache_key(self, data_hash: str, chart_type: str, **kwargs) -> str:
        """Generate cache key for chart"""
        cache_data = {
            'data_hash': data_hash,
            'chart_type': chart_type,
            'config': self.config.__dict__,
            'kwargs': kwargs
        }
        return str(hash(str(cache_data)))
    
    def _hash_data(self, data: Union[pd.DataFrame, Dict]) -> str:
        """Generate hash for data"""
        if isinstance(data, pd.DataFrame):
            return str(hash(tuple(data.values.flatten())))
        else:
            return str(hash(str(data)))
    
    def create_line_chart(self, data: pd.DataFrame, x_col: str, y_cols: List[str],
                         title: str = "", **kwargs) -> go.Figure:
        """
        Create optimized line chart
        
        Args:
            data: Input DataFrame
            x_col: X-axis column
            y_cols: Y-axis columns
            title: Chart title
            **kwargs: Additional Plotly arguments
        
        Returns:
            Plotly Figure
        """
        # Check cache
        data_hash = self._hash_data(data)
        cache_key = self._get_cache_key(data_hash, 'line', x_col=x_col, y_cols=y_cols, **kwargs)
        
        if self.config.cache_enabled and cache_key in self.render_cache:
            return self.render_cache[cache_key]
        
        # Process data
        processed_data = data.copy()
        if len(processed_data) > self.config.max_points:
            processed_data = self.data_processor.decimate_data(
                processed_data, self.config.max_points, x_col
            )
        
        # Create figure
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set1
        for i, y_col in enumerate(y_cols):
            if y_col in processed_data.columns:
                fig.add_trace(go.Scatter(
                    x=processed_data[x_col],
                    y=processed_data[y_col],
                    mode='lines+markers',
                    name=y_col,
                    line=dict(color=colors[i % len(colors)], width=2),
                    marker=dict(size=4),
                    hovertemplate=f"<b>{y_col}</b><br>" +
                                 f"{x_col}: %{{x}}<br>" +
                                 f"{y_col}: %{{y}}<br>" +
                                 "<extra></extra>"
                ))
        
        # Configure layout
        fig.update_layout(
            title=title,
            height=self.config.height,
            margin=self.config.margin or dict(l=40, r=40, t=40, b=40),
            hovermode='x unified',
            showlegend=len(y_cols) > 1,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            **kwargs
        )
        
        # Responsive design
        if self.config.responsive:
            fig.update_layout(
                autosize=True,
                margin=dict(l=0, r=0, t=30, b=0)
            )
        
        # Cache result
        if self.config.cache_enabled:
            self.render_cache[cache_key] = fig
        
        return fig
    
    def create_bar_chart(self, data: pd.DataFrame, x_col: str, y_col: str,
                        color_col: str = None, title: str = "", **kwargs) -> go.Figure:
        """Create optimized bar chart"""
        data_hash = self._hash_data(data)
        cache_key = self._get_cache_key(data_hash, 'bar', x_col=x_col, y_col=y_col, **kwargs)
        
        if self.config.cache_enabled and cache_key in self.render_cache:
            return self.render_cache[cache_key]
        
        # Process data for bar charts
        processed_data = data.copy()
        if len(processed_data) > self.config.max_points:
            # For bar charts, aggregate by grouping
            processed_data = processed_data.groupby(x_col)[y_col].agg(['sum', 'mean', 'count']).reset_index()
            processed_data[y_col] = processed_data['sum']  # Use sum as default
        
        # Create figure
        if color_col and color_col in processed_data.columns:
            fig = px.bar(processed_data, x=x_col, y=y_col, color=color_col, title=title)
        else:
            fig = px.bar(processed_data, x=x_col, y=y_col, title=title)
        
        # Configure layout
        fig.update_layout(
            height=self.config.height,
            margin=self.config.margin or dict(l=40, r=40, t=40, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            **kwargs
        )
        
        if self.config.cache_enabled:
            self.render_cache[cache_key] = fig
        
        return fig
    
    def create_heatmap(self, data: pd.DataFrame, x_col: str, y_col: str, 
                      z_col: str, title: str = "", **kwargs) -> go.Figure:
        """Create optimized heatmap"""
        data_hash = self._hash_data(data)
        cache_key = self._get_cache_key(data_hash, 'heatmap', x_col=x_col, y_col=y_col, z_col=z_col, **kwargs)
        
        if self.config.cache_enabled and cache_key in self.render_cache:
            return self.render_cache[cache_key]
        
        # Create pivot table for heatmap
        pivot_data = data.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='mean')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=title,
            height=self.config.height,
            margin=self.config.margin or dict(l=40, r=40, t=40, b=40),
            **kwargs
        )
        
        if self.config.cache_enabled:
            self.render_cache[cache_key] = fig
        
        return fig
    
    def create_scatter_plot(self, data: pd.DataFrame, x_col: str, y_col: str,
                          size_col: str = None, color_col: str = None,
                          title: str = "", **kwargs) -> go.Figure:
        """Create optimized scatter plot"""
        data_hash = self._hash_data(data)
        cache_key = self._get_cache_key(data_hash, 'scatter', x_col=x_col, y_col=y_col, **kwargs)
        
        if self.config.cache_enabled and cache_key in self.render_cache:
            return self.render_cache[cache_key]
        
        # Sample data if too large
        processed_data = data.copy()
        if len(processed_data) > self.config.max_points:
            processed_data = processed_data.sample(n=self.config.max_points)
        
        # Create scatter plot
        fig = px.scatter(
            processed_data, 
            x=x_col, 
            y=y_col,
            size=size_col,
            color=color_col,
            title=title,
            **kwargs
        )
        
        fig.update_layout(
            height=self.config.height,
            margin=self.config.margin or dict(l=40, r=40, t=40, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        if self.config.cache_enabled:
            self.render_cache[cache_key] = fig
        
        return fig

class ChartManager:
    """Manager for optimized charts with lazy loading and caching"""
    
    def __init__(self):
        self.charts = {}
        self.chart_configs = {}
        self.loading_states = {}
        
    def register_chart(self, chart_id: str, chart_fn: Callable, 
                      config: ChartConfig = None, lazy: bool = True):
        """Register a chart for lazy loading"""
        self.charts[chart_id] = chart_fn
        self.chart_configs[chart_id] = config or ChartConfig()
        
        if not lazy:
            # Load immediately
            self.load_chart(chart_id)
    
    def load_chart(self, chart_id: str, container = None):
        """Load and display a chart"""
        if chart_id not in self.charts:
            st.error(f"Chart not found: {chart_id}")
            return None
        
        if chart_id in self.loading_states:
            st.info(f"Loading {chart_id}...")
            return None
        
        self.loading_states[chart_id] = True
        
        try:
            config = self.chart_configs[chart_id]
            
            if config.lazy_render:
                with st.spinner(f"Rendering {chart_id}..."):
                    chart = self.charts[chart_id]()
            else:
                chart = self.charts[chart_id]()
            
            if container:
                with container:
                    st.plotly_chart(chart, use_container_width=True)
            else:
                st.plotly_chart(chart, use_container_width=True)
            
            del self.loading_states[chart_id]
            return chart
            
        except Exception as e:
            st.error(f"Failed to render chart {chart_id}: {str(e)}")
            if chart_id in self.loading_states:
                del self.loading_states[chart_id]
            return None
    
    def load_charts_parallel(self, chart_ids: List[str]):
        """Load multiple charts in parallel"""
        containers = {}
        for chart_id in chart_ids:
            containers[chart_id] = st.empty()
        
        def load_single_chart(chart_id):
            try:
                chart = self.charts[chart_id]()
                with containers[chart_id]:
                    st.plotly_chart(chart, use_container_width=True)
                return True
            except Exception as e:
                with containers[chart_id]:
                    st.error(f"Failed to load {chart_id}: {str(e)}")
                return False
        
        with ThreadPoolExecutor(max_workers=len(chart_ids)) as executor:
            futures = {executor.submit(load_single_chart, cid): cid for cid in chart_ids}
            results = {}
            
            for future in futures:
                chart_id = futures[future]
                results[chart_id] = future.result()
        
        return results

# Agricultural-specific chart functions
def create_yield_forecast_chart(data: pd.DataFrame) -> go.Figure:
    """Create optimized yield forecast chart"""
    chart = OptimizedChart(ChartConfig(max_points=500, height=400))
    
    return chart.create_line_chart(
        data=data,
        x_col='date',
        y_cols=['predicted_yield', 'actual_yield'],
        title="🌾 Yield Forecast vs Actual"
    )

def create_weather_dashboard(weather_data: pd.DataFrame) -> go.Figure:
    """Create optimized weather dashboard"""
    chart = OptimizedChart(ChartConfig(max_points=200, height=350))
    
    # Create subplot
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Temperature', 'Humidity', 'Rainfall', 'Wind Speed'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Add traces
    fig.add_trace(
        go.Scatter(x=weather_data['date'], y=weather_data['temperature'], 
                  name='Temperature', line=dict(color='red')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=weather_data['date'], y=weather_data['humidity'], 
                  name='Humidity', line=dict(color='blue')),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(x=weather_data['date'], y=weather_data['rainfall'], 
               name='Rainfall', marker_color='lightblue'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=weather_data['date'], y=weather_data['wind_speed'], 
                  name='Wind Speed', line=dict(color='green')),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="🌤️ Weather Dashboard",
        showlegend=False
    )
    
    return fig

def create_market_analysis_chart(market_data: pd.DataFrame) -> go.Figure:
    """Create optimized market analysis chart"""
    chart = OptimizedChart(ChartConfig(max_points=300, height=400))
    
    return chart.create_line_chart(
        data=market_data,
        x_col='date',
        y_cols=['price', 'volume'],
        title="💰 Market Price Analysis"
    )

# Demo and example usage
def demo_optimized_charts():
    """Demo of optimized chart system"""
    st.title("📊 Optimized Chart System Demo")
    
    # Generate sample data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    
    # Large dataset simulation
    large_data = pd.DataFrame({
        'date': dates,
        'yield': np.random.normal(100, 20, len(dates)),
        'temperature': 20 + 10 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365) + np.random.normal(0, 2, len(dates)),
        'rainfall': np.random.exponential(5, len(dates)),
        'price': 50 + np.cumsum(np.random.normal(0, 2, len(dates)))
    })
    
    st.write(f"Dataset size: {len(large_data)} points")
    
    # Chart configuration
    col1, col2 = st.columns(2)
    with col1:
        max_points = st.slider("Max Points", 100, 2000, 1000)
        cache_enabled = st.checkbox("Enable Caching", True)
    
    with col2:
        chart_height = st.slider("Chart Height", 300, 800, 400)
        lazy_render = st.checkbox("Lazy Rendering", True)
    
    config = ChartConfig(
        max_points=max_points,
        cache_enabled=cache_enabled,
        height=chart_height,
        lazy_render=lazy_render
    )
    
    # Create optimized charts
    chart_manager = ChartManager()
    optimized_chart = OptimizedChart(config)
    
    # Performance comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Optimized Chart")
        start_time = time.time()
        
        fig1 = optimized_chart.create_line_chart(
            large_data, 'date', ['yield', 'price'], 
            "Optimized Yield & Price Trends"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        optimized_time = time.time() - start_time
        st.success(f"Render time: {optimized_time:.3f}s")
    
    with col2:
        st.subheader("📈 Standard Chart")
        start_time = time.time()
        
        # Standard Plotly chart (no optimization)
        fig2 = px.line(large_data, x='date', y=['yield', 'price'], 
                      title="Standard Yield & Price Trends")
        st.plotly_chart(fig2, use_container_width=True)
        
        standard_time = time.time() - start_time
        st.info(f"Render time: {standard_time:.3f}s")
    
    # Performance metrics
    if optimized_time > 0 and standard_time > 0:
        improvement = ((standard_time - optimized_time) / standard_time) * 100
        if improvement > 0:
            st.success(f"⚡ Performance improvement: {improvement:.1f}%")
        else:
            st.warning(f"Performance difference: {abs(improvement):.1f}% slower")

if __name__ == "__main__":
    demo_optimized_charts()
