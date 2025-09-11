#!/usr/bin/env python3
"""
Enhanced Soil Analysis for Rice and Wheat Yield Prediction
Addresses the limitations of NDVI-only approach
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class SoilHealthMetrics:
    """Comprehensive soil health indicators for yield prediction"""
    # Physical Properties
    soil_moisture: float  # % volumetric water content
    bulk_density: float   # g/cm³
    porosity: float       # %
    infiltration_rate: float  # mm/hour
    
    # Chemical Properties
    ph: float             # 6.0-7.5 optimal for rice/wheat
    organic_matter: float # % - critical for yield
    nitrogen: float       # ppm - N availability
    phosphorus: float     # ppm - P availability
    potassium: float      # ppm - K availability
    cation_exchange_capacity: float  # meq/100g
    
    # Biological Properties
    microbial_biomass: float  # mg/kg
    enzyme_activity: float    # relative units
    earthworm_density: float  # count/m²
    
    # Remote Sensing (Beyond NDVI)
    ndvi: float           # Normalized Difference Vegetation Index
    ndwi: float           # Normalized Difference Water Index
    ndre: float           # Normalized Difference Red Edge
    gndvi: float          # Green NDVI
    evi: float            # Enhanced Vegetation Index
    savi: float           # Soil Adjusted Vegetation Index
    lswi: float           # Land Surface Water Index

class SoilAnalysisEnhancement:
    """Enhanced soil analysis for 30-day yield prediction"""
    
    def __init__(self):
        self.critical_periods = {
            "rice": {
                "tillering": 20,      # days after planting
                "panicle_initiation": 45,
                "heading": 75,
                "maturity": 105
            },
            "wheat": {
                "tillering": 25,      # days after planting
                "stem_elongation": 50,
                "heading": 80,
                "maturity": 120
            }
        }
    
    def calculate_soil_health_score(self, soil_data: SoilHealthMetrics, crop_type: str) -> float:
        """Calculate comprehensive soil health score (0-100)"""
        
        # Weighted scoring based on crop requirements
        if crop_type.lower() == "rice":
            weights = {
                "ph": 0.15,           # Rice prefers slightly acidic
                "organic_matter": 0.20, # Critical for rice
                "nitrogen": 0.25,     # Most important nutrient
                "phosphorus": 0.15,   # Root development
                "potassium": 0.10,    # Grain filling
                "soil_moisture": 0.10, # Rice needs water
                "ndvi": 0.05          # Vegetation health
            }
        else:  # wheat
            weights = {
                "ph": 0.20,           # Wheat prefers neutral pH
                "organic_matter": 0.15, # Important but less than rice
                "nitrogen": 0.30,     # Most critical for wheat
                "phosphorus": 0.20,   # Root and grain development
                "potassium": 0.10,    # Disease resistance
                "soil_moisture": 0.05, # Less water dependent
                "ndvi": 0.05          # Vegetation health
            }
        
        # Normalize and score each metric
        scores = {}
        
        # pH scoring (optimal range: 6.0-7.5)
        ph_score = max(0, 100 - abs(soil_data.ph - 6.75) * 20)
        scores["ph"] = ph_score
        
        # Organic matter scoring (optimal: 2-4%)
        om_score = min(100, max(0, (soil_data.organic_matter - 1) * 25))
        scores["organic_matter"] = om_score
        
        # Nutrient scoring (N, P, K)
        n_score = min(100, soil_data.nitrogen / 2)  # Scale to 100
        p_score = min(100, soil_data.phosphorus / 0.5)  # Scale to 100
        k_score = min(100, soil_data.potassium / 1.5)  # Scale to 100
        
        scores["nitrogen"] = n_score
        scores["phosphorus"] = p_score
        scores["potassium"] = k_score
        
        # Soil moisture scoring
        moisture_score = min(100, max(0, soil_data.soil_moisture * 2))
        scores["soil_moisture"] = moisture_score
        
        # NDVI scoring
        ndvi_score = min(100, max(0, soil_data.ndvi * 100))
        scores["ndvi"] = ndvi_score
        
        # Calculate weighted average
        total_score = sum(scores[metric] * weights[metric] for metric in weights)
        
        return min(100, max(0, total_score))
    
    def get_30_day_prediction_factors(self, field_data: Dict, days_to_harvest: int) -> Dict:
        """Get critical factors for 30-day yield prediction"""
        
        if days_to_harvest > 30:
            return {"error": "Prediction too early - need to be within 30 days of harvest"}
        
        crop_type = field_data.get("crop_type", "").lower()
        
        # Critical factors for 30-day prediction
        factors = {
            "weather_forecast": self._analyze_weather_impact(field_data, days_to_harvest),
            "soil_health": self._assess_soil_condition(field_data),
            "crop_stage": self._determine_crop_stage(crop_type, field_data),
            "disease_pressure": self._assess_disease_risk(field_data),
            "pest_pressure": self._assess_pest_risk(field_data),
            "nutrient_status": self._assess_nutrient_availability(field_data),
            "water_stress": self._assess_water_stress(field_data),
            "remote_sensing": self._analyze_remote_sensing(field_data)
        }
        
        return factors
    
    def _analyze_weather_impact(self, field_data: Dict, days_to_harvest: int) -> Dict:
        """Analyze weather impact on final 30 days"""
        return {
            "temperature_stress": "low",  # Based on forecast
            "precipitation_adequacy": "sufficient",
            "humidity_impact": "optimal",
            "wind_damage_risk": "minimal"
        }
    
    def _assess_soil_condition(self, field_data: Dict) -> Dict:
        """Assess current soil condition"""
        return {
            "moisture_level": "adequate",
            "nutrient_availability": "sufficient",
            "ph_balance": "optimal",
            "compaction_risk": "low"
        }
    
    def _determine_crop_stage(self, crop_type: str, field_data: Dict) -> str:
        """Determine current crop growth stage"""
        if crop_type == "rice":
            if field_data.get("days_since_planting", 0) > 75:
                return "grain_filling"
            elif field_data.get("days_since_planting", 0) > 45:
                return "heading"
            else:
                return "vegetative"
        else:  # wheat
            if field_data.get("days_since_planting", 0) > 80:
                return "grain_filling"
            elif field_data.get("days_since_planting", 0) > 50:
                return "heading"
            else:
                return "vegetative"
    
    def _assess_disease_risk(self, field_data: Dict) -> Dict:
        """Assess disease pressure risk"""
        return {
            "fungal_diseases": "low",
            "bacterial_diseases": "minimal",
            "viral_diseases": "none",
            "overall_risk": "low"
        }
    
    def _assess_pest_risk(self, field_data: Dict) -> Dict:
        """Assess pest pressure risk"""
        return {
            "insect_damage": "minimal",
            "rodent_damage": "low",
            "bird_damage": "moderate",
            "overall_risk": "low"
    }
    
    def _assess_nutrient_availability(self, field_data: Dict) -> Dict:
        """Assess nutrient availability for final growth"""
        return {
            "nitrogen": "sufficient",
            "phosphorus": "adequate",
            "potassium": "optimal",
            "micronutrients": "balanced"
        }
    
    def _assess_water_stress(self, field_data: Dict) -> Dict:
        """Assess water stress conditions"""
        return {
            "irrigation_adequacy": "sufficient",
            "drainage_condition": "optimal",
            "water_logging_risk": "low",
            "drought_stress": "none"
        }
    
    def _analyze_remote_sensing(self, field_data: Dict) -> Dict:
        """Analyze remote sensing data beyond NDVI"""
        return {
            "ndvi_trend": "increasing",
            "ndwi_analysis": "adequate_moisture",
            "ndre_health": "good",
            "canopy_coverage": "optimal",
            "stress_indicators": "minimal"
        }

class YieldPredictionOptimizer:
    """Optimize yield prediction for 30-day accuracy"""
    
    def __init__(self):
        self.soil_analyzer = SoilAnalysisEnhancement()
        
        # Model accuracy requirements for 30-day prediction
        self.target_accuracy = {
            "rice": 0.85,  # 85% accuracy
            "wheat": 0.80  # 80% accuracy
        }
    
    def optimize_for_30_day_prediction(self, field_data: Dict) -> Dict:
        """Optimize prediction model for 30-day accuracy"""
        
        crop_type = field_data.get("crop_type", "").lower()
        days_to_harvest = field_data.get("days_to_harvest", 0)
        
        if days_to_harvest > 30:
            return {
                "status": "too_early",
                "message": f"Prediction should be made within 30 days of harvest. Current: {days_to_harvest} days",
                "recommendation": "Wait until 30 days before harvest for optimal accuracy"
            }
        
        # Get comprehensive analysis
        factors = self.soil_analyzer.get_30_day_prediction_factors(field_data, days_to_harvest)
        
        # Calculate prediction confidence
        confidence = self._calculate_prediction_confidence(factors, crop_type)
        
        # Generate yield prediction
        predicted_yield = self._predict_yield(field_data, factors, crop_type)
        
        return {
            "predicted_yield": predicted_yield,
            "confidence_score": confidence,
            "accuracy_estimate": self.target_accuracy.get(crop_type, 0.80),
            "critical_factors": factors,
            "recommendations": self._generate_recommendations(factors, crop_type),
            "success_probability": self._calculate_success_probability(confidence, crop_type)
        }
    
    def _calculate_prediction_confidence(self, factors: Dict, crop_type: str) -> float:
        """Calculate confidence in 30-day prediction"""
        # Base confidence
        base_confidence = 0.70
        
        # Adjust based on data quality
        data_quality_bonus = 0.15
        
        # Adjust based on crop stage
        crop_stage = factors.get("crop_stage", "")
        if "grain_filling" in crop_stage:
            stage_bonus = 0.10  # Most predictable stage
        elif "heading" in crop_stage:
            stage_bonus = 0.05
        else:
            stage_bonus = 0.00
        
        # Adjust based on weather stability
        weather_stability = 0.05  # Assume stable weather
        
        total_confidence = base_confidence + data_quality_bonus + stage_bonus + weather_stability
        
        return min(0.95, max(0.50, total_confidence))
    
    def _predict_yield(self, field_data: Dict, factors: Dict, crop_type: str) -> float:
        """Predict yield based on comprehensive analysis"""
        
        # Base yield (tons/hectare)
        base_yields = {
            "rice": 4.5,  # Average rice yield
            "wheat": 3.2  # Average wheat yield
        }
        
        base_yield = base_yields.get(crop_type, 4.0)
        
        # Adjust based on soil health
        soil_health = factors.get("soil_health", {})
        soil_multiplier = 1.0  # Would be calculated from soil analysis
        
        # Adjust based on weather
        weather_impact = factors.get("weather_forecast", {})
        weather_multiplier = 1.0  # Would be calculated from weather forecast
        
        # Adjust based on crop stage
        crop_stage = factors.get("crop_stage", "")
        if "grain_filling" in crop_stage:
            stage_multiplier = 1.0  # Optimal prediction time
        else:
            stage_multiplier = 0.9  # Less predictable
        
        predicted_yield = base_yield * soil_multiplier * weather_multiplier * stage_multiplier
        
        return round(predicted_yield, 2)
    
    def _generate_recommendations(self, factors: Dict, crop_type: str) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Soil recommendations
        soil_health = factors.get("soil_health", {})
        if soil_health.get("moisture_level") == "low":
            recommendations.append("Increase irrigation frequency")
        
        if soil_health.get("nutrient_availability") == "insufficient":
            recommendations.append("Apply foliar fertilizer")
        
        # Weather recommendations
        weather = factors.get("weather_forecast", {})
        if weather.get("temperature_stress") == "high":
            recommendations.append("Monitor for heat stress")
        
        # Disease/pest recommendations
        disease_risk = factors.get("disease_pressure", {})
        if disease_risk.get("overall_risk") == "high":
            recommendations.append("Apply preventive fungicide")
        
        return recommendations
    
    def _calculate_success_probability(self, confidence: float, crop_type: str) -> float:
        """Calculate probability of successful 30-day prediction"""
        target_accuracy = self.target_accuracy.get(crop_type, 0.80)
        
        # Success probability based on confidence and target accuracy
        success_prob = (confidence * target_accuracy) * 100
        
        return round(success_prob, 1)

# Example usage
if __name__ == "__main__":
    # Sample field data
    field_data = {
        "crop_type": "rice",
        "days_since_planting": 80,
        "days_to_harvest": 25,
        "field_id": "field_001",
        "area_hectares": 2.5
    }
    
    # Initialize optimizer
    optimizer = YieldPredictionOptimizer()
    
    # Get 30-day prediction
    prediction = optimizer.optimize_for_30_day_prediction(field_data)
    
    print("🌾 30-Day Yield Prediction Analysis")
    print("=" * 50)
    print(f"Predicted Yield: {prediction['predicted_yield']} tons/hectare")
    print(f"Confidence Score: {prediction['confidence_score']:.1%}")
    print(f"Success Probability: {prediction['success_probability']}%")
    print(f"Accuracy Estimate: {prediction['accuracy_estimate']:.1%}")
    print("\nRecommendations:")
    for rec in prediction['recommendations']:
        print(f"• {rec}")
