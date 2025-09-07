import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class MultiFieldYieldPrediction:
    """Enhanced yield prediction system for multiple fields"""
    
    def __init__(self):
        self.crop_models = {
            'Rice': self._get_rice_model(),
            'Wheat': self._get_wheat_model(),
            'Corn': self._get_corn_model(),
            'Soybean': self._get_soybean_model(),
            'Cotton': self._get_cotton_model(),
            'Sugarcane': self._get_sugarcane_model()
        }
        logger.info("Multi-field yield prediction system initialized")
    
    def _get_rice_model(self) -> Dict:
        """Get rice yield prediction model parameters"""
        return {
            'base_yield': 4.5,  # tons per hectare
            'temperature_optimum': 28,
            'temperature_range': 8,
            'humidity_optimum': 70,
            'humidity_range': 20,
            'precipitation_optimum': 1500,  # mm per season
            'precipitation_range': 500,
            'soil_ph_optimum': 6.5,
            'soil_ph_range': 1.0,
            'nitrogen_optimum': 120,
            'nitrogen_range': 40,
            'ndvi_optimum': 0.8,
            'ndvi_range': 0.2
        }
    
    def _get_wheat_model(self) -> Dict:
        """Get wheat yield prediction model parameters"""
        return {
            'base_yield': 3.2,
            'temperature_optimum': 22,
            'temperature_range': 10,
            'humidity_optimum': 60,
            'humidity_range': 25,
            'precipitation_optimum': 600,
            'precipitation_range': 200,
            'soil_ph_optimum': 6.8,
            'soil_ph_range': 0.8,
            'nitrogen_optimum': 100,
            'nitrogen_range': 30,
            'ndvi_optimum': 0.75,
            'ndvi_range': 0.15
        }
    
    def _get_corn_model(self) -> Dict:
        """Get corn yield prediction model parameters"""
        return {
            'base_yield': 8.5,
            'temperature_optimum': 26,
            'temperature_range': 6,
            'humidity_optimum': 65,
            'humidity_range': 20,
            'precipitation_optimum': 800,
            'precipitation_range': 300,
            'soil_ph_optimum': 6.2,
            'soil_ph_range': 0.8,
            'nitrogen_optimum': 150,
            'nitrogen_range': 50,
            'ndvi_optimum': 0.85,
            'ndvi_range': 0.15
        }
    
    def _get_soybean_model(self) -> Dict:
        """Get soybean yield prediction model parameters"""
        return {
            'base_yield': 2.8,
            'temperature_optimum': 24,
            'temperature_range': 8,
            'humidity_optimum': 70,
            'humidity_range': 20,
            'precipitation_optimum': 700,
            'precipitation_range': 250,
            'soil_ph_optimum': 6.5,
            'soil_ph_range': 0.8,
            'nitrogen_optimum': 80,
            'nitrogen_range': 30,
            'ndvi_optimum': 0.75,
            'ndvi_range': 0.15
        }
    
    def _get_cotton_model(self) -> Dict:
        """Get cotton yield prediction model parameters"""
        return {
            'base_yield': 1.8,
            'temperature_optimum': 30,
            'temperature_range': 8,
            'humidity_optimum': 60,
            'humidity_range': 25,
            'precipitation_optimum': 600,
            'precipitation_range': 200,
            'soil_ph_optimum': 6.0,
            'soil_ph_range': 1.0,
            'nitrogen_optimum': 90,
            'nitrogen_range': 30,
            'ndvi_optimum': 0.70,
            'ndvi_range': 0.20
        }
    
    def _get_sugarcane_model(self) -> Dict:
        """Get sugarcane yield prediction model parameters"""
        return {
            'base_yield': 80.0,
            'temperature_optimum': 28,
            'temperature_range': 6,
            'humidity_optimum': 75,
            'humidity_range': 15,
            'precipitation_optimum': 2000,
            'precipitation_range': 500,
            'soil_ph_optimum': 6.5,
            'soil_ph_range': 0.8,
            'nitrogen_optimum': 200,
            'nitrogen_range': 60,
            'ndvi_optimum': 0.80,
            'ndvi_range': 0.15
        }
    
    def predict_yield_for_field(self, field_data: Dict) -> Dict:
        """Predict yield for a single field"""
        try:
            field_id = field_data['field_id']
            crop_type = field_data['crop_type']
            latitude = field_data['latitude']
            longitude = field_data['longitude']
            
            # Get model for crop type
            if crop_type not in self.crop_models:
                crop_type = 'Rice'  # Default to rice
            
            model = self.crop_models[crop_type]
            
            # Extract data
            real_time_weather = field_data.get('real_time_weather', {})
            historical_weather = field_data.get('historical_weather', [])
            soil_data = field_data.get('soil_data', {})
            satellite_data = field_data.get('satellite_data', [])
            
            # Calculate yield factors
            weather_factor = self._calculate_weather_factor(real_time_weather, historical_weather, model)
            soil_factor = self._calculate_soil_factor(soil_data, model)
            satellite_factor = self._calculate_satellite_factor(satellite_data, model)
            
            # Calculate base yield
            base_yield = model['base_yield']
            
            # Apply factors
            predicted_yield = base_yield * weather_factor * soil_factor * satellite_factor
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(weather_factor, soil_factor, satellite_factor)
            
            # Generate scenarios
            scenarios = self._generate_scenarios(predicted_yield, weather_factor, soil_factor, satellite_factor)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                weather_factor, soil_factor, satellite_factor, real_time_weather, soil_data
            )
            
            # Calculate risk factors
            risk_factors = self._calculate_risk_factors(
                real_time_weather, historical_weather, soil_data, satellite_data
            )
            
            prediction_result = {
                'field_id': field_id,
                'crop_type': crop_type,
                'predicted_yield': round(predicted_yield, 2),
                'confidence_score': round(confidence, 2),
                'weather_factor': round(weather_factor, 2),
                'soil_factor': round(soil_factor, 2),
                'satellite_factor': round(satellite_factor, 2),
                'scenarios': scenarios,
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'prediction_date': datetime.now().isoformat(),
                'latitude': latitude,
                'longitude': longitude
            }
            
            logger.info(f"Yield prediction completed for field {field_id}: {predicted_yield:.2f} tons/ha")
            return prediction_result
            
        except Exception as e:
            logger.error(f"Error predicting yield for field {field_id}: {e}")
            return {}
    
    def _calculate_weather_factor(self, real_time_weather: Dict, historical_weather: List[Dict], model: Dict) -> float:
        """Calculate weather impact factor"""
        try:
            if not real_time_weather or not historical_weather:
                return 0.8  # Default factor if no weather data
            
            # Current weather impact
            temp = real_time_weather.get('temperature_c', 25)
            humidity = real_time_weather.get('humidity', 70)
            precipitation = real_time_weather.get('precipitation', 0)
            
            # Temperature factor
            temp_opt = model['temperature_optimum']
            temp_range = model['temperature_range']
            temp_factor = max(0, 1 - abs(temp - temp_opt) / temp_range)
            
            # Humidity factor
            hum_opt = model['humidity_optimum']
            hum_range = model['humidity_range']
            hum_factor = max(0, 1 - abs(humidity - hum_opt) / hum_range)
            
            # Precipitation factor (based on historical data)
            total_precip = sum(day.get('precipitation', 0) for day in historical_weather)
            avg_precip = total_precip / len(historical_weather) if historical_weather else 0
            precip_opt = model['precipitation_optimum'] / 365  # Convert to daily average
            precip_range = model['precipitation_range'] / 365
            precip_factor = max(0, 1 - abs(avg_precip - precip_opt) / precip_range)
            
            # Combined weather factor
            weather_factor = (temp_factor * 0.4 + hum_factor * 0.3 + precip_factor * 0.3)
            return min(1.2, max(0.3, weather_factor))  # Clamp between 0.3 and 1.2
            
        except Exception as e:
            logger.error(f"Error calculating weather factor: {e}")
            return 0.8
    
    def _calculate_soil_factor(self, soil_data: Dict, model: Dict) -> float:
        """Calculate soil impact factor"""
        try:
            if not soil_data:
                return 0.8  # Default factor if no soil data
            
            ph = soil_data.get('ph', 6.5)
            nitrogen = soil_data.get('nitrogen', 50)
            organic_matter = soil_data.get('organic_matter', 2.0)
            
            # pH factor
            ph_opt = model['soil_ph_optimum']
            ph_range = model['soil_ph_range']
            ph_factor = max(0, 1 - abs(ph - ph_opt) / ph_range)
            
            # Nitrogen factor
            n_opt = model['nitrogen_optimum']
            n_range = model['nitrogen_range']
            n_factor = max(0, 1 - abs(nitrogen - n_opt) / n_range)
            
            # Organic matter factor
            om_factor = min(1.2, max(0.5, organic_matter / 2.0))
            
            # Combined soil factor
            soil_factor = (ph_factor * 0.4 + n_factor * 0.4 + om_factor * 0.2)
            return min(1.2, max(0.3, soil_factor))  # Clamp between 0.3 and 1.2
            
        except Exception as e:
            logger.error(f"Error calculating soil factor: {e}")
            return 0.8
    
    def _calculate_satellite_factor(self, satellite_data: List[Dict], model: Dict) -> float:
        """Calculate satellite/NDVI impact factor"""
        try:
            if not satellite_data:
                return 0.8  # Default factor if no satellite data
            
            # Get latest NDVI
            latest_ndvi = satellite_data[-1].get('ndvi', 0.5)
            
            # NDVI factor
            ndvi_opt = model['ndvi_optimum']
            ndvi_range = model['ndvi_range']
            ndvi_factor = max(0, 1 - abs(latest_ndvi - ndvi_opt) / ndvi_range)
            
            # Vegetation health factor
            health = satellite_data[-1].get('vegetation_health', 'Fair')
            health_factors = {'Excellent': 1.2, 'Good': 1.0, 'Fair': 0.8, 'Poor': 0.5}
            health_factor = health_factors.get(health, 0.8)
            
            # Combined satellite factor
            satellite_factor = (ndvi_factor * 0.7 + health_factor * 0.3)
            return min(1.2, max(0.3, satellite_factor))  # Clamp between 0.3 and 1.2
            
        except Exception as e:
            logger.error(f"Error calculating satellite factor: {e}")
            return 0.8
    
    def _calculate_confidence_score(self, weather_factor: float, soil_factor: float, satellite_factor: float) -> float:
        """Calculate confidence score for the prediction"""
        try:
            # Base confidence on data availability and consistency
            factors = [weather_factor, soil_factor, satellite_factor]
            avg_factor = np.mean(factors)
            factor_consistency = 1 - np.std(factors)  # Lower std = higher consistency
            
            confidence = (avg_factor * 0.6 + factor_consistency * 0.4)
            return min(0.95, max(0.3, confidence))  # Clamp between 0.3 and 0.95
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.7
    
    def _generate_scenarios(self, base_yield: float, weather_factor: float, 
                          soil_factor: float, satellite_factor: float) -> Dict:
        """Generate different yield scenarios"""
        try:
            # Drought scenario (reduced weather factor)
            drought_yield = base_yield * (weather_factor * 0.6) * soil_factor * satellite_factor
            
            # Optimal scenario (enhanced factors)
            optimal_yield = base_yield * min(1.2, weather_factor * 1.1) * min(1.2, soil_factor * 1.1) * min(1.2, satellite_factor * 1.1)
            
            # Normal scenario (base yield)
            normal_yield = base_yield * weather_factor * soil_factor * satellite_factor
            
            return {
                'drought': round(drought_yield, 2),
                'normal': round(normal_yield, 2),
                'optimal': round(optimal_yield, 2),
                'drought_percent': round((drought_yield / normal_yield - 1) * 100, 1),
                'optimal_percent': round((optimal_yield / normal_yield - 1) * 100, 1)
            }
            
        except Exception as e:
            logger.error(f"Error generating scenarios: {e}")
            return {}
    
    def _generate_recommendations(self, weather_factor: float, soil_factor: float, 
                                satellite_factor: float, weather: Dict, soil: Dict) -> List[str]:
        """Generate recommendations based on current conditions"""
        try:
            recommendations = []
            
            # Weather recommendations
            if weather_factor < 0.7:
                temp = weather.get('temperature_c', 25)
                if temp > 35:
                    recommendations.append("🌡️ High temperature detected - consider irrigation and shade")
                elif temp < 15:
                    recommendations.append("❄️ Low temperature detected - consider protective measures")
                
                humidity = weather.get('humidity', 70)
                if humidity < 40:
                    recommendations.append("💧 Low humidity - increase irrigation frequency")
                elif humidity > 85:
                    recommendations.append("🌧️ High humidity - monitor for fungal diseases")
            
            # Soil recommendations
            if soil_factor < 0.7:
                ph = soil.get('ph', 6.5)
                if ph < 6.0:
                    recommendations.append("🧪 Soil pH too low - consider lime application")
                elif ph > 7.5:
                    recommendations.append("🧪 Soil pH too high - consider sulfur application")
                
                nitrogen = soil.get('nitrogen', 50)
                if nitrogen < 30:
                    recommendations.append("🌱 Low nitrogen - apply nitrogen fertilizer")
                elif nitrogen > 150:
                    recommendations.append("⚠️ High nitrogen - reduce fertilizer application")
            
            # Satellite recommendations
            if satellite_factor < 0.7:
                recommendations.append("📡 Poor vegetation health - check for pests and diseases")
                recommendations.append("🔍 Consider field inspection and soil testing")
            
            # General recommendations
            if not recommendations:
                recommendations.append("✅ Field conditions are optimal - maintain current practices")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["⚠️ Unable to generate recommendations - check data quality"]
    
    def _calculate_risk_factors(self, weather: Dict, historical_weather: List[Dict], 
                              soil: Dict, satellite_data: List[Dict]) -> List[Dict]:
        """Calculate risk factors for the field"""
        try:
            risk_factors = []
            
            # Weather risks
            if weather:
                temp = weather.get('temperature_c', 25)
                if temp > 35:
                    risk_factors.append({
                        'type': 'Heat Stress',
                        'severity': 'High' if temp > 40 else 'Medium',
                        'description': f'Temperature {temp}°C exceeds optimal range',
                        'impact': 'Reduced yield and quality'
                    })
                
                precipitation = weather.get('precipitation', 0)
                if precipitation > 20:
                    risk_factors.append({
                        'type': 'Flooding Risk',
                        'severity': 'High' if precipitation > 50 else 'Medium',
                        'description': f'Heavy rainfall {precipitation}mm in 24h',
                        'impact': 'Waterlogging and root damage'
                    })
            
            # Soil risks
            if soil:
                ph = soil.get('ph', 6.5)
                if ph < 5.5 or ph > 8.0:
                    risk_factors.append({
                        'type': 'Soil pH Imbalance',
                        'severity': 'High',
                        'description': f'Soil pH {ph} is outside optimal range',
                        'impact': 'Nutrient availability issues'
                    })
            
            # Satellite risks
            if satellite_data:
                latest_ndvi = satellite_data[-1].get('ndvi', 0.5)
                if latest_ndvi < 0.3:
                    risk_factors.append({
                        'type': 'Poor Vegetation Health',
                        'severity': 'High',
                        'description': f'NDVI {latest_ndvi:.2f} indicates poor crop health',
                        'impact': 'Significant yield reduction expected'
                    })
            
            return risk_factors
            
        except Exception as e:
            logger.error(f"Error calculating risk factors: {e}")
            return []
    
    def predict_yield_for_multiple_fields(self, fields_data: Dict) -> Dict:
        """Predict yield for multiple fields"""
        try:
            predictions = {}
            
            for field_id, field_data in fields_data.items():
                prediction = self.predict_yield_for_field(field_data)
                if prediction:
                    predictions[field_id] = prediction
            
            # Calculate summary statistics
            if predictions:
                yields = [p['predicted_yield'] for p in predictions.values()]
                total_yield = sum(yields)
                avg_yield = np.mean(yields)
                max_yield = max(yields)
                min_yield = min(yields)
                
                summary = {
                    'total_fields': len(predictions),
                    'total_yield': round(total_yield, 2),
                    'average_yield': round(avg_yield, 2),
                    'max_yield': round(max_yield, 2),
                    'min_yield': round(min_yield, 2),
                    'yield_range': round(max_yield - min_yield, 2)
                }
            else:
                summary = {}
            
            result = {
                'predictions': predictions,
                'summary': summary,
                'prediction_date': datetime.now().isoformat()
            }
            
            logger.info(f"Multi-field yield prediction completed for {len(predictions)} fields")
            return result
            
        except Exception as e:
            logger.error(f"Error predicting yield for multiple fields: {e}")
            return {}
