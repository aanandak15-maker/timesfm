// Comprehensive Demo Data for Hackathon Presentation
// This file contains realistic agricultural data for impressive demonstrations

export interface DemoFarm {
  id: string;
  name: string;
  location: string;
  total_area: number;
  owner: string;
  established: string;
  description: string;
  image: string;
}

export interface DemoField {
  id: string;
  name: string;
  farm_id: string;
  area_acres: number;
  crop_type: string;
  latitude: number;
  longitude: number;
  soil_type: string;
  planting_date: string;
  harvest_date: string;
  status: string;
  created_at: string;
  yield_prediction?: number;
  health_score?: number;
}

export interface DemoSensorData {
  field_id: string;
  timestamp: string;
  temperature: number;
  humidity: number;
  soil_moisture: number;
  ph: number;
  ec: number;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  light_intensity: number;
  wind_speed: number;
  wind_direction: number;
  battery: number;
  signal: number;
  device_health: number;
}

export interface DemoWeatherData {
  location: string;
  temperature: number;
  humidity: number;
  wind_speed: number;
  wind_direction: number;
  pressure: number;
  visibility: number;
  uv_index: number;
  condition: string;
  description: string;
  icon: string;
  forecast: Array<{
    date: string;
    high: number;
    low: number;
    condition: string;
    precipitation: number;
  }>;
}

export interface DemoMarketData {
  commodity: string;
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  market: string;
  last_updated: string;
  trend: 'up' | 'down' | 'stable';
}

export interface DemoYieldPrediction {
  field_id: string;
  crop_type: string;
  predicted_yield: number;
  confidence: number;
  factors: {
    weather_impact: number;
    soil_health: number;
    irrigation: number;
    pest_control: number;
  };
  recommendations: string[];
  risk_factors: string[];
}

// Demo Farms Data
export const demoFarms: DemoFarm[] = [
  {
    id: "farm-1",
    name: "Sharma Family Farm",
    location: "Punjab, India",
    total_area: 2.5,
    owner: "Rajesh Sharma",
    established: "2015",
    description: "Traditional family farm specializing in rice and maize cultivation with modern IoT integration",
    image: "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=400"
  },
  {
    id: "farm-2", 
    name: "Patel Cotton Fields",
    location: "Gujarat, India",
    total_area: 1.8,
    owner: "Priya Patel",
    established: "2018",
    description: "Premium cotton cultivation with advanced soil monitoring and precision agriculture",
    image: "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400"
  },
  {
    id: "farm-3",
    name: "Kumar Rice Farm",
    location: "West Bengal, India", 
    total_area: 3.2,
    owner: "Amit Kumar",
    established: "2012",
    description: "Large-scale rice production with integrated pest management and smart irrigation",
    image: "https://images.unsplash.com/photo-1586771107445-d3ca888129ce?w=400"
  }
];

// Demo Fields Data
export const demoFields: DemoField[] = [
  {
    id: "field-1",
    name: "Rice Field North",
    farm_id: "farm-1",
    area_acres: 1.2,
    crop_type: "Rice",
    latitude: 28.368911,
    longitude: 77.541033,
    soil_type: "Loamy",
    planting_date: "2024-06-15",
    harvest_date: "2024-10-15",
    status: "growing",
    created_at: "2024-01-15T10:30:00Z",
    yield_prediction: 4.2,
    health_score: 85
  },
  {
    id: "field-2",
    name: "Maize Field South", 
    farm_id: "farm-1",
    area_acres: 1.3,
    crop_type: "Maize",
    latitude: 28.369911,
    longitude: 77.542033,
    soil_type: "Clay",
    planting_date: "2024-07-01",
    harvest_date: "2024-11-15",
    status: "growing",
    created_at: "2024-01-20T14:15:00Z",
    yield_prediction: 3.8,
    health_score: 92
  },
  {
    id: "field-3",
    name: "Cotton Field East",
    farm_id: "farm-2",
    area_acres: 1.8,
    crop_type: "Cotton",
    latitude: 30.368911,
    longitude: 75.541033,
    soil_type: "Sandy",
    planting_date: "2024-05-01",
    harvest_date: "2024-12-15",
    status: "harvested",
    created_at: "2024-02-10T09:20:00Z",
    yield_prediction: 2.5,
    health_score: 78
  }
];

