import { useQuery } from '@tanstack/react-query'
import { weatherApi } from '../services/weatherApi'
import { useErrorHandler } from './useErrorHandler'
import { useState, useEffect } from 'react'

interface LocationWeatherOptions {
  fieldId?: string
  fallbackLat?: number
  fallbackLon?: number
  refetchInterval?: number
}

export const useLocationWeather = (options: LocationWeatherOptions = {}) => {
  const { fieldId, fallbackLat = 28.368911, fallbackLon = 77.541033, refetchInterval = 5 * 60 * 1000 } = options
  const { handleError } = useErrorHandler()
  const [currentLocation, setCurrentLocation] = useState<{ lat: number; lon: number } | null>(null)
  const [isLocationLoading, setIsLocationLoading] = useState(false)

  // Get current GPS location
  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      console.warn('Geolocation not supported, using fallback coordinates')
      setCurrentLocation({ lat: fallbackLat, lon: fallbackLon })
      return
    }

    console.log('Requesting GPS location...')
    setIsLocationLoading(true)
    
    // Try high accuracy first
    navigator.geolocation.getCurrentPosition(
      (position) => {
        console.log('GPS Success (High Accuracy):', {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
          timestamp: position.timestamp
        })
        console.log('GPS Coordinates:', `Lat: ${position.coords.latitude}, Lon: ${position.coords.longitude}`)
        const newLocation = {
          lat: position.coords.latitude,
          lon: position.coords.longitude
        }
        console.log('Setting current location to:', newLocation)
        console.log('Location set:', `Lat: ${newLocation.lat}, Lon: ${newLocation.lon}`)
        setCurrentLocation(newLocation)
        setIsLocationLoading(false)
      },
      (error) => {
        console.warn('High accuracy GPS failed, trying low accuracy:', error.message)
        
        // Try low accuracy as fallback
        navigator.geolocation.getCurrentPosition(
          (position) => {
            console.log('GPS Success (Low Accuracy):', {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
              accuracy: position.coords.accuracy,
              timestamp: position.timestamp
            })
            console.log('GPS Coordinates:', `Lat: ${position.coords.latitude}, Lon: ${position.coords.longitude}`)
            const newLocation = {
              lat: position.coords.latitude,
              lon: position.coords.longitude
            }
            console.log('Setting current location to:', newLocation)
            console.log('Location set:', `Lat: ${newLocation.lat}, Lon: ${newLocation.lon}`)
            setCurrentLocation(newLocation)
            setIsLocationLoading(false)
          },
          (fallbackError) => {
            console.error('All GPS attempts failed:', fallbackError.message)
            console.warn('Using fallback coordinates:', fallbackLat, fallbackLon)
            setCurrentLocation({ lat: fallbackLat, lon: fallbackLon })
            setIsLocationLoading(false)
          },
          {
            enableHighAccuracy: false,
            timeout: 15000,
            maximumAge: 600000 // 10 minutes
          }
        )
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 300000 // 5 minutes
      }
    )
  }

  // Get field coordinates from API (if fieldId provided)
  const getFieldLocation = async () => {
    try {
      // This would fetch field coordinates from your API
      // For now, return fallback coordinates
      return { lat: fallbackLat, lon: fallbackLon }
    } catch (error) {
      console.warn('Failed to fetch field location, using fallback:', error)
      return { lat: fallbackLat, lon: fallbackLon }
    }
  }

  // Initialize location
  useEffect(() => {
    if (fieldId) {
      getFieldLocation().then(setCurrentLocation)
    } else {
      getCurrentLocation()
    }
  }, [fieldId])

  // Weather query
  const weatherQuery = useQuery({
    queryKey: ['weather', currentLocation?.lat, currentLocation?.lon, fieldId],
    queryFn: () => {
      if (!currentLocation) {
        throw new Error('Location not available')
      }
      console.log('Fetching weather for location:', currentLocation)
      console.log('Weather coordinates:', `Lat: ${currentLocation.lat}, Lon: ${currentLocation.lon}`)
      return weatherApi.getWeatherForecast(currentLocation.lat, currentLocation.lon)
    },
    enabled: !!currentLocation,
    refetchInterval,
    retry: 1
  })

  // Handle errors
  if (weatherQuery.error) {
    handleError(weatherQuery.error, { showToast: false })
  }

  return {
    ...weatherQuery,
    currentLocation,
    isLocationLoading,
    refreshLocation: getCurrentLocation,
    isLocationAvailable: !!currentLocation
  }
}
