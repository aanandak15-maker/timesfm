// Core agricultural data types
export interface Farm {
  id: string
  user_id: string
  name: string
  location: string
  total_area_acres: number
  description?: string
  latitude?: number
  longitude?: number
  created_at: string
  updated_at: string
}

export interface Field {
  id: string
  farm_id: string
  name: string
  crop_type: string
  area_acres: number
  latitude?: number
  longitude?: number
  soil_type?: string
  planting_date?: string
  harvest_date?: string
  status: 'preparing' | 'planted' | 'growing' | 'harvesting' | 'harvested'
  created_at: string
  updated_at: string
}

export interface WeatherData {
  location: string
  current: {
    temperature: number
    humidity: number
    wind_speed: number
    pressure: number
    conditions: string
    icon: string
  }
  forecast: Array<{
    date: string
    high: number
    low: number
    conditions: string
    precipitation: number
    icon: string
  }>
}

export interface YieldPrediction {
  field_id: string
  predicted_yield: number
  confidence_score: number
  prediction_date: string
  harvest_window: {
    optimal_start: string
    optimal_end: string
  }
  factors: {
    weather_score: number
    soil_score: number
    crop_health_score: number
  }
}

export interface MarketData {
  commodity: string
  current_price: number
  price_change: number
  price_change_percent: number
  volume: number
  trend: 'up' | 'down' | 'stable'
  last_updated: string
}

export interface DashboardStats {
  totalFarms: number
  totalFields: number
  totalAcres: number
  averageYield: number
  riskScore: number
  marketTrend: 'up' | 'down' | 'stable'
}

export interface User {
  id: string
  name: string
  email: string
  role: 'farmer' | 'admin' | 'analyst'
  created_at: string
}

// API Response types
export interface ApiResponse<T> {
  status: 'success' | 'error'
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  hasNext: boolean
  hasPrev: boolean
}

// Form types
export interface CreateFarmForm {
  name: string
  location: string
  total_area_acres: number
  description?: string
  latitude?: number
  longitude?: number
}

export interface CreateFieldForm {
  name: string
  farm_id: string
  crop_type: string
  area_acres: number
  latitude?: number
  longitude?: number
  soil_type?: string
  planting_date?: string
}

// Chart data types
export interface ChartDataPoint {
  date: string
  value: number
  label?: string
}

export interface YieldChartData {
  field_id: string
  field_name: string
  data: ChartDataPoint[]
}

// Alert types
export interface Alert {
  id: string
  type: 'weather' | 'field' | 'market' | 'system'
  severity: 'low' | 'medium' | 'high' | 'critical'
  title: string
  message: string
  timestamp: string
  read: boolean
  action_url?: string
}

