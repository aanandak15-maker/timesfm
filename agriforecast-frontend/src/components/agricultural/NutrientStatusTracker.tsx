import React, { useState, useEffect } from 'react'
import {
  Box,
  VStack,
  HStack,
  Text as ChakraText,
  Heading,
  Badge,
  Progress,
  SimpleGrid,
  Card,
  CardBody,
  CardHeader,
  Divider,
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
  Tag,
  TagLabel,
  TagLeftIcon,
} from '@chakra-ui/react'
import {
  Leaf,
  Droplets,
  Zap,
  TrendingUp,
  TrendingDown,
  Minus,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Lock,
  RefreshCw,
  Activity,
  Calendar,
  Target
} from 'lucide-react'

interface NutrientStatusData {
  field_id: string
  crop_type: string
  last_updated: string
  macronutrients: {
    nitrogen: {
      status: string
      level: number
      optimal_range: [number, number]
      trend: string
      last_application: string
      next_application: string
      efficiency: number
    }
    phosphorus: {
      status: string
      level: number
      optimal_range: [number, number]
      trend: string
      last_application: string
      next_application: string
      efficiency: number
    }
    potassium: {
      status: string
      level: number
      optimal_range: [number, number]
      trend: string
      last_application: string
      next_application: string
      efficiency: number
    }
  }
  micronutrients: {
    iron: { status: string; level: number; optimal_range: [number, number] }
    zinc: { status: string; level: number; optimal_range: [number, number] }
    manganese: { status: string; level: number; optimal_range: [number, number] }
    copper: { status: string; level: number; optimal_range: [number, number] }
    boron: { status: string; level: number; optimal_range: [number, number] }
    molybdenum: { status: string; level: number; optimal_range: [number, number] }
  }
  soil_analysis: {
    ph: number
    organic_matter: number
    cation_exchange_capacity: number
    base_saturation: number
    electrical_conductivity: number
    carbon_nitrogen_ratio: number
  }
  fertilizer_recommendations: Array<{
    nutrient: string
    amount: number
    unit: string
    timing: string
    method: string
    priority: string
    notes: string
  }>
  application_history: Array<{
    date: string
    nutrient: string
    product: string
    amount: number
    unit: string
    method: string
    effectiveness: number
    notes: string
  }>
  nutrient_use_efficiency: {
    overall: number
    nitrogen: number
    phosphorus: number
    potassium: number
    trend: string
  }
  soil_health_indicators: {
    microbial_activity: number
    enzyme_activity: number
    organic_matter_decomposition: number
    nutrient_mineralization: number
  }
}

