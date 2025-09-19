import { useState, useEffect } from 'react'
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
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Button,
  Icon,
  useColorModeValue,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  CircularProgress
} from '@chakra-ui/react'
import {
  Activity,
  RefreshCw
} from 'lucide-react'
// import { soilgridsApi } from '../../services/soilgridsApi'

interface SoilData {
  ph: number
  organicCarbon: number
  nitrogen: number
  phosphorus: number
  potassium: number
  calcium: number
  magnesium: number
  sulfur: number
  iron: number
  manganese: number
  zinc: number
  copper: number
  boron: number
  molybdenum: number
  texture: string
  bulkDensity: number
  waterHoldingCapacity: number
  cationExchangeCapacity: number
  baseSaturation: number
  aluminumSaturation: number
  electricalConductivity: number
  soilMoisture: number
  temperature: number
  lastUpdated: string
}

interface SoilRecommendations {
  fertilizer: string[]
  irrigation: string[]
  amendments: string[]
  cropRotation: string[]
  coverCrops: string[]
  tillage: string[]
  organicMatter: string[]
  phAdjustment: string[]
}

const AdvancedSoilAnalysis: React.FC = () => {
  const [soilData, setSoilData] = useState<SoilData | null>(null)
  const [recommendations, setRecommendations] = useState<SoilRecommendations | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null)

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  useEffect(() => {
    fetchSoilData()
  }, [])

  const fetchSoilData = async () => {
    setIsLoading(true)
    setError(null)
    
    try {
      // Simulate API call to SoilGrids
      const mockData: SoilData = {
        ph: 6.2 + Math.random() * 0.8,
        organicCarbon: 1.8 + Math.random() * 0.4,
        nitrogen: 0.12 + Math.random() * 0.08,
        phosphorus: 15 + Math.random() * 10,
        potassium: 120 + Math.random() * 80,
        calcium: 2000 + Math.random() * 1000,
        magnesium: 300 + Math.random() * 200,
        sulfur: 20 + Math.random() * 15,
        iron: 50 + Math.random() * 30,
        manganese: 25 + Math.random() * 15,
        zinc: 2 + Math.random() * 1.5,
        copper: 1 + Math.random() * 0.8,
        boron: 0.5 + Math.random() * 0.3,
        molybdenum: 0.1 + Math.random() * 0.05,
        texture: 'Loam',
        bulkDensity: 1.3 + Math.random() * 0.2,
        waterHoldingCapacity: 18 + Math.random() * 4,
        cationExchangeCapacity: 15 + Math.random() * 5,
        baseSaturation: 75 + Math.random() * 15,
        aluminumSaturation: 5 + Math.random() * 3,
        electricalConductivity: 0.8 + Math.random() * 0.4,
        soilMoisture: 45 + Math.random() * 20,
        temperature: 22 + Math.random() * 8,
        lastUpdated: new Date().toISOString()
      }

      setSoilData(mockData)
      setLastUpdate(new Date())
      
      // Generate recommendations based on soil data
      generateRecommendations(mockData)
      
    } catch (err) {
      setError('Failed to fetch soil data')
      console.error('Soil data error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const generateRecommendations = (data: SoilData) => {
    const recs: SoilRecommendations = {
      fertilizer: [],
      irrigation: [],
      amendments: [],
      cropRotation: [],
      coverCrops: [],
      tillage: [],
      organicMatter: [],
      phAdjustment: []
    }

    // pH recommendations
    if (data.ph < 6.0) {
      recs.phAdjustment.push('Apply lime to raise pH to 6.5-7.0')
    } else if (data.ph > 7.5) {
      recs.phAdjustment.push('Apply sulfur to lower pH')
    }

    // Nutrient recommendations
    if (data.phosphorus < 20) {
      recs.fertilizer.push('Apply phosphorus fertilizer (P2O5)')
    }
    if (data.potassium < 150) {
      recs.fertilizer.push('Apply potassium fertilizer (K2O)')
    }
    if (data.nitrogen < 0.15) {
      recs.fertilizer.push('Apply nitrogen fertilizer (N)')
    }

    // Organic matter recommendations
    if (data.organicCarbon < 2.0) {
      recs.organicMatter.push('Add compost or organic matter')
      recs.coverCrops.push('Plant cover crops to improve organic matter')
    }

    // Irrigation recommendations
    if (data.soilMoisture < 40) {
      recs.irrigation.push('Increase irrigation frequency')
    } else if (data.soilMoisture > 70) {
      recs.irrigation.push('Reduce irrigation to prevent waterlogging')
    }

    // Texture-based recommendations
    if (data.texture === 'Clay') {
      recs.tillage.push('Use reduced tillage to prevent compaction')
      recs.amendments.push('Add sand or organic matter to improve drainage')
    } else if (data.texture === 'Sand') {
      recs.amendments.push('Add clay or organic matter to improve water retention')
    }

    setRecommendations(recs)
  }

  const getNutrientStatus = (value: number, optimal: { min: number; max: number }) => {
    if (value < optimal.min) return { status: 'low', color: 'red' }
    if (value > optimal.max) return { status: 'high', color: 'orange' }
    return { status: 'optimal', color: 'green' }
  }

  const getPhStatus = (ph: number) => {
    if (ph < 6.0) return { status: 'acidic', color: 'red' }
    if (ph > 7.5) return { status: 'alkaline', color: 'orange' }
    return { status: 'optimal', color: 'green' }
  }

  if (isLoading) {
    return (
      <Box p={6} maxW="1200px" mx="auto">
        <VStack spacing={6} align="stretch">
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody>
              <VStack spacing={4}>
                <CircularProgress isIndeterminate color="blue.500" />
                <ChakraText>Analyzing soil data...</ChakraText>
              </VStack>
            </CardBody>
          </Card>
        </VStack>
      </Box>
    )
  }

  if (error) {
    return (
      <Box p={6} maxW="1200px" mx="auto">
        <VStack spacing={6} align="stretch">
          <Alert status="error" borderRadius="md">
            <AlertIcon />
            <Box>
              <AlertTitle>Error!</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Box>
          </Alert>
          <Button leftIcon={<Icon as={RefreshCw} />} onClick={fetchSoilData} colorScheme="blue">
            Retry Analysis
          </Button>
        </VStack>
      </Box>
    )
  }

  if (!soilData) {
    return (
      <Box p={6} maxW="1200px" mx="auto">
        <VStack spacing={6} align="stretch">
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody>
              <VStack spacing={4}>
                <Icon as={Activity} w={12} h={12} color="gray.400" />
                <Heading size="md" color="gray.600">No Soil Data Available</Heading>
                <ChakraText color="gray.500">Click the button below to start soil analysis</ChakraText>
                <Button leftIcon={<Icon as={RefreshCw} />} onClick={fetchSoilData} colorScheme="blue">
                  Start Soil Analysis
                </Button>
              </VStack>
            </CardBody>
          </Card>
        </VStack>
      </Box>
    )
  }

  return (
    <Box p={6} maxW="1200px" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <HStack justify="space-between">
              <VStack align="start" spacing={2}>
                <HStack>
                  <Icon as={Activity} w={8} h={8} color="green.500" />
                  <Heading size="lg" color="green.600">
                    Advanced Soil Analysis
                  </Heading>
                </HStack>
                <ChakraText color="gray.600">
                  Comprehensive soil health assessment and recommendations
                </ChakraText>
              </VStack>
              <VStack align="end" spacing={2}>
                <Button
                  leftIcon={<Icon as={RefreshCw} />}
                  onClick={fetchSoilData}
                  colorScheme="blue"
                  size="sm"
                  isLoading={isLoading}
                >
                  Refresh Data
                </Button>
                {lastUpdate && (
                  <ChakraText fontSize="sm" color="gray.500">
                    Last updated: {lastUpdate.toLocaleTimeString()}
                  </ChakraText>
                )}
              </VStack>
            </HStack>
          </CardBody>
        </Card>

        {/* Soil Properties */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <VStack spacing={6} align="stretch">
              <Heading size="md">Soil Properties</Heading>
              
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                {/* pH */}
                <Stat>
                  <StatLabel>pH Level</StatLabel>
                  <StatNumber color={getPhStatus(soilData.ph).color}>
                    {soilData.ph.toFixed(1)}
                  </StatNumber>
                  <StatHelpText>
                    <Badge colorScheme={getPhStatus(soilData.ph).color}>
                      {getPhStatus(soilData.ph).status}
                    </Badge>
                  </StatHelpText>
                </Stat>

                {/* Organic Carbon */}
                <Stat>
                  <StatLabel>Organic Carbon (%)</StatLabel>
                  <StatNumber color={getNutrientStatus(soilData.organicCarbon, { min: 1.5, max: 3.0 }).color}>
                    {soilData.organicCarbon.toFixed(1)}
                  </StatNumber>
                  <StatHelpText>
                    <Badge colorScheme={getNutrientStatus(soilData.organicCarbon, { min: 1.5, max: 3.0 }).color}>
                      {getNutrientStatus(soilData.organicCarbon, { min: 1.5, max: 3.0 }).status}
                    </Badge>
                  </StatHelpText>
                </Stat>

                {/* Nitrogen */}
                <Stat>
                  <StatLabel>Nitrogen (%)</StatLabel>
                  <StatNumber color={getNutrientStatus(soilData.nitrogen, { min: 0.1, max: 0.2 }).color}>
                    {soilData.nitrogen.toFixed(2)}
                  </StatNumber>
                  <StatHelpText>
                    <Badge colorScheme={getNutrientStatus(soilData.nitrogen, { min: 0.1, max: 0.2 }).color}>
                      {getNutrientStatus(soilData.nitrogen, { min: 0.1, max: 0.2 }).status}
                    </Badge>
                  </StatHelpText>
                </Stat>

                {/* Phosphorus */}
                <Stat>
                  <StatLabel>Phosphorus (ppm)</StatLabel>
                  <StatNumber color={getNutrientStatus(soilData.phosphorus, { min: 20, max: 40 }).color}>
                    {soilData.phosphorus.toFixed(0)}
                  </StatNumber>
                  <StatHelpText>
                    <Badge colorScheme={getNutrientStatus(soilData.phosphorus, { min: 20, max: 40 }).color}>
                      {getNutrientStatus(soilData.phosphorus, { min: 20, max: 40 }).status}
                    </Badge>
                  </StatHelpText>
                </Stat>

                {/* Potassium */}
                <Stat>
                  <StatLabel>Potassium (ppm)</StatLabel>
                  <StatNumber color={getNutrientStatus(soilData.potassium, { min: 150, max: 300 }).color}>
                    {soilData.potassium.toFixed(0)}
                  </StatNumber>
                  <StatHelpText>
                    <Badge colorScheme={getNutrientStatus(soilData.potassium, { min: 150, max: 300 }).color}>
                      {getNutrientStatus(soilData.potassium, { min: 150, max: 300 }).status}
                    </Badge>
                  </StatHelpText>
                </Stat>

                {/* Soil Moisture */}
                <Stat>
                  <StatLabel>Soil Moisture (%)</StatLabel>
                  <StatNumber color={getNutrientStatus(soilData.soilMoisture, { min: 40, max: 70 }).color}>
                    {soilData.soilMoisture.toFixed(0)}
                  </StatNumber>
                  <StatHelpText>
                    <Badge colorScheme={getNutrientStatus(soilData.soilMoisture, { min: 40, max: 70 }).color}>
                      {getNutrientStatus(soilData.soilMoisture, { min: 40, max: 70 }).status}
                    </Badge>
                  </StatHelpText>
                </Stat>
              </SimpleGrid>
            </VStack>
          </CardBody>
        </Card>

        {/* Recommendations */}
        {recommendations && (
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody>
              <VStack spacing={6} align="stretch">
                <Heading size="md">Recommendations</Heading>
                
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                  {Object.entries(recommendations).map(([category, items]) => (
                    <Box key={category}>
                      <Heading size="sm" mb={3} textTransform="capitalize">
                        {category.replace(/([A-Z])/g, ' $1').trim()}
                      </Heading>
                      {items.length > 0 ? (
                        <VStack align="stretch" spacing={2}>
                          {items.map((item: string, index: number) => (
                            <Badge key={index} colorScheme="blue" p={2} borderRadius="md">
                              {item}
                            </Badge>
                          ))}
                        </VStack>
                      ) : (
                        <ChakraText color="gray.500" fontSize="sm">
                          No recommendations for this category
                        </ChakraText>
                      )}
                    </Box>
                  ))}
                </SimpleGrid>
              </VStack>
            </CardBody>
          </Card>
        )}
      </VStack>
    </Box>
  )
}

export default AdvancedSoilAnalysis