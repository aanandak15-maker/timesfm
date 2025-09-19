import axios from 'axios'
import type { 
  Farm, 
  Field, 
  WeatherData, 
  YieldPrediction, 
  MarketData, 
  DashboardStats,
  CreateFarmForm,
  CreateFieldForm,
  ApiResponse,
} from '../types'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

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
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API Service
export const apiService = {
  // Health check
  async healthCheck(): Promise<ApiResponse<any>> {
    const response = await api.get('/api/health')
    return response.data
  },

  // Authentication
  async login(credentials: { username: string; password: string }): Promise<ApiResponse<{ token: string; user: any }>> {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  async logout(): Promise<ApiResponse<any>> {
    const response = await api.post('/auth/logout')
    return response.data
  },

  // Farms
  async getFarms(): Promise<Farm[]> {
    console.log('getFarms API call starting...')
    const response = await api.get('/api/farms')
    console.log('getFarms API response:', response.data)
    console.log('getFarms response.data.data:', response.data.data)
    console.log('getFarms response.data:', response.data)
    return response.data.data || response.data
  },

  async createFarm(farm: CreateFarmForm): Promise<Farm> {
    const response = await api.post('/api/farms', farm)
    return response.data.data || response.data
  },

  async updateFarm(id: string, updates: Partial<Farm>): Promise<Farm> {
    const response = await api.put(`/api/farms/${id}`, updates)
    return response.data.data || response.data
  },

  async deleteFarm(id: string): Promise<void> {
    await api.delete(`/api/farms/${id}`)
  },

  // Fields
  async getFields(farmId?: string): Promise<Field[]> {
    console.log('getFields called with:', farmId, typeof farmId)
    
    // If farmId is an object, extract the id property
    let actualFarmId = farmId
    if (farmId && typeof farmId === 'object') {
      console.log('farmId is an object:', farmId)
      actualFarmId = (farmId as any).id
      console.log('Extracted farm ID:', actualFarmId)
    }
    
    const url = actualFarmId ? `/api/fields?farm_id=${actualFarmId}` : '/api/fields'
    console.log('API call to:', url)
    const response = await api.get(url)
    console.log('API response:', response.data)
    console.log('Response data.data:', response.data.data)
    console.log('Response data length:', response.data.data?.length)
    return response.data.data || response.data
  },

  async createField(field: CreateFieldForm): Promise<Field> {
    console.log('createField API call with data:', field)
    const response = await api.post('/api/fields', field)
    console.log('createField API response:', response.data)
    return response.data.data || response.data
  },

  async updateField(id: string, updates: Partial<Field>): Promise<Field> {
    const response = await api.put(`/api/fields/${id}`, updates)
    return response.data.data || response.data
  },

  async deleteField(id: string): Promise<void> {
    await api.delete(`/api/fields/${id}`)
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
    const response = await api.post('/api/predict/yield', fieldData)
    return response.data.data || response.data
  },

  async batchPredict(fields: Array<{ field_id: string; [key: string]: any }>): Promise<YieldPrediction[]> {
    const response = await api.post('/api/predict/batch', { fields })
    return response.data.data || response.data
  },

  // Weather
  async getWeatherData(latitude: number, longitude: number): Promise<WeatherData> {
    const response = await api.get(`/api/weather/${latitude}/${longitude}`)
    return response.data.data || response.data
  },

  async getWeatherForecast(fieldId: string, days: number = 7): Promise<any> {
    const response = await api.get(`/api/weather/forecast?field_id=${fieldId}&days=${days}`)
    return response.data.data || response.data
  },

  // Market Intelligence
  async getMarketData(commodity: string): Promise<MarketData> {
    const response = await api.get(`/api/market/${commodity}`)
    return response.data.data || response.data
  },

  async getMarketPredictions(cropType: string, region?: string): Promise<any> {
    const params = new URLSearchParams({ crop_type: cropType })
    if (region) params.append('region', region)
    const response = await api.get(`/api/market/predictions?${params}`)
    return response.data.data || response.data
  },

  // Analytics
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await api.get('/api/analytics/dashboard')
    return response.data.data || response.data
  },

  async getYieldTrends(fieldId: string, timeRange: number = 365): Promise<any> {
    const response = await api.get(`/api/analytics/yield-trends?field_id=${fieldId}&days=${timeRange}`)
    return response.data.data || response.data
  },

  // Satellite Data
  async getSatelliteData(fieldId: string, startDate: string, endDate: string): Promise<any> {
    const response = await api.get(`/api/satellite/${fieldId}?start_date=${startDate}&end_date=${endDate}`)
    return response.data.data || response.data
  },

  // Real-time Features (from Streamlit platform)
  async getRealtimeStatus(): Promise<any> {
    const response = await api.get('/api/realtime/status')
    return response.data.data || response.data
  },

  async getNotifications(): Promise<any[]> {
    const response = await api.get('/api/notifications')
    return response.data.data || response.data
  },

  async getOfflineStatus(): Promise<any> {
    const response = await api.get('/api/offline/status')
    return response.data.data || response.data
  },

  // Performance Features (from Streamlit platform)
  async getPerformanceStats(): Promise<any> {
    const response = await api.get('/api/performance/stats')
    return response.data.data || response.data
  },

  async clearCache(): Promise<void> {
    await api.post('/api/performance/clear-cache')
  },

  // Phase 4 Advanced Features (from Streamlit platform)
  async getTimesFMAnalytics(fieldId: string): Promise<any> {
    const response = await api.get(`/api/timesfm/analytics?field_id=${fieldId}`)
    return response.data.data || response.data
  },

  async getDeploymentStatus(): Promise<any> {
    const response = await api.get('/api/deployment/status')
    return response.data.data || response.data
  },

  async runIntegrationTests(): Promise<any> {
    const response = await api.post('/api/testing/integration')
    return response.data.data || response.data
  }
}

export default apiService