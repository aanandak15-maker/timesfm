// Weather API service for real-time weather data
export interface WeatherData {
  location: {
    name: string
    country: string
    lat: number
    lon: number
  }
  current: {
    temperature: number
    humidity: number
    wind_speed: number
    pressure: number
    conditions: string
    icon: string
    feels_like: number
    uv_index: number
    visibility: number
  }
  forecast: Array<{
    date: string
    high: number
    low: number
    conditions: string
    precipitation: number
    icon: string
    wind_speed: number
    humidity: number
  }>
}

class WeatherApiService {
  private apiKey: string
  private baseUrl: string

  constructor() {
    // Using OpenWeatherMap API (free tier)
    this.apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY || 'demo'
    this.baseUrl = 'https://api.openweathermap.org/data/2.5'
    
    if (this.apiKey === 'demo') {
      console.warn('⚠️ Using demo weather data. Get a free API key at https://openweathermap.org/api for real weather data!')
    } else {
      console.log('✅ Real weather API key detected. Fetching live weather data...')
    }
  }

  async getCurrentWeather(lat: number, lon: number): Promise<WeatherData> {
    try {
      // Always try real API first, fallback to mock if it fails
      console.log('Attempting to fetch real current weather data...')
      const response = await fetch(
        `${this.baseUrl}/weather?lat=${lat}&lon=${lon}&appid=${this.apiKey}&units=metric`
      )

      if (!response.ok) {
        throw new Error(`Weather API error: ${response.status}`)
      }

      const data = await response.json()
      console.log('Real current weather data received:', data)
      return this.transformWeatherData(data)
    } catch (error) {
      console.warn('Real weather API failed, using mock data:', error)
      return this.getMockWeatherData(lat, lon)
    }
  }

  async getWeatherForecast(lat: number, lon: number): Promise<WeatherData> {
    console.log('Weather API called with coordinates:', { lat, lon })
    console.log('Weather API coordinates:', `Lat: ${lat}, Lon: ${lon}`)
    try {
      // Always try real API first, fallback to mock if it fails
      console.log('Attempting to fetch real weather data...')
      const response = await fetch(
        `${this.baseUrl}/forecast?lat=${lat}&lon=${lon}&appid=${this.apiKey}&units=metric`
      )

      if (!response.ok) {
        throw new Error(`Weather API error: ${response.status}`)
      }

      const data = await response.json()
      console.log('Real weather data received:', data)
      return this.transformForecastData(data)
    } catch (error) {
      console.warn('Real weather API failed, using mock data:', error)
      console.log('Using mock weather data for coordinates:', { lat, lon })
      console.log('Mock weather coordinates:', `Lat: ${lat}, Lon: ${lon}`)
      return this.getMockWeatherData(lat, lon)
    }
  }

  private transformWeatherData(data: any): WeatherData {
    return {
      location: {
        name: data.name,
        country: data.sys.country,
        lat: data.coord.lat,
        lon: data.coord.lon,
      },
      current: {
        temperature: Math.round(data.main.temp),
        humidity: data.main.humidity,
        wind_speed: data.wind.speed,
        pressure: data.main.pressure,
        conditions: data.weather[0].main,
        icon: data.weather[0].icon,
        feels_like: Math.round(data.main.feels_like),
        uv_index: 0, // Not available in current weather
        visibility: data.visibility / 1000, // Convert to km
      },
      forecast: [], // Will be populated by forecast call
    }
  }

  private transformForecastData(data: any): WeatherData {
    const current = data.list[0]
    const forecast = data.list.slice(0, 5).map((item: any) => ({
      date: item.dt_txt.split(' ')[0],
      high: Math.round(item.main.temp_max),
      low: Math.round(item.main.temp_min),
      conditions: item.weather[0].main,
      precipitation: item.pop * 100, // Convert to percentage
      icon: item.weather[0].icon,
      wind_speed: item.wind.speed,
      humidity: item.main.humidity,
    }))

    return {
      location: {
        name: data.city.name,
        country: data.city.country,
        lat: data.city.coord.lat,
        lon: data.city.coord.lon,
      },
      current: {
        temperature: Math.round(current.main.temp),
        humidity: current.main.humidity,
        wind_speed: current.wind.speed,
        pressure: current.main.pressure,
        conditions: current.weather[0].main,
        icon: current.weather[0].icon,
        feels_like: Math.round(current.main.feels_like),
        uv_index: 0,
        visibility: current.visibility / 1000,
      },
      forecast,
    }
  }

