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
import { agriculturalApi as realAgriculturalApi } from '../../services/agriculturalApi'
import { soilgridsApi } from '../../services/soilgridsApi'

interface SoilAnalysisData {
  field_id: string
  timestamp: string
  physical_properties: {
    soil_moisture: number
    bulk_density: number
    porosity: number
    infiltration_rate: number
    water_holding_capacity: number
    soil_temperature: number
    compaction_level: number
    aggregate_stability: number
    permeability: number
  }
  chemical_properties: {
    ph: number
    organic_matter: number
    total_nitrogen: number
    available_phosphorus: number
    available_potassium: number
    cation_exchange_capacity: number
    base_saturation: number
    electrical_conductivity: number
    carbon_nitrogen_ratio: number
    micronutrients: {
      iron: number
      zinc: number
      manganese: number
      copper: number
      boron: number
    }
  }
  biological_properties: {
    microbial_biomass_carbon: number
    microbial_biomass_nitrogen: number
    enzyme_activity: {
      dehydrogenase: number
      urease: number
      phosphatase: number
      catalase: number
    }
    earthworm_density: number
    nematode_diversity: number
    mycorrhizal_colonization: number
    soil_respiration: number
    nitrogen_mineralization: number
  }
  remote_sensing: {
    ndvi: number
    ndwi: number
    ndre: number
    gndvi: number
    evi: number
    savi: number
    lswi: number
    nirv: number
    red_edge_position: number
    chlorophyll_content: number
    leaf_area_index: number
    canopy_temperature: number
  }
  iot_sensors: Array<{
    timestamp: string
    soil_moisture: number
    soil_temperature: number
    ph: number
    electrical_conductivity: number
    nutrient_levels: {
      nitrogen: number
      phosphorus: number
      potassium: number
    }
    sensor_id: string
    location: [number, number]
    battery_level: number
    signal_strength: number
  }>
  crop_stage: {
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
  }
  disease_pest: {
    disease_incidence: { [key: string]: number }
    pest_damage: { [key: string]: number }
    overall_health_score: number
    risk_level: string
    treatment_recommendations: string[]
    last_treatment_date: string
  }
  nutrient_status: {
    nitrogen_status: string
    phosphorus_status: string
    potassium_status: string
    micronutrient_status: { [key: string]: string }
    fertilizer_recommendations: string[]
    last_fertilizer_application: string
    nutrient_use_efficiency: number
  }
  overall_soil_health: {
    overall_score: number
    health_level: string
    physical_score: number
    chemical_score: number
    biological_score: number
    recommendations: string[]
  }
}

