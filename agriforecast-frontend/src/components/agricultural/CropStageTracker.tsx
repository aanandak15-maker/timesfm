import React, { useState, useEffect } from 'react'
import {
  Box,
  VStack,
  HStack,
  Text as ChakraText,
  Heading,
  Badge,
  SimpleGrid,
  Card,
  CardBody,
  CardHeader,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Button,
  Icon,
  useColorModeValue,
  Tooltip,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  CircularProgress,
  CircularProgressLabel,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Flex,
  Spacer,
} from '@chakra-ui/react'
import {
  Sprout,
  Leaf,
  Flower,
  Wheat,
  Calendar,
  Clock,
  TrendingUp,
  TrendingDown,
  Minus,
  AlertTriangle,
  CheckCircle,
  Lock,
  RefreshCw,
  BarChart3
} from 'lucide-react'

interface CropStageData {
  field_id: string
  crop_type: string
  current_stage: string
  days_since_planting: number
  days_to_harvest: number
  stage_percentage: number
  tillering_count: number
  panicle_count: number
  stem_count: number
  heading_percentage: number
  grain_filling_percentage: number
  maturity_percentage: number
  stress_indicators: {
    water_stress: number
    nutrient_stress: number
    disease_stress: number
    pest_stress: number
  }
  growth_metrics: {
    plant_height: number
    leaf_count: number
    root_depth: number
    biomass: number
  }
  environmental_factors: {
    temperature: number
    humidity: number
    rainfall: number
    sunlight_hours: number
  }
  yield_predictions: {
    current_prediction: number
    confidence: number
    historical_average: number
    trend: string
  }
  stage_history: Array<{
    stage: string
    date: string
    duration: number
    notes: string
  }>
}

