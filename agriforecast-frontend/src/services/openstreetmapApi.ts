// OpenStreetMap API service - NO API KEY REQUIRED!
// Free global mapping and geocoding data

export interface OSMLocationData {
  address: string
  formatted_address: string
  coordinates: {
    lat: number
    lng: number
  }
  components: {
    country: string
    state: string
    district: string
    village?: string
    postcode?: string
  }
  place_id: string
  source: string
}

export interface OSMReverseGeocoding {
  address: string
  display_name: string
  lat: string
  lon: string
  address_components: any
}

class OpenStreetMapApiService {
  private baseUrl = 'https://nominatim.openstreetmap.org'

  constructor() {
    console.log('🗺️ OpenStreetMap API Service initialized - NO API KEY REQUIRED!')
  }

  // Geocoding - Convert address to coordinates
  async geocodeAddress(address: string): Promise<OSMLocationData | null> {
    try {
      console.log(`🗺️ Geocoding address with OpenStreetMap (FREE): ${address}`)
      
      const response = await fetch(
        `${this.baseUrl}/search?format=json&q=${encodeURIComponent(address)}&limit=1&addressdetails=1`,
        {
          headers: {
            'User-Agent': 'AgriForecast/1.0 (farming@agriforecast.ai)' // Required by OSM
          }
        }
      )

      if (!response.ok) {
        throw new Error(`OpenStreetMap geocoding error: ${response.status}`)
      }

      const data = await response.json()
      console.log('✅ OpenStreetMap geocoding data received:', data)
      
      if (data && data.length > 0) {
        return this.transformGeocodingData(data[0])
      }
      
      return null
    } catch (error) {
      console.warn('OpenStreetMap geocoding failed, using demo data:', error)
      return this.getDemoGeocodingData(address)
    }
  }

  // Reverse Geocoding - Convert coordinates to address
  async reverseGeocode(lat: number, lng: number): Promise<OSMLocationData | null> {
    try {
      console.log(`🗺️ Reverse geocoding with OpenStreetMap (FREE): ${lat}, ${lng}`)
      
      const response = await fetch(
        `${this.baseUrl}/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`,
        {
          headers: {
            'User-Agent': 'AgriForecast/1.0 (farming@agriforecast.ai)' // Required by OSM
          }
        }
      )

      if (!response.ok) {
        throw new Error(`OpenStreetMap reverse geocoding error: ${response.status}`)
      }

      const data = await response.json()
      console.log('✅ OpenStreetMap reverse geocoding data received:', data)
      
      return this.transformReverseGeocodingData(data)
    } catch (error) {
      console.warn('OpenStreetMap reverse geocoding failed, using demo data:', error)
      return this.getDemoReverseGeocodingData(lat, lng)
    }
  }

  // Search for places
  async searchPlaces(query: string, lat?: number, lng?: number): Promise<OSMLocationData[]> {
    try {
      console.log(`🗺️ Searching places with OpenStreetMap (FREE): ${query}`)
      
      let url = `${this.baseUrl}/search?format=json&q=${encodeURIComponent(query)}&limit=5&addressdetails=1`
      
      // Add viewbox for location-based search if coordinates provided
      if (lat && lng) {
        const bbox = this.createBoundingBox(lat, lng, 0.1) // 0.1 degree radius
        url += `&viewbox=${bbox}&bounded=1`
      }
      
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'AgriForecast/1.0 (farming@agriforecast.ai)' // Required by OSM
        }
      })

      if (!response.ok) {
        throw new Error(`OpenStreetMap search error: ${response.status}`)
      }

      const data = await response.json()
      console.log('✅ OpenStreetMap search data received:', data)
      
      return data.map((item: any) => this.transformGeocodingData(item))
    } catch (error) {
      console.warn('OpenStreetMap search failed, using demo data:', error)
      return this.getDemoSearchData(query)
    }
  }

  private transformGeocodingData(data: any): OSMLocationData {
    const address = data.address || {}
    
    return {
      address: data.display_name,
      formatted_address: data.display_name,
      coordinates: {
        lat: parseFloat(data.lat),
        lng: parseFloat(data.lon)
      },
      components: {
        country: address.country || 'Unknown',
        state: address.state || address.region || 'Unknown',
        district: address.county || address.district || 'Unknown',
        village: address.village || address.town || address.city,
        postcode: address.postcode
      },
      place_id: data.place_id?.toString() || `osm_${Date.now()}`,
      source: 'OpenStreetMap (FREE)'
    }
  }

  private transformReverseGeocodingData(data: any): OSMLocationData {
    return this.transformGeocodingData(data)
  }

  private createBoundingBox(lat: number, lng: number, radius: number): string {
    const left = lng - radius
    const bottom = lat - radius
    const right = lng + radius
    const top = lat + radius
    return `${left},${bottom},${right},${top}`
  }

  private getDemoGeocodingData(address: string): OSMLocationData {
    // Generate realistic demo data based on address
    const addressLower = address.toLowerCase()
    let coordinates = { lat: 28.3477, lng: 77.5573 } // Default to your location
    let state = 'Uttar Pradesh'
    let district = 'Gautam Buddha Nagar'
    
    // Basic location detection
    if (addressLower.includes('mumbai')) {
      coordinates = { lat: 19.0760, lng: 72.8777 }
      state = 'Maharashtra'
      district = 'Mumbai'
    } else if (addressLower.includes('delhi')) {
      coordinates = { lat: 28.7041, lng: 77.1025 }
      state = 'Delhi'
      district = 'New Delhi'
    } else if (addressLower.includes('bangalore')) {
      coordinates = { lat: 12.9716, lng: 77.5946 }
      state = 'Karnataka'
      district = 'Bangalore Urban'
    }
    
    return {
      address: address,
      formatted_address: `${address}, ${district}, ${state}, India`,
      coordinates,
      components: {
        country: 'India',
        state,
        district,
        village: 'Agricultural Area'
      },
      place_id: `demo_${Date.now()}`,
      source: 'Demo Data (OpenStreetMap unavailable)'
    }
  }

  private getDemoReverseGeocodingData(lat: number, lng: number): OSMLocationData {
    // Determine location based on coordinates
    let state = 'Uttar Pradesh'
    let district = 'Gautam Buddha Nagar'
    
    if (lat >= 19.0 && lat <= 19.3 && lng >= 72.7 && lng <= 73.0) {
      state = 'Maharashtra'
      district = 'Mumbai'
    } else if (lat >= 28.6 && lat <= 28.8 && lng >= 77.0 && lng <= 77.3) {
      state = 'Delhi'
      district = 'New Delhi'
    } else if (lat >= 12.8 && lat <= 13.2 && lng >= 77.4 && lng <= 77.8) {
      state = 'Karnataka'
      district = 'Bangalore Urban'
    }
    
    return {
      address: `Agricultural Field, ${lat.toFixed(4)}, ${lng.toFixed(4)}`,
      formatted_address: `Agricultural Field, ${district}, ${state}, India`,
      coordinates: { lat, lng },
      components: {
        country: 'India',
        state,
        district,
        village: 'Agricultural Area'
      },
      place_id: `demo_reverse_${Date.now()}`,
      source: 'Demo Data (OpenStreetMap unavailable)'
    }
  }

  private getDemoSearchData(query: string): OSMLocationData[] {
    return [
      this.getDemoGeocodingData(query),
      this.getDemoGeocodingData(`${query} Village`),
      this.getDemoGeocodingData(`${query} District`)
    ]
  }
}

export const openstreetmapApi = new OpenStreetMapApiService()
export default openstreetmapApi