  private getMockWeatherData(lat: number, lon: number): WeatherData {
    console.log('Generating mock weather data for coordinates:', { lat, lon })
    console.log('Mock data coordinates:', `Lat: ${lat}, Lon: ${lon}`)
    
    // Determine location based on coordinates
    let locationName = 'Unknown Location'
    let country = 'Unknown'
    
    // Check if coordinates are in India (approximate bounds)
    if (lat >= 6.0 && lat <= 37.0 && lon >= 68.0 && lon <= 98.0) {
      country = 'IN'
      // Determine Indian state/region based on coordinates
      if (lat >= 28.0 && lat <= 30.0 && lon >= 76.0 && lon <= 79.0) {
        locationName = 'Uttar Pradesh, India'
      } else if (lat >= 28.5 && lat <= 28.8 && lon >= 77.0 && lon <= 77.3) {
        locationName = 'Delhi, India'
      } else if (lat >= 28.3 && lat <= 28.4 && lon >= 77.5 && lon <= 77.6) {
        locationName = 'Noida/Greater Noida, Uttar Pradesh, India'
      } else if (lat >= 19.0 && lat <= 19.3 && lon >= 72.7 && lon <= 73.0) {
        locationName = 'Mumbai, India'
      } else if (lat >= 12.8 && lat <= 13.2 && lon >= 77.4 && lon <= 77.8) {
        locationName = 'Bangalore, India'
      } else if (lat >= 13.0 && lat <= 13.2 && lon >= 80.2 && lon <= 80.3) {
        locationName = 'Chennai, India'
      } else {
        locationName = 'India'
      }
    } else if (lat >= 40.0 && lat <= 45.0 && lon >= -75.0 && lon <= -70.0) {
      locationName = 'New York, US'
      country = 'US'
    } else if (lat >= 51.0 && lat <= 52.0 && lon >= -0.5 && lon <= 0.5) {
      locationName = 'London, UK'
      country = 'GB'
    } else if (lat >= 35.0 && lat <= 36.0 && lon >= 139.0 && lon <= 140.0) {
      locationName = 'Tokyo, Japan'
      country = 'JP'
    } else {
      locationName = `Location (${lat.toFixed(4)}, ${lon.toFixed(4)})`
      country = 'Unknown'
    }
    
    console.log('Selected location based on coordinates:', { name: locationName, country })
    
    return {
      location: {
        name: locationName,
        country: country,
        lat,
        lon,
      },
      current: {
        temperature: country === 'IN' ? Math.floor(Math.random() * 20) + 25 : Math.floor(Math.random() * 30) + 50, // 25-45°C for India, 50-80°F for others
        humidity: country === 'IN' ? Math.floor(Math.random() * 30) + 50 : Math.floor(Math.random() * 40) + 40, // 50-80% for India
        wind_speed: country === 'IN' ? Math.floor(Math.random() * 10) + 5 : Math.floor(Math.random() * 15) + 5, // 5-15 km/h for India
        pressure: Math.floor(Math.random() * 50) + 1000, // 1000-1050 hPa
        conditions: country === 'IN' ? 
          ['Sunny', 'Partly Cloudy', 'Hazy', 'Hot'][Math.floor(Math.random() * 4)] : 
          ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy'][Math.floor(Math.random() * 4)],
        icon: country === 'IN' ? 
          ['01d', '02d', '50d', '01d'][Math.floor(Math.random() * 4)] : 
          ['01d', '02d', '03d', '10d'][Math.floor(Math.random() * 4)],
        feels_like: country === 'IN' ? Math.floor(Math.random() * 20) + 30 : Math.floor(Math.random() * 30) + 50,
        uv_index: country === 'IN' ? Math.floor(Math.random() * 5) + 5 : Math.floor(Math.random() * 10), // Higher UV in India
        visibility: country === 'IN' ? Math.floor(Math.random() * 5) + 3 : Math.floor(Math.random() * 10) + 5, // Lower visibility in India due to pollution
      },
      forecast: Array.from({ length: 5 }, (_, i) => ({
        date: new Date(Date.now() + i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        high: country === 'IN' ? Math.floor(Math.random() * 15) + 30 : Math.floor(Math.random() * 20) + 60,
        low: country === 'IN' ? Math.floor(Math.random() * 10) + 20 : Math.floor(Math.random() * 20) + 40,
        conditions: country === 'IN' ? 
          ['Sunny', 'Partly Cloudy', 'Hazy', 'Hot'][Math.floor(Math.random() * 4)] : 
          ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy'][Math.floor(Math.random() * 4)],
        precipitation: Math.floor(Math.random() * 100),
        icon: country === 'IN' ? 
          ['01d', '02d', '50d', '01d'][Math.floor(Math.random() * 4)] : 
          ['01d', '02d', '03d', '10d'][Math.floor(Math.random() * 4)],
        wind_speed: country === 'IN' ? Math.floor(Math.random() * 10) + 5 : Math.floor(Math.random() * 15) + 5,
        humidity: country === 'IN' ? Math.floor(Math.random() * 30) + 50 : Math.floor(Math.random() * 40) + 40,
      })),
    }
  }
}

export const weatherApi = new WeatherApiService()
export default weatherApi