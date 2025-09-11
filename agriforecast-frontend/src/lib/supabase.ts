// Supabase configuration for AgriForecast
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://rdzyxfeggviqxajqddae.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkenl4ZmVnZ3ZpcXhhanFkZGFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc2MTMzNTIsImV4cCI6MjA3MzE4OTM1Mn0.ugxmvyNl1wt5GcEm0_dWbrhFqp6b3qzA1yqY1uE_nqg'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types for TypeScript
export interface Database {
  public: {
    Tables: {
      farms: {
        Row: {
          id: string
          name: string
          location: string
          area: number
          created_at: string
          user_id: string
        }
        Insert: {
          id?: string
          name: string
          location: string
          area: number
          created_at?: string
          user_id: string
        }
        Update: {
          id?: string
          name?: string
          location?: string
          area?: number
          created_at?: string
          user_id?: string
        }
      }
      fields: {
        Row: {
          id: string
          farm_id: string
          name: string
          crop_type: string
          area: number
          coordinates: any
          created_at: string
        }
        Insert: {
          id?: string
          farm_id: string
          name: string
          crop_type: string
          area: number
          coordinates: any
          created_at?: string
        }
        Update: {
          id?: string
          farm_id?: string
          name?: string
          crop_type?: string
          area?: number
          coordinates?: any
          created_at?: string
        }
      }
      weather_data: {
        Row: {
          id: string
          field_id: string
          temperature: number
          humidity: number
          precipitation: number
          wind_speed: number
          recorded_at: string
        }
        Insert: {
          id?: string
          field_id: string
          temperature: number
          humidity: number
          precipitation: number
          wind_speed: number
          recorded_at?: string
        }
        Update: {
          id?: string
          field_id?: string
          temperature?: number
          humidity?: number
          precipitation?: number
          wind_speed?: number
          recorded_at?: string
        }
      }
      yield_predictions: {
        Row: {
          id: string
          field_id: string
          predicted_yield: number
          confidence_score: number
          factors: any
          created_at: string
        }
        Insert: {
          id?: string
          field_id: string
          predicted_yield: number
          confidence_score: number
          factors: any
          created_at?: string
        }
        Update: {
          id?: string
          field_id?: string
          predicted_yield?: number
          confidence_score?: number
          factors?: any
          created_at?: string
        }
      }
    }
  }
}

export default supabase
