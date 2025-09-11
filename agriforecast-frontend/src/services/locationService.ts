// Location validation and utility service
export interface LocationValidation {
  isValid: boolean
  errors: string[]
  warnings: string[]
}

export interface LocationInfo {
  latitude: number
  longitude: number
  address?: string
  country?: string
  state?: string
  city?: string
  accuracy?: number
}

export class LocationService {
  // Validate coordinates
  static validateCoordinates(latitude: number, longitude: number): LocationValidation {
    const errors: string[] = []
    const warnings: string[] = []

    // Check latitude range
    if (latitude < -90 || latitude > 90) {
      errors.push('Latitude must be between -90 and 90 degrees')
    }

    // Check longitude range
    if (longitude < -180 || longitude > 180) {
      errors.push('Longitude must be between -180 and 180 degrees')
    }

    // Check for zero coordinates (might be default/empty)
    if (latitude === 0 && longitude === 0) {
      warnings.push('Coordinates appear to be default values (0, 0)')
    }

    // Check for very precise coordinates (might be test data)
    if (Math.abs(latitude - 28.368911) < 0.001 && Math.abs(longitude - 77.541033) < 0.001) {
      warnings.push('Coordinates match default test location')
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    }
  }

  // Get current location using GPS
  static async getCurrentLocation(): Promise<LocationInfo> {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported by this browser'))
        return
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy
          })
        },
        (error) => {
          reject(new Error(`Location error: ${error.message}`))
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000
        }
      )
    })
  }

  // Geocode address to coordinates
  static async geocodeAddress(address: string): Promise<LocationInfo> {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1&addressdetails=1`
      )
      const data = await response.json()

      if (data && data.length > 0) {
        const result = data[0]
        return {
          latitude: parseFloat(result.lat),
          longitude: parseFloat(result.lon),
          address: result.display_name,
          country: result.address?.country,
          state: result.address?.state,
          city: result.address?.city || result.address?.town || result.address?.village
        }
      } else {
        throw new Error('Address not found')
      }
    } catch (error) {
      throw new Error(`Geocoding failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  // Reverse geocode coordinates to address
  static async reverseGeocode(latitude: number, longitude: number): Promise<LocationInfo> {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&addressdetails=1`
      )
      const data = await response.json()

      if (data && data.display_name) {
        return {
          latitude,
          longitude,
          address: data.display_name,
          country: data.address?.country,
          state: data.address?.state,
          city: data.address?.city || data.address?.town || data.address?.village
        }
      } else {
        throw new Error('Reverse geocoding failed')
      }
    } catch (error) {
      throw new Error(`Reverse geocoding failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  // Calculate distance between two points (in kilometers)
  static calculateDistance(lat1: number, lng1: number, lat2: number, lng2: number): number {
    const R = 6371 // Earth's radius in kilometers
    const dLat = this.toRadians(lat2 - lat1)
    const dLng = this.toRadians(lng2 - lng1)
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) *
      Math.sin(dLng / 2) * Math.sin(dLng / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    return R * c
  }

  // Convert degrees to radians
  private static toRadians(degrees: number): number {
    return degrees * (Math.PI / 180)
  }

  // Get agricultural regions in India
  static getAgriculturalRegions() {
    return [
      { name: 'Punjab', lat: 30.7333, lng: 76.7794, crops: ['Wheat', 'Rice', 'Cotton'] },
      { name: 'Haryana', lat: 29.0588, lng: 76.0856, crops: ['Wheat', 'Rice', 'Sugarcane'] },
      { name: 'Uttar Pradesh', lat: 26.8467, lng: 80.9462, crops: ['Wheat', 'Rice', 'Sugarcane'] },
      { name: 'Maharashtra', lat: 19.7515, lng: 75.7139, crops: ['Cotton', 'Sugarcane', 'Soybean'] },
      { name: 'Karnataka', lat: 15.3173, lng: 75.7139, crops: ['Rice', 'Ragi', 'Jowar'] },
      { name: 'Tamil Nadu', lat: 11.1271, lng: 78.6569, crops: ['Rice', 'Sugarcane', 'Cotton'] },
      { name: 'Andhra Pradesh', lat: 15.9129, lng: 79.7400, crops: ['Rice', 'Cotton', 'Chillies'] },
      { name: 'Gujarat', lat: 23.0225, lng: 72.5714, crops: ['Cotton', 'Groundnut', 'Wheat'] },
      { name: 'Rajasthan', lat: 27.0238, lng: 74.2179, crops: ['Wheat', 'Barley', 'Mustard'] },
      { name: 'Madhya Pradesh', lat: 22.9734, lng: 78.6569, crops: ['Wheat', 'Soybean', 'Rice'] }
    ]
  }

  // Check if location is in India
  static isInIndia(latitude: number, longitude: number): boolean {
    // Rough bounding box for India
    return latitude >= 6.0 && latitude <= 37.0 && longitude >= 68.0 && longitude <= 97.0
  }

  // Get recommended crops for location
  static getRecommendedCrops(latitude: number, longitude: number): string[] {
    const regions = this.getAgriculturalRegions()
    const distances = regions.map(region => ({
      ...region,
      distance: this.calculateDistance(latitude, longitude, region.lat, region.lng)
    }))
    
    const closestRegion = distances.reduce((min, current) => 
      current.distance < min.distance ? current : min
    )
    
    return closestRegion.distance < 200 ? closestRegion.crops : ['Rice', 'Wheat', 'Maize']
  }
}
