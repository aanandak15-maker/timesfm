#!/usr/bin/env python3
"""
Advanced Yield Prediction Model for Agricultural Platform
Machine learning-based yield prediction with confidence intervals
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

logger = logging.getLogger(__name__)

class AdvancedYieldPrediction:
    """Advanced yield prediction with ML models and confidence intervals"""
    
    def __init__(self):
        self.models = {}
        self.feature_importance = {}
        self.model_performance = {}
        
    def prepare_training_data(self, historical_data: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for ML models"""
        try:
            # Convert to DataFrame
            df = pd.DataFrame(historical_data)
            
            # Feature engineering
            features = []
            targets = []
            
            for _, row in df.iterrows():
                # Weather features
                weather_features = [
                    row.get('avg_temperature', 25),
                    row.get('avg_humidity', 60),
                    row.get('total_precipitation', 100),
                    row.get('avg_wind_speed', 3),
                    row.get('sunshine_hours', 8)
                ]
                
                # Soil features
                soil_features = [
                    row.get('ph', 6.5),
                    row.get('nitrogen', 50),
                    row.get('phosphorus', 25),
                    row.get('potassium', 150),
                    row.get('organic_matter', 2.0),
                    row.get('soil_moisture', 50)
                ]
                
                # Crop features
                crop_features = [
                    row.get('crop_type_encoded', 0),  # Encoded crop type
                    row.get('planting_date_encoded', 0),  # Days since planting
                    row.get('field_area', 1.0),
                    row.get('irrigation_frequency', 1)
                ]
                
                # Combine all features
                feature_vector = weather_features + soil_features + crop_features
                features.append(feature_vector)
                targets.append(row.get('yield', 0))
            
            return np.array(features), np.array(targets)
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            return np.array([]), np.array([])
    
    def train_crop_model(self, crop_type: str, historical_data: List[Dict]) -> Dict:
        """Train ML model for specific crop type"""
        try:
            # Prepare data
            X, y = self.prepare_training_data(historical_data)
            
            if len(X) == 0:
                return {'status': 'error', 'message': 'No training data available'}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train Random Forest model
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Store model
            self.models[crop_type] = model
            self.model_performance[crop_type] = {
                'mae': mae,
                'r2': r2,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            # Feature importance
            feature_names = [
                'avg_temperature', 'avg_humidity', 'total_precipitation', 'avg_wind_speed', 'sunshine_hours',
                'ph', 'nitrogen', 'phosphorus', 'potassium', 'organic_matter', 'soil_moisture',
                'crop_type', 'planting_date', 'field_area', 'irrigation_frequency'
            ]
            
            self.feature_importance[crop_type] = dict(zip(
                feature_names, model.feature_importances_
            ))
            
            # Save model
            model_path = f"models/{crop_type}_yield_model.pkl"
            os.makedirs("models", exist_ok=True)
            joblib.dump(model, model_path)
            
            return {
                'status': 'success',
                'crop_type': crop_type,
                'performance': {
                    'mae': round(mae, 3),
                    'r2': round(r2, 3),
                    'training_samples': len(X_train),
                    'test_samples': len(X_test)
                },
                'feature_importance': self.feature_importance[crop_type]
            }
            
        except Exception as e:
            logger.error(f"Error training model for {crop_type}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def predict_yield(self, crop_type: str, field_data: Dict, weather_data: Dict, 
                     soil_data: Dict) -> Dict:
        """Predict yield for a specific field"""
        try:
            if crop_type not in self.models:
                return {'status': 'error', 'message': f'No model trained for {crop_type}'}
            
            model = self.models[crop_type]
            
            # Prepare features
            features = self._prepare_prediction_features(field_data, weather_data, soil_data)
            
            # Make prediction
            prediction = model.predict([features])[0]
            
            # Calculate confidence interval (simplified)
            # In production, you'd use proper uncertainty quantification
            confidence_interval = self._calculate_confidence_interval(model, features)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                field_data, weather_data, soil_data, prediction
            )
            
            return {
                'status': 'success',
                'predicted_yield': round(prediction, 2),
                'confidence_interval': {
                    'lower': round(prediction - confidence_interval, 2),
                    'upper': round(prediction + confidence_interval, 2)
                },
                'confidence_level': 0.95,
                'recommendations': recommendations,
                'model_performance': self.model_performance.get(crop_type, {}),
                'feature_importance': self.feature_importance.get(crop_type, {})
            }
            
        except Exception as e:
            logger.error(f"Error predicting yield: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def predict_multiple_scenarios(self, crop_type: str, field_data: Dict, 
                                  weather_scenarios: List[Dict], soil_data: Dict) -> Dict:
        """Predict yield for multiple weather scenarios"""
        try:
            scenarios = []
            
            for i, weather_scenario in enumerate(weather_scenarios):
                prediction = self.predict_yield(crop_type, field_data, weather_scenario, soil_data)
                
                if prediction['status'] == 'success':
                    scenarios.append({
                        'scenario_name': weather_scenario.get('name', f'Scenario {i+1}'),
                        'predicted_yield': prediction['predicted_yield'],
                        'confidence_interval': prediction['confidence_interval'],
                        'weather_conditions': weather_scenario
                    })
            
            # Calculate scenario comparison
            if scenarios:
                yields = [s['predicted_yield'] for s in scenarios]
                best_scenario = max(scenarios, key=lambda x: x['predicted_yield'])
                worst_scenario = min(scenarios, key=lambda x: x['predicted_yield'])
                
                return {
                    'status': 'success',
                    'scenarios': scenarios,
                    'summary': {
                        'best_yield': best_scenario['predicted_yield'],
                        'worst_yield': worst_scenario['predicted_yield'],
                        'yield_range': round(max(yields) - min(yields), 2),
                        'best_scenario': best_scenario['scenario_name'],
                        'worst_scenario': worst_scenario['scenario_name']
                    }
                }
            else:
                return {'status': 'error', 'message': 'No valid scenarios'}
                
        except Exception as e:
            logger.error(f"Error predicting multiple scenarios: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _prepare_prediction_features(self, field_data: Dict, weather_data: Dict, 
                                   soil_data: Dict) -> List[float]:
        """Prepare features for prediction"""
        # Weather features
        weather_features = [
            weather_data.get('temperature', 25),
            weather_data.get('humidity', 60),
            weather_data.get('precipitation', 100),
            weather_data.get('wind_speed', 3),
            weather_data.get('sunshine_hours', 8)
        ]
        
        # Soil features
        soil_features = [
            soil_data.get('ph', 6.5),
            soil_data.get('nitrogen', 50),
            soil_data.get('phosphorus', 25),
            soil_data.get('potassium', 150),
            soil_data.get('organic_matter', 2.0),
            soil_data.get('soil_moisture', 50)
        ]
        
        # Crop features
        crop_features = [
            field_data.get('crop_type_encoded', 0),
            field_data.get('planting_date_encoded', 0),
            field_data.get('area_m2', 1.0),
            field_data.get('irrigation_frequency', 1)
        ]
        
        return weather_features + soil_features + crop_features
    
    def _calculate_confidence_interval(self, model, features: List[float]) -> float:
        """Calculate confidence interval for prediction"""
        # Simplified confidence interval calculation
        # In production, use proper uncertainty quantification methods
        try:
            # Get predictions from individual trees
            predictions = [tree.predict([features])[0] for tree in model.estimators_]
            std_dev = np.std(predictions)
            
            # 95% confidence interval (1.96 * std_dev)
            return 1.96 * std_dev
        except:
            # Fallback to 10% of prediction
            return 0.1 * abs(model.predict([features])[0])
    
    def _generate_recommendations(self, field_data: Dict, weather_data: Dict, 
                                soil_data: Dict, predicted_yield: float) -> List[str]:
        """Generate agricultural recommendations based on prediction"""
        recommendations = []
        
        # Weather-based recommendations
        if weather_data.get('temperature', 25) > 30:
            recommendations.append("High temperature detected - consider irrigation and shade")
        
        if weather_data.get('humidity', 60) > 80:
            recommendations.append("High humidity - monitor for fungal diseases")
        
        if weather_data.get('precipitation', 0) < 50:
            recommendations.append("Low precipitation - irrigation may be needed")
        
        # Soil-based recommendations
        if soil_data.get('ph', 6.5) < 6.0:
            recommendations.append("Soil pH is low - consider lime application")
        elif soil_data.get('ph', 6.5) > 7.5:
            recommendations.append("Soil pH is high - consider sulfur application")
        
        if soil_data.get('nitrogen', 50) < 30:
            recommendations.append("Low nitrogen levels - consider nitrogen fertilizer")
        
        if soil_data.get('organic_matter', 2.0) < 1.5:
            recommendations.append("Low organic matter - consider compost or manure")
        
        # Yield-based recommendations
        if predicted_yield < 2.0:
            recommendations.append("Low predicted yield - review farming practices")
        elif predicted_yield > 8.0:
            recommendations.append("High predicted yield - ensure proper harvesting equipment")
        
        return recommendations
    
    def load_model(self, crop_type: str) -> bool:
        """Load pre-trained model"""
        try:
            model_path = f"models/{crop_type}_yield_model.pkl"
            if os.path.exists(model_path):
                self.models[crop_type] = joblib.load(model_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading model for {crop_type}: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Test the yield prediction system
    yield_predictor = AdvancedYieldPrediction()
    
    # Example field data
    field_data = {
        'crop_type_encoded': 1,  # Rice
        'planting_date_encoded': 30,  # 30 days since planting
        'area_m2': 325.12,
        'irrigation_frequency': 2
    }
    
    # Example weather data
    weather_data = {
        'temperature': 28,
        'humidity': 65,
        'precipitation': 120,
        'wind_speed': 4,
        'sunshine_hours': 7
    }
    
    # Example soil data
    soil_data = {
        'ph': 6.8,
        'nitrogen': 45,
        'phosphorus': 30,
        'potassium': 180,
        'organic_matter': 2.2,
        'soil_moisture': 55
    }
    
    # Predict yield
    prediction = yield_predictor.predict_yield('rice', field_data, weather_data, soil_data)
    print("Yield Prediction:", json.dumps(prediction, indent=2))
