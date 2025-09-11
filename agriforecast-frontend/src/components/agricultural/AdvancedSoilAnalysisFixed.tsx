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
  Spacer
} from '@chakra-ui/react'
import {
  Droplets,
  Activity,
  Microscope,
  Satellite,
  Wifi,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Lock,
  RefreshCw,
  TrendingUp,
  Minus
} from 'lucide-react'
import { soilgridsApi } from '../../services/soilgridsApi'

interface SoilData {
  ph: number
  organic_carbon: number
  nitrogen: number
  phosphorus: number
  potassium: number
  bulk_density: number
  moisture: number
  temperature: number
  source: string
}

const AdvancedSoilAnalysisFixed = () => {
  const [soilData, setSoilData] = useState<SoilData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')
  const textColor = useColorModeValue('gray.600', 'gray.300')

  useEffect(() => {
    const loadSoilData = async () => {
      setIsLoading(true)
      
      try {
        console.log('🌱 Fetching real soil data from SoilGrids (FREE)...')
        const data = await soilgridsApi.getSoilData(28.3477, 77.5573)
        
        const transformedData: SoilData = {
          ph: data.ph,
          organic_carbon: data.organic_carbon,
          nitrogen: data.nitrogen,
          phosphorus: data.phosphorus,
          potassium: data.potassium,
          bulk_density: data.bulk_density,
          moisture: 35 + Math.random() * 20, // Not available in SoilGrids
          temperature: 22 + Math.random() * 8, // Not available in SoilGrids
          source: data.source
        }
        
        setSoilData(transformedData)
        setLastUpdated(new Date())
        console.log('✅ Real soil data loaded successfully')
      } catch (error) {
        console.error('Error loading soil data:', error)
        
        // Fallback to demo data
        const demoData: SoilData = {
          ph: 6.5 + Math.random() * 1.0,
          organic_carbon: 2.0 + Math.random() * 1.5,
          nitrogen: 100 + Math.random() * 50,
          phosphorus: 20 + Math.random() * 20,
          potassium: 150 + Math.random() * 100,
          bulk_density: 1.3 + Math.random() * 0.3,
          moisture: 35 + Math.random() * 20,
          temperature: 22 + Math.random() * 8,
          source: 'Demo Data'
        }
        
        setSoilData(demoData)
        setLastUpdated(new Date())
      } finally {
        setIsLoading(false)
      }
    }

    loadSoilData()
  }, [])

  const getHealthColor = (value: number, type: string) => {
    switch (type) {
      case 'ph':
        if (value >= 6.0 && value <= 7.5) return 'green'
        if (value >= 5.5 && value <= 8.0) return 'yellow'
        return 'red'
      case 'organic_carbon':
        if (value >= 2.0) return 'green'
        if (value >= 1.0) return 'yellow'
        return 'red'
      case 'nitrogen':
        if (value >= 100) return 'green'
        if (value >= 50) return 'yellow'
        return 'red'
      default:
        return 'gray'
    }
  }

  if (isLoading) {
    return (
      <Box p={6} borderRadius="xl" border="1px" borderColor={borderColor} bg={bg}>
        <VStack spacing={4}>
          <Heading size="md">Loading Soil Analysis...</Heading>
          <CircularProgress isIndeterminate color="green.400" />
          <ChakraText>Fetching real soil data from SoilGrids...</ChakraText>
        </VStack>
      </Box>
    )
  }

  if (!soilData) {
    return (
      <Box p={6} borderRadius="xl" border="1px" borderColor={borderColor} bg={bg}>
        <Alert status="error">
          <AlertIcon />
          <AlertTitle>Soil Data Unavailable</AlertTitle>
          <AlertDescription>Unable to load soil analysis data.</AlertDescription>
        </Alert>
      </Box>
    )
  }

  return (
    <Box p={6} borderRadius="xl" border="1px" borderColor={borderColor} bg={bg}>
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <HStack justify="space-between">
          <HStack>
            <Icon as={Activity} color="green.500" />
            <Heading size="md">Advanced Soil Analysis</Heading>
            <Badge colorScheme="green" variant="subtle">
              {soilData.source.includes('SoilGrids') ? 'Real Data' : 'Demo Data'}
            </Badge>
          </HStack>
          <HStack>
            <Icon as={Lock} color="orange.500" />
            <ChakraText fontSize="sm" color="orange.500">
              Advanced Features Locked
            </ChakraText>
          </HStack>
        </HStack>

        {/* Main Metrics */}
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
          <Card>
            <CardBody>
              <Stat>
                <StatLabel>pH Level</StatLabel>
                <StatNumber color={`${getHealthColor(soilData.ph, 'ph')}.500`}>
                  {soilData.ph.toFixed(1)}
                </StatNumber>
                <StatHelpText>
                  {soilData.ph >= 6.0 && soilData.ph <= 7.5 ? 'Optimal' : 'Needs attention'}
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <Stat>
                <StatLabel>Organic Carbon</StatLabel>
                <StatNumber color={`${getHealthColor(soilData.organic_carbon, 'organic_carbon')}.500`}>
                  {soilData.organic_carbon.toFixed(1)}%
                </StatNumber>
                <StatHelpText>
                  {soilData.organic_carbon >= 2.0 ? 'Good' : 'Low'}
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <Stat>
                <StatLabel>Nitrogen</StatLabel>
                <StatNumber color={`${getHealthColor(soilData.nitrogen, 'nitrogen')}.500`}>
                  {soilData.nitrogen.toFixed(0)} mg/kg
                </StatNumber>
                <StatHelpText>
                  {soilData.nitrogen >= 100 ? 'Adequate' : 'Deficient'}
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <Stat>
                <StatLabel>Phosphorus</StatLabel>
                <StatNumber>{soilData.phosphorus.toFixed(0)} mg/kg</StatNumber>
                <StatHelpText>Available P</StatHelpText>
              </Stat>
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <Stat>
                <StatLabel>Potassium</StatLabel>
                <StatNumber>{soilData.potassium.toFixed(0)} mg/kg</StatNumber>
                <StatHelpText>Available K</StatHelpText>
              </Stat>
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <Stat>
                <StatLabel>Bulk Density</StatLabel>
                <StatNumber>{soilData.bulk_density.toFixed(2)} g/cm³</StatNumber>
                <StatHelpText>Soil compaction</StatHelpText>
              </Stat>
            </CardBody>
          </Card>
        </SimpleGrid>

        {/* Data Source */}
        <Alert status="info">
          <AlertIcon />
          <AlertTitle>Data Source: {soilData.source}</AlertTitle>
          <AlertDescription>
            {soilData.source.includes('SoilGrids') 
              ? 'Real global soil data from ISRIC - completely free, no API key required!'
              : 'Demo data - sign up for real agricultural APIs to get actual soil data.'
            }
          </AlertDescription>
        </Alert>

        {/* Last Updated */}
        {lastUpdated && (
          <HStack justify="space-between">
            <ChakraText fontSize="sm" color={textColor}>
              Last updated: {lastUpdated.toLocaleString()}
            </ChakraText>
            <Button
              size="sm"
              leftIcon={<Icon as={RefreshCw} />}
              onClick={() => window.location.reload()}
            >
              Refresh
            </Button>
          </HStack>
        )}
      </VStack>
    </Box>
  )
}

export default AdvancedSoilAnalysisFixed
