// Environment configuration for AgriForecast
export const environment = {
  // Weather API Configuration
  OPENWEATHER_API_KEY: import.meta.env.VITE_OPENWEATHER_API_KEY || '28f1d9ac94ed94535d682b7bf6c441bb',
  
  // Market Data API
  ALPHA_VANTAGE_API_KEY: import.meta.env.VITE_ALPHA_VANTAGE_API_KEY || 'KJRXQKB09I13GUPP',
  
  // NASA API
  NASA_API_KEY: import.meta.env.VITE_NASA_API_KEY || '4Od5nRoNq2NKdyFZ6ENS98kcpZg4RT3Efelbjleb',
  
  // Google Maps API
  GOOGLE_MAPS_API_KEY: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'demo',
  
  // Supabase Configuration
  SUPABASE_URL: import.meta.env.VITE_SUPABASE_URL || 'https://rdzyxfeggviqxajqddae.supabase.co',
  SUPABASE_ANON_KEY: import.meta.env.VITE_SUPABASE_ANON_KEY || 'your_supabase_anon_key',
  
  // Backend API URL
  BACKEND_URL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000',
  
  // Agricultural Data API
  AGRICULTURAL_API_KEY: import.meta.env.VITE_AGRICULTURAL_API_KEY || 'demo',
  
  // Demo Mode Configuration
  DEMO_MODE: true, // Set to false for production
  REALISTIC_DEMO: true, // Use realistic demo data
}

export default environment
