// Google Maps API service for real geocoding and mapping
export interface GeocodingResult {
  address: string
  coordinates: {
    lat: number
    lng: number
  }
  formatted_address: string
  place_id: string
  components: {
    country: string
    state: string
    district: string
    village?: string
  }
}

export interface ReverseGeocodingResult {
  address: string
  formatted_address: string
  place_id: string
  components: {
    country: string
    state: string
    district: string
    village?: string
  }
}

class MapsApiService {
  private apiKey: string
  private baseUrl: string

  constructor() {
    this.apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'demo'
    this.baseUrl = 'https://maps.googleapis.com/maps/api'
    
    if (this.apiKey === 'demo') {
      console.warn('⚠️ Using demo maps data. Google Maps API key not found!')
    } else {
      console.log('✅ Real Google Maps API key detected. Fetching live geocoding data...')
    }
  }

  async geocodeAddress(address: string): Promise<GeocodingResult | null> {
    try {
      if (this.apiKey === 'demo') {
        return this.getMockGeocodingResult(address)
      }

      console.log('Geocoding address:', address)
      
      const response = await fetch(
        `${this.baseUrl}/geocode/json?address=${encodeURIComponent(address)}&key=${this.apiKey}`
      )

      if (!response.ok) {
        throw new Error(`Geocoding API error: ${response.status}`)
      }

      const data = await response.json()
      console.log('Real geocoding data received:', data)
      
      if (data.results && data.results.length > 0) {
        return this.transformGeocodingResult(data.results[0])
      }
      
      return null
    } catch (error) {
      console.warn('Real geocoding API failed, using mock data:', error)
      return this.getMockGeocodingResult(address)
    }
  }

  async reverseGeocode(lat: number, lng: number): Promise<ReverseGeocodingResult | null> {
    try {
      if (this.apiKey === 'demo') {
        return this.getMockReverseGeocodingResult(lat, lng)
      }

      console.log('Reverse geocoding coordinates:', { lat, lng })
      
      const response = await fetch(
        `${this.baseUrl}/geocode/json?latlng=${lat},${lng}&key=${this.apiKey}`
      )

      if (!response.ok) {
        throw new Error(`Reverse geocoding API error: ${response.status}`)
      }

      const data = await response.json()
      console.log('Real reverse geocoding data received:', data)
      
      if (data.results && data.results.length > 0) {
        return this.transformReverseGeocodingResult(data.results[0])
      }
      
      return null
    } catch (error) {
      console.warn('Real reverse geocoding API failed, using mock data:', error)
      return this.getMockReverseGeocodingResult(lat, lng)
    }
  }

  private transformGeocodingResult(result: any): GeocodingResult {
    const location = result.geometry.location
    const components = this.extractAddressComponents(result.address_components)
    
    return {
      address: result.formatted_address,
      coordinates: {
        lat: location.lat,
        lng: location.lng
      },
      formatted_address: result.formatted_address,
      place_id: result.place_id,
      components
    }
  }

  private transformReverseGeocodingResult(result: any): ReverseGeocodingResult {
    const components = this.extractAddressComponents(result.address_components)
    
    return {
      address: result.formatted_address,
      formatted_address: result.formatted_address,
      place_id: result.place_id,
      components
    }
  }

  private extractAddressComponents(components: any[]): any {
    const result: any = {}
    
    components.forEach(component => {
      const types = component.types
      if (types.includes('country')) {
        result.country = component.long_name
      } else if (types.includes('administrative_area_level_1')) {
        result.state = component.long_name
      } else if (types.includes('administrative_area_level_2')) {
        result.district = component.long_name
      } else if (types.includes('locality') || types.includes('sublocality')) {
        result.village = component.long_name
      }
    })
    
    return result
  }

  private getMockGeocodingResult(address: string): GeocodingResult {
    // Enhanced mock data based on common Indian locations
    const mockLocations = {
      'delhi': { lat: 28.7041, lng: 77.1025, state: 'Delhi', district: 'New Delhi' },
      'mumbai': { lat: 19.0760, lng: 72.8777, state: 'Maharashtra', district: 'Mumbai' },
      'bangalore': { lat: 12.9716, lng: 77.5946, state: 'Karnataka', district: 'Bangalore Urban' },
      'chennai': { lat: 13.0827, lng: 80.2707, state: 'Tamil Nadu', district: 'Chennai' },
      'kolkata': { lat: 22.5726, lng: 88.3639, state: 'West Bengal', district: 'Kolkata' },
      'hyderabad': { lat: 17.3850, lng: 78.4867, state: 'Telangana', district: 'Hyderabad' },
      'pune': { lat: 18.5204, lng: 73.8567, state: 'Maharashtra', district: 'Pune' },
      'ahmedabad': { lat: 23.0225, lng: 72.5714, state: 'Gujarat', district: 'Ahmedabad' },
      'noida': { lat: 28.5355, lng: 77.3910, state: 'Uttar Pradesh', district: 'Gautam Buddha Nagar' },
      'gurgaon': { lat: 28.4595, lng: 77.0266, state: 'Haryana', district: 'Gurugram' }
    }
    
    const lowerAddress = address.toLowerCase()
    let location = null
    
    for (const [key, value] of Object.entries(mockLocations)) {
      if (lowerAddress.includes(key)) {
        location = value
        break
      }
    }
    
    if (!location) {
      // Default to Delhi area
      location = { lat: 28.7041, lng: 77.1025, state: 'Uttar Pradesh', district: 'Gautam Buddha Nagar' }
    }
    
    return {
      address: address,
      coordinates: {
        lat: location.lat + (Math.random() - 0.5) * 0.01,
        lng: location.lng + (Math.random() - 0.5) * 0.01
      },
      formatted_address: `${address}, ${location.district}, ${location.state}, India`,
      place_id: `mock_place_${Date.now()}`,
      components: {
        country: 'India',
        state: location.state,
        district: location.district,
        village: 'Agricultural Area'
      }
    }
  }

  private getMockReverseGeocodingResult(lat: number, lng: number): ReverseGeocodingResult {
    // Determine approximate location based on coordinates
    let state = 'Uttar Pradesh'
    let district = 'Gautam Buddha Nagar'
    
    if (lat >= 19.0 && lat <= 19.3 && lng >= 72.7 && lng <= 73.0) {
      state = 'Maharashtra'
      district = 'Mumbai'
    } else if (lat >= 12.8 && lat <= 13.2 && lng >= 77.4 && lng <= 77.8) {
      state = 'Karnataka'
      district = 'Bangalore Urban'
    } else if (lat >= 13.0 && lat <= 13.2 && lng >= 80.2 && lng <= 80.3) {
      state = 'Tamil Nadu'
      district = 'Chennai'
    }
    
    return {
      address: `Agricultural Field, ${district}, ${state}, India`,
      formatted_address: `Agricultural Field, ${district}, ${state}, India`,
      place_id: `mock_reverse_${Date.now()}`,
      components: {
        country: 'India',
        state: state,
        district: district,
        village: 'Agricultural Area'
      }
    }
  }
}

export const mapsApi = new MapsApiService()
export default mapsApi
