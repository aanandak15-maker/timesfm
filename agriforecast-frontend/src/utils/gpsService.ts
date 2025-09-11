// GPS service for field location detection and mapping

interface GPSLocation {
  latitude: number
  longitude: number
  accuracy: number
  timestamp: number
}

interface FieldBoundary {
  id: string
  name: string
  coordinates: GPSLocation[]
  area: number // in acres
  center: GPSLocation
}

class GPSService {
  private watchId: number | null = null
  private currentLocation: GPSLocation | null = null
  private fieldBoundaries: FieldBoundary[] = []

  // Request location permission and get current position
  async getCurrentLocation(): Promise<GPSLocation> {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('GPS not supported'))
        return
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location: GPSLocation = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            timestamp: position.timestamp
          }
          this.currentLocation = location
          resolve(location)
        },
        (error) => {
          reject(new Error(`GPS error: ${error.message}`))
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 60000
        }
      )
    })
  }

  // Start watching location for field mapping
  startLocationWatch(callback: (location: GPSLocation) => void): void {
    if (!navigator.geolocation) {
      throw new Error('GPS not supported')
    }

    this.watchId = navigator.geolocation.watchPosition(
      (position) => {
        const location: GPSLocation = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
          timestamp: position.timestamp
        }
        this.currentLocation = location
        callback(location)
      },
      (error) => {
        console.error('GPS watch error:', error)
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 1000
      }
    )
  }

  // Stop watching location
  stopLocationWatch(): void {
    if (this.watchId) {
      navigator.geolocation.clearWatch(this.watchId)
      this.watchId = null
    }
  }

  // Calculate distance between two points (in meters)
  calculateDistance(loc1: GPSLocation, loc2: GPSLocation): number {
    const R = 6371e3 // Earth's radius in meters
    const φ1 = (loc1.latitude * Math.PI) / 180
    const φ2 = (loc2.latitude * Math.PI) / 180
    const Δφ = ((loc2.latitude - loc1.latitude) * Math.PI) / 180
    const Δλ = ((loc2.longitude - loc1.longitude) * Math.PI) / 180

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

    return R * c
  }

  // Calculate area of a polygon (in acres)
  calculateArea(coordinates: GPSLocation[]): number {
    if (coordinates.length < 3) return 0

    let area = 0
    const n = coordinates.length

    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n
      area += coordinates[i].longitude * coordinates[j].latitude
      area -= coordinates[j].longitude * coordinates[i].latitude
    }

    area = Math.abs(area) / 2
    // Convert from square degrees to acres (approximate)
    return area * 0.000247105
  }

  // Create field boundary
  createFieldBoundary(name: string, coordinates: GPSLocation[]): FieldBoundary {
    const area = this.calculateArea(coordinates)
    const center = this.calculateCenter(coordinates)
    
    const boundary: FieldBoundary = {
      id: `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name,
      coordinates,
      area,
      center
    }

    this.fieldBoundaries.push(boundary)
    this.saveFieldBoundaries()
    
    return boundary
  }

  // Calculate center point of coordinates
  private calculateCenter(coordinates: GPSLocation[]): GPSLocation {
    let lat = 0
    let lng = 0

    coordinates.forEach(coord => {
      lat += coord.latitude
      lng += coord.longitude
    })

    return {
      latitude: lat / coordinates.length,
      longitude: lng / coordinates.length,
      accuracy: 0,
      timestamp: Date.now()
    }
  }

  // Get all field boundaries
  getFieldBoundaries(): FieldBoundary[] {
    return this.fieldBoundaries
  }

  // Find field by location
  findFieldByLocation(location: GPSLocation): FieldBoundary | null {
    for (const field of this.fieldBoundaries) {
      const distance = this.calculateDistance(location, field.center)
      // If within 100 meters of field center, consider it the same field
      if (distance < 100) {
        return field
      }
    }
    return null
  }

  // Save field boundaries to localStorage
  private saveFieldBoundaries(): void {
    localStorage.setItem('agriforecast-field-boundaries', JSON.stringify(this.fieldBoundaries))
  }

  // Load field boundaries from localStorage
  loadFieldBoundaries(): void {
    const saved = localStorage.getItem('agriforecast-field-boundaries')
    if (saved) {
      this.fieldBoundaries = JSON.parse(saved)
    }
  }

  // Get current location if available
  getCurrentLocationSync(): GPSLocation | null {
    return this.currentLocation
  }

  // Check if GPS is available
  isGPSAvailable(): boolean {
    return 'geolocation' in navigator
  }

  // Get location permission status
  async getPermissionStatus(): Promise<PermissionState> {
    if ('permissions' in navigator) {
      try {
        const permission = await navigator.permissions.query({ name: 'geolocation' as PermissionName })
        return permission.state
      } catch (error) {
        return 'prompt'
      }
    }
    return 'prompt'
  }

  // Request location permission
  async requestPermission(): Promise<boolean> {
    try {
      await this.getCurrentLocation()
      return true
    } catch (error) {
      return false
    }
  }
}

export const gpsService = new GPSService()
export default gpsService
