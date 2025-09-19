// Demo Configuration for Hackathon Presentation
export const DEMO_CONFIG = {
  // Enable demo mode
  DEMO_MODE: true,
  
  // Demo data settings
  SIMULATION_INTERVAL: 5000, // 5 seconds
  DATA_POINTS_LIMIT: 50,
  
  // Demo features
  FEATURES: {
    REAL_TIME_SIMULATION: true,
    AI_INSIGHTS: true,
    MARKET_DATA: true,
    WEATHER_DATA: true,
    IOT_SENSORS: true,
    FIELD_MAPPING: true,
    YIELD_PREDICTION: true,
    ALERTS: true,
    ANALYTICS: true
  },
  
  // Demo statistics
  STATS: {
    TOTAL_FARMS: 3,
    TOTAL_FIELDS: 3,
    TOTAL_AREA: 7.5,
    AVERAGE_YIELD: 3.5,
    TOTAL_REVENUE: 1250000,
    COST_SAVINGS: 180000,
    WATER_SAVED: 45000,
    FERTILIZER_OPTIMIZED: 25,
    PEST_REDUCTION: 40,
    YIELD_INCREASE: 18
  },
  
  // Demo notifications
  NOTIFICATIONS: [
    "🌱 Field 1 soil moisture is optimal for rice growth",
    "🌤️ Weather forecast shows ideal conditions for next 3 days", 
    "📈 Yield prediction updated - 15% increase expected",
    "💰 Market prices for rice increased by 2.3%",
    "🔋 IoT device battery levels are good across all fields",
    "🌾 Field 2 maize is ready for harvest in 5 days",
    "💧 Irrigation system activated automatically",
    "📊 Monthly analytics report is ready",
    "🤖 AI detected optimal fertilizer application window",
    "📱 New field mapping completed successfully"
  ],
  
  // Demo crops
  CROPS: [
    { name: "Rice", price: 2850, change: 45, changePercent: 1.6 },
    { name: "Maize", price: 1950, change: -25, changePercent: -1.3 },
    { name: "Cotton", price: 7200, change: 120, changePercent: 1.7 }
  ],
  
  // Demo locations
  LOCATIONS: [
    { name: "Punjab, India", lat: 28.368911, lng: 77.541033 },
    { name: "Gujarat, India", lat: 30.368911, lng: 75.541033 },
    { name: "West Bengal, India", lat: 22.5726, lng: 88.3639 }
  ]
};

export default DEMO_CONFIG;
