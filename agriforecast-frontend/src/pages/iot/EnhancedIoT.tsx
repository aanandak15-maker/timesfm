import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../../services/api'
import demoService from '../../services/demoService';
import {
  Box, VStack, HStack, Text, Heading, Button, SimpleGrid, Card, CardBody,
  Badge, Icon, useToast, Progress, Alert, AlertIcon, AlertDescription,
  Tabs, TabList, TabPanels, Tab, TabPanel, Stat, StatLabel, StatNumber,
  StatHelpText, useColorModeValue, Grid, GridItem, Image, Flex, Spinner,
  Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton,
  useDisclosure, FormControl, FormLabel, Input, Select, Textarea,
  Divider, Switch, Slider, SliderTrack, SliderFilledTrack, SliderThumb
} from '@chakra-ui/react';
import {
  Thermometer, Droplets, Sun, Wind, Battery, Signal, MapPin, 
  AlertTriangle, CheckCircle, Settings, Play, Pause, RotateCcw,
  Plus, Edit, Trash2, Eye, Smartphone, Wifi, WifiOff, Zap,
  Activity, Gauge, Leaf, Droplet, Wind as WindIcon, Lightbulb,
  Shield, AlertCircle, TrendingUp, TrendingDown, Minus
} from 'lucide-react';

// Enhanced field interface with comprehensive sensors
interface EnhancedField {
  id: string;
  name: string;
  crop: string;
  size: string; // in acres
  location: string;
  status: 'healthy' | 'needs_water' | 'needs_fertilizer' | 'pest_alert' | 'harvest_ready' | 'ph_alert' | 'nutrient_deficit';
  sensors: {
    // Environmental sensors
    temperature: number;
    humidity: number;
    soil_moisture: number;
    light_intensity: number;
    wind_speed: number;
    wind_direction: number;
    
    // Soil sensors
    ph: number;
    ec: number; // Electrical Conductivity
    nitrogen: number; // NPK levels
    phosphorus: number;
    potassium: number;
    
    // System sensors
    battery: number;
    signal: number;
    device_health: number;
  };
  lastUpdate: string;
  alerts: string[];
  recommendations: string[];
  historicalData: {
    timestamp: string;
    ph: number;
    temperature: number;
    soil_moisture: number;
    nitrogen: number;
  }[];
}

// Sensor simulation class
class IoTDeviceSimulator {
  private fieldId: string;
  private cropType: string;
  private isRunning: boolean = false;
  private intervalId: NodeJS.Timeout | null = null;

  constructor(fieldId: string, cropType: string) {
    this.fieldId = fieldId;
    this.cropType = cropType;
  }

  start() {
    this.isRunning = true;
    this.intervalId = setInterval(() => {
      this.updateSensorData();
    }, 5000); // Update every 5 seconds
  }

