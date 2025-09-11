import React, { useState, useEffect } from 'react'
import {
  Box,
  Button,
  VStack,
  HStack,
  Text as ChakraText,
  Input,
  FormControl,
  FormLabel,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Badge,
  Icon,
  useColorModeValue,
} from '@chakra-ui/react'
import { MapPin, Navigation, Search } from 'lucide-react'

interface LocationPickerProps {
  latitude: number
  longitude: number
  onLocationChange: (lat: number, lng: number, address?: string) => void
  disabled?: boolean
}

const LocationPicker: React.FC<LocationPickerProps> = ({
  latitude,
  longitude,
  onLocationChange,
  disabled = false
}) => {
  const { isOpen, onOpen, onClose } = useDisclosure()
  const [address, setAddress] = useState('')
  const [isValidLocation, setIsValidLocation] = useState(false)
  const [locationError, setLocationError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  // Validate coordinates
  useEffect(() => {
    const isValid = latitude >= -90 && latitude <= 90 && longitude >= -180 && longitude <= 180
    setIsValidLocation(isValid)
  }, [latitude, longitude])

  // Get current location using GPS
  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      setLocationError('Geolocation is not supported by this browser')
      return
    }

    setIsLoading(true)
    setLocationError('')

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        onLocationChange(lat, lng)
        setIsLoading(false)
      },
      (error) => {
        setLocationError(`Location error: ${error.message}`)
        setIsLoading(false)
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000
      }
    )
  }

  // Geocode address to coordinates
  const geocodeAddress = async () => {
    if (!address.trim()) {
      setLocationError('Please enter an address')
      return
    }

    setIsLoading(true)
    setLocationError('')

    try {
      // Using a free geocoding service (you can replace with Google Maps API)
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1`
      )
      const data = await response.json()

      if (data && data.length > 0) {
        const result = data[0]
        const lat = parseFloat(result.lat)
        const lng = parseFloat(result.lon)
        onLocationChange(lat, lng, result.display_name)
        setAddress(result.display_name)
      } else {
        setLocationError('Address not found. Please try a different address.')
      }
    } catch (error) {
      setLocationError('Failed to geocode address. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  // Reverse geocode coordinates to address
  const reverseGeocode = async (lat: number, lng: number) => {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
      )
      const data = await response.json()
      if (data && data.display_name) {
        setAddress(data.display_name)
      }
    } catch (error) {
      console.error('Reverse geocoding failed:', error)
    }
  }

  // Initialize address when coordinates change
  useEffect(() => {
    if (isValidLocation) {
      reverseGeocode(latitude, longitude)
    }
  }, [latitude, longitude, isValidLocation])

  return (
    <Box>
      <VStack spacing={4} align="stretch">
        {/* Current Location Display */}
        <Box p={4} bg={bg} borderRadius="lg" border="1px" borderColor={borderColor}>
          <HStack justify="space-between" mb={2}>
            <ChakraText fontWeight="semibold" color="gray.700">
              Field Location
            </ChakraText>
            <Badge colorScheme={isValidLocation ? 'green' : 'red'} variant="subtle">
              {isValidLocation ? 'Valid' : 'Invalid'}
            </Badge>
          </HStack>
          
          <VStack spacing={2} align="stretch">
            <HStack>
              <Icon as={MapPin} size={16} color="gray.500" />
              <ChakraText fontSize="sm" color="gray.600">
                Lat: {latitude.toFixed(6)}, Lng: {longitude.toFixed(6)}
              </ChakraText>
            </HStack>
            
            {address && (
              <HStack>
                <Icon as={Navigation} size={16} color="gray.500" />
                <ChakraText fontSize="sm" color="gray.600" noOfLines={2}>
                  {address}
                </ChakraText>
              </HStack>
            )}
          </VStack>
        </Box>

        {/* Location Input Methods */}
        <HStack spacing={2}>
          <Button
            leftIcon={<Navigation size={16} />}
            onClick={getCurrentLocation}
            isLoading={isLoading}
            loadingText="Getting Location..."
            size="sm"
            colorScheme="blue"
            variant="outline"
            disabled={disabled}
          >
            Use GPS
          </Button>
          
          <Button
            leftIcon={<Search size={16} />}
            onClick={onOpen}
            size="sm"
            colorScheme="green"
            variant="outline"
            disabled={disabled}
          >
            Search Address
          </Button>
        </HStack>

        {/* Error Display */}
        {locationError && (
          <Alert status="error" borderRadius="md">
            <AlertIcon />
            <AlertTitle>Location Error:</AlertTitle>
            <AlertDescription>{locationError}</AlertDescription>
          </Alert>
        )}

        {/* Address Search Modal */}
        <Modal isOpen={isOpen} onClose={onClose} size="lg">
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Search Address</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <VStack spacing={4}>
                <FormControl>
                  <FormLabel>Enter Address</FormLabel>
                  <Input
                    placeholder="e.g., 123 Main St, City, State, Country"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && geocodeAddress()}
                  />
                </FormControl>
                
                <HStack spacing={2}>
                  <Button
                    onClick={geocodeAddress}
                    isLoading={isLoading}
                    loadingText="Searching..."
                    colorScheme="blue"
                    leftIcon={<Search size={16} />}
                  >
                    Search
                  </Button>
                  <Button onClick={onClose} variant="outline">
                    Cancel
                  </Button>
                </HStack>

                {/* Popular Locations */}
                <Box w="full">
                  <ChakraText fontSize="sm" fontWeight="semibold" mb={2} color="gray.600">
                    Popular Agricultural Locations:
                  </ChakraText>
                  <VStack spacing={1} align="stretch">
                    {[
                      { name: 'Punjab, India', lat: 30.7333, lng: 76.7794 },
                      { name: 'Haryana, India', lat: 29.0588, lng: 76.0856 },
                      { name: 'Uttar Pradesh, India', lat: 26.8467, lng: 80.9462 },
                      { name: 'Maharashtra, India', lat: 19.7515, lng: 75.7139 },
                      { name: 'Karnataka, India', lat: 15.3173, lng: 75.7139 }
                    ].map((location, index) => (
                      <Button
                        key={index}
                        size="sm"
                        variant="ghost"
                        justifyContent="flex-start"
                        onClick={() => {
                          onLocationChange(location.lat, location.lng, location.name)
                          setAddress(location.name)
                          onClose()
                        }}
                      >
                        <Icon as={MapPin} size={14} mr={2} />
                        {location.name}
                      </Button>
                    ))}
                  </VStack>
                </Box>
              </VStack>
            </ModalBody>
          </ModalContent>
        </Modal>
      </VStack>
    </Box>
  )
}

export default LocationPicker
