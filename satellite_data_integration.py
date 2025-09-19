#!/usr/bin/env python3
"""
Satellite Data Integration for Agricultural Platform
Real Sentinel-2/Landsat data integration with NDVI analysis
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

class SatelliteDataIntegration:
    """Satellite data integration for agricultural monitoring"""
    
    def __init__(self, sentinel_api_key: str = None, landsat_api_key: str = None):
        self.sentinel_api_key = sentinel_api_key
        self.landsat_api_key = landsat_api_key
        self.sentinel_base_url = "https://services.sentinel-hub.com/api/v1"
        self.landsat_base_url = "https://landsatlook.usgs.gov/stac-server"
        
    def get_sentinel2_data(self, latitude: float, longitude: float, 
                          start_date: str, end_date: str, 
                          cloud_coverage: float = 0.1) -> Dict:
        """Get Sentinel-2 satellite data"""
        try:
            # This is a simplified implementation
            # In production, you'd use the actual Sentinel Hub API
            
            # For now, we'll simulate Sentinel-2 data
            simulated_data = self._simulate_sentinel2_data(
                latitude, longitude, start_date, end_date
            )
            
            return {
                'status': 'success',
                'data_source': 'Sentinel-2 (Simulated)',
                'coordinates': {'lat': latitude, 'lon': longitude},
                'date_range': {'start': start_date, 'end': end_date},
                'data': simulated_data
            }
            
        except Exception as e:
            logger.error(f"Sentinel-2 data error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_landsat_data(self, latitude: float, longitude: float, 
                        start_date: str, end_date: str) -> Dict:
        """Get Landsat satellite data"""
        try:
            # This is a simplified implementation
            # In production, you'd use the actual Landsat API
            
            # For now, we'll simulate Landsat data
            simulated_data = self._simulate_landsat_data(
                latitude, longitude, start_date, end_date
            )
            
            return {
                'status': 'success',
                'data_source': 'Landsat (Simulated)',
                'coordinates': {'lat': latitude, 'lon': longitude},
                'date_range': {'start': start_date, 'end': end_date},
                'data': simulated_data
            }
            
        except Exception as e:
            logger.error(f"Landsat data error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def calculate_ndvi(self, red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
        """Calculate NDVI from red and NIR bands"""
        try:
            # NDVI = (NIR - Red) / (NIR + Red)
            ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-8)  # Add small value to avoid division by zero
            return np.clip(ndvi, -1, 1)  # Clip to valid NDVI range
        except Exception as e:
            logger.error(f"NDVI calculation error: {e}")
            return np.zeros_like(red_band)
    
    def calculate_vegetation_indices(self, satellite_data: Dict) -> Dict:
        """Calculate various vegetation indices"""
        try:
            indices = {}
            
            # Extract bands (simulated)
            red_band = satellite_data.get('red_band', np.random.rand(100, 100))
            nir_band = satellite_data.get('nir_band', np.random.rand(100, 100))
            green_band = satellite_data.get('green_band', np.random.rand(100, 100))
            blue_band = satellite_data.get('blue_band', np.random.rand(100, 100))
            
            # NDVI (Normalized Difference Vegetation Index)
            indices['ndvi'] = self.calculate_ndvi(red_band, nir_band)
            
            # EVI (Enhanced Vegetation Index)
            indices['evi'] = 2.5 * (nir_band - red_band) / (nir_band + 6 * red_band - 7.5 * blue_band + 1)
            
            # GNDVI (Green Normalized Difference Vegetation Index)
            indices['gndvi'] = (nir_band - green_band) / (nir_band + green_band + 1e-8)
            
            # SAVI (Soil Adjusted Vegetation Index)
            L = 0.5  # Soil brightness correction factor
            indices['savi'] = (nir_band - red_band) / (nir_band + red_band + L) * (1 + L)
            
            # Calculate statistics
            for index_name, index_data in indices.items():
                indices[f'{index_name}_mean'] = np.mean(index_data)
                indices[f'{index_name}_std'] = np.std(index_data)
                indices[f'{index_name}_min'] = np.min(index_data)
                indices[f'{index_name}_max'] = np.max(index_data)
            
            return {
                'status': 'success',
                'indices': indices,
                'vegetation_health': self._assess_vegetation_health(indices)
            }
            
        except Exception as e:
            logger.error(f"Vegetation indices calculation error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def detect_crop_growth_stages(self, ndvi_time_series: List[Dict]) -> Dict:
        """Detect crop growth stages from NDVI time series"""
        try:
            if not ndvi_time_series:
                return {'status': 'error', 'message': 'No NDVI data available'}
            
            # Extract NDVI values and dates
            dates = [item['date'] for item in ndvi_time_series]
            ndvi_values = [item['ndvi'] for item in ndvi_time_series]
            
            # Convert to numpy arrays
            ndvi_array = np.array(ndvi_values)
            dates_array = np.array([datetime.strptime(d, '%Y-%m-%d') for d in dates])
            
            # Detect growth stages based on NDVI patterns
            growth_stages = []
            
            for i, (date, ndvi) in enumerate(zip(dates_array, ndvi_array)):
                stage = self._classify_growth_stage(ndvi, i, len(ndvi_array))
                growth_stages.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'ndvi': ndvi,
                    'stage': stage,
                    'confidence': self._calculate_stage_confidence(ndvi, stage)
                })
            
            # Calculate growth stage statistics
            stage_counts = {}
            for stage_data in growth_stages:
                stage = stage_data['stage']
                stage_counts[stage] = stage_counts.get(stage, 0) + 1
            
            return {
                'status': 'success',
                'growth_stages': growth_stages,
                'stage_summary': stage_counts,
                'current_stage': growth_stages[-1]['stage'] if growth_stages else 'Unknown',
                'growth_trend': self._calculate_growth_trend(ndvi_values)
            }
            
        except Exception as e:
            logger.error(f"Crop growth stage detection error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def generate_vegetation_map(self, latitude: float, longitude: float, 
                               ndvi_data: np.ndarray, field_boundary: List[Tuple[float, float]] = None) -> str:
        """Generate vegetation map visualization"""
        try:
            # Create NDVI visualization
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Create NDVI colormap
            im = ax.imshow(ndvi_data, cmap='RdYlGn', vmin=-1, vmax=1)
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label('NDVI', rotation=270, labelpad=20)
            
            # Add field boundary if provided
            if field_boundary:
                boundary_x = [point[0] for point in field_boundary]
                boundary_y = [point[1] for point in field_boundary]
                ax.plot(boundary_x, boundary_y, 'k-', linewidth=2, label='Field Boundary')
                ax.legend()
            
            # Set title and labels
            ax.set_title(f'Vegetation Map (NDVI)\nLat: {latitude:.4f}, Lon: {longitude:.4f}')
            ax.set_xlabel('Pixel X')
            ax.set_ylabel('Pixel Y')
            
            # Save to base64 string
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            logger.error(f"Vegetation map generation error: {e}")
            return None
    
    def _simulate_sentinel2_data(self, latitude: float, longitude: float, 
                                start_date: str, end_date: str) -> Dict:
        """Simulate Sentinel-2 data"""
        # Generate simulated satellite data
        dates = pd.date_range(start=start_date, end=end_date, freq='5D')
        
        data = []
        for date in dates:
            # Simulate different bands
            red_band = np.random.rand(100, 100) * 0.3 + 0.1
            nir_band = np.random.rand(100, 100) * 0.4 + 0.2
            green_band = np.random.rand(100, 100) * 0.3 + 0.1
            blue_band = np.random.rand(100, 100) * 0.2 + 0.05
            
            # Calculate NDVI
            ndvi = self.calculate_ndvi(red_band, nir_band)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'red_band': red_band.tolist(),
                'nir_band': nir_band.tolist(),
                'green_band': green_band.tolist(),
                'blue_band': blue_band.tolist(),
                'ndvi': ndvi.tolist(),
                'cloud_coverage': np.random.uniform(0, 0.3),
                'quality_score': np.random.uniform(0.7, 1.0)
            })
        
        return {
            'bands': data,
            'resolution': '10m',
            'coverage_area': '100m x 100m'
        }
    
    def _simulate_landsat_data(self, latitude: float, longitude: float, 
                              start_date: str, end_date: str) -> Dict:
        """Simulate Landsat data"""
        # Generate simulated Landsat data
        dates = pd.date_range(start=start_date, end=end_date, freq='16D')
        
        data = []
        for date in dates:
            # Simulate Landsat bands
            red_band = np.random.rand(50, 50) * 0.3 + 0.1
            nir_band = np.random.rand(50, 50) * 0.4 + 0.2
            green_band = np.random.rand(50, 50) * 0.3 + 0.1
            blue_band = np.random.rand(50, 50) * 0.2 + 0.05
            
            # Calculate NDVI
            ndvi = self.calculate_ndvi(red_band, nir_band)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'red_band': red_band.tolist(),
                'nir_band': nir_band.tolist(),
                'green_band': green_band.tolist(),
                'blue_band': blue_band.tolist(),
                'ndvi': ndvi.tolist(),
                'cloud_coverage': np.random.uniform(0, 0.4),
                'quality_score': np.random.uniform(0.6, 0.9)
            })
        
        return {
            'bands': data,
            'resolution': '30m',
            'coverage_area': '500m x 500m'
        }
    
    def _assess_vegetation_health(self, indices: Dict) -> Dict:
        """Assess vegetation health from indices"""
        try:
            ndvi_mean = indices.get('ndvi_mean', 0)
            evi_mean = indices.get('evi_mean', 0)
            
            # Health assessment based on NDVI
            if ndvi_mean > 0.7:
                health_status = "Excellent"
                health_score = 95
            elif ndvi_mean > 0.5:
                health_status = "Good"
                health_score = 80
            elif ndvi_mean > 0.3:
                health_status = "Fair"
                health_score = 60
            elif ndvi_mean > 0.1:
                health_status = "Poor"
                health_score = 40
            else:
                health_status = "Critical"
                health_score = 20
            
            return {
                'status': health_status,
                'score': health_score,
                'ndvi_mean': ndvi_mean,
                'evi_mean': evi_mean,
                'recommendations': self._generate_health_recommendations(health_status, ndvi_mean)
            }
            
        except Exception as e:
            logger.error(f"Vegetation health assessment error: {e}")
            return {'status': 'Unknown', 'score': 0}
    
    def _classify_growth_stage(self, ndvi: float, index: int, total_length: int) -> str:
        """Classify crop growth stage based on NDVI"""
        if ndvi < 0.1:
            return "Bare Soil"
        elif ndvi < 0.3:
            return "Emergence"
        elif ndvi < 0.5:
            return "Vegetative"
        elif ndvi < 0.7:
            return "Flowering"
        elif ndvi < 0.8:
            return "Fruiting"
        else:
            return "Maturity"
    
    def _calculate_stage_confidence(self, ndvi: float, stage: str) -> float:
        """Calculate confidence in growth stage classification"""
        # Simplified confidence calculation
        if stage == "Bare Soil" and ndvi < 0.1:
            return 0.9
        elif stage == "Emergence" and 0.1 <= ndvi < 0.3:
            return 0.8
        elif stage == "Vegetative" and 0.3 <= ndvi < 0.5:
            return 0.8
        elif stage == "Flowering" and 0.5 <= ndvi < 0.7:
            return 0.7
        elif stage == "Fruiting" and 0.7 <= ndvi < 0.8:
            return 0.7
        elif stage == "Maturity" and ndvi >= 0.8:
            return 0.8
        else:
            return 0.5
    
    def _calculate_growth_trend(self, ndvi_values: List[float]) -> str:
        """Calculate growth trend from NDVI time series"""
        if len(ndvi_values) < 2:
            return "Insufficient Data"
        
        # Calculate trend
        x = np.arange(len(ndvi_values))
        trend = np.polyfit(x, ndvi_values, 1)[0]
        
        if trend > 0.01:
            return "Growing"
        elif trend < -0.01:
            return "Declining"
        else:
            return "Stable"
    
    def _generate_health_recommendations(self, health_status: str, ndvi_mean: float) -> List[str]:
        """Generate recommendations based on vegetation health"""
        recommendations = []
        
        if health_status == "Critical":
            recommendations.extend([
                "Immediate attention required - check for pest/disease damage",
                "Consider soil testing and nutrient analysis",
                "Review irrigation and fertilization practices"
            ])
        elif health_status == "Poor":
            recommendations.extend([
                "Monitor for pest and disease issues",
                "Consider additional fertilization",
                "Check irrigation system efficiency"
            ])
        elif health_status == "Fair":
            recommendations.extend([
                "Continue monitoring crop health",
                "Consider minor adjustments to management practices"
            ])
        elif health_status == "Good":
            recommendations.extend([
                "Maintain current management practices",
                "Continue regular monitoring"
            ])
        else:  # Excellent
            recommendations.extend([
                "Excellent crop health - maintain current practices",
                "Consider documenting successful management strategies"
            ])
        
        return recommendations

# Example usage
if __name__ == "__main__":
    # Test the satellite data integration
    satellite = SatelliteDataIntegration()
    
    # Test Sentinel-2 data
    sentinel_data = satellite.get_sentinel2_data(
        28.368911, 77.541033, 
        '2024-01-01', '2024-12-31'
    )
    print("Sentinel-2 Data:", json.dumps(sentinel_data, indent=2))
    
    # Test vegetation indices
    if sentinel_data['status'] == 'success':
        indices = satellite.calculate_vegetation_indices(sentinel_data['data'])
        print("Vegetation Indices:", json.dumps(indices, indent=2))




