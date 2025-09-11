import {
  Box,
  Heading,
  Text as ChakraText,
  HStack,
  VStack,
  Icon,
  useColorModeValue,
  Skeleton,
  Badge,
} from '@chakra-ui/react'
import { useLocationWeather } from '../../hooks/useLocationWeather'
import { Cloud, Droplets, Wind, Thermometer, Sun, CloudRain, MapPin } from 'lucide-react'

const WeatherWidget = () => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  // Use location-aware weather hook
  const { 
    data: weatherData, 
    isLoading, 
    isLocationLoading 
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

  if (!weatherData || !weatherData.location || !weatherData.current) {
    return (
      <Box bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
        <Heading size="md" mb={4}>Weather Forecast</Heading>
        {isLocationLoading ? (
          <HStack>
            <Skeleton height="20px" width="200px" />
            <ChakraText fontSize="sm" color="blue.600">Detecting location...</ChakraText>
          </HStack>
        ) : (
          <ChakraText color="gray.500">Weather data unavailable</ChakraText>
        )}
      </Box>
    )
  }

  return (
    <Box bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
      <HStack justify="space-between" mb={4}>
        <Heading size="md">Weather Forecast</Heading>
        <HStack spacing={2}>
          <Badge colorScheme="blue" variant="subtle">
            {weatherData.location.name}
          </Badge>
          <Icon 
            as={MapPin} 
            w={4} 
            h={4} 
            color="green.500" 
          />
        </HStack>
      </HStack>

      {isLoading ? (
        <VStack spacing={4}>
          <Skeleton height="60px" />
          <Skeleton height="40px" />
        </VStack>
      ) : (
        <VStack spacing={4} align="stretch">
          {/* Current Weather */}
          <HStack justify="space-between" p={4} bg="blue.50" borderRadius="lg">
            <VStack align="start" spacing={1}>
              <ChakraText fontSize="2xl" fontWeight="bold">
                {weatherData.current.temperature}°F
              </ChakraText>
              <ChakraText color="gray.600">{weatherData.current.conditions}</ChakraText>
            </VStack>
            <Icon as={getWeatherIcon(weatherData.current.icon)} w={12} h={12} color="blue.500" />
          </HStack>

          {/* Weather Details */}
          <HStack justify="space-around" py={2}>
            <VStack spacing={1}>
              <Icon as={Droplets} w={5} h={5} color="blue.500" />
              <ChakraText fontSize="sm" color="gray.600">Humidity</ChakraText>
              <ChakraText fontWeight="semibold">{weatherData.current.humidity}%</ChakraText>
            </VStack>
            <VStack spacing={1}>
              <Icon as={Wind} w={5} h={5} color="gray.500" />
              <ChakraText fontSize="sm" color="gray.600">Wind</ChakraText>
              <ChakraText fontWeight="semibold">{weatherData.current.wind_speed} mph</ChakraText>
            </VStack>
            <VStack spacing={1}>
              <Icon as={Thermometer} w={5} h={5} color="red.500" />
              <ChakraText fontSize="sm" color="gray.600">Pressure</ChakraText>
              <ChakraText fontWeight="semibold">{weatherData.current.pressure} hPa</ChakraText>
            </VStack>
          </HStack>

          {/* 3-Day Forecast */}
          <VStack spacing={2} align="stretch">
            <ChakraText fontSize="sm" fontWeight="semibold" color="gray.700">
              3-Day Forecast
            </ChakraText>
            {weatherData.forecast.slice(0, 3).map((day, index) => (
              <HStack key={index} justify="space-between" py={2}>
                <ChakraText fontSize="sm" color="gray.600">
                  {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })}
                </ChakraText>
                <HStack spacing={2}>
                  <ChakraText fontSize="sm" fontWeight="semibold">
                    {day.high}°/{day.low}°
                  </ChakraText>
                  <ChakraText fontSize="sm" color="gray.600">
                    {day.conditions}
                  </ChakraText>
                </HStack>
              </HStack>
            ))}
          </VStack>
        </VStack>
      )}
    </Box>
  )
}

export default WeatherWidget