  stop() {
    this.isRunning = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  private updateSensorData() {
    // Simulate realistic sensor data based on crop type and time
    const now = new Date();
    const hour = now.getHours();
    const dayOfYear = Math.floor((now.getTime() - new Date(now.getFullYear(), 0, 0).getTime()) / (1000 * 60 * 60 * 24));
    
    // Dispatch custom event with updated sensor data
    const sensorData = this.generateRealisticSensorData(hour, dayOfYear);
    window.dispatchEvent(new CustomEvent('sensorUpdate', { 
      detail: { fieldId: this.fieldId, data: sensorData } 
    }));
  }

  private generateRealisticSensorData(hour: number, dayOfYear: number) {
    const baseTemp = this.getBaseTemperature(hour, dayOfYear);
    const seasonalFactor = Math.sin((dayOfYear / 365) * 2 * Math.PI);
    
    return {
      // Environmental sensors
      temperature: baseTemp + (Math.random() - 0.5) * 2,
      humidity: 60 + seasonalFactor * 20 + (Math.random() - 0.5) * 10,
      soil_moisture: this.getSoilMoisture(hour, dayOfYear),
      light_intensity: this.getLightIntensity(hour),
      wind_speed: 5 + Math.random() * 10,
      wind_direction: Math.random() * 360,
      
      // Soil sensors
      ph: this.getPHValue(dayOfYear),
      ec: this.getECValue(dayOfYear),
      nitrogen: this.getNPKValue('nitrogen', dayOfYear),
      phosphorus: this.getNPKValue('phosphorus', dayOfYear),
      potassium: this.getNPKValue('potassium', dayOfYear),
      
      // System sensors
      battery: Math.max(20, 100 - (dayOfYear * 0.1) + (Math.random() - 0.5) * 5),
      signal: 85 + (Math.random() - 0.5) * 10,
      device_health: 95 + (Math.random() - 0.5) * 5,
    };
  }

  private getBaseTemperature(hour: number, dayOfYear: number): number {
    const seasonalTemp = 25 + Math.sin((dayOfYear / 365) * 2 * Math.PI) * 8;
    const dailyVariation = Math.sin((hour / 24) * 2 * Math.PI) * 5;
    return seasonalTemp + dailyVariation;
  }

  private getSoilMoisture(hour: number, dayOfYear: number): number {
    const baseMoisture = 40 + Math.sin((dayOfYear / 365) * 2 * Math.PI) * 15;
    const irrigationEffect = hour >= 6 && hour <= 8 ? 20 : 0; // Morning irrigation
    return Math.min(80, baseMoisture + irrigationEffect + (Math.random() - 0.5) * 5);
  }

  private getLightIntensity(hour: number): number {
    if (hour >= 6 && hour <= 18) {
      const peakHour = 12;
      const distanceFromPeak = Math.abs(hour - peakHour);
      return Math.max(0, 1000 - (distanceFromPeak * 100));
    }
    return 0;
  }

  private getPHValue(dayOfYear: number): number {
    const cropOptimalPH = this.getCropOptimalPH();
    const seasonalVariation = Math.sin((dayOfYear / 365) * 2 * Math.PI) * 0.5;
    return cropOptimalPH + seasonalVariation + (Math.random() - 0.5) * 0.3;
  }

  private getECValue(dayOfYear: number): number {
    const cropOptimalEC = this.getCropOptimalEC();
    const seasonalVariation = Math.sin((dayOfYear / 365) * 2 * Math.PI) * 0.2;
    return cropOptimalEC + seasonalVariation + (Math.random() - 0.5) * 0.1;
  }

  private getNPKValue(nutrient: string, dayOfYear: number): number {
    const cropOptimal = this.getCropOptimalNPK(nutrient);
    const growthStage = this.getGrowthStage(dayOfYear);
    const stageMultiplier = this.getNPKStageMultiplier(nutrient, growthStage);
    return cropOptimal * stageMultiplier + (Math.random() - 0.5) * 10;
  }

  private getCropOptimalPH(): number {
    const optimalPH = {
      'Rice': 6.0,
      'Maize': 6.5,
      'Cotton': 6.8
    };
    return optimalPH[this.cropType as keyof typeof optimalPH] || 6.5;
  }

  private getCropOptimalEC(): number {
    const optimalEC = {
      'Rice': 1.2,
      'Maize': 1.5,
      'Cotton': 1.8
    };
    return optimalEC[this.cropType as keyof typeof optimalEC] || 1.5;
  }

  private getCropOptimalNPK(nutrient: string): number {
    const optimalNPK = {
      'Rice': { nitrogen: 120, phosphorus: 60, potassium: 80 },
      'Maize': { nitrogen: 150, phosphorus: 70, potassium: 90 },
      'Cotton': { nitrogen: 100, phosphorus: 50, potassium: 70 }
    };
    const cropNPK = optimalNPK[this.cropType as keyof typeof optimalNPK] || optimalNPK['Rice'];
    return cropNPK[nutrient as keyof typeof cropNPK];
  }

  private getGrowthStage(dayOfYear: number): string {
    if (dayOfYear < 30) return 'germination';
    if (dayOfYear < 60) return 'vegetative';
    if (dayOfYear < 90) return 'flowering';
    if (dayOfYear < 120) return 'fruiting';
    return 'maturity';
  }

  private getNPKStageMultiplier(nutrient: string, stage: string): number {
    const multipliers = {
      'nitrogen': { germination: 0.8, vegetative: 1.2, flowering: 1.0, fruiting: 0.9, maturity: 0.7 },
      'phosphorus': { germination: 1.1, vegetative: 1.0, flowering: 1.3, fruiting: 1.2, maturity: 0.8 },
      'potassium': { germination: 0.9, vegetative: 1.0, flowering: 1.1, fruiting: 1.4, maturity: 1.0 }
    };
    return multipliers[nutrient as keyof typeof multipliers]?.[stage as keyof typeof multipliers.nitrogen] || 1.0;
  }
}

const EnhancedIoT: React.FC = () => {
  const toast = useToast();
  const queryClient = useQueryClient();
  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const [selectedField, setSelectedField] = useState<EnhancedField | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [simulators, setSimulators] = useState<Map<string, IoTDeviceSimulator>>(new Map());
  const [localFields, setLocalFields] = useState<EnhancedField[]>([]);
  const [newFieldData, setNewFieldData] = useState({
    name: '',
    crop: '',
    size: '',
    location: '',
    farm_id: ''
  });

  // Fetch fields and farms data
  const { data: apiFields, isLoading: fieldsLoading } = useQuery({
    queryKey: ['fields'],
    queryFn: () => demoService.getFields(),
  });

  const { data: farms, isLoading: farmsLoading } = useQuery({
    queryKey: ['farms'],
    queryFn: () => demoService.getFarms(),
  });

  // Get field status based on sensor data
  const getFieldStatus = (field: any): EnhancedField['status'] => {
    // This would be determined by analyzing sensor data
    const statuses: EnhancedField['status'][] = ['healthy', 'needs_water', 'needs_fertilizer', 'pest_alert', 'harvest_ready', 'ph_alert', 'nutrient_deficit'];
    return statuses[Math.floor(Math.random() * statuses.length)];
  };

  // Transform API fields to enhanced format
  const fields: EnhancedField[] = React.useMemo(() => {
    if (!apiFields || !Array.isArray(apiFields)) return localFields;
    
    const transformedFields = apiFields.map((field: any) => ({
      id: field.id,
      name: field.name,
      crop: field.crop_type,
      size: field.area_acres?.toString() || '1.0',
      location: field.farm_id ? `Farm ${field.farm_id}` : 'Unknown Farm',
      status: getFieldStatus(field),
      sensors: {
        temperature: 25 + Math.random() * 10,
        humidity: 60 + Math.random() * 20,
        soil_moisture: 40 + Math.random() * 30,
        light_intensity: 500 + Math.random() * 500,
        wind_speed: 5 + Math.random() * 10,
        wind_direction: Math.random() * 360,
        ph: 6.5 + (Math.random() - 0.5) * 1,
        ec: 1.5 + (Math.random() - 0.5) * 0.5,
        nitrogen: 100 + Math.random() * 50,
        phosphorus: 50 + Math.random() * 30,
        potassium: 70 + Math.random() * 40,
        battery: 80 + Math.random() * 20,
        signal: 85 + Math.random() * 15,
        device_health: 95 + Math.random() * 5,
      },
      lastUpdate: new Date().toISOString(),
      alerts: [],
      recommendations: [],
      historicalData: []
    }));
    
    return transformedFields;
  }, [apiFields, localFields]);

  // Create field mutation
  const createFieldMutation = useMutation({
    mutationFn: apiService.createField,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fields'] });
      toast({
        title: 'Field added successfully!',
        description: 'Your new field is now being monitored',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      setNewFieldData({ name: '', crop: '', size: '', location: '', farm_id: '' });
      onClose();
    },
    onError: (error: any) => {
      console.error('Field creation error:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to add field';
      toast({
        title: 'Error adding field',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  // Handle field addition
  const handleAddFieldSubmit = () => {
    if (!newFieldData.name || !newFieldData.crop || !newFieldData.size || !newFieldData.farm_id) {
      toast({
        title: 'Missing required fields',
        description: 'Please fill in all required information',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    const fieldData = {
      name: newFieldData.name,
      farm_id: newFieldData.farm_id,
      crop_type: newFieldData.crop,
      area_acres: parseFloat(newFieldData.size),
      latitude: 28.368911,
      longitude: 77.541033,
      soil_type: 'Loamy'
    };

    console.log('Creating field with data:', fieldData);
    createFieldMutation.mutate(fieldData);
  };

  // Start/stop simulation
  const toggleSimulation = () => {
    if (isSimulating) {
      // Stop all simulators
      simulators.forEach(simulator => simulator.stop());
      setSimulators(new Map());
      setIsSimulating(false);
      toast({
        title: 'Simulation stopped',
        description: 'All IoT devices are now offline',
        status: 'info',
        duration: 2000,
        isClosable: true,
      });
    } else {
      // Start simulators for all fields
      const newSimulators = new Map();
      fields.forEach(field => {
        const simulator = new IoTDeviceSimulator(field.id, field.crop);
        simulator.start();
        newSimulators.set(field.id, simulator);
      });
      setSimulators(newSimulators);
      setIsSimulating(true);
      toast({
        title: 'Simulation started',
        description: `${fields.length} IoT devices are now active`,
        status: 'success',
        duration: 2000,
        isClosable: true,
      });
    }
  };

  // Listen for sensor updates
  useEffect(() => {
    const handleSensorUpdate = (event: CustomEvent) => {
      const { fieldId, data } = event.detail;
      // Update field sensor data
      setLocalFields(prevFields => 
        prevFields.map(field => 
          field.id === fieldId 
            ? { ...field, sensors: { ...field.sensors, ...data }, lastUpdate: new Date().toISOString() }
            : field
        )
      );
    };

    window.addEventListener('sensorUpdate', handleSensorUpdate as EventListener);
    return () => {
      window.removeEventListener('sensorUpdate', handleSensorUpdate as EventListener);
    };
  }, []);

  // Monitor online status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Get status color
  const getStatusColor = (status: EnhancedField['status']) => {
    const colors = {
      healthy: 'green',
      needs_water: 'blue',
      needs_fertilizer: 'orange',
      pest_alert: 'red',
      harvest_ready: 'purple',
      ph_alert: 'yellow',
      nutrient_deficit: 'red'
    };
    return colors[status] || 'gray';
  };

  // Get status icon
  const getStatusIcon = (status: EnhancedField['status']) => {
    const icons = {
      healthy: CheckCircle,
      needs_water: Droplets,
      needs_fertilizer: Leaf,
      pest_alert: AlertTriangle,
      harvest_ready: TrendingUp,
      ph_alert: AlertCircle,
      nutrient_deficit: Minus
    };
    return icons[status] || CheckCircle;
  };

  // Get sensor status
  const getSensorStatus = (value: number, optimal: { min: number; max: number }, type: 'higher' | 'lower' | 'range' = 'range') => {
    if (type === 'higher') return value >= optimal.min ? 'good' : 'warning';
    if (type === 'lower') return value <= optimal.max ? 'good' : 'warning';
    return value >= optimal.min && value <= optimal.max ? 'good' : 'warning';
  };

  if (fieldsLoading || farmsLoading) {
    return (
      <Box p={6} display="flex" justifyContent="center" alignItems="center" minH="400px">
        <Spinner size="xl" />
      </Box>
    );
  }

  return (
    <Box p={6} maxW="1400px" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <HStack justifyContent="space-between" alignItems="center">
          <Heading as="h1" size="xl">
            <HStack>
              <Icon as={Activity} size={32} />
              <Text>Enhanced IoT Monitoring</Text>
            </HStack>
          </Heading>
          <HStack spacing={4}>
            <Button
              colorScheme={isSimulating ? "red" : "green"}
              onClick={toggleSimulation}
              leftIcon={<Icon as={isSimulating ? Pause : Play} />}
            >
              {isSimulating ? 'Stop Simulation' : 'Start Simulation'}
            </Button>
            <Button colorScheme="blue" onClick={onOpen} leftIcon={<Icon as={Plus} />}>
              + Add Field
            </Button>
          </HStack>
        </HStack>

        {/* System Status */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <HStack spacing={6} alignItems="center">
              <HStack spacing={2}>
                <Icon as={isOnline ? Wifi : WifiOff} color={isOnline ? "green.500" : "red.500"} />
                <Text fontSize="sm" fontWeight="bold">
                  {isOnline ? 'Online' : 'Offline'}
                </Text>
              </HStack>
              <HStack spacing={2}>
                <Icon as={isSimulating ? Activity : Pause} color={isSimulating ? "green.500" : "gray.500"} />
                <Text fontSize="sm" fontWeight="bold">
                  {isSimulating ? 'Simulating' : 'Stopped'}
                </Text>
              </HStack>
              <HStack spacing={2}>
                <Icon as={Smartphone} color="blue.500" />
                <Text fontSize="sm" fontWeight="bold">
                  {fields.length} Fields Monitored
                </Text>
              </HStack>
            </HStack>
          </CardBody>
        </Card>

        {/* Fields Grid */}
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
          {fields.map((field) => (
            <Card key={field.id} bg={bg} border="1px" borderColor={borderColor} cursor="pointer"
                  onClick={() => setSelectedField(field)}>
              <CardBody>
                <VStack spacing={4} align="stretch">
                  {/* Field Header */}
                  <HStack justifyContent="space-between" alignItems="center">
                    <VStack align="start" spacing={0}>
                      <Text fontWeight="bold" fontSize="lg">{field.name}</Text>
                      <Text fontSize="sm" color="gray.600">{field.crop} • {field.size} acres</Text>
                    </VStack>
                    <Badge colorScheme={getStatusColor(field.status)}>
                      <HStack spacing={1}>
                        <Icon as={getStatusIcon(field.status)} size={12} />
                        <Text fontSize="xs">{field.status.replace('_', ' ')}</Text>
                      </HStack>
                    </Badge>
                  </HStack>

                  {/* Key Sensors */}
                  <SimpleGrid columns={2} spacing={3}>
                    <HStack spacing={2}>
                      <Icon as={Thermometer} size={16} color="red.500" />
                      <VStack align="start" spacing={0}>
                        <Text fontSize="xs" color="gray.600">Temperature</Text>
                        <Text fontSize="sm" fontWeight="bold">{field.sensors.temperature.toFixed(1)}°C</Text>
                      </VStack>
                    </HStack>
                    
                    <HStack spacing={2}>
                      <Icon as={Droplets} size={16} color="blue.500" />
                      <VStack align="start" spacing={0}>
                        <Text fontSize="xs" color="gray.600">Soil Moisture</Text>
                        <Text fontSize="sm" fontWeight="bold">{field.sensors.soil_moisture.toFixed(1)}%</Text>
                      </VStack>
                    </HStack>
                    
                    <HStack spacing={2}>
                      <Icon as={Gauge} size={16} color="purple.500" />
                      <VStack align="start" spacing={0}>
                        <Text fontSize="xs" color="gray.600">pH</Text>
                        <Text fontSize="sm" fontWeight="bold">{field.sensors.ph.toFixed(1)}</Text>
                      </VStack>
                    </HStack>
                    
                    <HStack spacing={2}>
                      <Icon as={Zap} size={16} color="yellow.500" />
                      <VStack align="start" spacing={0}>
                        <Text fontSize="xs" color="gray.600">EC</Text>
                        <Text fontSize="sm" fontWeight="bold">{field.sensors.ec.toFixed(1)}</Text>
                      </VStack>
                    </HStack>
                  </SimpleGrid>

                  {/* System Status */}
                  <HStack justifyContent="space-between" alignItems="center">
                    <HStack spacing={2}>
                      <Icon as={Battery} size={14} color={field.sensors.battery > 50 ? "green.500" : "red.500"} />
                      <Text fontSize="xs">{field.sensors.battery.toFixed(0)}%</Text>
                    </HStack>
                    <HStack spacing={2}>
                      <Icon as={Signal} size={14} color={field.sensors.signal > 70 ? "green.500" : "red.500"} />
                      <Text fontSize="xs">{field.sensors.signal.toFixed(0)}%</Text>
                    </HStack>
                    <Text fontSize="xs" color="gray.500">
                      {new Date(field.lastUpdate).toLocaleTimeString()}
                    </Text>
                  </HStack>
                </VStack>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>

        {/* Field Details Modal */}
        {selectedField && (
          <Modal isOpen={!!selectedField} onClose={() => setSelectedField(null)} size="6xl">
            <ModalOverlay />
            <ModalContent>
              <ModalHeader>
                <HStack>
                  <Icon as={MapPin} />
                  <Text>{selectedField.name} - Detailed Monitoring</Text>
                </HStack>
              </ModalHeader>
              <ModalCloseButton />
              <ModalBody pb={6}>
                <Tabs>
                  <TabList>
                    <Tab>Environmental</Tab>
                    <Tab>Soil Analysis</Tab>
                    <Tab>NPK Levels</Tab>
                    <Tab>System Health</Tab>
                    <Tab>Historical Data</Tab>
                  </TabList>

                  <TabPanels>
                    {/* Environmental Sensors */}
                    <TabPanel>
                      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                        <Card>
                          <CardBody>
                            <Stat>
                              <StatLabel>
                                <HStack>
                                  <Icon as={Thermometer} color="red.500" />
                                  <Text>Temperature</Text>
                                </HStack>
                              </StatLabel>
                              <StatNumber>{selectedField.sensors.temperature.toFixed(1)}°C</StatNumber>
                              <StatHelpText>
                                {selectedField.sensors.temperature > 35 ? 'High' : 
                                 selectedField.sensors.temperature < 15 ? 'Low' : 'Optimal'}
                              </StatHelpText>
                            </Stat>
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <Stat>
                              <StatLabel>
                                <HStack>
                                  <Icon as={Droplets} color="blue.500" />
                                  <Text>Humidity</Text>
                                </HStack>
                              </StatLabel>
                              <StatNumber>{selectedField.sensors.humidity.toFixed(1)}%</StatNumber>
                              <StatHelpText>
                                {selectedField.sensors.humidity > 80 ? 'High' : 
                                 selectedField.sensors.humidity < 40 ? 'Low' : 'Optimal'}
                              </StatHelpText>
                            </Stat>
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <Stat>
                              <StatLabel>
                                <HStack>
                                  <Icon as={Droplet} color="green.500" />
                                  <Text>Soil Moisture</Text>
                                </HStack>
                              </StatLabel>
                              <StatNumber>{selectedField.sensors.soil_moisture.toFixed(1)}%</StatNumber>
                              <StatHelpText>
                                {selectedField.sensors.soil_moisture > 70 ? 'High' : 
                                 selectedField.sensors.soil_moisture < 30 ? 'Low' : 'Optimal'}
                              </StatHelpText>
                            </Stat>
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <Stat>
                              <StatLabel>
                                <HStack>
                                  <Icon as={Lightbulb} color="yellow.500" />
                                  <Text>Light Intensity</Text>
                                </HStack>
                              </StatLabel>
                              <StatNumber>{selectedField.sensors.light_intensity.toFixed(0)} lux</StatNumber>
                              <StatHelpText>
                                {selectedField.sensors.light_intensity > 800 ? 'High' : 
                                 selectedField.sensors.light_intensity < 200 ? 'Low' : 'Optimal'}
                              </StatHelpText>
                            </Stat>
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <Stat>
                              <StatLabel>
                                <HStack>
                                  <Icon as={WindIcon} color="gray.500" />
                                  <Text>Wind Speed</Text>
                                </HStack>
                              </StatLabel>
                              <StatNumber>{selectedField.sensors.wind_speed.toFixed(1)} km/h</StatNumber>
                              <StatHelpText>
                                Direction: {selectedField.sensors.wind_direction.toFixed(0)}°
                              </StatHelpText>
                            </Stat>
                          </CardBody>
                        </Card>
                      </SimpleGrid>
                    </TabPanel>

                    {/* Soil Analysis */}
                    <TabPanel>
                      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                        <Card>
                          <CardBody>
                            <VStack spacing={4} align="stretch">
                              <Heading size="md">pH Level</Heading>
                              <Stat>
                                <StatNumber fontSize="3xl" color={getSensorStatus(selectedField.sensors.ph, { min: 6.0, max: 7.0 }) === 'good' ? 'green.500' : 'red.500'}>
                                  {selectedField.sensors.ph.toFixed(2)}
                                </StatNumber>
                                <StatHelpText>
                                  {selectedField.sensors.ph < 6.0 ? 'Too Acidic' : 
                                   selectedField.sensors.ph > 7.0 ? 'Too Alkaline' : 'Optimal'}
                                </StatHelpText>
                              </Stat>
                              <Progress 
                                value={(selectedField.sensors.ph / 14) * 100} 
                                colorScheme={getSensorStatus(selectedField.sensors.ph, { min: 6.0, max: 7.0 }) === 'good' ? 'green' : 'red'}
                              />
                            </VStack>
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <VStack spacing={4} align="stretch">
                              <Heading size="md">Electrical Conductivity (EC)</Heading>
                              <Stat>
                                <StatNumber fontSize="3xl" color={getSensorStatus(selectedField.sensors.ec, { min: 1.0, max: 2.0 }) === 'good' ? 'green.500' : 'red.500'}>
                                  {selectedField.sensors.ec.toFixed(2)} dS/m
                                </StatNumber>
                                <StatHelpText>
                                  {selectedField.sensors.ec < 1.0 ? 'Low Salinity' : 
                                   selectedField.sensors.ec > 2.0 ? 'High Salinity' : 'Optimal'}
                                </StatHelpText>
                              </Stat>
                              <Progress 
                                value={(selectedField.sensors.ec / 3) * 100} 
                                colorScheme={getSensorStatus(selectedField.sensors.ec, { min: 1.0, max: 2.0 }) === 'good' ? 'green' : 'red'}
                              />
                            </VStack>
                          </CardBody>
                        </Card>
                      </SimpleGrid>
                    </TabPanel>

                    {/* NPK Levels */}
                    <TabPanel>
                      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                        <Card>
                          <CardBody>
                            <VStack spacing={4} align="stretch">
                              <Heading size="md" color="blue.500">Nitrogen (N)</Heading>
                              <Stat>
                                <StatNumber fontSize="2xl">{selectedField.sensors.nitrogen.toFixed(0)} ppm</StatNumber>
                                <StatHelpText>
                                  {selectedField.sensors.nitrogen < 80 ? 'Deficient' : 
                                   selectedField.sensors.nitrogen > 150 ? 'Excessive' : 'Optimal'}
                                </StatHelpText>
                              </Stat>
                              <Progress 
                                value={(selectedField.sensors.nitrogen / 200) * 100} 
                                colorScheme={getSensorStatus(selectedField.sensors.nitrogen, { min: 80, max: 150 }) === 'good' ? 'green' : 'red'}
                              />
                            </VStack>
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <VStack spacing={4} align="stretch">
                              <Heading size="md" color="red.500">Phosphorus (P)</Heading>
                              <Stat>
                                <StatNumber fontSize="2xl">{selectedField.sensors.phosphorus.toFixed(0)} ppm</StatNumber>
                                <StatHelpText>
                                  {selectedField.sensors.phosphorus < 40 ? 'Deficient' : 
                                   selectedField.sensors.phosphorus > 80 ? 'Excessive' : 'Optimal'}
                                </StatHelpText>
                              </Stat>
                              <Progress 
                                value={(selectedField.sensors.phosphorus / 100) * 100} 
                                colorScheme={getSensorStatus(selectedField.sensors.phosphorus, { min: 40, max: 80 }) === 'good' ? 'green' : 'red'}
                              />
                            </VStack>
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <VStack spacing={4} align="stretch">
                              <Heading size="md" color="green.500">Potassium (K)</Heading>
                              <Stat>
                                <StatNumber fontSize="2xl">{selectedField.sensors.potassium.toFixed(0)} ppm</StatNumber>
                                <StatHelpText>
                                  {selectedField.sensors.potassium < 60 ? 'Deficient' : 
                                   selectedField.sensors.potassium > 120 ? 'Excessive' : 'Optimal'}
                                </StatHelpText>
                              </Stat>
                              <Progress 
                                value={(selectedField.sensors.potassium / 150) * 100} 
                                colorScheme={getSensorStatus(selectedField.sensors.potassium, { min: 60, max: 120 }) === 'good' ? 'green' : 'red'}
                              />
                            </VStack>
                          </CardBody>
                        </Card>
                      </SimpleGrid>
                    </TabPanel>

                    {/* System Health */}
                    <TabPanel>
                      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                        <Card>
                          <CardBody>
                            <Stat>
                              <StatLabel>
                                <HStack>
                                  <Icon as={Battery} color={selectedField.sensors.battery > 50 ? "green.500" : "red.500"} />
                                  <Text>Battery Level</Text>
                                </HStack>
                              </StatLabel>
                              <StatNumber>{selectedField.sensors.battery.toFixed(0)}%</StatNumber>
                              <StatHelpText>
                                {selectedField.sensors.battery > 50 ? 'Good' : 'Low - Replace Soon'}
                              </StatHelpText>
                            </Stat>
                            <Progress 
                              value={selectedField.sensors.battery} 
                              colorScheme={selectedField.sensors.battery > 50 ? 'green' : 'red'}
                            />
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <Stat>
                              <StatLabel>
                                <HStack>
                                  <Icon as={Signal} color={selectedField.sensors.signal > 70 ? "green.500" : "red.500"} />
                                  <Text>Signal Strength</Text>
                                </HStack>
                              </StatLabel>
                              <StatNumber>{selectedField.sensors.signal.toFixed(0)}%</StatNumber>
                              <StatHelpText>
                                {selectedField.sensors.signal > 70 ? 'Strong' : 'Weak'}
                              </StatHelpText>
                            </Stat>
                            <Progress 
                              value={selectedField.sensors.signal} 
                              colorScheme={selectedField.sensors.signal > 70 ? 'green' : 'red'}
                            />
                          </CardBody>
                        </Card>

                        <Card>
                          <CardBody>
                            <Stat>
                              <StatLabel>
                                <HStack>
                                  <Icon as={Shield} color={selectedField.sensors.device_health > 90 ? "green.500" : "red.500"} />
                                  <Text>Device Health</Text>
                                </HStack>
                              </StatLabel>
                              <StatNumber>{selectedField.sensors.device_health.toFixed(0)}%</StatNumber>
                              <StatHelpText>
                                {selectedField.sensors.device_health > 90 ? 'Excellent' : 'Needs Attention'}
                              </StatHelpText>
                            </Stat>
                            <Progress 
                              value={selectedField.sensors.device_health} 
                              colorScheme={selectedField.sensors.device_health > 90 ? 'green' : 'red'}
                            />
                          </CardBody>
                        </Card>
                      </SimpleGrid>
                    </TabPanel>

                    {/* Historical Data */}
                    <TabPanel>
                      <Card>
                        <CardBody>
                          <VStack spacing={4} align="stretch">
                            <Heading size="md">Historical Trends</Heading>
                            <Text color="gray.600">
                              Historical data visualization would be implemented here with charts showing:
                            </Text>
                            <VStack align="start" spacing={2}>
                              <Text>• pH levels over time</Text>
                              <Text>• Temperature variations</Text>
                              <Text>• Soil moisture patterns</Text>
                              <Text>• NPK level changes</Text>
                            </VStack>
                          </VStack>
                        </CardBody>
                      </Card>
                    </TabPanel>
                  </TabPanels>
                </Tabs>
              </ModalBody>
            </ModalContent>
          </Modal>
        )}

        {/* Add Field Modal */}
        <Modal isOpen={isOpen} onClose={onClose}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Add New Field</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <VStack spacing={4}>
                <FormControl isRequired>
                  <FormLabel>Field Name (खेत का नाम)</FormLabel>
                  <Input
                    placeholder="e.g., North Rice Field"
                    value={newFieldData.name}
                    onChange={(e) => setNewFieldData({ ...newFieldData, name: e.target.value })}
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Farm (खेत)</FormLabel>
                  <Select 
                    placeholder="Select farm"
                    value={newFieldData.farm_id}
                    onChange={(e) => setNewFieldData({ ...newFieldData, farm_id: e.target.value })}
                  >
                    {farms?.map((farm: any) => (
                      <option key={farm.id} value={farm.id}>{farm.name}</option>
                    ))}
                  </Select>
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Crop Type (फसल का प्रकार)</FormLabel>
                  <Select 
                    placeholder="Select crop"
                    value={newFieldData.crop}
                    onChange={(e) => setNewFieldData({ ...newFieldData, crop: e.target.value })}
                  >
                    <option value="Rice">Rice (चावल)</option>
                    <option value="Maize">Maize (मक्का)</option>
                    <option value="Cotton">Cotton (कपास)</option>
                  </Select>
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Field Size (खेत का आकार) - acres</FormLabel>
                  <Input
                    type="number"
                    placeholder="e.g., 1.5"
                    value={newFieldData.size}
                    onChange={(e) => setNewFieldData({ ...newFieldData, size: e.target.value })}
                    min="0.1"
                    max="10"
                    step="0.1"
                  />
                </FormControl>
                
                <HStack spacing={4} width="full">
                  <Button
                    colorScheme="green"
                    onClick={handleAddFieldSubmit}
                    isLoading={createFieldMutation.isPending}
                    loadingText="Adding..."
                    flex={1}
                  >
                    Add Field
                  </Button>
                  <Button variant="outline" onClick={onClose} flex={1}>
                    Cancel
                  </Button>
                </HStack>
              </VStack>
            </ModalBody>
          </ModalContent>
        </Modal>
      </VStack>
    </Box>
  );
};

export default EnhancedIoT;
