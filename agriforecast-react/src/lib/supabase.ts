import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'your-supabase-url'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'your-supabase-anon-key'

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  },
  realtime: {
    params: {
      eventsPerSecond: 10,
    },
  },
})

// Database types
export interface User {
  id: string
  email: string
  full_name: string
  avatar_url?: string
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

export interface WeatherData {
  id: string
  field_id: string
  date: string
  temperature_max: number
  temperature_min: number
  humidity: number
  rainfall: number
  wind_speed: number
  created_at: string
}

export interface YieldData {
  id: string
  field_id: string
  season: string
  actual_yield?: number
  predicted_yield?: number
  yield_date: string
  created_at: string
}

// API functions
export const api = {
  // Authentication
  async signUp(email: string, password: string, userData: { full_name: string }) {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: userData,
      },
    })
    return { data, error }
  },

  async signIn(email: string, password: string) {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    return { data, error }
  },

  async signOut() {
    const { error } = await supabase.auth.signOut()
    return { error }
  },

  async getCurrentUser() {
    const { data: { user } } = await supabase.auth.getUser()
    return user
  },

  // Farms
  async getFarms(userId: string): Promise<Farm[]> {
    const { data, error } = await supabase
      .from('farms')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data || []
  },

  async createFarm(farm: Omit<Farm, 'id' | 'created_at' | 'updated_at'>): Promise<Farm> {
    const { data, error } = await supabase
      .from('farms')
      .insert([farm])
      .select()
      .single()

    if (error) throw error
    return data
  },

  async updateFarm(id: string, updates: Partial<Farm>): Promise<Farm> {
    const { data, error } = await supabase
      .from('farms')
      .update({ ...updates, updated_at: new Date().toISOString() })
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  async deleteFarm(id: string) {
    const { error } = await supabase
      .from('farms')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Fields
  async getFields(farmId: string): Promise<Field[]> {
    const { data, error } = await supabase
      .from('fields')
      .select('*')
      .eq('farm_id', farmId)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data || []
  },

  async createField(field: Omit<Field, 'id' | 'created_at' | 'updated_at'>): Promise<Field> {
    const { data, error } = await supabase
      .from('fields')
      .insert([field])
      .select()
      .single()

    if (error) throw error
    return data
  },

  async updateField(id: string, updates: Partial<Field>): Promise<Field> {
    const { data, error } = await supabase
      .from('fields')
      .update({ ...updates, updated_at: new Date().toISOString() })
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  async deleteField(id: string) {
    const { error } = await supabase
      .from('fields')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Weather Data
  async getWeatherData(fieldId: string, limit: number = 30): Promise<WeatherData[]> {
    const { data, error } = await supabase
      .from('weather_data')
      .select('*')
      .eq('field_id', fieldId)
      .order('date', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data || []
  },

  async addWeatherData(weatherData: Omit<WeatherData, 'id' | 'created_at'>): Promise<WeatherData> {
    const { data, error } = await supabase
      .from('weather_data')
      .insert([weatherData])
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Yield Data
  async getYieldData(fieldId: string): Promise<YieldData[]> {
    const { data, error } = await supabase
      .from('yield_data')
      .select('*')
      .eq('field_id', fieldId)
      .order('yield_date', { ascending: false })

    if (error) throw error
    return data || []
  },

  async addYieldData(yieldData: Omit<YieldData, 'id' | 'created_at'>): Promise<YieldData> {
    const { data, error } = await supabase
      .from('yield_data')
      .insert([yieldData])
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Real-time subscriptions
  subscribeToFarmChanges(userId: string, callback: (payload: any) => void) {
    return supabase
      .channel('farms-changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'farms',
          filter: `user_id=eq.${userId}`,
        },
        callback
      )
      .subscribe()
  },

  subscribeToFieldChanges(farmId: string, callback: (payload: any) => void) {
    return supabase
      .channel('fields-changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'fields',
          filter: `farm_id=eq.${farmId}`,
        },
        callback
      )
      .subscribe()
  },

  subscribeToWeatherUpdates(fieldId: string, callback: (payload: any) => void) {
    return supabase
      .channel('weather-updates')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'weather_data',
          filter: `field_id=eq.${fieldId}`,
        },
        callback
      )
      .subscribe()
  },
}

export default supabase