// Demo Sensor Data Generator
export const generateDemoSensorData = (fieldId: string): DemoSensorData => {
  const baseData = {
    field_id: fieldId,
    timestamp: new Date().toISOString(),
    battery: 85 + Math.random() * 15,
    signal: 90 + Math.random() * 10,
    device_health: 95 + Math.random() * 5
  };

  // Generate realistic sensor data based on time of day and field type
  const hour = new Date().getHours();
  const isDaytime = hour >= 6 && hour <= 18;
  
  return {
    ...baseData,
    temperature: isDaytime ? 28 + Math.random() * 8 : 22 + Math.random() * 6,
    humidity: isDaytime ? 45 + Math.random() * 20 : 60 + Math.random() * 25,
    soil_moisture: 35 + Math.random() * 30,
    ph: 6.2 + (Math.random() - 0.5) * 1.2,
    ec: 1.2 + (Math.random() - 0.5) * 0.6,
    nitrogen: 80 + Math.random() * 40,
    phosphorus: 45 + Math.random() * 25,
    potassium: 65 + Math.random() * 35,
    light_intensity: isDaytime ? 400 + Math.random() * 600 : 10 + Math.random() * 20,
    wind_speed: 3 + Math.random() * 12,
    wind_direction: Math.random() * 360
  };
};

// Demo Weather Data
export const demoWeatherData: DemoWeatherData = {
  location: "Punjab, India",
  temperature: 32,
  humidity: 65,
  wind_speed: 8,
  wind_direction: 245,
  pressure: 1013,
  visibility: 10,
  uv_index: 7,
  condition: "Partly Cloudy",
  description: "Ideal conditions for crop growth",
  icon: "partly-cloudy",
  forecast: [
    { date: "2024-09-20", high: 34, low: 24, condition: "Sunny", precipitation: 0 },
    { date: "2024-09-21", high: 32, low: 23, condition: "Partly Cloudy", precipitation: 10 },
    { date: "2024-09-22", high: 30, low: 22, condition: "Light Rain", precipitation: 60 },
    { date: "2024-09-23", high: 28, low: 20, condition: "Rain", precipitation: 85 },
    { date: "2024-09-24", high: 31, low: 21, condition: "Clear", precipitation: 5 }
  ]
};

// Demo Market Data
export const demoMarketData: DemoMarketData[] = [
  {
    commodity: "Rice",
    price: 2850,
    change: 45,
    change_percent: 1.6,
    volume: 125000,
    market: "Mumbai APMC",
    last_updated: new Date().toISOString(),
    trend: "up"
  },
  {
    commodity: "Maize", 
    price: 1950,
    change: -25,
    change_percent: -1.3,
    volume: 89000,
    market: "Delhi APMC",
    last_updated: new Date().toISOString(),
    trend: "down"
  },
  {
    commodity: "Cotton",
    price: 7200,
    change: 120,
    change_percent: 1.7,
    volume: 67000,
    market: "Ahmedabad APMC",
    last_updated: new Date().toISOString(),
    trend: "up"
  }
];

