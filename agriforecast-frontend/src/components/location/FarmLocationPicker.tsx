import React, { useState } from 'react'
import {
  Box,
  Button,
  VStack,
  HStack,
  Text as ChakraText,
  Input,
  FormControl,
  FormLabel,
  Select,
  useColorModeValue,
  Badge,
  Icon,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react'
import { MapPin, Search, Navigation, CheckCircle } from 'lucide-react'
import { LocationService } from '../../services/locationService'

interface FarmLocationPickerProps {
  location: string
  onLocationChange: (location: string) => void
  disabled?: boolean
}

const FarmLocationPicker: React.FC<FarmLocationPickerProps> = ({
  location,
  onLocationChange,
  disabled = false
}) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [searchError, setSearchError] = useState('')
  const [selectedRegion, setSelectedRegion] = useState('')

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  const agriculturalRegions = LocationService.getAgriculturalRegions()

  // Handle region selection
  const handleRegionSelect = (regionName: string) => {
    setSelectedRegion(regionName)
    onLocationChange(regionName)
    setSearchError('')
  }

  // Handle custom location search
  const handleLocationSearch = async () => {
    if (!searchQuery.trim()) {
      setSearchError('Please enter a location')
      return
    }

    setIsSearching(true)
    setSearchError('')

    try {
      // Validate the location by geocoding
      const locationInfo = await LocationService.geocodeAddress(searchQuery)
      
      // Check if location is in India
      if (LocationService.isInIndia(locationInfo.latitude, locationInfo.longitude)) {
        onLocationChange(locationInfo.address || searchQuery)
        setSearchError('')
      } else {
        setSearchError('Location is outside India. Please select an Indian location.')
      }
    } catch (error) {
      setSearchError(`Location not found: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsSearching(false)
    }
  }

  // Get current location
  const getCurrentLocation = async () => {
    setIsSearching(true)
    setSearchError('')

    try {
      const locationInfo = await LocationService.getCurrentLocation()
      
      if (LocationService.isInIndia(locationInfo.latitude, locationInfo.longitude)) {
        // Reverse geocode to get address
        const addressInfo = await LocationService.reverseGeocode(locationInfo.latitude, locationInfo.longitude)
        onLocationChange(addressInfo.address || 'Current Location')
        setSearchError('')
      } else {
        setSearchError('Current location is outside India. Please select an Indian location.')
      }
    } catch (error) {
      setSearchError(`Failed to get location: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <Box>
      <VStack spacing={4} align="stretch">
        {/* Current Location Display */}
        <Box p={4} bg={bg} borderRadius="lg" border="1px" borderColor={borderColor}>
          <HStack justify="space-between" mb={2}>
            <ChakraText fontWeight="semibold" color="gray.700">
              Farm Location
            </ChakraText>
            <Badge colorScheme="blue" variant="subtle">
              {location || 'Not Set'}
            </Badge>
          </HStack>
          
          {location && (
            <HStack>
              <Icon as={MapPin} size={16} color="gray.500" />
              <ChakraText fontSize="sm" color="gray.600">
                {location}
              </ChakraText>
            </HStack>
          )}
        </Box>

        {/* Location Input Methods */}
        <VStack spacing={3} align="stretch">
          {/* Custom Location Search */}
          <FormControl>
            <FormLabel>Search Custom Location</FormLabel>
            <HStack>
              <Input
                placeholder="Enter city, state, or address"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleLocationSearch()}
                disabled={disabled || isSearching}
              />
              <Button
                onClick={handleLocationSearch}
                isLoading={isSearching}
                loadingText="Searching..."
                leftIcon={<Search size={16} />}
                colorScheme="blue"
                disabled={disabled}
              >
                Search
              </Button>
            </HStack>
          </FormControl>

          {/* GPS Location */}
          <Button
            leftIcon={<Navigation size={16} />}
            onClick={getCurrentLocation}
            isLoading={isSearching}
            loadingText="Getting Location..."
            size="sm"
            colorScheme="green"
            variant="outline"
            disabled={disabled}
          >
            Use Current Location
          </Button>

          {/* Predefined Agricultural Regions */}
          <FormControl>
            <FormLabel>Select Agricultural Region</FormLabel>
            <Select
              placeholder="Choose from major agricultural regions"
              value={selectedRegion}
              onChange={(e) => handleRegionSelect(e.target.value)}
              disabled={disabled}
            >
              {agriculturalRegions.map((region, index) => (
                <option key={index} value={region.name}>
                  {region.name} - {region.crops.join(', ')}
                </option>
              ))}
            </Select>
          </FormControl>
        </VStack>

        {/* Error Display */}
        {searchError && (
          <Alert status="error" borderRadius="md">
            <AlertIcon />
            <AlertTitle>Location Error:</AlertTitle>
            <AlertDescription>{searchError}</AlertDescription>
          </Alert>
        )}

        {/* Agricultural Regions Info */}
        <Box p={3} bg="blue.50" borderRadius="md" border="1px" borderColor="blue.200">
          <HStack mb={2}>
            <Icon as={CheckCircle} size={16} color="blue.600" />
            <ChakraText fontSize="sm" fontWeight="semibold" color="blue.700">
              Agricultural Regions
            </ChakraText>
          </HStack>
          <ChakraText fontSize="xs" color="blue.600">
            Select from major agricultural regions in India for better crop recommendations and weather data accuracy.
          </ChakraText>
        </Box>
      </VStack>
    </Box>
  )
}

export default FarmLocationPicker
