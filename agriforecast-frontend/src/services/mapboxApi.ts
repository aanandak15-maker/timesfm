// Mapbox API service - Optional mapping service
// Only use if you need advanced mapping features

export interface MapboxLocationData {
  address: string
  coordinates: {
    lat: number
    lng: number
  }
  place_name: string
  context: Array<{
    id: string
    text: string
    wikidata?: string
  }>
  source: string
}

export interface MapboxGeocodingResult {
  features: Array<{
    place_name: string
    center: [number, number]
    context: Array<{
      id: string
      text: string
      wikidata?: string
    }>
  }>
}

class MapboxApiService {
  private apiKey: string
  private baseUrl = 'https://api.mapbox.com'

  constructor() {
    this.apiKey = import.meta.env.VITE_MAPBOX_API_KEY || 'pk.eyJ1IjoiYW5hbmQyODQyIiwiYSI6ImNtZmIxaDB2cjFrcGIybHFzb2N5eDc0c2MifQ.HiMPiOCSPvZnXTbEQtMj0g'
    
    if (this.apiKey === 'demo') {
      console.warn('⚠️ Using demo mapping data. Mapbox API key not found!')
    } else {
      console.log('🗺️ Mapbox API service initialized with your token')
    }
  }

  // Geocoding - Convert address to coordinates
  async geocodeAddress(address: string): Promise<MapboxLocationData | null> {
    try {
      console.log(`🗺️ Geocoding address with Mapbox: ${address}`)
      
      const response = await fetch(
        `${this.baseUrl}/geocoding/v5/mapbox.places/${encodeURIComponent(address)}.json?access_token=${this.apiKey}&limit=1&country=IN`
      )

      if (!response.ok) {
        throw new Error(`Mapbox geocoding error: ${response.status}`)
      }

      const data: MapboxGeocodingResult = await response.json()
      console.log('✅ Mapbox geocoding data received:', data)
      
      if (data.features && data.features.length > 0) {
        const feature = data.features[0]
        return {
          address: address,
          coordinates: {
            lat: feature.center[1],
            lng: feature.center[0]
          },
          place_name: feature.place_name,
          context: feature.context || [],
          source: 'Mapbox'
        }
      }
      
      return null
    } catch (error) {
      console.warn('Mapbox geocoding failed, using OpenStreetMap fallback:', error)
      // Fallback to OpenStreetMap
      const { openstreetmapApi } = await import('./openstreetmapApi')
      return await openstreetmapApi.geocodeAddress(address)
    }
  }

  // Reverse Geocoding - Convert coordinates to address
  async reverseGeocode(lat: number, lng: number): Promise<MapboxLocationData | null> {
    try {
      console.log(`🗺️ Reverse geocoding with Mapbox: ${lat}, ${lng}`)
      
      const response = await fetch(
        `${this.baseUrl}/geocoding/v5/mapbox.places/${lng},${lat}.json?access_token=${this.apiKey}&limit=1`
      )

      if (!response.ok) {
        throw new Error(`Mapbox reverse geocoding error: ${response.status}`)
      }

      const data: MapboxGeocodingResult = await response.json()
      console.log('✅ Mapbox reverse geocoding data received:', data)
      
      if (data.features && data.features.length > 0) {
        const feature = data.features[0]
        return {
          address: feature.place_name,
          coordinates: { lat, lng },
          place_name: feature.place_name,
          context: feature.context || [],
          source: 'Mapbox'
        }
      }
      
      return null
    } catch (error) {
      console.warn('Mapbox reverse geocoding failed, using OpenStreetMap fallback:', error)
      // Fallback to OpenStreetMap
      const { openstreetmapApi } = await import('./openstreetmapApi')
      return await openstreetmapApi.reverseGeocode(lat, lng)
    }
  }

  // Search for places
  async searchPlaces(query: string, lat?: number, lng?: number): Promise<MapboxLocationData[]> {
    try {
      console.log(`🗺️ Searching places with Mapbox: ${query}`)
      
      let url = `${this.baseUrl}/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${this.apiKey}&limit=5&country=IN`
      
      // Add proximity for location-based search if coordinates provided
      if (lat && lng) {
        url += `&proximity=${lng},${lat}`
      }
      
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`Mapbox search error: ${response.status}`)
      }

      const data: MapboxGeocodingResult = await response.json()
      console.log('✅ Mapbox search data received:', data)
      
      return data.features.map(feature => ({
        address: feature.place_name,
        coordinates: {
          lat: feature.center[1],
          lng: feature.center[0]
        },
        place_name: feature.place_name,
        context: feature.context || [],
        source: 'Mapbox'
      }))
    } catch (error) {
      console.warn('Mapbox search failed, using OpenStreetMap fallback:', error)
      // Fallback to OpenStreetMap
      const { openstreetmapApi } = await import('./openstreetmapApi')
      return await openstreetmapApi.searchPlaces(query, lat, lng)
    }
  }

  // Get map style URL for Mapbox GL JS
  getMapStyleUrl(style: 'streets' | 'satellite' | 'hybrid' = 'streets'): string {
    const styleMap = {
      streets: 'mapbox://styles/mapbox/streets-v12',
      satellite: 'mapbox://styles/mapbox/satellite-v9',
      hybrid: 'mapbox://styles/mapbox/satellite-streets-v12'
    }
    
    return `${styleMap[style]}?access_token=${this.apiKey}`
  }

  // Get map tile URL for custom implementations
  getTileUrl(layer: 'streets' | 'satellite' | 'terrain' = 'streets'): string {
    const layerMap = {
      streets: 'mapbox/streets-v12',
      satellite: 'mapbox/satellite-v9',
      terrain: 'mapbox/outdoors-v12'
    }
    
    return `https://api.mapbox.com/styles/v1/${layerMap[layer]}/tiles/{z}/{x}/{y}?access_token=${this.apiKey}`
  }
}

export const mapboxApi = new MapboxApiService()
export default mapboxApi
