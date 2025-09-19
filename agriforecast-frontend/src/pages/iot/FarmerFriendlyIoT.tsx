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
  useDisclosure, FormControl, FormLabel, Input, Select, Textarea
} from '@chakra-ui/react';
import {
  Thermometer, Droplets, Sun, Wind, Battery, Signal, MapPin, 
  AlertTriangle, CheckCircle, Settings, Play, Pause, RotateCcw,
  Plus, Edit, Trash2, Eye, Smartphone, Wifi, WifiOff
} from 'lucide-react';

// Simple field interface for small farmers
interface SimpleField {
  id: string;
  name: string;
  crop: string;
  size: string; // in acres or bigha
  location: string; // simple village/town name
  status: 'healthy' | 'needs_water' | 'needs_fertilizer' | 'pest_alert' | 'harvest_ready';
  sensors: {
    temperature: number;
    humidity: number;
    soil_moisture: number;
    light: number;
    battery: number;
    signal: number;
  };
  lastUpdate: string;
  alerts: string[];
}

const FarmerFriendlyIoT: React.FC = () => {
  const toast = useToast();
  const queryClient = useQueryClient();
  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const [selectedField, setSelectedField] = useState<SimpleField | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [newFieldData, setNewFieldData] = useState({
    name: '',
    crop: '',
    size: '',
    location: '',
    farm_id: ''
  });

  // Fetch fields from API
  const { data: apiFields, isLoading: fieldsLoading, error: fieldsError } = useQuery({
    queryKey: ['fields'],
    queryFn: () => demoService.getFields(),
  });

  // Fetch farms from API
  const { data: farms, isLoading: farmsLoading } = useQuery({
    queryKey: ['farms'],
    queryFn: () => demoService.getFarms(),
  });

  // Convert API fields to SimpleField format
  const fields: SimpleField[] = apiFields?.map(field => ({
    id: field.id,
    name: field.name,
    crop: field.crop_type || 'Unknown',
    size: `${field.area || 1} acres`,
    location: `Farm: ${farms?.find(f => f.id === field.farm_id)?.name || 'Unknown'}`,
    status: 'healthy' as const,
    sensors: {
      temperature: 25 + Math.random() * 10,
      humidity: 50 + Math.random() * 30,
      soil_moisture: 40 + Math.random() * 30,
      light: 600 + Math.random() * 400,
      battery: 80 + Math.random() * 20,
      signal: 70 + Math.random() * 30
    },
    lastUpdate: new Date().toLocaleString(),
    alerts: []
  })) || [];

  // Set selected field when fields are loaded
  useEffect(() => {
    if (fields.length > 0 && !selectedField) {
      setSelectedField(fields[0]);
    }
  }, [fields, selectedField]);

  // Check online status
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

  // Simulate sensor updates
  useEffect(() => {
    if (isSimulating) {
      const interval = setInterval(() => {
        // Trigger a refetch of fields to simulate sensor updates
        queryClient.invalidateQueries({ queryKey: ['fields'] });
      }, 5000); // Update every 5 seconds
      
      return () => clearInterval(interval);
    }
  }, [isSimulating, queryClient]);

  // Create field mutation
  const createFieldMutation = useMutation({
    mutationFn: apiService.createField,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fields'] });
      toast({
        title: 'Field added successfully!',
        description: 'Your new field has been added to the system',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      setNewFieldData({
        name: '',
        crop: '',
        size: '',
        location: '',
        farm_id: ''
      });
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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'green';
      case 'needs_water': return 'blue';
      case 'needs_fertilizer': return 'orange';
      case 'pest_alert': return 'red';
      case 'harvest_ready': return 'purple';
      default: return 'gray';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'healthy': return 'स्वस्थ (Healthy)';
      case 'needs_water': return 'पानी चाहिए (Needs Water)';
      case 'needs_fertilizer': return 'खाद चाहिए (Needs Fertilizer)';
      case 'pest_alert': return 'कीट चेतावनी (Pest Alert)';
      case 'harvest_ready': return 'कटाई तैयार (Ready for Harvest)';
      default: return 'अज्ञात (Unknown)';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return CheckCircle;
      case 'needs_water': return Droplets;
      case 'needs_fertilizer': return Sun;
      case 'pest_alert': return AlertTriangle;
      case 'harvest_ready': return CheckCircle;
      default: return AlertTriangle;
    }
  };

  const handleStartStopSimulation = () => {
    setIsSimulating(!isSimulating);
    toast({
      title: isSimulating ? 'Simulation Stopped' : 'Simulation Started',
      description: isSimulating ? 'Sensor updates stopped' : 'Sensor updates started every 5 seconds',
      status: isSimulating ? 'info' : 'success',
      duration: 2000,
      isClosable: true,
    });
  };

  const addNewField = () => {
    setNewFieldData({
      name: '',
      crop: '',
      size: '',
      location: '',
      farm_id: farms && farms.length > 0 ? farms[0].id : ''
    });
    onOpen();
  };

  const handleAddFieldSubmit = () => {
    if (!newFieldData.name || !newFieldData.crop || !newFieldData.size || !newFieldData.location || !newFieldData.farm_id) {
      toast({
        title: 'Please fill all fields',
        description: 'All fields including farm selection are required',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    if (!farms || farms.length === 0) {
      toast({
        title: 'No farms available',
        description: 'Please create a farm first before adding fields',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    // Extract area from size string (e.g., "2 acres" -> 2)
    const areaMatch = newFieldData.size.match(/(\d+(?:\.\d+)?)/);
    const area = areaMatch ? parseFloat(areaMatch[1]) : 1;

    // Extract crop type from the selected option
    const cropType = newFieldData.crop.split(' (')[0]; // Remove Hindi part

    const fieldData = {
      name: newFieldData.name,
      farm_id: newFieldData.farm_id,
      crop_type: cropType,
      area_acres: area, // Fixed: backend expects area_acres, not area
      latitude: 28.368911, // Default coordinates for India
      longitude: 77.541033, // Default coordinates for India
      soil_type: 'Loamy', // Fixed: backend expects proper case
      planting_date: new Date().toISOString().split('T')[0]
    };

    console.log('Creating field with data:', fieldData);
    createFieldMutation.mutate(fieldData);
  };

  if (fieldsLoading || farmsLoading) {
    return (
      <VStack p={8} spacing={4} align="center">
        <Spinner size="xl" color="green.500" />
        <Text fontSize="xl">Loading your fields...</Text>
      </VStack>
    );
  }

  if (fieldsError) {
    return (
      <VStack p={8} spacing={4} align="center">
        <Alert status="error">
          <AlertIcon />
          <AlertDescription>
            Error loading fields: {fieldsError.message}
          </AlertDescription>
        </Alert>
      </VStack>
    );
  }

  return (
    <Box p={4} maxW="1200px" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <VStack spacing={4}>
              <HStack>
                <Icon as={Smartphone} w={8} h={8} color="green.500" />
                <Heading size="lg" color="green.600">
                  किसान IoT डैशबोर्ड (Farmer IoT Dashboard)
                </Heading>
              </HStack>
              
              <HStack spacing={4} wrap="wrap">
                <HStack>
                  <Icon as={isOnline ? Wifi : WifiOff} color={isOnline ? 'green' : 'red'} />
                  <Text fontSize="sm" color={isOnline ? 'green.600' : 'red.600'}>
                    {isOnline ? 'Online' : 'Offline Mode'}
                  </Text>
                </HStack>
                
                <Button
                  colorScheme={isSimulating ? 'red' : 'green'}
                  leftIcon={isSimulating ? <Icon as={Pause} /> : <Icon as={Play} />}
                  onClick={handleStartStopSimulation}
                  size="sm"
                >
                  {isSimulating ? 'Stop Updates' : 'Start Updates'}
                </Button>
                
                <Button
                  leftIcon={<Icon as={Plus} />}
                  onClick={addNewField}
                  colorScheme="blue"
                  size="sm"
                >
                  Add Field
                </Button>
              </HStack>
            </VStack>
          </CardBody>
        </Card>

        {/* Offline Alert */}
        {!isOnline && (
          <Alert status="warning">
            <AlertIcon />
            <AlertDescription>
              You're offline. Data will sync when connection is restored.
            </AlertDescription>
          </Alert>
        )}

        {/* Fields Overview */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <Heading size="md" mb={4}>Your Fields (आपके खेत)</Heading>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              {fields.map(field => (
                <Card
                  key={field.id}
                  bg={selectedField?.id === field.id ? 'green.50' : bg}
                  border="2px"
                  borderColor={selectedField?.id === field.id ? 'green.300' : borderColor}
                  cursor="pointer"
                  onClick={() => setSelectedField(field)}
                  _hover={{ borderColor: 'green.400', shadow: 'md' }}
                >
                  <CardBody>
                    <VStack spacing={3} align="stretch">
                      <HStack justify="space-between">
                        <Text fontWeight="bold" fontSize="lg">{field.name}</Text>
                        <Badge colorScheme={getStatusColor(field.status)}>
                          {getStatusText(field.status)}
                        </Badge>
                      </HStack>
                      
                      <Text fontSize="sm" color="gray.600">
                        {field.crop} • {field.size}
                      </Text>
                      
                      <Text fontSize="sm" color="gray.500">
                        {field.location}
                      </Text>
                      
                      <HStack justify="space-between">
                        <HStack>
                          <Icon as={Thermometer} color="red" />
                          <Text fontSize="sm">{field.sensors.temperature}°C</Text>
                        </HStack>
                        <HStack>
                          <Icon as={Droplets} color="blue" />
                          <Text fontSize="sm">{field.sensors.soil_moisture}%</Text>
                        </HStack>
                      </HStack>
                      
                      <HStack justify="space-between">
                        <HStack>
                          <Icon as={Battery} color="green" />
                          <Text fontSize="sm">{field.sensors.battery.toFixed(0)}%</Text>
                        </HStack>
                        <HStack>
                          <Icon as={Signal} color="blue" />
                          <Text fontSize="sm">{field.sensors.signal.toFixed(0)}%</Text>
                        </HStack>
                      </HStack>
                      
                      {field.alerts.length > 0 && (
                        <Alert status="warning" size="sm">
                          <AlertIcon />
                          <Text fontSize="xs">{field.alerts[0]}</Text>
                        </Alert>
                      )}
                    </VStack>
                  </CardBody>
                </Card>
              ))}
            </SimpleGrid>
          </CardBody>
        </Card>

        {/* Selected Field Details */}
        {selectedField && (
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody>
              <VStack spacing={6} align="stretch">
                <HStack justify="space-between">
                  <Heading size="md">{selectedField.name}</Heading>
                  <HStack>
                    <Button size="sm" leftIcon={<Icon as={Edit} />}>
                      Edit
                    </Button>
                    <Button size="sm" leftIcon={<Icon as={Eye} />} colorScheme="blue">
                      View Map
                    </Button>
                  </HStack>
                </HStack>

                <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(4, 1fr)' }} gap={4}>
                  {/* Temperature */}
                  <GridItem>
                    <Card bg="red.50" border="1px" borderColor="red.200">
                      <CardBody textAlign="center">
                        <VStack spacing={2}>
                          <Icon as={Thermometer} w={8} h={8} color="red.500" />
                          <Text fontWeight="bold" color="red.700">Temperature</Text>
                          <Text fontSize="2xl" fontWeight="bold" color="red.600">
                            {selectedField.sensors.temperature}°C
                          </Text>
                          <Text fontSize="sm" color="red.600">
                            {selectedField.sensors.temperature > 35 ? 'Hot' : 
                             selectedField.sensors.temperature < 20 ? 'Cold' : 'Normal'}
                          </Text>
                        </VStack>
                      </CardBody>
                    </Card>
                  </GridItem>

                  {/* Humidity */}
                  <GridItem>
                    <Card bg="blue.50" border="1px" borderColor="blue.200">
                      <CardBody textAlign="center">
                        <VStack spacing={2}>
                          <Icon as={Droplets} w={8} h={8} color="blue.500" />
                          <Text fontWeight="bold" color="blue.700">Humidity</Text>
                          <Text fontSize="2xl" fontWeight="bold" color="blue.600">
                            {selectedField.sensors.humidity}%
                          </Text>
                          <Text fontSize="sm" color="blue.600">
                            {selectedField.sensors.humidity > 70 ? 'High' : 
                             selectedField.sensors.humidity < 40 ? 'Low' : 'Normal'}
                          </Text>
                        </VStack>
                      </CardBody>
                    </Card>
                  </GridItem>

                  {/* Soil Moisture */}
                  <GridItem>
                    <Card bg="green.50" border="1px" borderColor="green.200">
                      <CardBody textAlign="center">
                        <VStack spacing={2}>
                          <Icon as={Droplets} w={8} h={8} color="green.500" />
                          <Text fontWeight="bold" color="green.700">Soil Moisture</Text>
                          <Text fontSize="2xl" fontWeight="bold" color="green.600">
                            {selectedField.sensors.soil_moisture}%
                          </Text>
                          <Progress 
                            value={selectedField.sensors.soil_moisture} 
                            colorScheme="green" 
                            size="sm" 
                          />
                          <Text fontSize="sm" color="green.600">
                            {selectedField.sensors.soil_moisture > 60 ? 'Good' : 
                             selectedField.sensors.soil_moisture < 30 ? 'Dry' : 'Normal'}
                          </Text>
                        </VStack>
                      </CardBody>
                    </Card>
                  </GridItem>

                  {/* Light */}
                  <GridItem>
                    <Card bg="yellow.50" border="1px" borderColor="yellow.200">
                      <CardBody textAlign="center">
                        <VStack spacing={2}>
                          <Icon as={Sun} w={8} h={8} color="yellow.500" />
                          <Text fontWeight="bold" color="yellow.700">Light</Text>
                          <Text fontSize="2xl" fontWeight="bold" color="yellow.600">
                            {selectedField.sensors.light}
                          </Text>
                          <Text fontSize="sm" color="yellow.600">
                            {selectedField.sensors.light > 800 ? 'Bright' : 
                             selectedField.sensors.light < 400 ? 'Dim' : 'Normal'}
                          </Text>
                        </VStack>
                      </CardBody>
                    </Card>
                  </GridItem>
                </Grid>

                {/* Alerts */}
                {selectedField.alerts.length > 0 && (
                  <Card bg="orange.50" border="1px" borderColor="orange.200">
                    <CardBody>
                      <VStack spacing={2} align="stretch">
                        <HStack>
                          <Icon as={AlertTriangle} color="orange.500" />
                          <Text fontWeight="bold" color="orange.700">Alerts</Text>
                        </HStack>
                        {selectedField.alerts.map((alert, index) => (
                          <Text key={index} fontSize="sm" color="orange.600">
                            • {alert}
                          </Text>
                        ))}
                      </VStack>
                    </CardBody>
                  </Card>
                )}

                {/* Last Update */}
                <Text fontSize="sm" color="gray.500" textAlign="center">
                  Last updated: {selectedField.lastUpdate}
                </Text>
              </VStack>
            </CardBody>
          </Card>
        )}

        {/* Add Field Modal */}
        <Modal isOpen={isOpen} onClose={onClose} size="lg">
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Add New Field</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <VStack spacing={4}>
                <FormControl>
                  <FormLabel>Field Name (खेत का नाम)</FormLabel>
                  <Input 
                    placeholder="e.g., मेरा धान का खेत" 
                    value={newFieldData.name}
                    onChange={(e) => setNewFieldData({ ...newFieldData, name: e.target.value })}
                  />
                </FormControl>
                
                <FormControl>
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
                
                <FormControl>
                  <FormLabel>Field Size (खेत का आकार)</FormLabel>
                  <Input 
                    placeholder="e.g., 2 acres, 1.5 bigha" 
                    value={newFieldData.size}
                    onChange={(e) => setNewFieldData({ ...newFieldData, size: e.target.value })}
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Farm (खेत)</FormLabel>
                  <Select 
                    placeholder="Select a farm"
                    value={newFieldData.farm_id}
                    onChange={(e) => setNewFieldData({ ...newFieldData, farm_id: e.target.value })}
                    isDisabled={!farms || farms.length === 0}
                  >
                    {!farms || farms.length === 0 ? (
                      <option value="" disabled>No farms available</option>
                    ) : (
                      farms.map((farm: any) => (
                        <option key={farm.id} value={farm.id}>
                          {farm.name} - {farm.location}
                        </option>
                      ))
                    )}
                  </Select>
                  {!farms || farms.length === 0 ? (
                    <Text fontSize="sm" color="red.500" mt={1}>
                      Please create a farm first in the Farms section
                    </Text>
                  ) : null}
                </FormControl>
                
                <FormControl>
                  <FormLabel>Location (स्थान)</FormLabel>
                  <Input 
                    placeholder="e.g., Village: Ramgarh" 
                    value={newFieldData.location}
                    onChange={(e) => setNewFieldData({ ...newFieldData, location: e.target.value })}
                  />
                </FormControl>
                
                <HStack spacing={4} width="full">
                  <Button 
                    colorScheme="green" 
                    onClick={handleAddFieldSubmit}
                    flex={1}
                    isLoading={createFieldMutation.isPending}
                    loadingText="Adding..."
                  >
                    Add Field
                  </Button>
                  <Button 
                    variant="outline" 
                    onClick={onClose}
                    flex={1}
                    isDisabled={createFieldMutation.isPending}
                  >
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

export default FarmerFriendlyIoT;
