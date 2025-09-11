import { useState } from 'react'
import {
  Box,
  Button,
  VStack,
  HStack,
  Text as ChakraText,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Code,
  Badge,
  useColorModeValue,
} from '@chakra-ui/react'
import { Navigation, MapPin, CheckCircle } from 'lucide-react'

const GPSDebugger = () => {
  const [location, setLocation] = useState<{ lat: number; lon: number } | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [debugInfo, setDebugInfo] = useState<any>(null)

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  const testGPS = () => {
    setError(null)
    setDebugInfo(null)
    setIsLoading(true)

    // Check if geolocation is supported
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by this browser')
      setIsLoading(false)
      return
    }

    console.log('Testing GPS location...')
    setDebugInfo({
      geolocationSupported: true,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      protocol: window.location.protocol,
      hostname: window.location.hostname
    })

    navigator.geolocation.getCurrentPosition(
      (position) => {
        console.log('GPS Success:', position)
        console.log('GPS Debugger Coordinates:', `Lat: ${position.coords.latitude}, Lon: ${position.coords.longitude}`)
        setLocation({
          lat: position.coords.latitude,
          lon: position.coords.longitude
        })
        setDebugInfo((prev: any) => ({
          ...prev,
          success: true,
          accuracy: position.coords.accuracy,
          altitude: position.coords.altitude,
          altitudeAccuracy: position.coords.altitudeAccuracy,
          heading: position.coords.heading,
          speed: position.coords.speed,
          timestamp: position.timestamp
        }))
        setIsLoading(false)
      },
      (error) => {
        console.error('GPS Error:', error)
        setError(`GPS Error: ${error.message} (Code: ${error.code})`)
        setDebugInfo((prev: any) => ({
          ...prev,
          success: false,
          errorCode: error.code,
          errorMessage: error.message
        }))
        setIsLoading(false)
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 0
      }
    )
  }

  const testWithDifferentOptions = () => {
    setError(null)
    setDebugInfo(null)
    setIsLoading(true)

    navigator.geolocation.getCurrentPosition(
      (position) => {
        console.log('GPS Success (Low Accuracy):', position)
        console.log('GPS Debugger Low Accuracy Coordinates:', `Lat: ${position.coords.latitude}, Lon: ${position.coords.longitude}`)
        setLocation({
          lat: position.coords.latitude,
          lon: position.coords.longitude
        })
        setDebugInfo((prev: any) => ({
          ...prev,
          success: true,
          accuracy: position.coords.accuracy,
          method: 'low_accuracy'
        }))
        setIsLoading(false)
      },
      (error) => {
        console.error('GPS Error (Low Accuracy):', error)
        setError(`GPS Error: ${error.message} (Code: ${error.code})`)
        setIsLoading(false)
      },
      {
        enableHighAccuracy: false,
        timeout: 10000,
        maximumAge: 60000
      }
    )
  }

  return (
    <Box p={6} bg={bg} borderRadius="xl" border="1px" borderColor={borderColor}>
      <VStack spacing={6} align="stretch">
        <HStack>
          <Navigation size={24} color="blue" />
          <ChakraText fontSize="xl" fontWeight="bold">GPS Location Debugger</ChakraText>
        </HStack>

        {/* Test Buttons */}
        <HStack spacing={4}>
          <Button
            leftIcon={<Navigation size={16} />}
            onClick={testGPS}
            isLoading={isLoading}
            loadingText="Testing GPS..."
            colorScheme="blue"
            size="lg"
          >
            Test High Accuracy GPS
          </Button>
          <Button
            leftIcon={<MapPin size={16} />}
            onClick={testWithDifferentOptions}
            isLoading={isLoading}
            loadingText="Testing..."
            colorScheme="green"
            size="lg"
          >
            Test Low Accuracy GPS
          </Button>
        </HStack>

        {/* Location Result */}
        {location && (
          <Alert status="success" borderRadius="md">
            <AlertIcon />
            <Box>
              <AlertTitle>Location Found!</AlertTitle>
              <AlertDescription>
                <VStack align="start" spacing={2}>
                  <HStack>
                    <ChakraText fontWeight="semibold">Latitude:</ChakraText>
                    <Code>{location.lat.toFixed(6)}</Code>
                  </HStack>
                  <HStack>
                    <ChakraText fontWeight="semibold">Longitude:</ChakraText>
                    <Code>{location.lon.toFixed(6)}</Code>
                  </HStack>
                  <HStack>
                    <Badge colorScheme="green">
                      <HStack spacing={1}>
                        <CheckCircle size={12} />
                        <ChakraText>GPS Working</ChakraText>
                      </HStack>
                    </Badge>
                  </HStack>
                </VStack>
              </AlertDescription>
            </Box>
          </Alert>
        )}

        {/* Error Display */}
        {error && (
          <Alert status="error" borderRadius="md">
            <AlertIcon />
            <Box>
              <AlertTitle>GPS Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Box>
          </Alert>
        )}

        {/* Debug Information */}
        {debugInfo && (
          <Box>
            <ChakraText fontSize="lg" fontWeight="semibold" mb={3}>
              Debug Information
            </ChakraText>
            <Code whiteSpace="pre-wrap" p={4} borderRadius="md" bg="gray.50" color="gray.800">
              {JSON.stringify(debugInfo, null, 2)}
            </Code>
          </Box>
        )}

        {/* Browser Compatibility Check */}
        <Box p={4} bg="blue.50" borderRadius="md" border="1px" borderColor="blue.200">
          <ChakraText fontSize="sm" fontWeight="semibold" color="blue.700" mb={2}>
            Browser Compatibility:
          </ChakraText>
          <VStack spacing={1} align="start" fontSize="xs" color="blue.600">
            <HStack>
              <ChakraText>Geolocation API:</ChakraText>
              <Badge colorScheme={navigator.geolocation ? 'green' : 'red'}>
                {navigator.geolocation ? 'Supported' : 'Not Supported'}
              </Badge>
            </HStack>
            <HStack>
              <ChakraText>HTTPS Required:</ChakraText>
              <Badge colorScheme={window.location.protocol === 'https:' ? 'green' : 'orange'}>
                {window.location.protocol === 'https:' ? 'Yes' : 'No (May cause issues)'}
              </Badge>
            </HStack>
            <HStack>
              <ChakraText>Localhost:</ChakraText>
              <Badge colorScheme={window.location.hostname === 'localhost' ? 'green' : 'blue'}>
                {window.location.hostname === 'localhost' ? 'Yes' : 'No'}
              </Badge>
            </HStack>
          </VStack>
        </Box>
      </VStack>
    </Box>
  )
}

export default GPSDebugger