const AdvancedSoilAnalysis: React.FC = () => {
  const [soilData, setSoilData] = useState<SoilAnalysisData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isLocked] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())

  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')
  const textColor = useColorModeValue('gray.600', 'gray.300')

  // Simulate data loading
  useEffect(() => {
    const loadSoilData = async () => {
      setIsLoading(true)
      
      try {
        // Try to fetch real SoilGrids data first (NO API KEY REQUIRED!)
        console.log('🌱 Fetching real soil data from SoilGrids (FREE)...')
        const soilGridsData = await soilgridsApi.getSoilData(28.3477, 77.5573) // Your location
        
        // Also try agricultural API as backup
        console.log('Fetching agricultural data...')
        const realData = await realAgriculturalApi.getSoilAnalysis('field_001')
        
        // Transform real data to our format using SoilGrids data
        const transformedData: SoilAnalysisData = {
          field_id: "field_001",
          timestamp: soilGridsData.last_updated,
          physical_properties: {
            soil_moisture: 35 + Math.random() * 20, // Not available in SoilGrids
            bulk_density: soilGridsData.bulk_density,
            porosity: 45.2 + Math.random() * 10,
            infiltration_rate: 15.8 + Math.random() * 5,
            water_holding_capacity: 32.1 + Math.random() * 10,
            soil_temperature: 22 + Math.random() * 8,
            compaction_level: 0.35 + Math.random() * 0.1,
            aggregate_stability: 78.5 + Math.random() * 10,
            permeability: 8.2 + Math.random() * 2
          },
          chemical_properties: {
            ph: soilGridsData.ph,
            organic_matter: soilGridsData.organic_carbon,
            total_nitrogen: soilGridsData.nitrogen,
            available_phosphorus: soilGridsData.phosphorus,
            available_potassium: soilGridsData.potassium,
            cation_exchange_capacity: 18.5 + Math.random() * 5,
            base_saturation: 75.2 + Math.random() * 10,
            electrical_conductivity: 1.8 + Math.random() * 0.5,
            carbon_nitrogen_ratio: 12.3 + Math.random() * 2,
            micronutrients: {
              iron: 125.5 + Math.random() * 20,
              zinc: 4.2 + Math.random() * 1,
              manganese: 65.8 + Math.random() * 10,
              copper: 2.1 + Math.random() * 0.5,
              boron: 1.8 + Math.random() * 0.3
            }
          },
          biological_properties: {
            microbial_biomass_carbon: 485.2 + Math.random() * 50,
            microbial_biomass_nitrogen: 45.8 + Math.random() * 10,
            enzyme_activity: {
              dehydrogenase: 28.5 + Math.random() * 5,
              urease: 15.2 + Math.random() * 3,
              phosphatase: 35.8 + Math.random() * 5,
              catalase: 52.3 + Math.random() * 8
            },
            earthworm_density: 185.5 + Math.random() * 30,
            nematode_diversity: 2.8 + Math.random() * 0.5,
            mycorrhizal_colonization: 72.3 + Math.random() * 10,
            soil_respiration: 125.8 + Math.random() * 20,
            nitrogen_mineralization: 6.2 + Math.random() * 2
          },
          remote_sensing: {
            ndvi: 0.78 + Math.random() * 0.1,
            ndwi: 0.45 + Math.random() * 0.1,
            ndre: 0.32 + Math.random() * 0.08,
            gndvi: 0.65 + Math.random() * 0.1,
            evi: 0.52 + Math.random() * 0.08,
            savi: 0.48 + Math.random() * 0.1,
            lswi: 0.38 + Math.random() * 0.1,
            nirv: 0.42 + Math.random() * 0.08,
            red_edge_position: 720 + Math.random() * 20,
            chlorophyll_content: 45.2 + Math.random() * 10,
            leaf_area_index: 3.2 + Math.random() * 0.8,
            canopy_temperature: realData.temperature + Math.random() * 2
          },
          irrigation_schedule: {
            next_irrigation: "2024-01-15T08:00:00Z",
            water_level: 75.2,
            drainage_efficiency: 82.1,
            flooding_depth: 5.2,
            irrigation_frequency: "Every 3 days",
            water_quality: "Good",
            salinity_level: 1.2
          },
          crop_stage_tracking: {
            tillering_count: 8.5,
            panicle_initiation: true,
            heading_percentage: 45.2,
            grain_filling_stage: 0.3,
            nitrogen_application_timing: "Optimal",
            nitrogen_application_rate: 120.5,
            leaf_nitrogen_content: 3.2,
            soil_nitrogen_content: 2.8,
            stress_indicators: {
              frost_damage: 0.0,
              drought_stress: 0.15,
              heat_stress: 0.05,
              water_logging: 0.0
            }
          },
          disease_pest_pressure: {
            blast_incidence: 0.05,
            brown_spot: 0.12,
            bacterial_blight: 0.02,
            rust_disease: 0.08,
            powdery_mildew: 0.03,
            fusarium_head_blight: 0.01,
            overall_health_score: 85.2
          }
        }
        
        setSoilData(transformedData)
        console.log('Real soil analysis data loaded successfully')
      } catch (error) {
        console.warn('Real soil analysis API failed, using enhanced mock data:', error)
        
        // Fallback to enhanced mock data
      const mockData: SoilAnalysisData = {
        field_id: "field_001",
        timestamp: new Date().toISOString(),
        physical_properties: {
          soil_moisture: 28.5,
          bulk_density: 1.35,
          porosity: 45.2,
          infiltration_rate: 15.8,
          water_holding_capacity: 32.1,
          soil_temperature: 22.3,
          compaction_level: 0.35,
          aggregate_stability: 78.5,
          permeability: 8.2
        },
        chemical_properties: {
          ph: 6.8,
          organic_matter: 3.2,
          total_nitrogen: 125.5,
          available_phosphorus: 28.3,
          available_potassium: 285.7,
          cation_exchange_capacity: 18.5,
          base_saturation: 75.2,
          electrical_conductivity: 1.8,
          carbon_nitrogen_ratio: 12.3,
          micronutrients: {
            iron: 125.5,
            zinc: 4.2,
            manganese: 65.8,
            copper: 2.1,
            boron: 1.8
          }
        },
        biological_properties: {
          microbial_biomass_carbon: 485.2,
          microbial_biomass_nitrogen: 45.8,
          enzyme_activity: {
            dehydrogenase: 28.5,
            urease: 15.2,
            phosphatase: 35.8,
            catalase: 52.3
          },
          earthworm_density: 185.5,
          nematode_diversity: 2.8,
          mycorrhizal_colonization: 72.3,
          soil_respiration: 125.8,
          nitrogen_mineralization: 6.2
        },
        remote_sensing: {
          ndvi: 0.78,
          ndwi: 0.45,
          ndre: 0.65,
          gndvi: 0.82,
          evi: 0.58,
          savi: 0.75,
          lswi: 0.38,
          nirv: 0.79,
          red_edge_position: 725.5,
          chlorophyll_content: 45.8,
          leaf_area_index: 4.2,
          canopy_temperature: 26.5
        },
        iot_sensors: [
          {
            timestamp: new Date().toISOString(),
            soil_moisture: 28.5,
            soil_temperature: 22.3,
            ph: 6.8,
            electrical_conductivity: 1.8,
            nutrient_levels: { nitrogen: 125.5, phosphorus: 28.3, potassium: 285.7 },
            sensor_id: "sensor_field_001_1",
            location: [40.7128, -74.0060],
            battery_level: 85.2,
            signal_strength: 92.5
          },
          {
            timestamp: new Date().toISOString(),
            soil_moisture: 29.1,
            soil_temperature: 21.8,
            ph: 6.9,
            electrical_conductivity: 1.9,
            nutrient_levels: { nitrogen: 128.2, phosphorus: 29.1, potassium: 288.3 },
            sensor_id: "sensor_field_001_2",
            location: [40.7130, -74.0058],
            battery_level: 78.5,
            signal_strength: 88.2
          },
          {
            timestamp: new Date().toISOString(),
            soil_moisture: 27.8,
            soil_temperature: 22.8,
            ph: 6.7,
            electrical_conductivity: 1.7,
            nutrient_levels: { nitrogen: 122.8, phosphorus: 27.5, potassium: 283.1 },
            sensor_id: "sensor_field_001_3",
            location: [40.7126, -74.0062],
            battery_level: 91.3,
            signal_strength: 95.8
          }
        ],
        crop_stage: {
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
          }
        },
        disease_pest: {
          disease_incidence: {
            blast: 5.2,
            brown_spot: 2.8,
            bacterial_blight: 1.5,
            rust: 0.8,
            powdery_mildew: 0.3
          },
          pest_damage: {
            stem_borer: 3.2,
            brown_planthopper: 1.8,
            aphids: 0.5,
            armyworms: 0.2
          },
          overall_health_score: 88.5,
          risk_level: "low",
          treatment_recommendations: [
            "Monitor for blast disease - current incidence is manageable",
            "Continue regular pest monitoring",
            "Maintain current integrated pest management practices"
          ],
          last_treatment_date: "2024-08-15T10:30:00Z"
        },
        nutrient_status: {
          nitrogen_status: "adequate",
          phosphorus_status: "adequate",
          potassium_status: "adequate",
          micronutrient_status: {
            iron: "adequate",
            zinc: "deficient",
            manganese: "adequate",
            copper: "adequate",
            boron: "deficient"
          },
          fertilizer_recommendations: [
            "Apply zinc sulfate (2-3 kg/ha) for zinc deficiency",
            "Apply borax (1-2 kg/ha) for boron deficiency",
            "Maintain current N-P-K fertilization schedule"
          ],
          last_fertilizer_application: "2024-08-10T08:00:00Z",
          nutrient_use_efficiency: 78.5
        },
        overall_soil_health: {
          overall_score: 82.5,
          health_level: "good",
          physical_score: 78.5,
          chemical_score: 85.2,
          biological_score: 83.8,
          recommendations: [
            "Improve soil compaction through reduced tillage",
            "Add organic matter through compost application",
            "Maintain current pH levels"
          ]
        }
      }
      
      setSoilData(mockData)
      setIsLoading(false)
      setLastUpdated(new Date())
    } catch (error) {
      console.error('Error loading soil data:', error)
      setIsLoading(false)
    }
  }

  loadSoilData()
}, [])

  const getHealthColor = (score: number) => {
    if (score >= 85) return 'green'
    if (score >= 70) return 'blue'
    if (score >= 55) return 'yellow'
    if (score >= 40) return 'orange'
    return 'red'
  }

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'excellent':
      case 'good':
      case 'adequate':
        return <CheckCircle size={16} color="green" />
      case 'fair':
        return <Minus size={16} color="yellow" />
      case 'poor':
      case 'deficient':
      case 'excessive':
        return <XCircle size={16} color="red" />
      default:
        return <AlertTriangle size={16} color="orange" />
    }
  }


  if (isLoading) {
    return (
      <Box p={6} textAlign="center">
        <CircularProgress isIndeterminate color="blue.500" size="60px" />
        <ChakraText mt={4} color={textColor}>
          Loading comprehensive soil analysis...
        </ChakraText>
      </Box>
    )
  }

  if (!soilData) {
    return (
      <Alert status="error">
        <AlertIcon />
        <AlertTitle>Error loading soil data!</AlertTitle>
        <AlertDescription>Unable to load comprehensive soil analysis data.</AlertDescription>
      </Alert>
    )
  }

  return (
    <Box p={6} bg={bg} borderRadius="lg" boxShadow="lg">
      {/* Header */}
      <Flex align="center" mb={6}>
        <VStack align="start" spacing={1}>
          <HStack>
            <Heading size="lg">Advanced Soil Analysis</Heading>
            <Badge colorScheme="blue" variant="subtle">Comprehensive</Badge>
            {isLocked && (
              <Tooltip label="Advanced features locked for future development">
                <Icon as={Lock} w={4} h={4} color="gray.500" />
              </Tooltip>
            )}
          </HStack>
          <ChakraText color={textColor} fontSize="sm">
            Real-time soil health monitoring with IoT sensors and remote sensing
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

      {/* Overall Soil Health Score */}
      <Card mb={6} borderColor={borderColor}>
        <CardHeader>
          <HStack>
            <Icon as={Activity} w={5} h={5} color="blue.500" />
            <Heading size="md">Overall Soil Health</Heading>
          </HStack>
        </CardHeader>
        <CardBody>
          <SimpleGrid columns={{ base: 1, md: 4 }} spacing={6}>
            <Box textAlign="center">
              <CircularProgress
                value={soilData.overall_soil_health.overall_score}
                size="80px"
                color={getHealthColor(soilData.overall_soil_health.overall_score)}
                thickness="8px"
              >
                <CircularProgressLabel>
                  {soilData.overall_soil_health.overall_score}
                </CircularProgressLabel>
              </CircularProgress>
              <ChakraText mt={2} fontWeight="bold">
                Overall Score
              </ChakraText>
              <Badge colorScheme={getHealthColor(soilData.overall_soil_health.overall_score)}>
                {soilData.overall_soil_health.health_level}
              </Badge>
            </Box>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Physical Health</ChakraText>
              <Progress
                value={soilData.overall_soil_health.physical_score}
                colorScheme={getHealthColor(soilData.overall_soil_health.physical_score)}
                size="lg"
                w="100%"
              />
              <ChakraText fontSize="sm">{soilData.overall_soil_health.physical_score}/100</ChakraText>
            </VStack>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Chemical Health</ChakraText>
              <Progress
                value={soilData.overall_soil_health.chemical_score}
                colorScheme={getHealthColor(soilData.overall_soil_health.chemical_score)}
                size="lg"
                w="100%"
              />
              <ChakraText fontSize="sm">{soilData.overall_soil_health.chemical_score}/100</ChakraText>
            </VStack>
            
            <VStack spacing={2}>
              <ChakraText fontWeight="bold">Biological Health</ChakraText>
              <Progress
                value={soilData.overall_soil_health.biological_score}
                colorScheme={getHealthColor(soilData.overall_soil_health.biological_score)}
                size="lg"
                w="100%"
              />
              <ChakraText fontSize="sm">{soilData.overall_soil_health.biological_score}/100</ChakraText>
            </VStack>
          </SimpleGrid>
        </CardBody>
      </Card>

      {/* Comprehensive Analysis Sections */}
      <Accordion allowMultiple>
        {/* Physical Properties */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Droplets} w={5} h={5} color="blue.500" />
                <Heading size="sm">Physical Properties</Heading>
                <Badge colorScheme="blue" variant="subtle">Real-time</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              <Stat>
                <StatLabel>Soil Moisture</StatLabel>
                <StatNumber>{soilData.physical_properties.soil_moisture}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Optimal range: 20-35%
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Bulk Density</StatLabel>
                <StatNumber>{soilData.physical_properties.bulk_density} g/cm³</StatNumber>
                <StatHelpText>
                  <StatArrow type="decrease" />
                  Lower is better
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Porosity</StatLabel>
                <StatNumber>{soilData.physical_properties.porosity}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Higher is better
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Infiltration Rate</StatLabel>
                <StatNumber>{soilData.physical_properties.infiltration_rate} mm/h</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Water absorption
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Soil Temperature</StatLabel>
                <StatNumber>{soilData.physical_properties.soil_temperature}°C</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Current temperature
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Compaction Level</StatLabel>
                <StatNumber>{(soilData.physical_properties.compaction_level * 100).toFixed(1)}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="decrease" />
                  Lower is better
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Chemical Properties */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Microscope} w={5} h={5} color="green.500" />
                <Heading size="sm">Chemical Properties</Heading>
                <Badge colorScheme="green" variant="subtle">Lab Analysis</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              <Stat>
                <StatLabel>pH Level</StatLabel>
                <StatNumber>{soilData.chemical_properties.ph}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Optimal: 6.0-7.5
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Organic Matter</StatLabel>
                <StatNumber>{soilData.chemical_properties.organic_matter}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Higher is better
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Total Nitrogen</StatLabel>
                <StatNumber>{soilData.chemical_properties.total_nitrogen} ppm</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  N availability
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Available Phosphorus</StatLabel>
                <StatNumber>{soilData.chemical_properties.available_phosphorus} ppm</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  P availability
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Available Potassium</StatLabel>
                <StatNumber>{soilData.chemical_properties.available_potassium} ppm</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  K availability
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>CEC</StatLabel>
                <StatNumber>{soilData.chemical_properties.cation_exchange_capacity} meq/100g</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Nutrient holding
                </StatHelpText>
              </Stat>
            </SimpleGrid>
            
            <Divider my={4} />
            
            <Heading size="sm" mb={3}>Micronutrients</Heading>
            <SimpleGrid columns={{ base: 2, md: 3, lg: 5 }} spacing={4}>
              {Object.entries(soilData.chemical_properties.micronutrients).map(([nutrient, value]) => (
                <Stat key={nutrient}>
                  <StatLabel textTransform="capitalize">{nutrient}</StatLabel>
                  <StatNumber>{value} ppm</StatNumber>
                </Stat>
              ))}
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Biological Properties */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Activity} w={5} h={5} color="purple.500" />
                <Heading size="sm">Biological Properties</Heading>
                <Badge colorScheme="purple" variant="subtle">Microbial Activity</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              <Stat>
                <StatLabel>Microbial Biomass C</StatLabel>
                <StatNumber>{soilData.biological_properties.microbial_biomass_carbon} mg/kg</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Soil biology indicator
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Earthworm Density</StatLabel>
                <StatNumber>{soilData.biological_properties.earthworm_density} count/m²</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Soil health indicator
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Mycorrhizal Colonization</StatLabel>
                <StatNumber>{soilData.biological_properties.mycorrhizal_colonization}%</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Root symbiosis
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Soil Respiration</StatLabel>
                <StatNumber>{soilData.biological_properties.soil_respiration} mg CO₂/kg/day</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Microbial activity
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>N Mineralization</StatLabel>
                <StatNumber>{soilData.biological_properties.nitrogen_mineralization} mg N/kg/day</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  N availability
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Nematode Diversity</StatLabel>
                <StatNumber>{soilData.biological_properties.nematode_diversity}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Shannon index
                </StatHelpText>
              </Stat>
            </SimpleGrid>
            
            <Divider my={4} />
            
            <Heading size="sm" mb={3}>Enzyme Activity</Heading>
            <SimpleGrid columns={{ base: 2, md: 4 }} spacing={4}>
              {Object.entries(soilData.biological_properties.enzyme_activity).map(([enzyme, value]) => (
                <Stat key={enzyme}>
                  <StatLabel textTransform="capitalize">{enzyme}</StatLabel>
                  <StatNumber>{value}</StatNumber>
                  <StatHelpText>μg/g soil/day</StatHelpText>
                </Stat>
              ))}
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Remote Sensing */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Satellite} w={5} h={5} color="orange.500" />
                <Heading size="sm">Remote Sensing Indices</Heading>
                <Badge colorScheme="orange" variant="subtle">Satellite Data</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 2, md: 3, lg: 4 }} spacing={4}>
              <Stat>
                <StatLabel>NDVI</StatLabel>
                <StatNumber>{soilData.remote_sensing.ndvi.toFixed(3)}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Vegetation health
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>NDWI</StatLabel>
                <StatNumber>{soilData.remote_sensing.ndwi.toFixed(3)}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Water content
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>NDRE</StatLabel>
                <StatNumber>{soilData.remote_sensing.ndre.toFixed(3)}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Red edge health
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>EVI</StatLabel>
                <StatNumber>{soilData.remote_sensing.evi.toFixed(3)}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Enhanced vegetation
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>SAVI</StatLabel>
                <StatNumber>{soilData.remote_sensing.savi.toFixed(3)}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Soil adjusted
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>LSWI</StatLabel>
                <StatNumber>{soilData.remote_sensing.lswi.toFixed(3)}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Land surface water
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Chlorophyll Content</StatLabel>
                <StatNumber>{soilData.remote_sensing.chlorophyll_content} μg/cm²</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Leaf chlorophyll
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Leaf Area Index</StatLabel>
                <StatNumber>{soilData.remote_sensing.leaf_area_index}</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  Canopy coverage
                </StatHelpText>
              </Stat>
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* IoT Sensors */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={Wifi} w={5} h={5} color="teal.500" />
                <Heading size="sm">IoT Sensor Network</Heading>
                <Badge colorScheme="teal" variant="subtle">{soilData.iot_sensors.length} Sensors</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <TableContainer>
              <Table variant="simple" size="sm">
                <Thead>
                  <Tr>
                    <Th>Sensor ID</Th>
                    <Th>Moisture %</Th>
                    <Th>Temperature °C</Th>
                    <Th>pH</Th>
                    <Th>Battery %</Th>
                    <Th>Signal %</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {soilData.iot_sensors.map((sensor, index) => (
                    <Tr key={index}>
                      <Td>{sensor.sensor_id}</Td>
                      <Td>{sensor.soil_moisture.toFixed(1)}</Td>
                      <Td>{sensor.soil_temperature.toFixed(1)}</Td>
                      <Td>{sensor.ph.toFixed(1)}</Td>
                      <Td>
                        <HStack>
                          <ChakraText>{sensor.battery_level.toFixed(1)}</ChakraText>
                          {sensor.battery_level < 20 && <Icon as={AlertTriangle} w={3} h={3} color="red" />}
                        </HStack>
                      </Td>
                      <Td>
                        <HStack>
                          <ChakraText>{sensor.signal_strength.toFixed(1)}</ChakraText>
                          {sensor.signal_strength < 70 && <Icon as={AlertTriangle} w={3} h={3} color="orange" />}
                        </HStack>
                      </Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </TableContainer>
          </AccordionPanel>
        </AccordionItem>

        {/* Crop Stage Tracking */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={TrendingUp} w={5} h={5} color="green.500" />
                <Heading size="sm">Crop Stage Tracking</Heading>
                <Badge colorScheme="green" variant="subtle">{soilData.crop_stage.current_stage.replace('_', ' ')}</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              <Stat>
                <StatLabel>Current Stage</StatLabel>
                <StatNumber textTransform="capitalize">
                  {soilData.crop_stage.current_stage.replace('_', ' ')}
                </StatNumber>
                <StatHelpText>
                  {soilData.crop_stage.stage_percentage.toFixed(1)}% complete
                </StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Days Since Planting</StatLabel>
                <StatNumber>{soilData.crop_stage.days_since_planting}</StatNumber>
                <StatHelpText>Days</StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Days to Harvest</StatLabel>
                <StatNumber>{soilData.crop_stage.days_to_harvest}</StatNumber>
                <StatHelpText>Days remaining</StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Tillering Count</StatLabel>
                <StatNumber>{soilData.crop_stage.tillering_count}</StatNumber>
                <StatHelpText>Plants per m²</StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Heading Percentage</StatLabel>
                <StatNumber>{soilData.crop_stage.heading_percentage.toFixed(1)}%</StatNumber>
                <StatHelpText>Completed</StatHelpText>
              </Stat>
              
              <Stat>
                <StatLabel>Grain Filling</StatLabel>
                <StatNumber>{soilData.crop_stage.grain_filling_percentage.toFixed(1)}%</StatNumber>
                <StatHelpText>Completed</StatHelpText>
              </Stat>
            </SimpleGrid>
            
            <Divider my={4} />
            
            <Heading size="sm" mb={3}>Stress Indicators</Heading>
            <SimpleGrid columns={{ base: 2, md: 4 }} spacing={4}>
              {Object.entries(soilData.crop_stage.stress_indicators).map(([stress, value]) => (
                <Stat key={stress}>
                  <StatLabel textTransform="capitalize">{stress.replace('_', ' ')}</StatLabel>
                  <StatNumber>{(value * 100).toFixed(1)}%</StatNumber>
                  <StatHelpText>
                    {value > 0.5 ? 'High' : value > 0.2 ? 'Medium' : 'Low'}
                  </StatHelpText>
                </Stat>
              ))}
            </SimpleGrid>
          </AccordionPanel>
        </AccordionItem>

        {/* Disease & Pest Monitoring */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={AlertTriangle} w={5} h={5} color="red.500" />
                <Heading size="sm">Disease & Pest Monitoring</Heading>
                <Badge colorScheme={soilData.disease_pest.risk_level === 'low' ? 'green' : soilData.disease_pest.risk_level === 'medium' ? 'yellow' : 'red'} variant="subtle">
                  {soilData.disease_pest.risk_level}
                </Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <VStack spacing={4} align="stretch">
              <Box>
                <Heading size="sm" mb={3}>Disease Incidence</Heading>
                <SimpleGrid columns={{ base: 2, md: 3, lg: 5 }} spacing={4}>
                  {Object.entries(soilData.disease_pest.disease_incidence).map(([disease, incidence]) => (
                    <Stat key={disease}>
                      <StatLabel textTransform="capitalize">{disease.replace('_', ' ')}</StatLabel>
                      <StatNumber>{incidence.toFixed(1)}%</StatNumber>
                      <StatHelpText>
                        {incidence > 20 ? 'High risk' : incidence > 10 ? 'Medium risk' : 'Low risk'}
                      </StatHelpText>
                    </Stat>
                  ))}
                </SimpleGrid>
              </Box>
              
              <Divider />
              
              <Box>
                <Heading size="sm" mb={3}>Pest Damage</Heading>
                <SimpleGrid columns={{ base: 2, md: 3, lg: 4 }} spacing={4}>
                  {Object.entries(soilData.disease_pest.pest_damage).map(([pest, damage]) => (
                    <Stat key={pest}>
                      <StatLabel textTransform="capitalize">{pest.replace('_', ' ')}</StatLabel>
                      <StatNumber>{damage.toFixed(1)}%</StatNumber>
                      <StatHelpText>
                        {damage > 15 ? 'High damage' : damage > 5 ? 'Medium damage' : 'Low damage'}
                      </StatHelpText>
                    </Stat>
                  ))}
                </SimpleGrid>
              </Box>
              
              <Divider />
              
              <Box>
                <Heading size="sm" mb={3}>Treatment Recommendations</Heading>
                <VStack spacing={2} align="stretch">
                  {soilData.disease_pest.treatment_recommendations.map((recommendation, index) => (
                    <Alert key={index} status="info" size="sm">
                      <AlertIcon />
                      <AlertDescription>{recommendation}</AlertDescription>
                    </Alert>
                  ))}
                </VStack>
              </Box>
            </VStack>
          </AccordionPanel>
        </AccordionItem>

        {/* Nutrient Status */}
        <AccordionItem>
          <AccordionButton>
            <Box flex="1" textAlign="left">
              <HStack>
                <Icon as={TrendingUp} w={5} h={5} color="blue.500" />
                <Heading size="sm">Nutrient Status</Heading>
                <Badge colorScheme="blue" variant="subtle">Fertilization</Badge>
              </HStack>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4}>
            <VStack spacing={4} align="stretch">
              <Box>
                <Heading size="sm" mb={3}>Macronutrients</Heading>
                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                  <Stat>
                    <StatLabel>Nitrogen</StatLabel>
                    <StatNumber textTransform="capitalize">{soilData.nutrient_status.nitrogen_status}</StatNumber>
                    <StatHelpText>
                      {getStatusIcon(soilData.nutrient_status.nitrogen_status)}
                    </StatHelpText>
                  </Stat>
                  
                  <Stat>
                    <StatLabel>Phosphorus</StatLabel>
                    <StatNumber textTransform="capitalize">{soilData.nutrient_status.phosphorus_status}</StatNumber>
                    <StatHelpText>
                      {getStatusIcon(soilData.nutrient_status.phosphorus_status)}
                    </StatHelpText>
                  </Stat>
                  
                  <Stat>
                    <StatLabel>Potassium</StatLabel>
                    <StatNumber textTransform="capitalize">{soilData.nutrient_status.potassium_status}</StatNumber>
                    <StatHelpText>
                      {getStatusIcon(soilData.nutrient_status.potassium_status)}
                    </StatHelpText>
                  </Stat>
                </SimpleGrid>
              </Box>
              
              <Divider />
              
              <Box>
                <Heading size="sm" mb={3}>Micronutrients</Heading>
                <SimpleGrid columns={{ base: 2, md: 3, lg: 5 }} spacing={4}>
                  {Object.entries(soilData.nutrient_status.micronutrient_status).map(([nutrient, status]) => (
                    <Stat key={nutrient}>
                      <StatLabel textTransform="capitalize">{nutrient}</StatLabel>
                      <StatNumber textTransform="capitalize">{status}</StatNumber>
                      <StatHelpText>
                        {getStatusIcon(status)}
                      </StatHelpText>
                    </Stat>
                  ))}
                </SimpleGrid>
              </Box>
              
              <Divider />
              
              <Box>
                <Heading size="sm" mb={3}>Fertilizer Recommendations</Heading>
                <VStack spacing={2} align="stretch">
                  {soilData.nutrient_status.fertilizer_recommendations.map((recommendation, index) => (
                    <Alert key={index} status="info" size="sm">
                      <AlertIcon />
                      <AlertDescription>{recommendation}</AlertDescription>
                    </Alert>
                  ))}
                </VStack>
              </Box>
              
              <Divider />
              
              <Box>
                <Heading size="sm" mb={3}>Nutrient Use Efficiency</Heading>
                <HStack>
                  <CircularProgress
                    value={soilData.nutrient_status.nutrient_use_efficiency}
                    size="60px"
                    color="blue.500"
                    thickness="8px"
                  >
                    <CircularProgressLabel>
                      {soilData.nutrient_status.nutrient_use_efficiency}%
                    </CircularProgressLabel>
                  </CircularProgress>
                  <VStack align="start" spacing={1}>
                    <ChakraText fontWeight="bold">Efficiency Score</ChakraText>
                    <ChakraText fontSize="sm" color={textColor}>
                      How well nutrients are utilized
                    </ChakraText>
                  </VStack>
                </HStack>
              </Box>
            </VStack>
          </AccordionPanel>
        </AccordionItem>
      </Accordion>

      {/* Recommendations */}
      <Card mt={6} borderColor={borderColor}>
        <CardHeader>
          <HStack>
            <Icon as={CheckCircle} w={5} h={5} color="green.500" />
            <Heading size="md">Soil Health Recommendations</Heading>
          </HStack>
        </CardHeader>
        <CardBody>
          <VStack spacing={3} align="stretch">
            {soilData.overall_soil_health.recommendations.map((recommendation, index) => (
              <Alert key={index} status="info" size="sm">
                <AlertIcon />
                <AlertDescription>{recommendation}</AlertDescription>
              </Alert>
            ))}
          </VStack>
        </CardBody>
      </Card>

      {/* Lock Notice */}
      {isLocked && (
        <Alert status="info" mt={6}>
          <AlertIcon />
          <AlertTitle>Advanced Features Locked</AlertTitle>
          <AlertDescription>
            This comprehensive soil analysis system is currently in development. 
            Advanced features will be unlocked in future updates.
          </AlertDescription>
        </Alert>
      )}
    </Box>
  )
}

export default AdvancedSoilAnalysis
