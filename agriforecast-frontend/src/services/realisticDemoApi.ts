// Realistic Demo Data Service - Feels like real production data
export interface RealisticDemoData {
  location: {
    name: string
    state: string
    country: string
    coordinates: { lat: number; lng: number }
  }
  weather: {
    current: any
    forecast: any[]
  }
  market: {
    rice: { price: number; change: number; trend: 'up' | 'down' | 'stable' }
    wheat: { price: number; change: number; trend: 'up' | 'down' | 'stable' }
    corn: { price: number; change: number; trend: 'up' | 'down' | 'stable' }
  }
  soil: {
    ph: number
    moisture: number
    temperature: number
    organic_matter: number
    nitrogen: number
    phosphorus: number
    potassium: number
  }
  crop: {
    stage: string
    health_score: number
    days_to_harvest: number
    yield_prediction: number
  }
  satellite: {
    ndvi: number
    ndwi: number
    cloud_cover: number
    last_image_date: string
  }
}

class RealisticDemoApiService {
  private baseLocation = {
    lat: 28.3477,
    lng: 77.5573,
    name: 'Noida/Greater Noida',
    state: 'Uttar Pradesh',
    country: 'India'
  }

  // Generate realistic Indian agricultural data
  generateRealisticData(): RealisticDemoData {
    const now = new Date()
    const season = this.getIndianSeason(now)
    const timeOfDay = now.getHours()
    
    return {
      location: this.baseLocation,
      weather: this.generateRealisticWeather(season, timeOfDay),
      market: this.generateRealisticMarketData(season),
      soil: this.generateRealisticSoilData(season),
      crop: this.generateRealisticCropData(season),
      satellite: this.generateRealisticSatelliteData(season)
    }
  }

  private getIndianSeason(date: Date): 'kharif' | 'rabi' | 'summer' | 'monsoon' {
    const month = date.getMonth() + 1
    if (month >= 6 && month <= 9) return 'monsoon'
    if (month >= 10 && month <= 12) return 'kharif'
    if (month >= 1 && month <= 3) return 'rabi'
    return 'summer'
  }

  private generateRealisticWeather(season: string, timeOfDay: number): any {
    const baseTemp = this.getBaseTemperature(season, timeOfDay)
    const humidity = this.getBaseHumidity(season)
    const conditions = this.getWeatherConditions(season, timeOfDay)
    
    return {
      current: {
        temperature: Math.round(baseTemp + (Math.random() - 0.5) * 4),
        humidity: Math.round(humidity + (Math.random() - 0.5) * 10),
        condition: conditions.current,
        wind_speed: Math.round(5 + Math.random() * 15),
        pressure: Math.round(1010 + Math.random() * 20),
        uv_index: Math.round(3 + Math.random() * 8),
        visibility: Math.round(8 + Math.random() * 4),
        feels_like: Math.round(baseTemp + (Math.random() - 0.5) * 3)
      },
      forecast: this.generateForecast(season)
    }
  }

  private getBaseTemperature(season: string, timeOfDay: number): number {
    const seasonTemps = {
      'monsoon': 28,
      'kharif': 32,
      'rabi': 22,
      'summer': 38
    }
    
    const baseTemp = seasonTemps[season] || 30
    const dailyVariation = timeOfDay < 6 ? -8 : timeOfDay < 12 ? 4 : timeOfDay < 18 ? 6 : -2
    return baseTemp + dailyVariation
  }

  private getBaseHumidity(season: string): number {
    const seasonHumidity = {
      'monsoon': 85,
      'kharif': 70,
      'rabi': 60,
      'summer': 45
    }
    return seasonHumidity[season] || 65
  }

  private getWeatherConditions(season: string, timeOfDay: number): any {
    const conditions = {
      'monsoon': ['Heavy Rain', 'Light Rain', 'Overcast', 'Drizzle'],
      'kharif': ['Partly Cloudy', 'Clear', 'Hazy', 'Overcast'],
      'rabi': ['Clear', 'Partly Cloudy', 'Fog', 'Overcast'],
      'summer': ['Clear', 'Hazy', 'Partly Cloudy', 'Dust Storm']
    }
    
    const possibleConditions = conditions[season] || ['Clear', 'Partly Cloudy']
    return {
      current: possibleConditions[Math.floor(Math.random() * possibleConditions.length)],
      description: this.getWeatherDescription(season)
    }
  }

  private getWeatherDescription(season: string): string {
    const descriptions = {
      'monsoon': 'Heavy rainfall expected. Good for rice cultivation.',
      'kharif': 'Ideal conditions for kharif crops. Monitor irrigation.',
      'rabi': 'Cool and dry conditions. Perfect for wheat cultivation.',
      'summer': 'Hot and dry. Ensure adequate irrigation and shade.'
    }
    return descriptions[season] || 'Normal weather conditions for farming.'
  }

