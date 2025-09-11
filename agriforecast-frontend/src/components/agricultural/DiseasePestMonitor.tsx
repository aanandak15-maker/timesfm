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
  TagLeftIcon
} from '@chakra-ui/react'
import {
  Bug,
  Shield,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Lock,
  RefreshCw,
  TrendingUp,
  TrendingDown,
  Minus,
  Activity,
  Zap,
  Sun
} from 'lucide-react'

interface DiseasePestData {
  field_id: string
  crop_type: string
  overall_health_score: number
  risk_level: string
  last_updated: string
  diseases: Array<{
    name: string
    incidence: number
    severity: string
    risk_level: string
    symptoms: string[]
    treatment: string[]
    prevention: string[]
    last_detected: string
    trend: string
  }>
  pests: Array<{
    name: string
    damage: number
    severity: string
    risk_level: string
    symptoms: string[]
    treatment: string[]
    prevention: string[]
    last_detected: string
    trend: string
  }>
  environmental_conditions: {
    temperature: number
    humidity: number
    rainfall: number
    wind_speed: number
    disease_favorability: number
    pest_favorability: number
  }
  treatment_history: Array<{
    date: string
    type: string
    product: string
    effectiveness: number
    notes: string
  }>
  recommendations: {
    immediate_actions: string[]
    preventive_measures: string[]
    monitoring_schedule: string[]
    treatment_plan: string[]
  }
}

