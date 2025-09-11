import {
  Box,
  Heading,
  Text as ChakraText,
  VStack,
  HStack,
  useColorModeValue,
  SimpleGrid,
  Card,
  CardBody,
  Badge,
  Icon,
  Skeleton,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react'
import { useLocationWeather } from '../../hooks/useLocationWeather'
import GPSDebugger from '../../components/debug/GPSDebugger'
import ApiStatusChecker from '../../components/debug/ApiStatusChecker'
import { Cloud, Droplets, Wind, Thermometer, Sun, CloudRain, RefreshCw, MapPin, Navigation } from 'lucide-react'

const Weather = () => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  // Use location-aware weather hook
  const { 
    data: weatherData, 
    isLoading, 
    refetch, 
    isLocationLoading, 
    refreshLocation
  } = useLocationWeather({
    refetchInterval: 5 * 60 * 1000 // Refetch every 5 minutes
  })

  const getWeatherIcon = (icon: string) => {
    switch (icon) {
      case '01d':
      case '01n':
        return Sun
      case '02d':
      case '02n':
      case '03d':
      case '03n':
        return Cloud
      case '10d':
      case '10n':
        return CloudRain
      default:
        return Cloud
    }
  }

  if (isLoading || isLocationLoading) {
    return (
      <Box>
        <VStack align="start" spacing={4} mb={8}>
          <Skeleton height="40px" width="300px" />
          <Skeleton height="20px" width="500px" />
          {isLocationLoading && (
            <HStack>
              <Icon as={Navigation} w={4} h={4} color="blue.500" />
              <ChakraText fontSize="sm" color="blue.600">Detecting your location...</ChakraText>
            </HStack>
          )}
        </VStack>
        <SimpleGrid columns={{ base: 1, md: 5 }} spacing={4}>
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} height="200px" />
          ))}
        </SimpleGrid>
      </Box>
    )
  }

  if (!weatherData || !weatherData.location || !weatherData.current) {
    return (
      <Alert status="error" borderRadius="xl">
        <AlertIcon />
        <Box>
          <AlertTitle>Weather Data Unavailable</AlertTitle>
          <AlertDescription>
            Unable to fetch weather data. Please try again later.
          </AlertDescription>
        </Box>
      </Alert>
    )
  }

  return (
    <Box>
      <VStack align="start" spacing={4} mb={8}>
        <HStack justify="space-between" w="full">
          <VStack align="start" spacing={2}>
            <Heading size="lg">Weather Monitoring</Heading>
            <ChakraText color="gray.600">
              Real-time weather data and forecasts for your fields
            </ChakraText>
          </VStack>
          <HStack>
            <Badge colorScheme="blue" variant="subtle">
              {weatherData.location.name}, {weatherData.location.country}
            </Badge>
            <HStack spacing={2}>
              <Icon 
                as={MapPin} 
                w={4} 
                h={4} 
                color="green.500" 
              />
              <Icon 
                as={RefreshCw} 
                w={4} 
                h={4} 
                color="blue.500" 
                cursor="pointer"
                onClick={() => refetch()}
                _hover={{ color: 'blue.700' }}
              />
              <Icon 
                as={Navigation} 
                w={4} 
                h={4} 
                color="purple.500" 
                cursor="pointer"
                onClick={refreshLocation}
                _hover={{ color: 'purple.700' }}
              />
            </HStack>
          </HStack>
        </HStack>
      </VStack>

      {/* Current Weather */}
      <Card bg={bg} border="1px" borderColor={borderColor} mb={8}>
        <CardBody>
          <HStack justify="space-between" mb={4}>
            <VStack align="start" spacing={1}>
              <ChakraText fontSize="sm" color="gray.600">Current Conditions</ChakraText>
              <Heading size="2xl">{weatherData.current.temperature}°F</Heading>
              <ChakraText color="gray.600">{weatherData.current.conditions}</ChakraText>
              <ChakraText fontSize="sm" color="gray.500">
                Feels like {weatherData.current.feels_like}°F
              </ChakraText>
            </VStack>
            <Icon as={getWeatherIcon(weatherData.current.icon)} w={16} h={16} color="blue.500" />
          </HStack>

          <SimpleGrid columns={4} spacing={4}>
            <VStack spacing={1}>
              <Icon as={Droplets} w={6} h={6} color="blue.500" />
              <ChakraText fontSize="sm" color="gray.600">Humidity</ChakraText>
              <ChakraText fontWeight="semibold">{weatherData.current.humidity}%</ChakraText>
            </VStack>
            <VStack spacing={1}>
              <Icon as={Wind} w={6} h={6} color="gray.500" />
              <ChakraText fontSize="sm" color="gray.600">Wind</ChakraText>
              <ChakraText fontWeight="semibold">{weatherData.current.wind_speed} mph</ChakraText>
            </VStack>
            <VStack spacing={1}>
              <Icon as={Thermometer} w={6} h={6} color="red.500" />
              <ChakraText fontSize="sm" color="gray.600">Pressure</ChakraText>
              <ChakraText fontWeight="semibold">{weatherData.current.pressure} hPa</ChakraText>
            </VStack>
            <VStack spacing={1}>
              <ChakraText fontSize="sm" color="gray.600">Visibility</ChakraText>
              <ChakraText fontWeight="semibold">{weatherData.current.visibility} km</ChakraText>
            </VStack>
          </SimpleGrid>
        </CardBody>
      </Card>

      {/* 5-Day Forecast */}
      <Card bg={bg} border="1px" borderColor={borderColor} mb={8}>
        <CardBody>
          <Heading size="md" mb={4}>5-Day Forecast</Heading>
          <SimpleGrid columns={{ base: 1, md: 5 }} spacing={4}>
            {weatherData.forecast.slice(0, 5).map((day, index) => {
              const WeatherIcon = getWeatherIcon(day.icon)
              return (
                <VStack key={index} spacing={3} p={3} bg="gray.50" borderRadius="lg">
                  <ChakraText fontSize="sm" fontWeight="semibold">
                    {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })}
                  </ChakraText>
                  <Icon as={WeatherIcon} w={8} h={8} color="blue.500" />
                  <VStack spacing={1}>
                    <ChakraText fontSize="lg" fontWeight="bold">
                      {day.high}°/{day.low}°
                    </ChakraText>
                    <ChakraText fontSize="sm" color="gray.600">
                      {day.conditions}
                    </ChakraText>
                    <ChakraText fontSize="xs" color="gray.500">
                      {day.precipitation}% rain
                    </ChakraText>
                    <ChakraText fontSize="xs" color="gray.500">
                      Wind: {day.wind_speed} mph
                    </ChakraText>
                  </VStack>
                </VStack>
              )
            })}
          </SimpleGrid>
        </CardBody>
      </Card>

      {/* GPS Debugger */}
      <GPSDebugger />
      
      {/* API Status Checker */}
      <ApiStatusChecker />
    </Box>
  )
}

export default Weather