const CropStageTracker: React.FC = () => {
  const [cropData, setCropData] = useState<CropStageData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isLocked] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')
  const textColor = useColorModeValue('gray.600', 'gray.300')

  // Simulate data loading
  useEffect(() => {
    const loadCropData = async () => {
      setIsLoading(true)
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      const mockData: CropStageData = {
        field_id: "field_001",
        crop_type: "rice",
        current_stage: "grain_filling",
        days_since_planting: 85,
        days_to_harvest: 35,
        stage_percentage: 65.5,
        tillering_count: 18,
        panicle_count: 12,
        stem_count: 0,
        heading_percentage: 95.2,
        grain_filling_percentage: 65.5,
        maturity_percentage: 0,
        stress_indicators: {
          water_stress: 0.15,
          nutrient_stress: 0.08,
          disease_stress: 0.05,
          pest_stress: 0.12
        },
        growth_metrics: {
          plant_height: 85.5,
          leaf_count: 12.3,
          root_depth: 45.2,
          biomass: 1250.8
        },
        environmental_factors: {
          temperature: 28.5,
          humidity: 75.2,
          rainfall: 15.8,
          sunlight_hours: 8.5
        },
        yield_predictions: {
          current_prediction: 4.2,
          confidence: 85.5,
          historical_average: 3.8,
          trend: "increasing"
        },
        stage_history: [
          {
            stage: "planting",
            date: "2024-03-15",
            duration: 0,
            notes: "Seeds planted, optimal soil conditions"
          },
          {
            stage: "tillering",
            date: "2024-04-15",
            duration: 30,
            notes: "Good tiller development, adequate moisture"
          },
          {
            stage: "stem_elongation",
            date: "2024-05-15",
            duration: 30,
            notes: "Rapid stem growth, nitrogen application"
          },
          {
            stage: "heading",
            date: "2024-06-15",
            duration: 30,
            notes: "Panicle initiation, flowering stage"
          },
          {
            stage: "grain_filling",
            date: "2024-07-15",
            duration: 30,
            notes: "Grain development, monitoring for pests"
          }
        ]
      }
      
      setCropData(mockData)
      setIsLoading(false)
      setLastUpdated(new Date())
    }

    loadCropData()
  }, [])

  const getStageIcon = (stage: string) => {
    switch (stage.toLowerCase()) {
      case 'planting':
        return <Sprout size={20} color="green" />
      case 'tillering':
        return <Leaf size={20} color="lightgreen" />
      case 'stem_elongation':
        return <TrendingUp size={20} color="blue" />
      case 'heading':
        return <Flower size={20} color="purple" />
      case 'grain_filling':
        return <Wheat size={20} color="gold" />
      case 'maturity':
        return <CheckCircle size={20} color="orange" />
      default:
        return <Calendar size={20} color="gray" />
    }
  }

  const getStageColor = (stage: string) => {
    switch (stage.toLowerCase()) {
      case 'planting':
        return 'green'
      case 'tillering':
        return 'blue'
      case 'stem_elongation':
        return 'purple'
      case 'heading':
        return 'pink'
      case 'grain_filling':
        return 'yellow'
      case 'maturity':
        return 'orange'
      default:
        return 'gray'
    }
  }

  const getStressLevel = (value: number) => {
    if (value > 0.7) return { level: 'High', color: 'red' }
    if (value > 0.4) return { level: 'Medium', color: 'orange' }
    return { level: 'Low', color: 'green' }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'increasing':
        return <TrendingUp size={16} color="green" />
      case 'decreasing':
        return <TrendingDown size={16} color="red" />
      default:
        return <Minus size={16} color="gray" />
    }
  }

  if (isLoading) {
    return (
      <Box p={6} textAlign="center">
        <CircularProgress isIndeterminate color="blue.500" size="60px" />
        <ChakraText mt={4} color={textColor}>
          Loading crop stage data...
        </ChakraText>
      </Box>
    )
  }

  if (!cropData) {
    return (
      <Alert status="error">
        <AlertIcon />
        <AlertTitle>Error loading crop data!</AlertTitle>
        <AlertDescription>Unable to load crop stage tracking data.</AlertDescription>
      </Alert>
    )
  }

  return (
    <Box p={6} bg={bg} borderRadius="lg" boxShadow="lg">
      {/* Header */}
      <Flex align="center" mb={6}>
        <VStack align="start" spacing={1}>
          <HStack>
            <Heading size="lg">Crop Stage Tracking</Heading>
            <Badge colorScheme={getStageColor(cropData.current_stage)} variant="subtle">
              {cropData.current_stage.replace('_', ' ').toUpperCase()}
            </Badge>
            {isLocked && (
              <Tooltip label="Advanced features locked for future development">
                <Icon as={Lock} w={4} h={4} color="gray.500" />
              </Tooltip>
            )}
          </HStack>
          <ChakraText color={textColor} fontSize="sm">
            Real-time monitoring of crop development stages and growth metrics
          </ChakraText>
        </VStack>
        <Spacer />
        <HStack>
          <ChakraText fontSize="sm" color={textColor}>
            Last updated: {lastUpdated.toLocaleTimeString()}
          </ChakraText>
          <Button size="sm" variant="ghost" onClick={() => window.location.reload()}>
            <Icon as={RefreshCw} w={4} h={4} />
          </Button>
        </HStack>
      </Flex>

      {/* Current Stage Overview */}
      <Card mb={6} borderColor={borderColor}>
        <CardHeader>
          <HStack>
            {getStageIcon(cropData.current_stage)}
            <Heading size="md">Current Stage: {cropData.current_stage.replace('_', ' ').toUpperCase()}</Heading>
          </HStack>
        </CardHeader>
        <CardBody>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
            <Box textAlign="center">
              <CircularProgress
                value={cropData.stage_percentage}
                size="80px"
                color={getStageColor(cropData.current_stage)}
                thickness="8px"
              >
                <CircularProgressLabel>
                  {cropData.stage_percentage.toFixed(0)}%
                </CircularProgressLabel>
              </CircularProgress>
              <ChakraText mt={2} fontWeight="bold">
                Stage Completion
              </ChakraText>
            </Box>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Days Since Planting</ChakraText>
              <ChakraText fontSize="2xl" color="blue.500">
                {cropData.days_since_planting}
              </ChakraText>
              <ChakraText fontSize="sm" color={textColor}>Days</ChakraText>
            </VStack>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Days to Harvest</ChakraText>
              <ChakraText fontSize="2xl" color="green.500">
                {cropData.days_to_harvest}
              </ChakraText>
              <ChakraText fontSize="sm" color={textColor}>Days remaining</ChakraText>
            </VStack>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Crop Type</ChakraText>
              <ChakraText fontSize="2xl" color="purple.500" textTransform="capitalize">
                {cropData.crop_type}
              </ChakraText>
              <ChakraText fontSize="sm" color={textColor}>Primary crop</ChakraText>
            </VStack>
          </SimpleGrid>
        </CardBody>
      </Card>

      {/* Comprehensive Analysis Sections */}
      <Accordion allowMultiple>
        {/* Growth Metrics */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={BarChart3} w={5} h={5} color="blue.500" />
                <Heading size="sm">Growth Metrics</Heading>
                <Badge colorScheme="blue" variant="subtle">Real-time</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
              <Stat>
                <StatLabel>Plant Height</StatLabel>
                <StatNumber>{cropData.growth_metrics.plant_height} cm</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Average height
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Leaf Count</StatLabel>
                <StatNumber>{cropData.growth_metrics.leaf_count}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Per plant
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Root Depth</StatLabel>
                <StatNumber>{cropData.growth_metrics.root_depth} cm</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Root system
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Biomass</StatLabel>
                <StatNumber>{cropData.growth_metrics.biomass} g/m²</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Dry weight
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Crop-Specific Metrics */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Wheat} w={5} h={5} color="green.500" />
                <Heading size="sm">Crop-Specific Metrics</Heading>
                <Badge colorScheme="green" variant="subtle">{cropData.crop_type}</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              <Stat>
                <StatLabel>Tillering Count</StatLabel>
                <StatNumber>{cropData.tillering_count}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Tillers per plant
                </StatHelpText>
              </Stat>
              
              {cropData.crop_type === 'rice' && (
                <Stat>
                  <StatLabel>Panicle Count</StatLabel>
                  <StatNumber>{cropData.panicle_count}</StatNumber>
                  <StatHelpText>
                    <StatArrow type="increase" />
                    Panicles per plant
                  </StatHelpText>
                </Stat>
              )}
              
              {cropData.crop_type === 'wheat' && (
                <Stat>
                  <StatLabel>Stem Count</StatLabel>
                  <StatNumber>{cropData.stem_count}</StatNumber>
                  <StatHelpText>
                    <StatArrow type="increase" />
                    Stems per plant
                  </StatHelpText>
                </Stat>
              )}
              
              <Stat>
                <StatLabel>Heading Percentage</StatLabel>
                <StatNumber>{cropData.heading_percentage.toFixed(1)}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Completed
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Grain Filling</StatLabel>
                <StatNumber>{cropData.grain_filling_percentage.toFixed(1)}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Completed
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Maturity</StatLabel>
                <StatNumber>{cropData.maturity_percentage.toFixed(1)}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Completed
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Stress Indicators */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={AlertTriangle} w={5} h={5} color="red.500" />
                <Heading size="sm">Stress Indicators</Heading>
                <Badge colorScheme="red" variant="subtle">Monitoring</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
              {Object.entries(cropData.stress_indicators).map(([stress, value]) => {
                const stressInfo = getStressLevel(value)
                return (
                  <Stat key={stress}>
                    <StatLabel textTransform="capitalize">{stress.replace('_', ' ')}</StatLabel>
                    <StatNumber color={stressInfo.color}>
                      {(value * 100).toFixed(1)}%
                    </StatNumber>
                    <StatHelpText>
                      <StatArrow type={value > 0.5 ? "decrease" : "increase"} />
                      {stressInfo.level} stress
                    </StatHelpText>
                  </Stat>
                )
              })}
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Environmental Factors */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Calendar} w={5} h={5} color="orange.500" />
                <Heading size="sm">Environmental Factors</Heading>
                <Badge colorScheme="orange" variant="subtle">Weather</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
              <Stat>
                <StatLabel>Temperature</StatLabel>
                <StatNumber>{cropData.environmental_factors.temperature}°C</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Current
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Humidity</StatLabel>
                <StatNumber>{cropData.environmental_factors.humidity}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Relative humidity
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Rainfall</StatLabel>
                <StatNumber>{cropData.environmental_factors.rainfall} mm</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Last 7 days
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Sunlight Hours</StatLabel>
                <StatNumber>{cropData.environmental_factors.sunlight_hours} hrs</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Daily average
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Yield Predictions */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={TrendingUp} w={5} h={5} color="purple.500" />
                <Heading size="sm">Yield Predictions</Heading>
                <Badge colorScheme="purple" variant="subtle">AI Forecast</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
              <Stat>
                <StatLabel>Current Prediction</StatLabel>
                <StatNumber>{cropData.yield_predictions.current_prediction} t/ha</StatNumber>
                <StatHelpText>
                  {getTrendIcon(cropData.yield_predictions.trend)}
                  {cropData.yield_predictions.trend}
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Confidence</StatLabel>
                <StatNumber>{cropData.yield_predictions.confidence}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Prediction accuracy
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Historical Average</StatLabel>
                <StatNumber>{cropData.yield_predictions.historical_average} t/ha</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Past 5 years
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Yield Trend</StatLabel>
                <StatNumber textTransform="capitalize">
                  {cropData.yield_predictions.trend}
                </StatNumber>
                <StatHelpText>
                  {getTrendIcon(cropData.yield_predictions.trend)}
                  vs. historical
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Stage History */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Clock} w={5} h={5} color="teal.500" />
                <Heading size="sm">Stage History</Heading>
                <Badge colorScheme="teal" variant="subtle">Timeline</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <TableContainer>
              <Table variant="simple" size="sm">
                <Thead>
                  <Tr>
                    <Th>Stage</Th>
                    <Th>Date</Th>
                    <Th>Duration (Days)</Th>
                    <Th>Notes</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {cropData.stage_history.map((stage, index) => (
                    <Tr key={index}>
                      <Td>
                        <HStack>
                          {getStageIcon(stage.stage)}
                          <ChakraText textTransform="capitalize">
                            {stage.stage.replace('_', ' ')}
                          </ChakraText>
                        </HStack>
                      </Td>
                      <Td>{new Date(stage.date).toLocaleDateString()}</Td>
                      <Td>{stage.duration}</Td>
                      <Td>{stage.notes}</Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </TableContainer>
          </AccordionPanel>
        </AccordionItem>
      </Accordion>

      {/* Lock Notice */}
      {isLocked && (
        <Alert status="info" mt={6}>
          <AlertIcon />
          <AlertTitle>Advanced Features Locked</AlertTitle>
          <AlertDescription>
            This comprehensive crop stage tracking system is currently in development. 
            Advanced features will be unlocked in future updates.
          </AlertDescription>
        </Alert>
      )}
    </Box>
  )
}

export default CropStageTracker