const DiseasePestMonitor: React.FC = () => {
  const [monitorData, setMonitorData] = useState<DiseasePestData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isLocked] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')
  const textColor = useColorModeValue('gray.600', 'gray.300')

  // Simulate data loading
  useEffect(() => {
    const loadMonitorData = async () => {
      setIsLoading(true)
      await new Promise(resolve => setTimeout(resolve, 1800))
      
      const mockData: DiseasePestData = {
        field_id: "field_001",
        crop_type: "rice",
        overall_health_score: 88.5,
        risk_level: "low",
        last_updated: new Date().toISOString(),
        diseases: [
          {
            name: "Rice Blast",
            incidence: 5.2,
            severity: "low",
            risk_level: "medium",
            symptoms: ["Small spots on leaves", "Spindle-shaped lesions", "Gray centers"],
            treatment: ["Tricyclazole fungicide", "Azoxystrobin application", "Remove infected plants"],
            prevention: ["Resistant varieties", "Proper spacing", "Avoid excess nitrogen"],
            last_detected: "2024-08-15",
            trend: "decreasing"
          },
          {
            name: "Brown Spot",
            incidence: 2.8,
            severity: "very_low",
            risk_level: "low",
            symptoms: ["Small brown spots", "Yellow halos", "Leaf yellowing"],
            treatment: ["Copper fungicide", "Mancozeb application"],
            prevention: ["Crop rotation", "Proper drainage", "Balanced nutrition"],
            last_detected: "2024-08-10",
            trend: "stable"
          },
          {
            name: "Bacterial Blight",
            incidence: 1.5,
            severity: "very_low",
            risk_level: "low",
            symptoms: ["Water-soaked lesions", "Yellow margins", "Leaf wilting"],
            treatment: ["Copper-based bactericide", "Streptomycin application"],
            prevention: ["Clean seed", "Avoid overhead irrigation", "Proper spacing"],
            last_detected: "2024-08-05",
            trend: "decreasing"
          }
        ],
        pests: [
          {
            name: "Stem Borer",
            damage: 3.2,
            severity: "low",
            risk_level: "medium",
            symptoms: ["Dead hearts", "White heads", "Holes in stems"],
            treatment: ["Chlorantraniliprole", "Flubendiamide", "Biological control"],
            prevention: ["Early planting", "Trap crops", "Natural enemies"],
            last_detected: "2024-08-12",
            trend: "stable"
          },
          {
            name: "Brown Planthopper",
            damage: 1.8,
            severity: "very_low",
            risk_level: "low",
            symptoms: ["Yellowing leaves", "Honeydew secretion", "Sooty mold"],
            treatment: ["Imidacloprid", "Thiamethoxam", "Biological control"],
            prevention: ["Resistant varieties", "Avoid excess nitrogen", "Natural enemies"],
            last_detected: "2024-08-08",
            trend: "decreasing"
          },
          {
            name: "Aphids",
            damage: 0.5,
            severity: "very_low",
            risk_level: "low",
            symptoms: ["Curled leaves", "Stunted growth", "Honeydew"],
            treatment: ["Pyrethroid insecticides", "Biological control"],
            prevention: ["Natural enemies", "Avoid excess nitrogen", "Proper irrigation"],
            last_detected: "2024-08-03",
            trend: "decreasing"
          }
        ],
        environmental_conditions: {
          temperature: 28.5,
          humidity: 75.2,
          rainfall: 15.8,
          wind_speed: 12.5,
          disease_favorability: 35.5,
          pest_favorability: 42.3
        },
        treatment_history: [
          {
            date: "2024-08-15",
            type: "Fungicide",
            product: "Tricyclazole 75% WP",
            effectiveness: 85,
            notes: "Applied for rice blast prevention"
          },
          {
            date: "2024-08-10",
            type: "Insecticide",
            product: "Chlorantraniliprole 20% SC",
            effectiveness: 90,
            notes: "Stem borer control"
          },
          {
            date: "2024-08-05",
            type: "Biological",
            product: "Trichoderma harzianum",
            effectiveness: 70,
            notes: "Soil health improvement"
          }
        ],
        recommendations: {
          immediate_actions: [
            "Monitor for rice blast - current incidence is manageable",
            "Continue regular pest monitoring",
            "Maintain current integrated pest management practices"
          ],
          preventive_measures: [
            "Use resistant varieties for next planting",
            "Implement proper crop rotation",
            "Maintain balanced nutrition program",
            "Improve field drainage"
          ],
          monitoring_schedule: [
            "Daily visual inspection of leaves",
            "Weekly trap monitoring for pests",
            "Bi-weekly disease assessment",
            "Monthly soil health check"
          ],
          treatment_plan: [
            "Apply preventive fungicide if humidity > 80%",
            "Use biological control for minor pest issues",
            "Reserve chemical treatment for severe cases",
            "Document all treatments and effectiveness"
          ]
        }
      }
      
      setMonitorData(mockData)
      setIsLoading(false)
      setLastUpdated(new Date())
    }

    loadMonitorData()
  }, [])

  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'low':
        return 'green'
      case 'medium':
        return 'yellow'
      case 'high':
        return 'orange'
      case 'critical':
        return 'red'
      default:
        return 'gray'
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'very_low':
        return 'green'
      case 'low':
        return 'blue'
      case 'medium':
        return 'yellow'
      case 'high':
        return 'orange'
      case 'very_high':
        return 'red'
      default:
        return 'gray'
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'increasing':
        return <TrendingUp size={16} color="red" />
      case 'decreasing':
        return <TrendingDown size={16} color="green" />
      case 'stable':
        return <Minus size={16} color="gray" />
      default:
        return <Minus size={16} color="gray" />
    }
  }

  const getRiskIcon = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'low':
        return <CheckCircle size={16} color="green" />
      case 'medium':
        return <AlertTriangle size={16} color="yellow" />
      case 'high':
        return <XCircle size={16} color="orange" />
      case 'critical':
        return <XCircle size={16} color="red" />
      default:
        return <Minus size={16} color="gray" />
    }
  }

  if (isLoading) {
    return (
      <Box p={6} textAlign="center">
        <CircularProgress isIndeterminate color="blue.500" size="60px" />
        <ChakraText mt={4} color={textColor}>
          Loading disease and pest monitoring data...
        </ChakraText>
      </Box>
    )
  }

  if (!monitorData) {
    return (
      <Alert status="error">
        <AlertIcon />
        <AlertTitle>Error loading monitoring data!</AlertTitle>
        <AlertDescription>Unable to load disease and pest monitoring data.</AlertDescription>
      </Alert>
    )
  }

  return (
    <Box p={6} bg={bg} borderRadius="lg" boxShadow="lg">
      {/* Header */}
      <Flex align="center" mb={6}>
        <VStack align="start" spacing={1}>
          <HStack>
            <Heading size="lg">Disease & Pest Monitoring</Heading>
            <Badge colorScheme={getRiskColor(monitorData.risk_level)} variant="subtle">
              {monitorData.risk_level.toUpperCase()} RISK
            </Badge>
            {isLocked && (
              <Tooltip label="Advanced features locked for future development">
                <Icon as={Lock} w={4} h={4} color="gray.500" />
              </Tooltip>
            )}
          </HStack>
          <ChakraText color={textColor} fontSize="sm">
            Real-time monitoring of diseases and pests with AI-powered detection
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

      {/* Overall Health Score */}
      <Card mb={6} borderColor={borderColor}>
        <CardHeader>
          <HStack>
            <Icon as={Activity} w={5} h={5} color="blue.500" />
            <Heading size="md">Overall Crop Health</Heading>
          </HStack>
        </CardHeader>
        <CardBody>
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
            <Box textAlign="center">
              <CircularProgress
                value={monitorData.overall_health_score}
                size="80px"
                color={getRiskColor(monitorData.risk_level)}
                thickness="8px"
              >
                <CircularProgressLabel>
                  {monitorData.overall_health_score}
                </CircularProgressLabel>
              </CircularProgress>
              <ChakraText mt={2} fontWeight="bold">
                Health Score
              </ChakraText>
              <Badge colorScheme={getRiskColor(monitorData.risk_level)}>
                {monitorData.risk_level}
              </Badge>
            </Box>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Disease Favorability</ChakraText>
              <Progress
                value={monitorData.environmental_conditions.disease_favorability}
                colorScheme={monitorData.environmental_conditions.disease_favorability > 70 ? 'red' : monitorData.environmental_conditions.disease_favorability > 50 ? 'yellow' : 'green'}
                size="lg"
                w="100%"
              />
              <ChakraText fontSize="sm">{monitorData.environmental_conditions.disease_favorability}%</ChakraText>
            </VStack>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Pest Favorability</ChakraText>
              <Progress
                value={monitorData.environmental_conditions.pest_favorability}
                colorScheme={monitorData.environmental_conditions.pest_favorability > 70 ? 'red' : monitorData.environmental_conditions.pest_favorability > 50 ? 'yellow' : 'green'}
                size="lg"
                w="100%"
              />
              <ChakraText fontSize="sm">{monitorData.environmental_conditions.pest_favorability}%</ChakraText>
            </VStack>
          </SimpleGrid>
        </CardBody>
      </Card>

      {/* Comprehensive Analysis Sections */}
      <Accordion allowMultiple>
        {/* Diseases */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Shield} w={5} h={5} color="red.500" />
                <Heading size="sm">Disease Monitoring</Heading>
                <Badge colorScheme="red" variant="subtle">{monitorData.diseases.length} Diseases</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <VStack spacing={4} align="stretch">
              {monitorData.diseases.map((disease, index) => (
                <Card key={index} borderColor={borderColor}>
                  <CardHeader>
                    <HStack justify="space-between">
                      <HStack>
                        <Icon as={Shield} w={4} h={4} color="red.500" />
                        <Heading size="sm">{disease.name}</Heading>
                        <Badge colorScheme={getSeverityColor(disease.severity)} variant="subtle">
                          {disease.severity.replace('_', ' ')}
                        </Badge>
                      </HStack>
                      <HStack>
                        <Tag colorScheme={getRiskColor(disease.risk_level)}>
                          <TagLeftIcon as={() => getRiskIcon(disease.risk_level)} />
                          <TagLabel>{disease.risk_level}</TagLabel>
                        </Tag>
                        {getTrendIcon(disease.trend)}
                      </HStack>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
                      <Stat>
                        <StatLabel>Incidence</StatLabel>
                        <StatNumber>{disease.incidence}%</StatNumber>
                        <StatHelpText>
                          <StatArrow type={disease.trend === 'increasing' ? 'decrease' : 'increase'} />
                          {disease.trend}
                        </StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Severity</StatLabel>
                        <StatNumber textTransform="capitalize">
                          {disease.severity.replace('_', ' ')}
                        </StatNumber>
                        <StatHelpText>
                          {getRiskIcon(disease.risk_level)}
                          {disease.risk_level} risk
                        </StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Last Detected</StatLabel>
                        <StatNumber>{new Date(disease.last_detected).toLocaleDateString()}</StatNumber>
                        <StatHelpText>
                          <StatArrow type="decrease" />
                          Days ago
                        </StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Trend</StatLabel>
                        <StatNumber textTransform="capitalize">
                          {disease.trend}
                        </StatNumber>
                        <StatHelpText>
                          {getTrendIcon(disease.trend)}
                          vs. last week
                        </StatHelpText>
                      </Stat>
                    </SimpleGrid>
                    
                    <Divider my={4} />
                    
                    <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                      <Box>
                        <Heading size="sm" mb={2}>Symptoms</Heading>
                        <VStack spacing={1} align="stretch">
                          {disease.symptoms.map((symptom, i) => (
                            <ChakraText key={i} fontSize="sm" color={textColor}>
                              • {symptom}
                            </ChakraText>
                          ))}
                        </VStack>
                      </Box>
                      
                      <Box>
                        <Heading size="sm" mb={2}>Treatment</Heading>
                        <VStack spacing={1} align="stretch">
                          {disease.treatment.map((treatment, i) => (
                            <ChakraText key={i} fontSize="sm" color={textColor}>
                              • {treatment}
                            </ChakraText>
                          ))}
                        </VStack>
                      </Box>
                      
                      <Box>
                        <Heading size="sm" mb={2}>Prevention</Heading>
                        <VStack spacing={1} align="stretch">
                          {disease.prevention.map((prevention, i) => (
                            <ChakraText key={i} fontSize="sm" color={textColor}>
                              • {prevention}
                            </ChakraText>
                          ))}
                        </VStack>
                      </Box>
                    </SimpleGrid>
                  </CardBody>
                </Card>
              ))}
            </VStack>
          </AccordionPanel>
        </AccordionItem>

        {/* Pests */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Bug} w={5} h={5} color="orange.500" />
                <Heading size="sm">Pest Monitoring</Heading>
                <Badge colorScheme="orange" variant="subtle">{monitorData.pests.length} Pests</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <VStack spacing={4} align="stretch">
              {monitorData.pests.map((pest, index) => (
                <Card key={index} borderColor={borderColor}>
                  <CardHeader>
                    <HStack justify="space-between">
                      <HStack>
                        <Icon as={Bug} w={4} h={4} color="orange.500" />
                        <Heading size="sm">{pest.name}</Heading>
                        <Badge colorScheme={getSeverityColor(pest.severity)} variant="subtle">
                          {pest.severity.replace('_', ' ')}
                        </Badge>
                      </HStack>
                      <HStack>
                        <Tag colorScheme={getRiskColor(pest.risk_level)}>
                          <TagLeftIcon as={() => getRiskIcon(pest.risk_level)} />
                          <TagLabel>{pest.risk_level}</TagLabel>
                        </Tag>
                        {getTrendIcon(pest.trend)}
                      </HStack>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
                      <Stat>
                        <StatLabel>Damage</StatLabel>
                        <StatNumber>{pest.damage}%</StatNumber>
                        <StatHelpText>
                          <StatArrow type={pest.trend === 'increasing' ? 'decrease' : 'increase'} />
                          {pest.trend}
                        </StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Severity</StatLabel>
                        <StatNumber textTransform="capitalize">
                          {pest.severity.replace('_', ' ')}
                        </StatNumber>
                        <StatHelpText>
                          {getRiskIcon(pest.risk_level)}
                          {pest.risk_level} risk
                        </StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Last Detected</StatLabel>
                        <StatNumber>{new Date(pest.last_detected).toLocaleDateString()}</StatNumber>
                        <StatHelpText>
                          <StatArrow type="decrease" />
                          Days ago
                        </StatHelpText>
                      </Stat>
                      
                      <Stat>
                        <StatLabel>Trend</StatLabel>
                        <StatNumber textTransform="capitalize">
                          {pest.trend}
                        </StatNumber>
                        <StatHelpText>
                          {getTrendIcon(pest.trend)}
                          vs. last week
                        </StatHelpText>
                      </Stat>
                    </SimpleGrid>
                    
                    <Divider my={4} />
                    
                    <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                      <Box>
                        <Heading size="sm" mb={2}>Symptoms</Heading>
                        <VStack spacing={1} align="stretch">
                          {pest.symptoms.map((symptom, i) => (
                            <ChakraText key={i} fontSize="sm" color={textColor}>
                              • {symptom}
                            </ChakraText>
                          ))}
                        </VStack>
                      </Box>
                      
                      <Box>
                        <Heading size="sm" mb={2}>Treatment</Heading>
                        <VStack spacing={1} align="stretch">
                          {pest.treatment.map((treatment, i) => (
                            <ChakraText key={i} fontSize="sm" color={textColor}>
                              • {treatment}
                            </ChakraText>
                          ))}
                        </VStack>
                      </Box>
                      
                      <Box>
                        <Heading size="sm" mb={2}>Prevention</Heading>
                        <VStack spacing={1} align="stretch">
                          {pest.prevention.map((prevention, i) => (
                            <ChakraText key={i} fontSize="sm" color={textColor}>
                              • {prevention}
                            </ChakraText>
                          ))}
                        </VStack>
                      </Box>
                    </SimpleGrid>
                  </CardBody>
                </Card>
              ))}
            </VStack>
          </AccordionPanel>
        </AccordionItem>

        {/* Environmental Conditions */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Sun} w={5} h={5} color="yellow.500" />
                <Heading size="sm">Environmental Conditions</Heading>
                <Badge colorScheme="yellow" variant="subtle">Weather</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              <Stat>
                <StatLabel>Temperature</StatLabel>
                <StatNumber>{monitorData.environmental_conditions.temperature}°C</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Current
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Humidity</StatLabel>
                <StatNumber>{monitorData.environmental_conditions.humidity}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Relative humidity
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Rainfall</StatLabel>
                <StatNumber>{monitorData.environmental_conditions.rainfall} mm</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Last 7 days
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Wind Speed</StatLabel>
                <StatNumber>{monitorData.environmental_conditions.wind_speed} km/h</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Current
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Disease Favorability</StatLabel>
                <StatNumber>{monitorData.environmental_conditions.disease_favorability}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Conditions favor disease
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Pest Favorability</StatLabel>
                <StatNumber>{monitorData.environmental_conditions.pest_favorability}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Conditions favor pests
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Treatment History */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Zap} w={5} h={5} color="purple.500" />
                <Heading size="sm">Treatment History</Heading>
                <Badge colorScheme="purple" variant="subtle">{monitorData.treatment_history.length} Treatments</Badge>
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
                    <Th>Type</Th>
                    <Th>Product</Th>
                    <Th>Effectiveness</Th>
                    <Th>Notes</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {monitorData.treatment_history.map((treatment, index) => (
                    <Tr key={index}>
                      <Td>{new Date(treatment.date).toLocaleDateString()}</Td>
                      <Td>
                        <Badge colorScheme="blue" variant="subtle">
                          {treatment.type}
                        </Badge>
                      </Td>
                      <Td>{treatment.product}</Td>
                      <Td>
                        <HStack>
                          <ChakraText>{treatment.effectiveness}%</ChakraText>
                          <Progress
                            value={treatment.effectiveness}
                            size="sm"
                            colorScheme={treatment.effectiveness > 80 ? 'green' : treatment.effectiveness > 60 ? 'yellow' : 'red'}
                            w="50px"
                          />
                        </HStack>
                      </Td>
                      <Td>{treatment.notes}</Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </TableContainer>
          </AccordionPanel>
        </AccordionItem>

        {/* Recommendations */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={CheckCircle} w={5} h={5} color="green.500" />
                <Heading size="sm">Recommendations</Heading>
                <Badge colorScheme="green" variant="subtle">Action Plan</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
              <Box>
                <Heading size="sm" mb={3}>Immediate Actions</Heading>
                <VStack spacing={2} align="stretch">
                  {monitorData.recommendations.immediate_actions.map((action, index) => (
                    <Alert key={index} status="info" size="sm">
                      <AlertIcon />
                      <AlertDescription>{action}</AlertDescription>
                    </Alert>
                  ))}
                </VStack>
              </Box>
              
              <Box>
                <Heading size="sm" mb={3}>Preventive Measures</Heading>
                <VStack spacing={2} align="stretch">
                  {monitorData.recommendations.preventive_measures.map((measure, index) => (
                    <Alert key={index} status="success" size="sm">
                      <AlertIcon />
                      <AlertDescription>{measure}</AlertDescription>
                    </Alert>
                  ))}
                </VStack>
              </Box>
              
              <Box>
                <Heading size="sm" mb={3}>Monitoring Schedule</Heading>
                <VStack spacing={2} align="stretch">
                  {monitorData.recommendations.monitoring_schedule.map((schedule, index) => (
                    <Alert key={index} status="warning" size="sm">
                      <AlertIcon />
                      <AlertDescription>{schedule}</AlertDescription>
                    </Alert>
                  ))}
                </VStack>
              </Box>
              
              <Box>
                <Heading size="sm" mb={3}>Treatment Plan</Heading>
                <VStack spacing={2} align="stretch">
                  {monitorData.recommendations.treatment_plan.map((plan, index) => (
                    <Alert key={index} status="error" size="sm">
                      <AlertIcon />
                      <AlertDescription>{plan}</AlertDescription>
                    </Alert>
                  ))}
                </VStack>
              </Box>
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
            This comprehensive disease and pest monitoring system is currently in development. 
            Advanced features will be unlocked in future updates.
          </AlertDescription>
        </Alert>
      )}
    </Box>
  )
}

export default DiseasePestMonitor
