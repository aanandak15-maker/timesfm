"""
Advanced Yield Prediction Model for Rice Fields
Uses weather, soil, satellite data, and crop growth stages
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
from field_data_integration import FieldDataIntegration

logger = logging.getLogger(__name__)

class YieldPredictionModel:
    """Advanced yield prediction model for rice fields"""
    
    def __init__(self):
        self.field_integration = FieldDataIntegration()
        
        # Rice growth parameters
        self.rice_growth_stages = {
            'germination': {'days': 7, 'temp_opt': 30, 'water_req': 0.1},
            'vegetative': {'days': 35, 'temp_opt': 28, 'water_req': 0.3},
            'reproductive': {'days': 30, 'temp_opt': 26, 'water_req': 0.4},
            'ripening': {'days': 30, 'temp_opt': 24, 'water_req': 0.2},
            'maturity': {'days': 15, 'temp_opt': 22, 'water_req': 0.1}
        }
        
        # Yield factors and weights
        self.yield_factors = {
            'weather': 0.35,
            'soil': 0.25,
            'ndvi': 0.20,
            'growth_stage': 0.20
        }
        
        logger.info("Yield prediction model initialized")
    
    def calculate_weather_score(self, weather_data: Dict) -> float:
        """Calculate weather suitability score (0-1)"""
        try:
            temp = weather_data.get('temperature_c', 25)
            humidity = weather_data.get('humidity', 70)
            precipitation = weather_data.get('precipitation', 0)
            
            # Temperature score (optimal around 26-28°C for rice)
            temp_score = 1 - abs(temp - 27) / 15  # Penalty for deviation from optimal
            temp_score = max(0, min(1, temp_score))
            
            # Humidity score (optimal 70-80%)
            humidity_score = 1 - abs(humidity - 75) / 50
            humidity_score = max(0, min(1, humidity_score))
            
            # Precipitation score (moderate rainfall preferred)
            precip_score = 1 - abs(precipitation - 5) / 20  # 5mm/day optimal
            precip_score = max(0, min(1, precip_score))
            
            # Weighted average
            weather_score = (temp_score * 0.4 + humidity_score * 0.3 + precip_score * 0.3)
            
            return weather_score
            
        except Exception as e:
            logger.error(f"Error calculating weather score: {e}")
            return 0.5  # Default neutral score
    
    def calculate_soil_score(self, soil_data: Dict) -> float:
        """Calculate soil suitability score (0-1)"""
        try:
            if not soil_data:
                return 0.5  # Default neutral score
            
            # pH score (optimal 6.0-7.0 for rice)
            ph = soil_data.get('ph', 6.5)
            ph_score = 1 - abs(ph - 6.5) / 2.0
            ph_score = max(0, min(1, ph_score))
            
            # Organic matter score (optimal 2-4%)
            om = soil_data.get('organic_matter', 3.0)
            om_score = 1 - abs(om - 3.0) / 3.0
            om_score = max(0, min(1, om_score))
            
            # Clay content score (optimal 20-40% for rice)
            clay = soil_data.get('clay_content', 30.0)
            clay_score = 1 - abs(clay - 30.0) / 30.0
            clay_score = max(0, min(1, clay_score))
            
            # Water holding capacity score
            awc = soil_data.get('water_capacity', 0.15)
            awc_score = min(1, awc / 0.2)  # Higher is better, cap at 0.2
            
            # Weighted average
            soil_score = (ph_score * 0.3 + om_score * 0.3 + clay_score * 0.2 + awc_score * 0.2)
            
            return soil_score
            
        except Exception as e:
            logger.error(f"Error calculating soil score: {e}")
            return 0.5  # Default neutral score
    
    def calculate_ndvi_score(self, ndvi_data: Dict) -> float:
        """Calculate NDVI-based health score (0-1)"""
        try:
            if not ndvi_data:
                return 0.5  # Default neutral score
            
            mean_ndvi = ndvi_data.get('mean_ndvi', 0.5)
            max_ndvi = ndvi_data.get('max_ndvi', 0.7)
            
            # NDVI score (higher is better, optimal > 0.7)
            ndvi_score = min(1, mean_ndvi / 0.8)
            
            # Consistency score (less variation is better)
            ndvi_values = ndvi_data.get('ndvi_values', [])
            if len(ndvi_values) > 1:
                consistency = 1 - (np.std(ndvi_values) / np.mean(ndvi_values))
                consistency = max(0, min(1, consistency))
            else:
                consistency = 0.5
            
            # Combined NDVI score
            ndvi_score = (ndvi_score * 0.7 + consistency * 0.3)
            
            return ndvi_score
            
        except Exception as e:
            logger.error(f"Error calculating NDVI score: {e}")
            return 0.5  # Default neutral score
    
    def calculate_growth_stage_score(self, days_since_planting: int) -> float:
        """Calculate growth stage appropriateness score (0-1)"""
        try:
            total_days = sum(stage['days'] for stage in self.rice_growth_stages.values())
            
            if days_since_planting < 0:
                return 0.1  # Before planting
            elif days_since_planting > total_days:
                return 0.8  # Past maturity, ready for harvest
            
            # Calculate which stage we're in
            cumulative_days = 0
            for stage, params in self.rice_growth_stages.items():
                cumulative_days += params['days']
                if days_since_planting <= cumulative_days:
                    # We're in this stage
                    stage_progress = (days_since_planting - (cumulative_days - params['days'])) / params['days']
                    
                    # Different stages have different optimal scores
                    stage_scores = {
                        'germination': 0.3,
                        'vegetative': 0.6,
                        'reproductive': 0.9,  # Most critical for yield
                        'ripening': 0.8,
                        'maturity': 0.7
                    }
                    
                    base_score = stage_scores[stage]
                    progress_bonus = stage_progress * 0.2
                    
                    return min(1, base_score + progress_bonus)
            
            return 0.5  # Default neutral score
            
        except Exception as e:
            logger.error(f"Error calculating growth stage score: {e}")
            return 0.5  # Default neutral score
    
    def predict_yield_scenarios(self, field_data: Dict, days_since_planting: int = 60) -> Dict:
        """Predict yield for different scenarios"""
        try:
            # Calculate individual scores
            weather_score = self.calculate_weather_score(field_data.get('real_time_weather', {}))
            soil_score = self.calculate_soil_score(field_data.get('soil_data', {}))
            ndvi_score = self.calculate_ndvi_score(field_data.get('ndvi_data', {}))
            growth_score = self.calculate_growth_stage_score(days_since_planting)
            
            # Base yield potential (tons per acre for rice)
            base_yield = 3.5  # Average rice yield in tons/acre
            
            # Calculate scenario multipliers
            scenarios = {
                'drought': {
                    'weather_mult': 0.6,  # Reduced water availability
                    'soil_mult': 0.8,    # Soil stress
                    'ndvi_mult': 0.7,    # Reduced vegetation
                    'growth_mult': 0.9   # Growth stress
                },
                'normal': {
                    'weather_mult': 1.0,
                    'soil_mult': 1.0,
                    'ndvi_mult': 1.0,
                    'growth_mult': 1.0
                },
                'optimal': {
                    'weather_mult': 1.2,  # Perfect conditions
                    'soil_mult': 1.1,    # Excellent soil
                    'ndvi_mult': 1.1,    # Healthy vegetation
                    'growth_mult': 1.1   # Optimal growth
                }
            }
            
            predictions = {}
            
            for scenario_name, multipliers in scenarios.items():
                # Calculate weighted score for this scenario
                scenario_score = (
                    weather_score * multipliers['weather_mult'] * self.yield_factors['weather'] +
                    soil_score * multipliers['soil_mult'] * self.yield_factors['soil'] +
                    ndvi_score * multipliers['ndvi_mult'] * self.yield_factors['ndvi'] +
                    growth_score * multipliers['growth_mult'] * self.yield_factors['growth_stage']
                )
                
                # Calculate yield prediction
                predicted_yield = base_yield * scenario_score
                
                # Calculate confidence based on data availability
                data_quality = field_data.get('data_quality', {})
                confidence = (
                    (0.3 if data_quality.get('weather_available', False) else 0) +
                    (0.3 if data_quality.get('soil_data_available', False) else 0) +
                    (0.2 if data_quality.get('ndvi_data_available', False) else 0) +
                    (0.2 if data_quality.get('historical_weather_available', False) else 0)
                )
                
                predictions[scenario_name] = {
                    'yield_tons_per_acre': round(predicted_yield, 2),
                    'yield_kg_per_m2': round(predicted_yield * 0.404686, 2),  # Convert to kg/m²
                    'total_yield_kg': round(predicted_yield * 0.404686 * field_data['field_info']['area_m2'], 2),
                    'confidence': round(confidence, 2),
                    'score_breakdown': {
                        'weather': round(weather_score * multipliers['weather_mult'], 3),
                        'soil': round(soil_score * multipliers['soil_mult'], 3),
                        'ndvi': round(ndvi_score * multipliers['ndvi_mult'], 3),
                        'growth': round(growth_score * multipliers['growth_mult'], 3)
                    }
                }
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting yield scenarios: {e}")
            return {}
    
    def get_risk_factors(self, field_data: Dict, predictions: Dict) -> List[Dict]:
        """Identify risk factors affecting yield"""
        risk_factors = []
        
        try:
            # Weather risks
            weather = field_data.get('real_time_weather', {})
            if weather:
                temp = weather.get('temperature_c', 25)
                if temp > 35:
                    risk_factors.append({
                        'factor': 'High Temperature',
                        'severity': 'High' if temp > 40 else 'Medium',
                        'impact': 'Heat stress reduces grain filling',
                        'recommendation': 'Increase irrigation frequency'
                    })
                elif temp < 15:
                    risk_factors.append({
                        'factor': 'Low Temperature',
                        'severity': 'High' if temp < 10 else 'Medium',
                        'impact': 'Cold stress affects growth',
                        'recommendation': 'Consider protective measures'
                    })
                
                humidity = weather.get('humidity', 70)
                if humidity < 40:
                    risk_factors.append({
                        'factor': 'Low Humidity',
                        'severity': 'Medium',
                        'impact': 'Increased water stress',
                        'recommendation': 'Monitor soil moisture closely'
                    })
            
            # Soil risks
            soil = field_data.get('soil_data', {})
            if soil:
                ph = soil.get('ph', 6.5)
                if ph < 5.5 or ph > 7.5:
                    risk_factors.append({
                        'factor': 'Suboptimal pH',
                        'severity': 'Medium',
                        'impact': 'Nutrient availability issues',
                        'recommendation': 'Consider pH adjustment'
                    })
                
                om = soil.get('organic_matter', 3.0)
                if om < 2.0:
                    risk_factors.append({
                        'factor': 'Low Organic Matter',
                        'severity': 'Medium',
                        'impact': 'Reduced soil fertility',
                        'recommendation': 'Add organic amendments'
                    })
            
            # NDVI risks
            ndvi = field_data.get('ndvi_data', {})
            if ndvi:
                mean_ndvi = ndvi.get('mean_ndvi', 0.5)
                if mean_ndvi < 0.4:
                    risk_factors.append({
                        'factor': 'Low Vegetation Health',
                        'severity': 'High',
                        'impact': 'Poor crop development',
                        'recommendation': 'Check for pests/diseases'
                    })
            
            # Confidence-based risks
            for scenario, data in predictions.items():
                if data['confidence'] < 0.6:
                    risk_factors.append({
                        'factor': f'Low Data Quality ({scenario})',
                        'severity': 'Medium',
                        'impact': 'Unreliable predictions',
                        'recommendation': 'Improve data collection'
                    })
            
            return risk_factors
            
        except Exception as e:
            logger.error(f"Error identifying risk factors: {e}")
            return []
    
    def generate_field_report(self, days_since_planting: int = 60) -> Dict:
        """Generate comprehensive field report"""
        try:
            logger.info("Generating comprehensive field report...")
            
            # Get field data
            field_data = self.field_integration.get_field_summary()
            
            # Predict yields
            predictions = self.predict_yield_scenarios(field_data, days_since_planting)
            
            # Identify risks
            risk_factors = self.get_risk_factors(field_data, predictions)
            
            # Generate report
            report = {
                'field_info': field_data['field_info'],
                'data_quality': field_data['data_quality'],
                'current_conditions': {
                    'weather': field_data.get('real_time_weather', {}),
                    'soil': field_data.get('soil_data', {}),
                    'ndvi': field_data.get('ndvi_data', {})
                },
                'yield_predictions': predictions,
                'risk_factors': risk_factors,
                'recommendations': self.generate_recommendations(field_data, predictions, risk_factors),
                'generated_at': datetime.now().isoformat(),
                'days_since_planting': days_since_planting
            }
            
            logger.info("Field report generated successfully")
            return report
            
        except Exception as e:
            logger.error(f"Error generating field report: {e}")
            return {}
    
    def generate_recommendations(self, field_data: Dict, predictions: Dict, risk_factors: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        try:
            # Yield-based recommendations
            normal_yield = predictions.get('normal', {}).get('yield_tons_per_acre', 0)
            optimal_yield = predictions.get('optimal', {}).get('yield_tons_per_acre', 0)
            
            if optimal_yield > normal_yield * 1.1:
                recommendations.append("Conditions are excellent - consider maximizing inputs for optimal yield")
            elif normal_yield < 2.5:
                recommendations.append("Yield potential is low - review management practices")
            
            # Risk-based recommendations
            high_risk_factors = [rf for rf in risk_factors if rf['severity'] == 'High']
            if high_risk_factors:
                recommendations.append(f"Address {len(high_risk_factors)} high-risk factors immediately")
            
            # Weather-based recommendations
            weather = field_data.get('real_time_weather', {})
            if weather:
                temp = weather.get('temperature_c', 25)
                if temp > 30:
                    recommendations.append("High temperatures detected - increase irrigation frequency")
                elif temp < 20:
                    recommendations.append("Cool temperatures - monitor for cold stress")
            
            # Growth stage recommendations
            days_since_planting = field_data.get('days_since_planting', 60)
            if days_since_planting < 30:
                recommendations.append("Early growth stage - focus on establishment and weed control")
            elif days_since_planting < 60:
                recommendations.append("Vegetative stage - ensure adequate nitrogen supply")
            elif days_since_planting < 90:
                recommendations.append("Reproductive stage - critical for yield, monitor closely")
            else:
                recommendations.append("Ripening stage - reduce irrigation, prepare for harvest")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Unable to generate recommendations at this time"]

def test_yield_prediction():
    """Test the yield prediction model"""
    model = YieldPredictionModel()
    
    print("🌾 Testing Yield Prediction Model")
    print("=" * 50)
    
    # Generate field report
    report = model.generate_field_report(days_since_planting=60)
    
    if report:
        print(f"\n📍 Field: {report['field_info']['area_acres']:.2f} acres")
        print(f"🌱 Crop: {report['field_info']['crop']}")
        print(f"📅 Days since planting: {report['days_since_planting']}")
        
        print(f"\n📊 Yield Predictions:")
        for scenario, data in report['yield_predictions'].items():
            print(f"  {scenario.title()}: {data['yield_tons_per_acre']} tons/acre (confidence: {data['confidence']})")
        
        print(f"\n⚠️  Risk Factors ({len(report['risk_factors'])}):")
        for risk in report['risk_factors'][:3]:  # Show top 3
            print(f"  • {risk['factor']} ({risk['severity']}): {risk['impact']}")
        
        print(f"\n💡 Recommendations:")
        for rec in report['recommendations'][:3]:  # Show top 3
            print(f"  • {rec}")
    
    print("\n" + "=" * 50)
    print("🎯 Yield Prediction Test Complete!")

if __name__ == "__main__":
    test_yield_prediction()




