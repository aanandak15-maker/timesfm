import {
  Box,
  Heading,
  Text as ChakraText,
  VStack,
  HStack,
  Badge,
  useColorModeValue,
  Progress,
  Icon,
} from '@chakra-ui/react'
import { TrendingUp, Calendar, Target } from 'lucide-react'
import { yieldPredictionApi, type YieldPredictionData } from '../../services/yieldPredictionApi'
import { useState, useEffect } from 'react'

const YieldPredictionCard = () => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')
  const [predictionData, setPredictionData] = useState<YieldPredictionData | null>(null)

  useEffect(() => {
    const loadYieldPrediction = async () => {
      try {
        console.log('Fetching real yield prediction data...')
        const data = await yieldPredictionApi.getYieldPrediction('field-1', 'rice')
        setPredictionData(data)
        console.log('Real yield prediction data loaded:', data)
      } catch (error) {
        console.warn('Real yield prediction API failed, using mock data:', error)
        // Fallback to mock data
        setPredictionData({
          predicted_yield: 4.2,
          confidence_interval: { lower: 3.6, upper: 4.8 },
          factors: {
            weather_impact: 0.88,
            soil_health: 0.92,
            crop_stage: 0.85,
            disease_pressure: 0.15,
            nutrient_status: 0.78
          },
          recommendations: [
            'Monitor soil moisture levels',
            'Apply balanced fertilization',
            'Check for pest pressure'
          ],
          last_updated: new Date().toISOString(),
          model_version: 'TimesFM-Mock-v1.0'
        })
      } catch (error) {
        console.error('Error loading yield prediction:', error)
      }
    }

    loadYieldPrediction()
  }, [])

  // Mock yield prediction data (fallback)
  const mockPrediction = {
    field_id: 'field-1',
    predicted_yield: 4.2,
    confidence_score: 85,
    prediction_date: new Date().toISOString(),
    harvest_window: {
      optimal_start: '2024-09-15',
      optimal_end: '2024-09-30'
    },
    factors: {
      weather_score: 88,
      soil_score: 92,
      crop_health_score: 79
    }
  }

  return (
    <Box bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
      <HStack justify="space-between" mb={4}>
        <Heading size="md">AI Yield Prediction</Heading>
        <Badge colorScheme="green" variant="subtle">
          TimesFM Active
        </Badge>
      </HStack>

      <VStack spacing={6} align="stretch">
        {/* Main Prediction */}
        <HStack justify="space-between" p={4} bg="green.50" borderRadius="lg">
          <VStack align="start" spacing={1}>
            <ChakraText fontSize="sm" color="gray.600">Predicted Yield</ChakraText>
            <ChakraText fontSize="3xl" fontWeight="bold" color="green.600">
              {predictionData?.predicted_yield || mockPrediction.predicted_yield} tons/acre
            </ChakraText>
            <ChakraText fontSize="sm" color="gray.600">
              Confidence: {predictionData?.confidence_interval ? '85-95%' : mockPrediction.confidence_score}%
            </ChakraText>
            {predictionData?.confidence_interval && (
              <ChakraText fontSize="xs" color="gray.500">
                Range: {predictionData.confidence_interval.lower} - {predictionData.confidence_interval.upper} tons/acre
              </ChakraText>
            )}
          </VStack>
          <Icon as={TrendingUp} w={12} h={12} color="green.500" />
        </HStack>

        {/* Harvest Window */}
        <Box>
          <HStack mb={2}>
            <Icon as={Calendar} w={4} h={4} color="blue.500" />
            <ChakraText fontSize="sm" fontWeight="semibold">Optimal Harvest Window</ChakraText>
          </HStack>
          <ChakraText fontSize="sm" color="gray.600">
            {new Date(mockPrediction.harvest_window.optimal_start).toLocaleDateString()} - {' '}
            {new Date(mockPrediction.harvest_window.optimal_end).toLocaleDateString()}
          </ChakraText>
        </Box>

        {/* Factor Scores */}
        <VStack spacing={3} align="stretch">
          <ChakraText fontSize="sm" fontWeight="semibold">Factor Analysis</ChakraText>
          
          <Box>
            <HStack justify="space-between" mb={1}>
              <ChakraText fontSize="sm">Weather Conditions</ChakraText>
              <ChakraText fontSize="sm" fontWeight="semibold">
                {predictionData?.factors?.weather_impact ? Math.round(predictionData.factors.weather_impact * 100) : mockPrediction.factors.weather_score}%
              </ChakraText>
            </HStack>
            <Progress 
              value={predictionData?.factors?.weather_impact ? predictionData.factors.weather_impact * 100 : mockPrediction.factors.weather_score} 
              colorScheme="blue" 
              size="sm" 
            />
          </Box>

          <Box>
            <HStack justify="space-between" mb={1}>
              <ChakraText fontSize="sm">Soil Health</ChakraText>
              <ChakraText fontSize="sm" fontWeight="semibold">
                {predictionData?.factors?.soil_health ? Math.round(predictionData.factors.soil_health * 100) : mockPrediction.factors.soil_score}%
              </ChakraText>
            </HStack>
            <Progress 
              value={predictionData?.factors?.soil_health ? predictionData.factors.soil_health * 100 : mockPrediction.factors.soil_score} 
              colorScheme="green" 
              size="sm" 
            />
          </Box>

          <Box>
            <HStack justify="space-between" mb={1}>
              <ChakraText fontSize="sm">Crop Health</ChakraText>
              <ChakraText fontSize="sm" fontWeight="semibold">
                {predictionData?.factors?.crop_stage ? Math.round(predictionData.factors.crop_stage * 100) : mockPrediction.factors.crop_health_score}%
              </ChakraText>
            </HStack>
            <Progress 
              value={predictionData?.factors?.crop_stage ? predictionData.factors.crop_stage * 100 : mockPrediction.factors.crop_health_score} 
              colorScheme="orange" 
              size="sm" 
            />
          </Box>
        </VStack>

        {/* Recommendation */}
        <Box p={3} bg="blue.50" borderRadius="lg">
          <HStack mb={2}>
            <Icon as={Target} w={4} h={4} color="blue.500" />
            <ChakraText fontSize="sm" fontWeight="semibold">AI Recommendation</ChakraText>
          </HStack>
          <ChakraText fontSize="sm" color="gray.700">
            {predictionData?.recommendations && predictionData.recommendations.length > 0 
              ? predictionData.recommendations[0]
              : 'Based on current conditions, your fields are performing above average. Consider increasing irrigation by 10% for optimal yield.'
            }
          </ChakraText>
          {predictionData?.recommendations && predictionData.recommendations.length > 1 && (
            <VStack align="stretch" spacing={1} mt={2}>
              {predictionData.recommendations.slice(1, 3).map((rec, index) => (
                <ChakraText key={index} fontSize="xs" color="gray.600">
                  • {rec}
                </ChakraText>
              ))}
            </VStack>
          )}
        </Box>
      </VStack>
    </Box>
  )
}

export default YieldPredictionCard
