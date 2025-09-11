import React, { useState, useEffect } from 'react'
import {
  Box,
  VStack,
  HStack,
  Text as ChakraText,
  Badge,
  Button,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  useColorModeValue,
  Divider,
} from '@chakra-ui/react'
import { CheckCircle, XCircle, RefreshCw, Globe, DollarSign, Satellite } from 'lucide-react'
import { weatherApi } from '../../services/weatherApi'
import { marketApi } from '../../services/marketApi'
import { nasaApi } from '../../services/nasaApi'

interface ApiStatus {
  name: string
  status: 'loading' | 'success' | 'error'
  message: string
  icon: React.ReactNode
  color: string
}

const ApiStatusChecker = () => {
  const [apiStatuses, setApiStatuses] = useState<ApiStatus[]>([])
  const [isChecking, setIsChecking] = useState(false)

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  const checkApis = async () => {
    setIsChecking(true)
    const statuses: ApiStatus[] = []

    // Check Weather API
    try {
      console.log('Testing Weather API...')
      const weatherData = await weatherApi.getWeatherForecast(28.3477, 77.5573)
      statuses.push({
        name: 'OpenWeatherMap',
        status: 'success',
        message: `Weather data received for ${weatherData.location.name}`,
        icon: <Globe size={16} />,
        color: 'green'
      })
    } catch (error) {
      statuses.push({
        name: 'OpenWeatherMap',
        status: 'error',
        message: `Failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        icon: <XCircle size={16} />,
        color: 'red'
      })
    }

    // Check Market API
    try {
      console.log('Testing Market API...')
      const marketData = await marketApi.getCommodityPrices()
      statuses.push({
        name: 'Alpha Vantage',
        status: 'success',
        message: `Commodity prices received (${marketData.length} items)`,
        icon: <DollarSign size={16} />,
        color: 'green'
      })
    } catch (error) {
      statuses.push({
        name: 'Alpha Vantage',
        status: 'error',
        message: `Failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        icon: <XCircle size={16} />,
        color: 'red'
      })
    }

    // Check NASA API
    try {
      console.log('Testing NASA API...')
      const nasaData = await nasaApi.getAgriculturalData(28.3477, 77.5573)
      statuses.push({
        name: 'NASA Satellite',
        status: 'success',
        message: `Satellite data received (NDVI: ${nasaData.ndvi.value.toFixed(2)})`,
        icon: <Satellite size={16} />,
        color: 'green'
      })
    } catch (error) {
      statuses.push({
        name: 'NASA Satellite',
        status: 'error',
        message: `Failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        icon: <XCircle size={16} />,
        color: 'red'
      })
    }

    setApiStatuses(statuses)
    setIsChecking(false)
  }

  useEffect(() => {
    checkApis()
  }, [])

  const successCount = apiStatuses.filter(s => s.status === 'success').length
  const totalCount = apiStatuses.length

  return (
    <Box p={6} bg={bg} borderRadius="xl" border="1px" borderColor={borderColor}>
      <VStack spacing={4} align="stretch">
        <HStack>
          <RefreshCw size={24} color="blue" />
          <ChakraText fontSize="xl" fontWeight="bold">API Status Checker</ChakraText>
        </HStack>

        <HStack>
          <Button
            leftIcon={<RefreshCw size={16} />}
            onClick={checkApis}
            isLoading={isChecking}
            loadingText="Checking APIs..."
            colorScheme="blue"
            size="sm"
          >
            Refresh Status
          </Button>
          <Badge colorScheme={successCount === totalCount ? 'green' : 'yellow'}>
            {successCount}/{totalCount} APIs Working
          </Badge>
        </HStack>

        <Divider />

        {apiStatuses.length === 0 && !isChecking && (
          <Alert status="info" borderRadius="md">
            <AlertIcon />
            <AlertDescription>Click "Refresh Status" to check API connections</AlertDescription>
          </Alert>
        )}

        {apiStatuses.map((api, index) => (
          <Box key={index} p={4} borderWidth={1} borderRadius="md" borderColor={borderColor}>
            <HStack justify="space-between">
              <HStack>
                {api.icon}
                <ChakraText fontWeight="semibold">{api.name}</ChakraText>
              </HStack>
              <Badge colorScheme={api.color}>
                {api.status === 'success' ? (
                  <HStack spacing={1}>
                    <CheckCircle size={12} />
                    <ChakraText>Connected</ChakraText>
                  </HStack>
                ) : (
                  <HStack spacing={1}>
                    <XCircle size={12} />
                    <ChakraText>Failed</ChakraText>
                  </HStack>
                )}
              </Badge>
            </HStack>
            <ChakraText fontSize="sm" color="gray.600" mt={2}>
              {api.message}
            </ChakraText>
          </Box>
        ))}

        {successCount === totalCount && totalCount > 0 && (
          <Alert status="success" borderRadius="md">
            <AlertIcon />
            <AlertTitle>All APIs Working!</AlertTitle>
            <AlertDescription>
              Your field is now connected to real-time weather, market, and satellite data.
            </AlertDescription>
          </Alert>
        )}

        {successCount < totalCount && totalCount > 0 && (
          <Alert status="warning" borderRadius="md">
            <AlertIcon />
            <AlertTitle>Some APIs Failed</AlertTitle>
            <AlertDescription>
              Check your API keys in the .env file and ensure you have internet connection.
            </AlertDescription>
          </Alert>
        )}
      </VStack>
    </Box>
  )
}

export default ApiStatusChecker