const NutrientStatusTracker: React.FC = () => {
  const [nutrientData, setNutrientData] = useState<NutrientStatusData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isLocked] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')
  const textColor = useColorModeValue('gray.600', 'gray.300')

  // Simulate data loading
  useEffect(() => {
    const loadNutrientData = async () => {
      setIsLoading(true)
      await new Promise(resolve => setTimeout(resolve, 1600))
      
      const mockData: NutrientStatusData = {
        field_id: "field_001",
        crop_type: "rice",
        last_updated: new Date().toISOString(),
        macronutrients: {
          nitrogen: {
            status: "adequate",
            level: 125.5,
            optimal_range: [100, 150],
            trend: "stable",
            last_application: "2024-08-10",
            next_application: "2024-09-15",
            efficiency: 78.5
          },
          phosphorus: {
            status: "adequate",
            level: 28.3,
            optimal_range: [20, 40],
            trend: "increasing",
            last_application: "2024-08-05",
            next_application: "2024-09-20",
            efficiency: 82.3
          },
          potassium: {
            status: "adequate",
            level: 285.7,
            optimal_range: [200, 350],
            trend: "stable",
            last_application: "2024-08-08",
            next_application: "2024-09-25",
            efficiency: 75.8
          }
        },
        micronutrients: {
          iron: { status: "adequate", level: 125.5, optimal_range: [50, 200] },
          zinc: { status: "deficient", level: 4.2, optimal_range: [5, 15] },
          manganese: { status: "adequate", level: 65.8, optimal_range: [20, 100] },
          copper: { status: "adequate", level: 2.1, optimal_range: [1, 5] },
          boron: { status: "deficient", level: 1.8, optimal_range: [2, 5] },
          molybdenum: { status: "adequate", level: 0.8, optimal_range: [0.5, 2] }
        },
        soil_analysis: {
          ph: 6.8,
          organic_matter: 3.2,
          cation_exchange_capacity: 18.5,
          base_saturation: 75.2,
          electrical_conductivity: 1.8,
          carbon_nitrogen_ratio: 12.3
        },
        fertilizer_recommendations: [
          {
            nutrient: "Zinc",
            amount: 2.5,
            unit: "kg/ha",
            timing: "Immediate",
            method: "Foliar spray",
            priority: "High",
            notes: "Apply zinc sulfate for deficiency correction"
          },
          {
            nutrient: "Boron",
            amount: 1.5,
            unit: "kg/ha",
            timing: "Next 7 days",
            method: "Soil application",
            priority: "High",
            notes: "Apply borax to improve grain quality"
          },
          {
            nutrient: "Nitrogen",
            amount: 25,
            unit: "kg/ha",
            timing: "Next 2 weeks",
            method: "Split application",
            priority: "Medium",
            notes: "Top-dress for grain filling stage"
          },
          {
            nutrient: "Phosphorus",
            amount: 15,
            unit: "kg/ha",
            timing: "Next 3 weeks",
            method: "Band placement",
            priority: "Low",
            notes: "Maintain current P levels"
          }
        ],
        application_history: [
          {
            date: "2024-08-10",
            nutrient: "Nitrogen",
            product: "Urea 46%",
            amount: 30,
            unit: "kg/ha",
            method: "Top-dress",
            effectiveness: 85,
            notes: "Applied during tillering stage"
          },
          {
            date: "2024-08-05",
            nutrient: "Phosphorus",
            product: "DAP 18-46-0",
            amount: 20,
            unit: "kg/ha",
            method: "Band placement",
            effectiveness: 90,
            notes: "Applied at planting"
          },
          {
            date: "2024-08-08",
            nutrient: "Potassium",
            product: "MOP 60%",
            amount: 25,
            unit: "kg/ha",
            method: "Broadcast",
            effectiveness: 80,
            notes: "Applied during stem elongation"
          },
          {
            date: "2024-08-12",
            nutrient: "Zinc",
            product: "Zinc Sulfate",
            amount: 2,
            unit: "kg/ha",
            method: "Foliar spray",
            effectiveness: 75,
            notes: "Corrected zinc deficiency"
          }
        ],
        nutrient_use_efficiency: {
          overall: 78.5,
          nitrogen: 78.5,
          phosphorus: 82.3,
          potassium: 75.8,
          trend: "increasing"
        },
        soil_health_indicators: {
          microbial_activity: 85.2,
          enzyme_activity: 78.5,
          organic_matter_decomposition: 82.1,
          nutrient_mineralization: 76.8
        }
      }
      
      setNutrientData(mockData)
      setIsLoading(false)
      setLastUpdated(new Date())
    }

    loadNutrientData()
  }, [])

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'adequate':
      case 'optimal':
        return 'green'
      case 'deficient':
      case 'low':
        return 'red'
      case 'excessive':
      case 'high':
        return 'orange'
      case 'marginal':
        return 'yellow'
      default:
        return 'gray'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'adequate':
      case 'optimal':
        return <CheckCircle size={16} color="green" />
      case 'deficient':
      case 'low':
        return <XCircle size={16} color="red" />
      case 'excessive':
      case 'high':
        return <AlertTriangle size={16} color="orange" />
      case 'marginal':
        return <Minus size={16} color="yellow" />
      default:
        return <Minus size={16} color="gray" />
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'increasing':
        return <TrendingUp size={16} color="green" />
      case 'decreasing':
        return <TrendingDown size={16} color="red" />
      case 'stable':
        return <Minus size={16} color="gray" />
      default:
        return <Minus size={16} color="gray" />
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'red'
      case 'medium':
        return 'yellow'
      case 'low':
        return 'green'
      default:
        return 'gray'
    }
  }

  const isInOptimalRange = (level: number, range: [number, number]) => {
    return level >= range[0] && level <= range[1]
  }

  if (isLoading) {
    return (
      <Box p={6} textAlign="center">
        <CircularProgress isIndeterminate color="blue.500" size="60px" />
        <ChakraText mt={4} color={textColor}>
          Loading nutrient status data...
        </ChakraText>
      </Box>
    )
  }

  if (!nutrientData) {
    return (
      <Alert status="error">
        <AlertIcon />
        <AlertTitle>Error loading nutrient data!</AlertTitle>
        <AlertDescription>Unable to load nutrient status tracking data.</AlertDescription>
      </Alert>
    )
  }

  return (
    <Box p={6} bg={bg} borderRadius="lg" boxShadow="lg">
      {/* Header */}
      <Flex align="center" mb={6}>
        <VStack align="start" spacing={1}>
          <HStack>
            <Heading size="lg">Nutrient Status Tracking</Heading>
            <Badge colorScheme="blue" variant="subtle">Comprehensive</Badge>
            {isLocked && (
              <Tooltip label="Advanced features locked for future development">
                <Icon as={Lock} w={4} h={4} color="gray.500" />
              </Tooltip>
            )}
          </HStack>
          <ChakraText color={textColor} fontSize="sm">
            Real-time monitoring of soil nutrients and fertilizer recommendations
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

      {/* Overall Nutrient Efficiency */}
      <Card mb={6} borderColor={borderColor}>
        <CardHeader>
          <HStack>
            <Icon as={Target} w={5} h={5} color="blue.500" />
            <Heading size="md">Nutrient Use Efficiency</Heading>
          </HStack>
        </CardHeader>
        <CardBody>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
            <Box textAlign="center">
              <CircularProgress
                value={nutrientData.nutrient_use_efficiency.overall}
                size="80px"
                color="blue.500"
                thickness="8px"
              >
                <CircularProgressLabel>
                  {nutrientData.nutrient_use_efficiency.overall}%
                </CircularProgressLabel>
              </CircularProgress>
              <ChakraText mt={2} fontWeight="bold">
                Overall Efficiency
              </ChakraText>
              <ChakraText fontSize="sm" color={textColor}>
                {getTrendIcon(nutrientData.nutrient_use_efficiency.trend)}
                {nutrientData.nutrient_use_efficiency.trend}
              </ChakraText>
            </Box>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Nitrogen Efficiency</ChakraText>
              <Progress
                value={nutrientData.nutrient_use_efficiency.nitrogen}
                colorScheme="blue"
                size="lg"
                w="100%"
              />
              <ChakraText fontSize="sm">{nutrientData.nutrient_use_efficiency.nitrogen}%</ChakraText>
            </VStack>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Phosphorus Efficiency</ChakraText>
              <Progress
                value={nutrientData.nutrient_use_efficiency.phosphorus}
                colorScheme="green"
                size="lg"
                w="100%"
              />
              <ChakraText fontSize="sm">{nutrientData.nutrient_use_efficiency.phosphorus}%</ChakraText>
            </VStack>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Potassium Efficiency</ChakraText>
              <Progress
                value={nutrientData.nutrient_use_efficiency.potassium}
                colorScheme="orange"
                size="lg"
                w="100%"
              />
              <ChakraText fontSize="sm">{nutrientData.nutrient_use_efficiency.potassium}%</ChakraText>
            </VStack>
          </SimpleGrid>
        </CardBody>
      </Card>

      {/* Comprehensive Analysis Sections */}
      <Accordion allowMultiple>
        {/* Macronutrients */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Leaf} w={5} h={5} color="green.500" />
                <Heading size="sm">Macronutrients</Heading>
                <Badge colorScheme="green" variant="subtle">N-P-K</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
              {Object.entries(nutrientData.macronutrients).map(([nutrient, data]) => (
                <Card key={nutrient} borderColor={borderColor}>
                  <CardHeader>
                    <HStack justify="space-between">
                      <Heading size="sm" textTransform="capitalize">{nutrient}</Heading>
                      <Tag colorScheme={getStatusColor(data.status)}>
                        <TagLeftIcon as={() => getStatusIcon(data.status)} />
                        <TagLabel>{data.status}</TagLabel>
                      </Tag>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <VStack spacing={3} align="stretch">
                      <Stat>
                        <StatLabel>Current Level</StatLabel>
                        <StatNumber>{data.level} ppm</StatNumber>
                        <StatHelpText>
                          Optimal: {data.optimal_range[0]}-{data.optimal_range[1]} ppm
                        </StatHelpText>
                      </Stat>
                      
                      <Box>
                        <HStack justify="space-between" mb={2}>
                          <ChakraText fontSize="sm">Level Status</ChakraText>
                          <ChakraText fontSize="sm" color={isInOptimalRange(data.level, data.optimal_range) ? 'green.500' : 'red.500'}>
                            {isInOptimalRange(data.level, data.optimal_range) ? 'In Range' : 'Out of Range'}
                          </ChakraText>
                        </HStack>
                        <Progress
                          value={Math.min(100, (data.level / data.optimal_range[1]) * 100)}
                          colorScheme={isInOptimalRange(data.level, data.optimal_range) ? 'green' : 'red'}
                          size="sm"
                        />
                      </Box>
                      
                      <Stat>
                        <StatLabel>Efficiency</StatLabel>
                        <StatNumber>{data.efficiency}%</StatNumber>
                        <StatHelpText>
                          <StatArrow type="increase" />
                          Nutrient utilization
                        </StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Trend</StatLabel>
                        <StatNumber textTransform="capitalize">
                          {data.trend}
                        </StatNumber>
                        <StatHelpText>
                          {getTrendIcon(data.trend)}
                          vs. last month
                        </StatHelpText>
                      </Stat>
                      
                      <Divider />
                      
                      <VStack spacing={2} align="stretch">
                        <ChakraText fontSize="sm" fontWeight="bold">Application Schedule</ChakraText>
                        <ChakraText fontSize="sm" color={textColor}>
                          Last: {new Date(data.last_application).toLocaleDateString()}
                        </ChakraText>
                        <ChakraText fontSize="sm" color={textColor}>
                          Next: {new Date(data.next_application).toLocaleDateString()}
                        </ChakraText>
                      </VStack>
                    </VStack>
                  </CardBody>
                </Card>
              ))}
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Micronutrients */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Zap} w={5} h={5} color="purple.500" />
                <Heading size="sm">Micronutrients</Heading>
                <Badge colorScheme="purple" variant="subtle">Trace Elements</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 2, md: 3, lg: 6 }} spacing={4}>
              {Object.entries(nutrientData.micronutrients).map(([nutrient, data]) => (
                <Card key={nutrient} borderColor={borderColor}>
                  <CardBody>
                    <VStack spacing={2}>
                      <Heading size="sm" textTransform="capitalize">{nutrient}</Heading>
                      <Tag colorScheme={getStatusColor(data.status)} size="sm">
                        <TagLeftIcon as={() => getStatusIcon(data.status)} />
                        <TagLabel>{data.status}</TagLabel>
                      </Tag>
                      <ChakraText fontSize="lg" fontWeight="bold">
                        {data.level} ppm
                      </ChakraText>
                      <ChakraText fontSize="sm" color={textColor} textAlign="center">
                        Range: {data.optimal_range[0]}-{data.optimal_range[1]} ppm
                      </ChakraText>
                      <Progress
                        value={Math.min(100, (data.level / data.optimal_range[1]) * 100)}
                        colorScheme={isInOptimalRange(data.level, data.optimal_range) ? 'green' : 'red'}
                        size="sm"
                        w="100%"
                      />
                    </VStack>
                  </CardBody>
                </Card>
              ))}
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Soil Analysis */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Droplets} w={5} h={5} color="blue.500" />
                <Heading size="sm">Soil Analysis</Heading>
                <Badge colorScheme="blue" variant="subtle">Lab Results</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              <Stat>
                <StatLabel>pH Level</StatLabel>
                <StatNumber>{nutrientData.soil_analysis.ph}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Optimal: 6.0-7.5
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Organic Matter</StatLabel>
                <StatNumber>{nutrientData.soil_analysis.organic_matter}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Higher is better
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>CEC</StatLabel>
                <StatNumber>{nutrientData.soil_analysis.cation_exchange_capacity} meq/100g</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Nutrient holding capacity
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Base Saturation</StatLabel>
                <StatNumber>{nutrientData.soil_analysis.base_saturation}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Cation saturation
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>EC</StatLabel>
                <StatNumber>{nutrientData.soil_analysis.electrical_conductivity} dS/m</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Salt content
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>C:N Ratio</StatLabel>
                <StatNumber>{nutrientData.soil_analysis.carbon_nitrogen_ratio}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Carbon to nitrogen
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Fertilizer Recommendations */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Target} w={5} h={5} color="orange.500" />
                <Heading size="sm">Fertilizer Recommendations</Heading>
                <Badge colorScheme="orange" variant="subtle">{nutrientData.fertilizer_recommendations.length} Recommendations</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <VStack spacing={4} align="stretch">
              {nutrientData.fertilizer_recommendations.map((recommendation, index) => (
                <Card key={index} borderColor={borderColor}>
                  <CardHeader>
                    <HStack justify="space-between">
                      <Heading size="sm">{recommendation.nutrient}</Heading>
                      <Tag colorScheme={getPriorityColor(recommendation.priority)}>
                        <TagLabel>{recommendation.priority} Priority</TagLabel>
                      </Tag>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
                      <Stat>
                        <StatLabel>Amount</StatLabel>
                        <StatNumber>{recommendation.amount} {recommendation.unit}</StatNumber>
                        <StatHelpText>Application rate</StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Timing</StatLabel>
                        <StatNumber fontSize="md">{recommendation.timing}</StatNumber>
                        <StatHelpText>When to apply</StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Method</StatLabel>
                        <StatNumber fontSize="md">{recommendation.method}</StatNumber>
                        <StatHelpText>Application method</StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Notes</StatLabel>
                        <StatNumber fontSize="sm" color={textColor}>
                          {recommendation.notes}
                        </StatNumber>
                      </Stat>
                    </SimpleGrid>
                  </CardBody>
                </Card>
              ))}
            </VStack>
          </AccordionPanel>
        </AccordionItem>

        {/* Application History */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Calendar} w={5} h={5} color="teal.500" />
                <Heading size="sm">Application History</Heading>
                <Badge colorScheme="teal" variant="subtle">{nutrientData.application_history.length} Applications</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <TableContainer>
              <Table variant="simple" size="sm">
                <Thead>
                  <Tr>
                    <Th>Date</Th>
                    <Th>Nutrient</Th>
                    <Th>Product</Th>
                    <Th>Amount</Th>
                    <Th>Method</Th>
                    <Th>Effectiveness</Th>
                    <Th>Notes</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {nutrientData.application_history.map((application, index) => (
                    <Tr key={index}>
                      <Td>{new Date(application.date).toLocaleDateString()}</Td>
                      <Td>
                        <Badge colorScheme="blue" variant="subtle">
                          {application.nutrient}
                        </Badge>
                      </Td>
                      <Td>{application.product}</Td>
                      <Td>{application.amount} {application.unit}</Td>
                      <Td>{application.method}</Td>
                      <Td>
                        <HStack>
                          <ChakraText>{application.effectiveness}%</ChakraText>
                          <Progress
                            value={application.effectiveness}
                            size="sm"
                            colorScheme={application.effectiveness > 80 ? 'green' : application.effectiveness > 60 ? 'yellow' : 'red'}
                            w="50px"
                          />
                        </HStack>
                      </Td>
                      <Td>{application.notes}</Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </TableContainer>
          </AccordionPanel>
        </AccordionItem>

        {/* Soil Health Indicators */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Activity} w={5} h={5} color="green.500" />
                <Heading size="sm">Soil Health Indicators</Heading>
                <Badge colorScheme="green" variant="subtle">Biological</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
              <Stat>
                <StatLabel>Microbial Activity</StatLabel>
                <StatNumber>{nutrientData.soil_health_indicators.microbial_activity}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Soil biology
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Enzyme Activity</StatLabel>
                <StatNumber>{nutrientData.soil_health_indicators.enzyme_activity}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Biochemical processes
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>OM Decomposition</StatLabel>
                <StatNumber>{nutrientData.soil_health_indicators.organic_matter_decomposition}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Organic matter breakdown
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>N Mineralization</StatLabel>
                <StatNumber>{nutrientData.soil_health_indicators.nutrient_mineralization}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Nutrient release
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>
      </Accordion>

      {/* Lock Notice */}
      {isLocked && (
        <Alert status="info" mt={6}>
          <AlertIcon />
          <AlertTitle>Advanced Features Locked</AlertTitle>
          <AlertDescription>
            This comprehensive nutrient status tracking system is currently in development. 
            Advanced features will be unlocked in future updates.
          </AlertDescription>
        </Alert>
      )}
    </Box>
  )
}

export default NutrientStatusTracker
