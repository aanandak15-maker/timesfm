import axios from 'axios'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API Types
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
  created_at: string
  updated_at: string
}

export interface Farm {
  id: string
  user_id: string
  name: string
  location: string
  total_area_acres: number
  description?: string
  created_at: string
  updated_at: string
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

export interface WeatherData {
  location: string
  current: {
    temperature: number
    humidity: number
    wind_speed: number
    pressure: number
    conditions: string
  }
  forecast: Array<{
    date: string
    high: number
    low: number
    conditions: string
    precipitation: number
  }>
}

export interface RiskAssessment {
  overall_risk_score: number
  factors: {
    weather_risk: number
    pest_risk: number
    disease_risk: number
    market_risk: number
    irrigation_risk: number
  }
  recommendations: string[]
}

// API Functions
export const apiService = {
  // Health check
  async healthCheck() {
    const response = await api.get('/api/health')
    return response.data
  },

  // Authentication
  async login(credentials: { username: string; password: string }) {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  async logout() {
    const response = await api.post('/auth/logout')
    return response.data
  },

  // Farms
  async getFarms(): Promise<Farm[]> {
    const response = await api.get('/api/farms')
    return response.data.data || response.data
  },

  async createFarm(farm: Omit<Farm, 'id' | 'created_at' | 'updated_at'>): Promise<Farm> {
    const response = await api.post('/farms', farm)
    return response.data
  },

  async updateFarm(id: string, updates: Partial<Farm>): Promise<Farm> {
    const response = await api.put(`/farms/${id}`, updates)
    return response.data
  },

  async deleteFarm(id: string) {
    const response = await api.delete(`/farms/${id}`)
    return response.data
  },

  // Fields
  async getFields(farmId?: string): Promise<Field[]> {
    const url = farmId ? `/api/fields?farm_id=${farmId}` : '/api/fields'
    const response = await api.get(url)
    return response.data.data || response.data
  },

  async createField(field: Omit<Field, 'id' | 'created_at' | 'updated_at'>): Promise<Field> {
    const response = await api.post('/fields', field)
    return response.data
  },

  async updateField(id: string, updates: Partial<Field>): Promise<Field> {
    const response = await api.put(`/fields/${id}`, updates)
    return response.data
  },

  async deleteField(id: string) {
    const response = await api.delete(`/fields/${id}`)
    return response.data
  },

  // AI Predictions (TimesFM Integration)
  async predictYield(fieldData: {
    field_id: string
    crop_type: string
    area_acres: number
    latitude?: number
    longitude?: number
    soil_type?: string
    historical_data?: number[]
  }): Promise<YieldPrediction> {
    const response = await api.post('/predict/yield', fieldData)
    return response.data
  },

  async batchPredict(fields: Array<{ field_id: string; [key: string]: any }>): Promise<YieldPrediction[]> {
    const response = await api.post('/predict/batch', { fields })
    return response.data
  },

  async riskAssessment(fieldData: {
    field_id: string
    crop_type: string
    latitude?: number
    longitude?: number
    soil_type?: string
  }): Promise<RiskAssessment> {
    const response = await api.post('/risk/assessment', fieldData)
    return response.data
  },

  // Weather
  async getWeatherData(latitude: number, longitude: number): Promise<WeatherData> {
    const response = await api.get(`/weather?lat=${latitude}&lon=${longitude}`)
    return response.data
  },

  async getWeatherForecast(fieldId: string, days: number = 7): Promise<any> {
    const response = await api.get(`/weather/forecast?field_id=${fieldId}&days=${days}`)
    return response.data
  },

  async getWeatherImpact(fieldData: {
    field_id: string
    latitude: number
    longitude: number
    crop_type: string
    days_ahead: number
  }): Promise<any> {
    const response = await api.post('/forecast/weather-impact', fieldData)
    return response.data
  },

  // Market Intelligence
  async getMarketPredictions(cropType: string, region?: string): Promise<any> {
    const params = new URLSearchParams({ crop_type: cropType })
    if (region) params.append('region', region)
    const response = await api.get(`/market/predictions?${params}`)
    return response.data
  },

  async getCropInsights(cropType: string, region?: string): Promise<any> {
    const params = new URLSearchParams({ crop_type: cropType })
    if (region) params.append('region', region)
    const response = await api.get(`/insights/crop?${params}`)
    return response.data
  },

  // Analytics
  async getYieldTrends(fieldId: string, timeRange: number = 365): Promise<any> {
    const response = await api.get(`/analytics/yield-trends?field_id=${fieldId}&days=${timeRange}`)
    return response.data
  },

  async getWeatherAnalytics(location: { latitude: number; longitude: number }, timeRange: number = 30): Promise<any> {
    const response = await api.get(`/analytics/weather?lat=${location.latitude}&lon=${location.longitude}&days=${timeRange}`)
    return response.data
  },

  // Optimization
  async optimizeIrrigation(fieldData: {
    field_id: string
    crop_type: string
    soil_type: string
    current_moisture?: number
    weather_forecast?: any
  }): Promise<any> {
    const response = await api.post('/optimize/irrigation', fieldData)
    return response.data
  },

  // Real-time features
  async subscribeToFieldUpdates(fieldId: string, callback: (data: any) => void) {
    // WebSocket connection for real-time updates
    const wsUrl = API_BASE_URL.replace('http', 'ws') + `/ws/field/${fieldId}`
    const ws = new WebSocket(wsUrl)
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      callback(data)
    }
    
    return ws
  },
}

export default apiService