  private generateForecast(season: string): any[] {
    const days = []
    for (let i = 1; i <= 5; i++) {
      const date = new Date()
      date.setDate(date.getDate() + i)
      
      days.push({
        date: date.toISOString().split('T')[0],
        high: Math.round(25 + Math.random() * 15),
        low: Math.round(15 + Math.random() * 10),
        condition: this.getWeatherConditions(season, 12).current,
        precipitation: Math.round(Math.random() * 20),
        wind_speed: Math.round(5 + Math.random() * 15)
      })
    }
    return days
  }

  private generateRealisticMarketData(season: string): any {
    const basePrices = {
      'monsoon': { rice: 2800, wheat: 2400, corn: 2200 },
      'kharif': { rice: 3000, wheat: 2500, corn: 2300 },
      'rabi': { rice: 2900, wheat: 2600, corn: 2100 },
      'summer': { rice: 3100, wheat: 2700, corn: 2400 }
    }
    
    const prices = basePrices[season] || { rice: 2900, wheat: 2500, corn: 2200 }
    
    return {
      rice: {
        price: prices.rice + Math.round((Math.random() - 0.5) * 200),
        change: Math.round((Math.random() - 0.5) * 100),
        trend: Math.random() > 0.5 ? 'up' : 'down'
      },
      wheat: {
        price: prices.wheat + Math.round((Math.random() - 0.5) * 150),
        change: Math.round((Math.random() - 0.5) * 80),
        trend: Math.random() > 0.5 ? 'up' : 'down'
      },
      corn: {
        price: prices.corn + Math.round((Math.random() - 0.5) * 100),
        change: Math.round((Math.random() - 0.5) * 60),
        trend: Math.random() > 0.5 ? 'up' : 'down'
      }
    }
  }

  private generateRealisticSoilData(season: string): any {
    const seasonFactors = {
      'monsoon': { moisture: 0.8, ph: 0.1, organic: 0.05 },
      'kharif': { moisture: 0.6, ph: 0.0, organic: 0.0 },
      'rabi': { moisture: 0.4, ph: -0.1, organic: -0.02 },
      'summer': { moisture: 0.3, ph: -0.2, organic: -0.05 }
    }
    
    const factors = seasonFactors[season] || { moisture: 0.5, ph: 0.0, organic: 0.0 }
    
    return {
      ph: 6.5 + factors.ph + (Math.random() - 0.5) * 0.5,
      moisture: Math.round((35 + factors.moisture * 20 + Math.random() * 10) * 10) / 10,
      temperature: Math.round((22 + Math.random() * 8) * 10) / 10,
      organic_matter: Math.round((2.5 + factors.organic + Math.random() * 0.5) * 10) / 10,
      nitrogen: Math.round((120 + Math.random() * 40) * 10) / 10,
      phosphorus: Math.round((25 + Math.random() * 15) * 10) / 10,
      potassium: Math.round((200 + Math.random() * 100) * 10) / 10
    }
  }

  private generateRealisticCropData(season: string): any {
    const cropStages = {
      'monsoon': ['Vegetative', 'Flowering', 'Grain Filling'],
      'kharif': ['Flowering', 'Grain Filling', 'Maturity'],
      'rabi': ['Germination', 'Vegetative', 'Flowering'],
      'summer': ['Maturity', 'Harvest', 'Post-Harvest']
    }
    
    const stages = cropStages[season] || ['Vegetative', 'Flowering']
    const currentStage = stages[Math.floor(Math.random() * stages.length)]
    
    return {
      stage: currentStage,
      health_score: Math.round(75 + Math.random() * 20),
      days_to_harvest: Math.round(30 + Math.random() * 60),
      yield_prediction: Math.round((3.5 + Math.random() * 1.5) * 10) / 10
    }
  }

  private generateRealisticSatelliteData(season: string): any {
    const seasonNDVI = {
      'monsoon': 0.7,
      'kharif': 0.8,
      'rabi': 0.6,
      'summer': 0.4
    }
    
    const baseNDVI = seasonNDVI[season] || 0.6
    
    return {
      ndvi: Math.round((baseNDVI + (Math.random() - 0.5) * 0.2) * 100) / 100,
      ndwi: Math.round((0.4 + Math.random() * 0.3) * 100) / 100,
      cloud_cover: Math.round(Math.random() * 30),
      last_image_date: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    }
  }
}

export const realisticDemoApi = new RealisticDemoApiService()
export default realisticDemoApi