// Demo Yield Predictions
export const demoYieldPredictions: DemoYieldPrediction[] = [
  {
    field_id: "field-1",
    crop_type: "Rice",
    predicted_yield: 4.2,
    confidence: 87,
    factors: {
      weather_impact: 85,
      soil_health: 90,
      irrigation: 88,
      pest_control: 82
    },
    recommendations: [
      "Increase irrigation frequency by 15%",
      "Apply nitrogen fertilizer in next 7 days",
      "Monitor for brown plant hopper infestation"
    ],
    risk_factors: [
      "High temperature stress expected next week",
      "Soil pH slightly acidic - consider lime application"
    ]
  },
  {
    field_id: "field-2",
    crop_type: "Maize",
    predicted_yield: 3.8,
    confidence: 92,
    factors: {
      weather_impact: 95,
      soil_health: 88,
      irrigation: 90,
      pest_control: 85
    },
    recommendations: [
      "Optimal growth conditions detected",
      "Consider foliar spray for micronutrients",
      "Harvest window opens in 3 weeks"
    ],
    risk_factors: [
      "Monitor for corn earworm activity"
    ]
  },
  {
    field_id: "field-3",
    crop_type: "Cotton",
    predicted_yield: 2.5,
    confidence: 78,
    factors: {
      weather_impact: 75,
      soil_health: 80,
      irrigation: 85,
      pest_control: 70
    },
    recommendations: [
      "Harvest completed successfully",
      "Prepare field for next season",
      "Apply post-harvest soil treatment"
    ],
    risk_factors: [
      "Pest damage reduced yield by 15%",
      "Late season weather affected quality"
    ]
  }
];

// Demo Analytics Data
export const demoAnalytics = {
  totalFarms: 3,
  totalFields: 3,
  totalArea: 7.5,
  averageYield: 3.5,
  totalRevenue: 1250000,
  costSavings: 180000,
  waterSaved: 45000, // liters
  fertilizerOptimized: 25, // percentage
  pestReduction: 40, // percentage
  yieldIncrease: 18, // percentage
  monthlyTrends: [
    { month: "Jan", yield: 2.8, cost: 45000, revenue: 120000 },
    { month: "Feb", yield: 3.1, cost: 42000, revenue: 135000 },
    { month: "Mar", yield: 3.3, cost: 48000, revenue: 145000 },
    { month: "Apr", yield: 3.6, cost: 52000, revenue: 160000 },
    { month: "May", yield: 3.8, cost: 55000, revenue: 175000 },
    { month: "Jun", yield: 4.0, cost: 58000, revenue: 185000 },
    { month: "Jul", yield: 4.2, cost: 62000, revenue: 195000 },
    { month: "Aug", yield: 4.1, cost: 60000, revenue: 190000 },
    { month: "Sep", yield: 3.9, cost: 57000, revenue: 180000 }
  ]
};

// Demo Alerts and Notifications
export const demoAlerts = [
  {
    id: "alert-1",
    type: "warning",
    title: "Soil Moisture Low",
    message: "Field 1 soil moisture is below optimal level (35%). Consider irrigation.",
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    field_id: "field-1",
    severity: "medium"
  },
  {
    id: "alert-2", 
    type: "info",
    title: "Harvest Window Opening",
    message: "Field 2 maize is ready for harvest in 3-5 days.",
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
    field_id: "field-2",
    severity: "low"
  },
  {
    id: "alert-3",
    type: "success",
    title: "Pest Control Successful",
    message: "Integrated pest management reduced pest damage by 40% this season.",
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
    field_id: "field-3",
    severity: "low"
  }
];

// Demo AI Insights
export const demoAIInsights = [
  {
    id: "insight-1",
    type: "optimization",
    title: "Irrigation Optimization",
    description: "AI analysis suggests 15% reduction in water usage while maintaining yield through precision irrigation scheduling.",
    impact: "Save 6,750 liters of water per month",
    confidence: 92,
    implementation: "Easy",
    cost_savings: 2500
  },
  {
    id: "insight-2",
    type: "prediction", 
    title: "Yield Prediction",
    description: "Machine learning models predict 18% increase in rice yield based on current soil and weather conditions.",
    impact: "Additional 0.75 tons per acre expected",
    confidence: 87,
    implementation: "Medium",
    cost_savings: 15000
  },
  {
    id: "insight-3",
    type: "prevention",
    title: "Disease Prevention",
    description: "Early detection algorithm identified potential fungal infection risk. Preventive treatment recommended.",
    impact: "Prevent 25% yield loss",
    confidence: 89,
    implementation: "Easy", 
    cost_savings: 8000
  }
];

export default {
  demoFarms,
  demoFields,
  generateDemoSensorData,
  demoWeatherData,
  demoMarketData,
  demoYieldPredictions,
  demoAnalytics,
  demoAlerts,
  demoAIInsights
};
