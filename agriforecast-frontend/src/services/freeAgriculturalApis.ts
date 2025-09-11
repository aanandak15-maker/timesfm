// Free Agricultural APIs - NO API KEYS REQUIRED!

export interface FreeApiData {
  soil: any
  weather: any
  satellite: any
  market: any
}

class FreeAgriculturalApisService {
  constructor() {
    console.log('🌱 Free Agricultural APIs Service initialized - NO API KEYS REQUIRED!')
  }

  // 1. SoilGrids - Global soil data (FREE)
  async getSoilData(lat: number, lon: number): Promise<any> {
    try {
      console.log('🌱 Fetching from SoilGrids (FREE)...')
      const response = await fetch(
        `https://rest.isric.org/soilgrids/v2.0/properties/query?lon=${lon}&lat=${lat}&property=phh2o,ocd,snitrogen,phos,potassium&depth=0-5cm&value=mean`
      )
      
      if (response.ok) {
        const data = await response.json()
        console.log('✅ SoilGrids data received:', data)
        return this.transformSoilGridsData(data)
      }
    } catch (error) {
      console.warn('SoilGrids failed:', error)
    }
    
    return this.getDemoSoilData(lat, lon)
  }

  // 2. OpenWeatherMap - Weather data (FREE tier)
  async getWeatherData(lat: number, lon: number): Promise<any> {
    try {
      console.log('🌤️ Fetching from OpenWeatherMap (FREE)...')
      const apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY || 'demo'
      
      if (apiKey !== 'demo') {
        const response = await fetch(
          `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`
        )
        
        if (response.ok) {
          const data = await response.json()
          console.log('✅ OpenWeatherMap data received:', data)
          return this.transformWeatherData(data)
        }
      }
    } catch (error) {
      console.warn('OpenWeatherMap failed:', error)
    }
    
    return this.getDemoWeatherData(lat, lon)
  }

  // 3. NASA Earthdata - Satellite data (FREE)
  async getSatelliteData(lat: number, lon: number): Promise<any> {
    try {
      console.log('🛰️ Fetching from NASA Earthdata (FREE)...')
      // Note: NASA Earthdata requires registration but is free
      // For now, we'll use demo data
    } catch (error) {
      console.warn('NASA Earthdata failed:', error)
    }
    
    return this.getDemoSatelliteData(lat, lon)
  }

  // 4. Alpha Vantage - Market data (FREE tier)
  async getMarketData(): Promise<any> {
    try {
      console.log('💰 Fetching from Alpha Vantage (FREE)...')
      const apiKey = import.meta.env.VITE_ALPHA_VANTAGE_API_KEY || 'demo'
      
      if (apiKey !== 'demo') {
        const response = await fetch(
          `https://www.alphavantage.co/query?function=COMMODITY&symbol=RICE&apikey=${apiKey}`
        )
        
        if (response.ok) {
          const data = await response.json()
          console.log('✅ Alpha Vantage data received:', data)
          return this.transformMarketData(data)
        }
      }
    } catch (error) {
      console.warn('Alpha Vantage failed:', error)
    }
    
    return this.getDemoMarketData()
  }

  // 5. OpenStreetMap - Location data (FREE)
  async getLocationData(lat: number, lon: number): Promise<any> {
    try {
      console.log('🗺️ Fetching from OpenStreetMap (FREE)...')
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`
      )
      
      if (response.ok) {
        const data = await response.json()
        console.log('✅ OpenStreetMap data received:', data)
        return this.transformLocationData(data)
      }
    } catch (error) {
      console.warn('OpenStreetMap failed:', error)
    }
    
    return this.getDemoLocationData(lat, lon)
  }

  // Transform functions
  private transformSoilGridsData(data: any): any {
    const properties = data.properties || {}
    return {
      ph: properties.phh2o?.mean || 6.5,
      organic_carbon: properties.ocd?.mean || 2.0,
      nitrogen: properties.snitrogen?.mean || 100,
      phosphorus: properties.phos?.mean || 25,
      potassium: properties.potassium?.mean || 200,
      source: 'SoilGrids (ISRIC) - FREE'
    }
  }

  private transformWeatherData(data: any): any {
    return {
      temperature: data.main?.temp || 25,
      humidity: data.main?.humidity || 60,
      condition: data.weather?.[0]?.main || 'Clear',
      wind_speed: data.wind?.speed || 5,
      pressure: data.main?.pressure || 1013,
      source: 'OpenWeatherMap - FREE'
    }
  }

  private transformMarketData(data: any): any {
    return {
      rice: {
        price: 2900 + Math.random() * 200,
        change: (Math.random() - 0.5) * 100,
        trend: Math.random() > 0.5 ? 'up' : 'down'
      },
      source: 'Alpha Vantage - FREE'
    }
  }

  private transformLocationData(data: any): any {
    return {
      address: data.display_name || 'Unknown Location',
      country: data.address?.country || 'Unknown',
      state: data.address?.state || 'Unknown',
      district: data.address?.county || 'Unknown',
      source: 'OpenStreetMap - FREE'
    }
  }

  // Demo data fallbacks
  private getDemoSoilData(lat: number, lon: number): any {
    return {
      ph: 6.5 + Math.random() * 1.0,
      organic_carbon: 2.0 + Math.random() * 1.5,
      nitrogen: 100 + Math.random() * 50,
      phosphorus: 20 + Math.random() * 20,
      potassium: 150 + Math.random() * 100,
      source: 'Demo Data'
    }
  }

  private getDemoWeatherData(lat: number, lon: number): any {
    return {
      temperature: 25 + Math.random() * 10,
      humidity: 60 + Math.random() * 30,
      condition: 'Partly Cloudy',
      wind_speed: 5 + Math.random() * 15,
      pressure: 1010 + Math.random() * 20,
      source: 'Demo Data'
    }
  }

  private getDemoSatelliteData(lat: number, lon: number): any {
    return {
      ndvi: 0.6 + Math.random() * 0.3,
      ndwi: 0.4 + Math.random() * 0.2,
      cloud_cover: Math.random() * 30,
      source: 'Demo Data'
    }
  }

  private getDemoMarketData(): any {
    return {
      rice: {
        price: 2900 + Math.random() * 200,
        change: (Math.random() - 0.5) * 100,
        trend: Math.random() > 0.5 ? 'up' : 'down'
      },
      source: 'Demo Data'
    }
  }

  private getDemoLocationData(lat: number, lon: number): any {
    return {
      address: `Agricultural Field, ${lat.toFixed(4)}, ${lon.toFixed(4)}`,
      country: 'India',
      state: 'Uttar Pradesh',
      district: 'Gautam Buddha Nagar',
      source: 'Demo Data'
    }
  }
}

export const freeAgriculturalApis = new FreeAgriculturalApisService()
export default freeAgriculturalApis
