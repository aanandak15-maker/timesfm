/**
 * IoT Dashboard - Real-time sensor data simulation and monitoring
 * Provides comprehensive IoT sensor data visualization and analysis
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Card,
  CardBody,
  CardHeader,
  Heading,
  Button,
  Badge,
  Grid,
  GridItem,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  useToast,
  Alert,
  AlertIcon,
  AlertDescription,
  Spinner,
  Progress,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  useColorModeValue,
  Switch,
  FormControl,
  FormLabel,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  SliderMark
} from '@chakra-ui/react';
import { 
  Thermometer, 
  Droplets, 
  Sun, 
  Wind, 
  Activity,
  Wifi,
  Battery,
  Signal,
  AlertTriangle,
  CheckCircle,
  Settings,
  Play,
  Pause,
  RotateCcw,
  Zap,
  Eye,
  BarChart3,
  Satellite,
  MapPin,
  Globe
} from 'lucide-react';
import { googleEarthEngineApi, type GEEData, type GEETimeSeries } from '../../services/googleEarthEngineApi';

interface SensorData {
  id: string;
  name: string;
  value: number;
  unit: string;
  status: 'normal' | 'warning' | 'critical';
  lastUpdate: Date;
  location: string;
  battery: number;
  signal: number;
}

interface IoTField {
  id: string;
  name: string;
  location: string;
  sensors: SensorData[];
  status: 'active' | 'inactive' | 'maintenance';
  coordinates: {
    lat: number;
    lon: number;
  };
  geeData?: GEEData;
  timeSeries?: GEETimeSeries;
}

const IoTDashboard: React.FC = () => {
  const [fields, setFields] = useState<IoTField[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationSpeed, setSimulationSpeed] = useState(1000);
  const [selectedField, setSelectedField] = useState<string | null>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const toast = useToast();
  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  // Initialize IoT fields with simulated sensors
  useEffect(() => {
    initializeIoTFields();
  }, []);

  // Start/stop simulation
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isSimulating) {
      interval = setInterval(() => {
        updateSensorData();
      }, simulationSpeed);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isSimulating, simulationSpeed]);

  const initializeIoTFields = async () => {
    const mockFields: IoTField[] = [
      {
        id: 'field-1',
        name: 'Rice Field 1',
        location: 'Uttar Pradesh, India',
        status: 'active',
        coordinates: { lat: 28.368911, lon: 77.541033 },
        sensors: [
          {
            id: 'temp-1',
            name: 'Temperature Sensor',
            value: 28.5,
            unit: '°C',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'North Corner',
            battery: 85,
            signal: 92
          },
          {
            id: 'humidity-1',
            name: 'Humidity Sensor',
            value: 65.2,
            unit: '%',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'Center',
            battery: 78,
            signal: 88
          },
          {
            id: 'soil-1',
            name: 'Soil Moisture',
            value: 42.8,
            unit: '%',
            status: 'warning',
            lastUpdate: new Date(),
            location: 'South Corner',
            battery: 92,
            signal: 95
          },
          {
            id: 'light-1',
            name: 'Light Sensor',
            value: 850,
            unit: 'lux',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'East Side',
            battery: 67,
            signal: 85
          },
          {
            id: 'wind-1',
            name: 'Wind Speed',
            value: 12.3,
            unit: 'km/h',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'West Side',
            battery: 89,
            signal: 90
          }
        ]
      },
      {
        id: 'field-2',
        name: 'Wheat Field 1',
        location: 'Punjab, India',
        status: 'active',
        coordinates: { lat: 30.368911, lon: 75.541033 },
        sensors: [
          {
            id: 'temp-2',
            name: 'Temperature Sensor',
            value: 26.8,
            unit: '°C',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'North Corner',
            battery: 91,
            signal: 94
          },
          {
            id: 'humidity-2',
            name: 'Humidity Sensor',
            value: 58.7,
            unit: '%',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'Center',
            battery: 83,
            signal: 87
          },
          {
            id: 'soil-2',
            name: 'Soil Moisture',
            value: 38.2,
            unit: '%',
            status: 'critical',
            lastUpdate: new Date(),
            location: 'South Corner',
            battery: 76,
            signal: 82
          },
          {
            id: 'light-2',
            name: 'Light Sensor',
            value: 920,
            unit: 'lux',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'East Side',
            battery: 88,
            signal: 91
          }
        ]
      },
      {
        id: 'field-3',
        name: 'Corn Field 1',
        location: 'Haryana, India',
        status: 'active',
        coordinates: { lat: 29.368911, lon: 76.541033 },
        sensors: [
          {
            id: 'temp-3',
            name: 'Temperature Sensor',
            value: 30.2,
            unit: '°C',
            status: 'warning',
            lastUpdate: new Date(),
            location: 'North Corner',
            battery: 72,
            signal: 79
          },
          {
            id: 'humidity-3',
            name: 'Humidity Sensor',
            value: 71.5,
            unit: '%',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'Center',
            battery: 95,
            signal: 96
          },
          {
            id: 'soil-3',
            name: 'Soil Moisture',
            value: 55.1,
            unit: '%',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'South Corner',
            battery: 81,
            signal: 86
          },
          {
            id: 'light-3',
            name: 'Light Sensor',
            value: 780,
            unit: 'lux',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'East Side',
            battery: 69,
            signal: 84
          },
          {
            id: 'wind-3',
            name: 'Wind Speed',
            value: 8.7,
            unit: 'km/h',
            status: 'normal',
            lastUpdate: new Date(),
            location: 'West Side',
            battery: 93,
            signal: 89
          }
        ]
      }
    ];

    // Fetch GEE data for each field
    const fieldsWithGEEData = await Promise.all(
      mockFields.map(async (field) => {
        try {
          const geeData = await googleEarthEngineApi.getAgriculturalData(
            field.coordinates.lat,
            field.coordinates.lon
          );
          const timeSeries = await googleEarthEngineApi.getTimeSeriesData(
            field.coordinates.lat,
            field.coordinates.lon,
            30
          );
          
          return {
            ...field,
            geeData,
            timeSeries
          };
        } catch (error) {
          console.error(`Error fetching GEE data for ${field.name}:`, error);
          return field;
        }
      })
    );

    setFields(fieldsWithGEEData);
    setIsLoading(false);
  };

  const updateSensorData = () => {
    setFields(prevFields => 
      prevFields.map(field => ({
        ...field,
        sensors: field.sensors.map(sensor => {
          // Simulate realistic sensor data changes
          const variation = (Math.random() - 0.5) * 2; // -1 to 1
          let newValue = sensor.value + variation;
          
          // Keep values within realistic ranges
          switch (sensor.name) {
            case 'Temperature Sensor':
              newValue = Math.max(15, Math.min(40, newValue));
              break;
            case 'Humidity Sensor':
              newValue = Math.max(30, Math.min(90, newValue));
              break;
            case 'Soil Moisture':
              newValue = Math.max(10, Math.min(80, newValue));
              break;
            case 'Light Sensor':
              newValue = Math.max(100, Math.min(1200, newValue));
              break;
            case 'Wind Speed':
              newValue = Math.max(0, Math.min(50, newValue));
              break;
          }

          // Update status based on values
          let status: 'normal' | 'warning' | 'critical' = 'normal';
          if (sensor.name === 'Temperature Sensor' && (newValue > 35 || newValue < 20)) {
            status = newValue > 35 ? 'critical' : 'warning';
          } else if (sensor.name === 'Soil Moisture' && newValue < 30) {
            status = 'critical';
          } else if (sensor.name === 'Humidity Sensor' && (newValue > 80 || newValue < 40)) {
            status = 'warning';
          }

          return {
            ...sensor,
            value: Math.round(newValue * 10) / 10,
            status,
            lastUpdate: new Date(),
            battery: Math.max(10, sensor.battery - Math.random() * 0.1),
            signal: Math.max(50, sensor.signal + (Math.random() - 0.5) * 2)
          };
        })
      }))
    );

    // Check for alerts
    checkForAlerts();
  };

  const checkForAlerts = () => {
    const newAlerts: any[] = [];
    
    fields.forEach(field => {
      field.sensors.forEach(sensor => {
        if (sensor.status === 'critical') {
          newAlerts.push({
            id: `${sensor.id}-${Date.now()}`,
            type: 'critical',
            message: `${sensor.name} in ${field.name} is in critical condition (${sensor.value}${sensor.unit})`,
            timestamp: new Date(),
            field: field.name,
            sensor: sensor.name
          });
        } else if (sensor.status === 'warning') {
          newAlerts.push({
            id: `${sensor.id}-${Date.now()}`,
            type: 'warning',
            message: `${sensor.name} in ${field.name} needs attention (${sensor.value}${sensor.unit})`,
            timestamp: new Date(),
            field: field.name,
            sensor: sensor.name
          });
        }
      });
    });

    if (newAlerts.length > 0) {
      setAlerts(prev => [...newAlerts, ...prev].slice(0, 10)); // Keep last 10 alerts
      
      // Show toast for critical alerts
      newAlerts.filter(alert => alert.type === 'critical').forEach(alert => {
        toast({
          title: 'Critical Alert',
          description: alert.message,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      });
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'normal': return 'green';
      case 'warning': return 'yellow';
      case 'critical': return 'red';
      default: return 'gray';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'normal': return <CheckCircle size={16} />;
      case 'warning': return <AlertTriangle size={16} />;
      case 'critical': return <AlertTriangle size={16} />;
      default: return <Activity size={16} />;
    }
  };

  const getSensorIcon = (sensorName: string) => {
    switch (sensorName) {
      case 'Temperature Sensor': return <Thermometer size={20} />;
      case 'Humidity Sensor': return <Droplets size={20} />;
      case 'Soil Moisture': return <Droplets size={20} />;
      case 'Light Sensor': return <Sun size={20} />;
      case 'Wind Speed': return <Wind size={20} />;
      default: return <Activity size={20} />;
    }
  };

  const toggleSimulation = () => {
    setIsSimulating(!isSimulating);
    toast({
      title: isSimulating ? 'Simulation Stopped' : 'Simulation Started',
      description: isSimulating ? 'IoT sensors are now static' : 'IoT sensors are updating in real-time',
      status: 'info',
      duration: 2000,
    });
  };

  const resetSimulation = () => {
    setIsSimulating(false);
    initializeIoTFields();
    setAlerts([]);
    toast({
      title: 'Simulation Reset',
      description: 'All sensor data has been reset to initial values',
      status: 'info',
      duration: 2000,
    });
  };

  if (isLoading) {
    return (
      <Box p={8} textAlign="center">
        <Spinner size="xl" />
        <Text mt={4}>Loading IoT Dashboard...</Text>
      </Box>
    );
  }

  const selectedFieldData = selectedField ? fields.find(f => f.id === selectedField) : null;

  return (
    <Box p={6}>
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <HStack justify="space-between" align="center">
          <VStack align="start" spacing={2}>
            <Heading size="lg" color="blue.600">
              🌾 IoT Sensor Dashboard
            </Heading>
            <Text color="gray.600">
              Real-time monitoring of agricultural sensors across all fields
            </Text>
          </VStack>
          
          <HStack spacing={4}>
            <Button
              leftIcon={isSimulating ? <Pause /> : <Play />}
              colorScheme={isSimulating ? 'red' : 'green'}
              onClick={toggleSimulation}
            >
              {isSimulating ? 'Stop Simulation' : 'Start Simulation'}
            </Button>
            <Button
              leftIcon={<RotateCcw />}
              variant="outline"
              onClick={resetSimulation}
            >
              Reset
            </Button>
          </HStack>
        </HStack>

        {/* Simulation Controls */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <HStack spacing={6} align="center">
              <FormControl>
                <FormLabel>Simulation Speed</FormLabel>
                <HStack>
                  <Text fontSize="sm">Slow</Text>
                  <Slider
                    value={simulationSpeed}
                    onChange={(val) => setSimulationSpeed(val)}
                    min={500}
                    max={3000}
                    step={500}
                    w="200px"
                  >
                    <SliderTrack>
                      <SliderFilledTrack />
                    </SliderTrack>
                    <SliderThumb />
                  </Slider>
                  <Text fontSize="sm">Fast</Text>
                </HStack>
              </FormControl>
              
              <VStack align="start" spacing={1}>
                <Text fontSize="sm" fontWeight="bold">Status</Text>
                <HStack>
                  <Badge colorScheme={isSimulating ? 'green' : 'gray'}>
                    {isSimulating ? 'Running' : 'Stopped'}
                  </Badge>
                  <Text fontSize="sm">
                    {isSimulating ? `${simulationSpeed}ms interval` : 'Static data'}
                  </Text>
                </HStack>
              </VStack>
            </HStack>
          </CardBody>
        </Card>

        {/* Alerts */}
        {alerts.length > 0 && (
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardHeader>
              <Heading size="md">🚨 Active Alerts</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={2} align="stretch">
                {alerts.slice(0, 5).map((alert) => (
                  <Alert
                    key={alert.id}
                    status={alert.type === 'critical' ? 'error' : 'warning'}
                    borderRadius="md"
                  >
                    <AlertIcon />
                    <AlertDescription>
                      <Text fontWeight="bold">{alert.field}</Text>
                      <Text fontSize="sm">{alert.message}</Text>
                      <Text fontSize="xs" color="gray.500">
                        {alert.timestamp.toLocaleTimeString()}
                      </Text>
                    </AlertDescription>
                  </Alert>
                ))}
              </VStack>
            </CardBody>
          </Card>
        )}

        {/* Main Content */}
        <Tabs>
          <TabList>
            <Tab>Field Overview</Tab>
            <Tab>Sensor Details</Tab>
            <Tab>Satellite Data</Tab>
            <Tab>Analytics</Tab>
          </TabList>

          <TabPanels>
            {/* Field Overview Tab */}
            <TabPanel>
              <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }} gap={6}>
                {fields.map((field) => (
                  <GridItem key={field.id}>
                    <Card 
                      bg={bg} 
                      border="1px" 
                      borderColor={borderColor}
                      cursor="pointer"
                      onClick={() => setSelectedField(field.id)}
                      _hover={{ shadow: 'md' }}
                    >
                      <CardHeader>
                        <HStack justify="space-between">
                          <VStack align="start" spacing={1}>
                            <Heading size="md">{field.name}</Heading>
                            <Text fontSize="sm" color="gray.600">{field.location}</Text>
                          </VStack>
                          <Badge colorScheme={getStatusColor(field.status)}>
                            {field.status}
                          </Badge>
                        </HStack>
                      </CardHeader>
                      <CardBody>
                        <VStack spacing={3} align="stretch">
                          <HStack justify="space-between">
                            <Text fontSize="sm" fontWeight="bold">Sensors</Text>
                            <Text fontSize="sm">{field.sensors.length}</Text>
                          </HStack>
                          
                          <VStack spacing={2} align="stretch">
                            {field.sensors.slice(0, 3).map((sensor) => (
                              <HStack key={sensor.id} justify="space-between">
                                <HStack>
                                  {getSensorIcon(sensor.name)}
                                  <Text fontSize="sm">{sensor.name}</Text>
                                </HStack>
                                <HStack>
                                  <Text fontSize="sm" fontWeight="bold">
                                    {sensor.value}{sensor.unit}
                                  </Text>
                                  <Badge size="sm" colorScheme={getStatusColor(sensor.status)}>
                                    {sensor.status}
                                  </Badge>
                                </HStack>
                              </HStack>
                            ))}
                          </VStack>
                          
                          <HStack justify="space-between" fontSize="xs" color="gray.500">
                            <HStack>
                              <Battery size={12} />
                              <Text>Avg: {Math.round(field.sensors.reduce((sum, s) => sum + s.battery, 0) / field.sensors.length)}%</Text>
                            </HStack>
                            <HStack>
                              <Signal size={12} />
                              <Text>Avg: {Math.round(field.sensors.reduce((sum, s) => sum + s.signal, 0) / field.sensors.length)}%</Text>
                            </HStack>
                          </HStack>
                        </VStack>
                      </CardBody>
                    </Card>
                  </GridItem>
                ))}
              </Grid>
            </TabPanel>

            {/* Sensor Details Tab */}
            <TabPanel>
              {selectedFieldData ? (
                <VStack spacing={6} align="stretch">
                  <Card bg={bg} border="1px" borderColor={borderColor}>
                    <CardHeader>
                      <Heading size="md">{selectedFieldData.name} - Sensor Details</Heading>
                    </CardHeader>
                    <CardBody>
                      <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)' }} gap={4}>
                        {selectedFieldData.sensors.map((sensor) => (
                          <GridItem key={sensor.id}>
                            <Card bg="gray.50" border="1px" borderColor="gray.200">
                              <CardBody>
                                <VStack spacing={3} align="stretch">
                                  <HStack justify="space-between">
                                    <HStack>
                                      {getSensorIcon(sensor.name)}
                                      <Text fontWeight="bold">{sensor.name}</Text>
                                    </HStack>
                                    <Badge colorScheme={getStatusColor(sensor.status)}>
                                      {sensor.status}
                                    </Badge>
                                  </HStack>
                                  
                                  <VStack spacing={2} align="stretch">
                                    <HStack justify="space-between">
                                      <Text fontSize="sm">Current Value</Text>
                                      <Text fontSize="lg" fontWeight="bold" color="blue.600">
                                        {sensor.value}{sensor.unit}
                                      </Text>
                                    </HStack>
                                    
                                    <HStack justify="space-between">
                                      <Text fontSize="sm">Location</Text>
                                      <Text fontSize="sm">{sensor.location}</Text>
                                    </HStack>
                                    
                                    <HStack justify="space-between">
                                      <Text fontSize="sm">Battery</Text>
                                      <HStack>
                                        <Progress value={sensor.battery} size="sm" w="60px" />
                                        <Text fontSize="sm">{Math.round(sensor.battery)}%</Text>
                                      </HStack>
                                    </HStack>
                                    
                                    <HStack justify="space-between">
                                      <Text fontSize="sm">Signal</Text>
                                      <HStack>
                                        <Progress value={sensor.signal} size="sm" w="60px" />
                                        <Text fontSize="sm">{Math.round(sensor.signal)}%</Text>
                                      </HStack>
                                    </HStack>
                                    
                                    <HStack justify="space-between">
                                      <Text fontSize="sm">Last Update</Text>
                                      <Text fontSize="sm">{sensor.lastUpdate.toLocaleTimeString()}</Text>
                                    </HStack>
                                  </VStack>
                                </VStack>
                              </CardBody>
                            </Card>
                          </GridItem>
                        ))}
                      </Grid>
                    </CardBody>
                  </Card>
                </VStack>
              ) : (
                <Card bg={bg} border="1px" borderColor={borderColor}>
                  <CardBody textAlign="center" py={12}>
                    <Eye size={48} color="gray" />
                    <Text mt={4} fontSize="lg" color="gray.600">
                      Select a field to view detailed sensor information
                    </Text>
                  </CardBody>
                </Card>
              )}
            </TabPanel>

            {/* Satellite Data Tab */}
            <TabPanel>
              {selectedFieldData ? (
                <VStack spacing={6} align="stretch">
                  <Card bg={bg} border="1px" borderColor={borderColor}>
                    <CardHeader>
                      <HStack>
                        <Satellite size={24} color="blue" />
                        <Heading size="md">{selectedFieldData.name} - Satellite Data</Heading>
                      </HStack>
                    </CardHeader>
                    <CardBody>
                      {selectedFieldData.geeData ? (
                        <VStack spacing={6} align="stretch">
                          {/* GEE Data Overview */}
                          <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(4, 1fr)' }} gap={4}>
                            <GridItem>
                              <Card bg="green.50" border="1px" borderColor="green.200">
                                <CardBody textAlign="center">
                                  <VStack spacing={2}>
                                    <Globe size={32} color="green" />
                                    <Text fontWeight="bold" color="green.700">NDVI</Text>
                                    <Text fontSize="2xl" fontWeight="bold" color="green.600">
                                      {selectedFieldData.geeData.ndvi}
                                    </Text>
                                    <Badge colorScheme="green" size="sm">
                                      {selectedFieldData.geeData.vegetationHealth}
                                    </Badge>
                                  </VStack>
                                </CardBody>
                              </Card>
                            </GridItem>
                            
                            <GridItem>
                              <Card bg="blue.50" border="1px" borderColor="blue.200">
                                <CardBody textAlign="center">
                                  <VStack spacing={2}>
                                    <Sun size={32} color="blue" />
                                    <Text fontWeight="bold" color="blue.700">EVI</Text>
                                    <Text fontSize="2xl" fontWeight="bold" color="blue.600">
                                      {selectedFieldData.geeData.evi}
                                    </Text>
                                    <Text fontSize="sm" color="blue.600">Enhanced Vegetation</Text>
                                  </VStack>
                                </CardBody>
                              </Card>
                            </GridItem>
                            
                            <GridItem>
                              <Card bg="orange.50" border="1px" borderColor="orange.200">
                                <CardBody textAlign="center">
                                  <VStack spacing={2}>
                                    <Droplets size={32} color="orange" />
                                    <Text fontWeight="bold" color="orange.700">SAVI</Text>
                                    <Text fontSize="2xl" fontWeight="bold" color="orange.600">
                                      {selectedFieldData.geeData.savi}
                                    </Text>
                                    <Text fontSize="sm" color="orange.600">Soil Adjusted</Text>
                                  </VStack>
                                </CardBody>
                              </Card>
                            </GridItem>
                            
                            <GridItem>
                              <Card bg="purple.50" border="1px" borderColor="purple.200">
                                <CardBody textAlign="center">
                                  <VStack spacing={2}>
                                    <MapPin size={32} color="purple" />
                                    <Text fontWeight="bold" color="purple.700">Crop Stage</Text>
                                    <Text fontSize="lg" fontWeight="bold" color="purple.600" textTransform="capitalize">
                                      {selectedFieldData.geeData.cropStage}
                                    </Text>
                                    <Text fontSize="sm" color="purple.600">Growth Phase</Text>
                                  </VStack>
                                </CardBody>
                              </Card>
                            </GridItem>
                          </Grid>

                          {/* Environmental Data */}
                          <Card bg="gray.50" border="1px" borderColor="gray.200">
                            <CardHeader>
                              <Heading size="sm">Environmental Conditions</Heading>
                            </CardHeader>
                            <CardBody>
                              <Grid templateColumns={{ base: '1fr', md: 'repeat(3, 1fr)' }} gap={4}>
                                <GridItem>
                                  <HStack justify="space-between">
                                    <HStack>
                                      <Thermometer size={20} color="red" />
                                      <Text>Temperature</Text>
                                    </HStack>
                                    <Text fontWeight="bold">{selectedFieldData.geeData.temperature}°C</Text>
                                  </HStack>
                                </GridItem>
                                
                                <GridItem>
                                  <HStack justify="space-between">
                                    <HStack>
                                      <Droplets size={20} color="blue" />
                                      <Text>Precipitation</Text>
                                    </HStack>
                                    <Text fontWeight="bold">{selectedFieldData.geeData.precipitation}mm</Text>
                                  </HStack>
                                </GridItem>
                                
                                <GridItem>
                                  <HStack justify="space-between">
                                    <HStack>
                                      <Activity size={20} color="green" />
                                      <Text>Soil Moisture</Text>
                                    </HStack>
                                    <Text fontWeight="bold">{selectedFieldData.geeData.soilMoisture}%</Text>
                                  </HStack>
                                </GridItem>
                              </Grid>
                            </CardBody>
                          </Card>

                          {/* Data Source Info */}
                          <Alert status="info" borderRadius="md">
                            <AlertIcon />
                            <AlertDescription>
                              <Text fontWeight="bold">Data Source:</Text> {selectedFieldData.geeData.dataSource}
                              <br />
                              <Text fontSize="sm" color="gray.600">
                                Last Updated: {new Date(selectedFieldData.geeData.timestamp).toLocaleString()}
                              </Text>
                            </AlertDescription>
                          </Alert>
                        </VStack>
                      ) : (
                        <VStack spacing={4} py={8}>
                          <Spinner size="xl" />
                          <Text>Loading satellite data from Google Earth Engine...</Text>
                        </VStack>
                      )}
                    </CardBody>
                  </Card>

                  {/* Time Series Chart */}
                  {selectedFieldData.timeSeries && (
                    <Card bg={bg} border="1px" borderColor={borderColor}>
                      <CardHeader>
                        <Heading size="md">30-Day Vegetation Index Trends</Heading>
                      </CardHeader>
                      <CardBody>
                        <VStack spacing={4} align="stretch">
                          <Text fontSize="sm" color="gray.600">
                            NDVI, EVI, and SAVI trends over the last 30 days
                          </Text>
                          
                          {/* Simple trend visualization */}
                          <Grid templateColumns={{ base: '1fr', md: 'repeat(3, 1fr)' }} gap={4}>
                            <GridItem>
                              <VStack spacing={2}>
                                <Text fontWeight="bold" color="green.600">NDVI Trend</Text>
                                <Progress 
                                  value={selectedFieldData.timeSeries.ndvi[selectedFieldData.timeSeries.ndvi.length - 1] * 100} 
                                  colorScheme="green" 
                                  size="lg"
                                />
                                <Text fontSize="sm">
                                  Current: {selectedFieldData.timeSeries.ndvi[selectedFieldData.timeSeries.ndvi.length - 1].toFixed(3)}
                                </Text>
                              </VStack>
                            </GridItem>
                            
                            <GridItem>
                              <VStack spacing={2}>
                                <Text fontWeight="bold" color="blue.600">EVI Trend</Text>
                                <Progress 
                                  value={selectedFieldData.timeSeries.evi[selectedFieldData.timeSeries.evi.length - 1] * 100} 
                                  colorScheme="blue" 
                                  size="lg"
                                />
                                <Text fontSize="sm">
                                  Current: {selectedFieldData.timeSeries.evi[selectedFieldData.timeSeries.evi.length - 1].toFixed(3)}
                                </Text>
                              </VStack>
                            </GridItem>
                            
                            <GridItem>
                              <VStack spacing={2}>
                                <Text fontWeight="bold" color="orange.600">SAVI Trend</Text>
                                <Progress 
                                  value={selectedFieldData.timeSeries.savi[selectedFieldData.timeSeries.savi.length - 1] * 100} 
                                  colorScheme="orange" 
                                  size="lg"
                                />
                                <Text fontSize="sm">
                                  Current: {selectedFieldData.timeSeries.savi[selectedFieldData.timeSeries.savi.length - 1].toFixed(3)}
                                </Text>
                              </VStack>
                            </GridItem>
                          </Grid>
                        </VStack>
                      </CardBody>
                    </Card>
                  )}
                </VStack>
              ) : (
                <Card bg={bg} border="1px" borderColor={borderColor}>
                  <CardBody textAlign="center" py={12}>
                    <Satellite size={48} color="gray" />
                    <Text mt={4} fontSize="lg" color="gray.600">
                      Select a field to view satellite data from Google Earth Engine
                    </Text>
                  </CardBody>
                </Card>
              )}
            </TabPanel>

            {/* Analytics Tab */}
            <TabPanel>
              <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(4, 1fr)' }} gap={6}>
                <GridItem>
                  <Card bg={bg} border="1px" borderColor={borderColor}>
                    <CardBody>
                      <Stat>
                        <StatLabel>Total Sensors</StatLabel>
                        <StatNumber>
                          {fields.reduce((sum, field) => sum + field.sensors.length, 0)}
                        </StatNumber>
                        <StatHelpText>
                          <StatArrow type="increase" />
                          Across {fields.length} fields
                        </StatHelpText>
                      </Stat>
                    </CardBody>
                  </Card>
                </GridItem>
                
                <GridItem>
                  <Card bg={bg} border="1px" borderColor={borderColor}>
                    <CardBody>
                      <Stat>
                        <StatLabel>Active Alerts</StatLabel>
                        <StatNumber color="red.500">{alerts.length}</StatNumber>
                        <StatHelpText>
                          {alerts.filter(a => a.type === 'critical').length} critical
                        </StatHelpText>
                      </Stat>
                    </CardBody>
                  </Card>
                </GridItem>
                
                <GridItem>
                  <Card bg={bg} border="1px" borderColor={borderColor}>
                    <CardBody>
                      <Stat>
                        <StatLabel>Avg Battery</StatLabel>
                        <StatNumber>
                          {Math.round(
                            fields.reduce((sum, field) => 
                              sum + field.sensors.reduce((s, sensor) => s + sensor.battery, 0), 0
                            ) / fields.reduce((sum, field) => sum + field.sensors.length, 0)
                          )}%
                        </StatNumber>
                        <StatHelpText>
                          <StatArrow type="decrease" />
                          Battery health
                        </StatHelpText>
                      </Stat>
                    </CardBody>
                  </Card>
                </GridItem>
                
                <GridItem>
                  <Card bg={bg} border="1px" borderColor={borderColor}>
                    <CardBody>
                      <Stat>
                        <StatLabel>Avg Signal</StatLabel>
                        <StatNumber>
                          {Math.round(
                            fields.reduce((sum, field) => 
                              sum + field.sensors.reduce((s, sensor) => s + sensor.signal, 0), 0
                            ) / fields.reduce((sum, field) => sum + field.sensors.length, 0)
                          )}%
                        </StatNumber>
                        <StatHelpText>
                          <StatArrow type="increase" />
                          Signal strength
                        </StatHelpText>
                      </Stat>
                    </CardBody>
                  </Card>
                </GridItem>
              </Grid>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Box>
  );
};

export default IoTDashboard;
