import React, { useState, useEffect } from 'react';
import {
  Box, VStack, HStack, Text, Heading, Button, Card, CardBody,
  Badge, Icon, useToast, Alert, AlertIcon, AlertDescription,
  useColorModeValue, Grid, GridItem, Modal, ModalOverlay,
  ModalContent, ModalHeader, ModalBody, ModalCloseButton, useDisclosure,
  FormControl, FormLabel, Input, Select, NumberInput, NumberInputField,
  Progress, Stat, StatLabel, StatNumber, StatHelpText,
  SimpleGrid, Divider, Flex, Spinner
} from '@chakra-ui/react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import { geeService } from '../../services/googleEarthEngineApi';
import {
  MapPin, Satellite, Camera, Upload, CheckCircle, AlertTriangle,
  Play, Pause, RotateCcw, Save, Eye, Edit, Trash2, Plus,
  Target, Compass, Globe, Layers, BarChart3, TrendingUp,
  Calendar, Thermometer, Droplets, Sun, Cloud, Zap, Ruler
} from 'lucide-react';

interface FieldBoundary {
  id: string;
  name: string;
  coordinates: { lat: number; lon: number }[];
  center: { lat: number; lon: number };
  area: number; // in acres
  accuracy: number; // percentage
  created_at: string;
  validated: boolean;
}

interface CropAnalysis {
  cropType: string;
  growthStage: string;
  healthScore: number; // 0-100
  stressFactors: string[];
  recommendations: string[];
  expectedYield: number; // tons per acre
  confidence: number; // 0-100
}

const SimpleFieldMapper: React.FC = () => {
  const toast = useToast();
  const queryClient = useQueryClient();
  const { isOpen, onOpen, onClose } = useDisclosure();

  const [newFieldData, setNewFieldData] = useState({
    name: '',
    crop_type: '',
    field_size: '',
    planting_date: '',
    expected_harvest: ''
  });
  
  const [currentLocation, setCurrentLocation] = useState<{ lat: number; lon: number } | null>(null);
  const [fieldBoundary, setFieldBoundary] = useState<FieldBoundary | null>(null);
  const [cropAnalysis, setCropAnalysis] = useState<CropAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [mappingStep, setMappingStep] = useState(1); // 1: Basic Info, 2: Location, 3: Analysis, 4: Save

  // Get current location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCurrentLocation({
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          });
        },
        (error) => {
          console.error('Error getting GPS location:', error);
          // Default to a location in India
          setCurrentLocation({ lat: 28.368911, lon: 77.541033 });
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      );
    } else {
      setCurrentLocation({ lat: 28.368911, lon: 77.541033 });
    }
  }, []);

  // Create field mutation
  const createFieldMutation = useMutation({
    mutationFn: apiService.createField,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fields'] });
      toast({
        title: 'Field saved successfully!',
        description: 'Your field has been mapped and saved',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });

      // Reset form data
      setNewFieldData({
        name: '',
        crop_type: '',
        field_size: '',
        planting_date: '',
        expected_harvest: ''
      });
      setFieldBoundary(null);
      setCropAnalysis(null);
      setMappingStep(1);
      onClose();
    },
    onError: (error: any) => {
      console.error('Field creation error:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to save field';
      toast({
        title: 'Error saving field',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  // Create field boundary from GPS location
  const createFieldBoundary = () => {
    if (!currentLocation || !newFieldData.field_size) return;

    const area = parseFloat(newFieldData.field_size);
    const boundary: FieldBoundary = {
      id: `field-${Date.now()}`,
      name: newFieldData.name || `Field ${new Date().toLocaleDateString()}`,
      coordinates: [
        { lat: currentLocation.lat - 0.001, lon: currentLocation.lon - 0.001 },
        { lat: currentLocation.lat + 0.001, lon: currentLocation.lon - 0.001 },
        { lat: currentLocation.lat + 0.001, lon: currentLocation.lon + 0.001 },
        { lat: currentLocation.lat - 0.001, lon: currentLocation.lon + 0.001 },
        { lat: currentLocation.lat - 0.001, lon: currentLocation.lon - 0.001 },
      ],
      center: currentLocation,
      area: area,
      accuracy: 95,
      created_at: new Date().toISOString(),
      validated: true
    };

    setFieldBoundary(boundary);
    setMappingStep(3);

    toast({
      title: 'Field boundary created!',
      description: `Area: ${boundary.area} acres, Accuracy: ${boundary.accuracy}%`,
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  // Analyze crop with satellite data
  const analyzeCrop = async () => {
    if (!currentLocation || !newFieldData.crop_type) return;

    setIsLoading(true);
    try {
      // Get crop health analysis
      const analysis = await geeService.getCropHealthAnalysis(
        currentLocation.lat,
        currentLocation.lon,
        newFieldData.crop_type
      );

      if (analysis) {
        setCropAnalysis(analysis);
        setMappingStep(4);
        
        toast({
          title: 'Crop analysis complete!',
          description: `Health score: ${analysis.healthScore.toFixed(1)}%`,
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error('Crop analysis error:', error);
      toast({
        title: 'Analysis failed',
        description: 'Could not analyze crop health',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Save field
  const saveField = () => {
    if (!newFieldData.name || !newFieldData.crop_type || !newFieldData.field_size) {
      toast({
        title: 'Missing required fields',
        description: 'Please fill in all required information',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    const location = currentLocation || { lat: 28.368911, lon: 77.541033 };
    const area = parseFloat(newFieldData.field_size) || 1.0;

    const fieldData = {
      name: newFieldData.name,
      farm_id: 'default-farm',
      crop_type: newFieldData.crop_type,
      area_acres: area,
      latitude: location.lat,
      longitude: location.lon,
      soil_type: 'Loamy',
      planting_date: newFieldData.planting_date || new Date().toISOString().split('T')[0],
      harvest_date: newFieldData.expected_harvest || null,
      crop_analysis: cropAnalysis || null,
      mapping_method: 'gps_simple'
    };

    console.log('Saving field with data:', fieldData);
    createFieldMutation.mutate(fieldData);
  };

  const bg = useColorModeValue('white', 'gray.700');
  const cardBg = useColorModeValue('gray.50', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Box p={6} maxW="1200px" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <HStack justifyContent="space-between" alignItems="center">
          <Heading as="h1" size="xl">
            <HStack>
              <Icon as={MapPin} size={32} />
              <Text>Simple Field Mapper</Text>
            </HStack>
          </Heading>
          <Button colorScheme="green" onClick={onOpen} leftIcon={<Icon as={Plus} />}>
            + New Field
          </Button>
        </HStack>

        <Text fontSize="lg" color="gray.600">
          Easy field mapping for small and marginal farmers. Simple steps to map your field and get crop insights.
        </Text>

        {/* Current Location Display */}
        <Card bg="blue.50" border="1px" borderColor="blue.200">
          <CardBody>
            <HStack spacing={4} alignItems="center">
              <Icon as={MapPin} size={24} color="blue.600" />
              <VStack align="start" spacing={0}>
                <Text fontWeight="bold">Current Location (GPS)</Text>
                {currentLocation ? (
                  <Text fontSize="sm">
                    Lat: {currentLocation.lat.toFixed(6)}, Lon: {currentLocation.lon.toFixed(6)}
                  </Text>
                ) : (
                  <Text fontSize="sm" color="gray.500">
                    Detecting location...
                  </Text>
                )}
              </VStack>
            </HStack>
          </CardBody>
        </Card>

        {/* Mapping Steps */}
        <Card bg={cardBg} border="1px" borderColor={borderColor}>
          <CardBody>
            <VStack spacing={4} align="stretch">
              <Heading size="md">Field Mapping Steps</Heading>
              
              <SimpleGrid columns={{ base: 1, md: 4 }} spacing={4}>
                {/* Step 1: Basic Info */}
                <Card bg={mappingStep >= 1 ? "green.50" : "gray.50"} border="1px" borderColor={mappingStep >= 1 ? "green.200" : "gray.200"}>
                  <CardBody textAlign="center">
                    <Icon as={Edit} size={24} color={mappingStep >= 1 ? "green.600" : "gray.400"} />
                    <Text fontSize="sm" fontWeight="bold" mt={2}>1. Basic Info</Text>
                    <Text fontSize="xs" color="gray.600">Field name & crop</Text>
                  </CardBody>
                </Card>

                {/* Step 2: Location */}
                <Card bg={mappingStep >= 2 ? "green.50" : "gray.50"} border="1px" borderColor={mappingStep >= 2 ? "green.200" : "gray.200"}>
                  <CardBody textAlign="center">
                    <Icon as={Target} size={24} color={mappingStep >= 2 ? "green.600" : "gray.400"} />
                    <Text fontSize="sm" fontWeight="bold" mt={2}>2. Location</Text>
                    <Text fontSize="xs" color="gray.600">GPS & boundary</Text>
                  </CardBody>
                </Card>

                {/* Step 3: Analysis */}
                <Card bg={mappingStep >= 3 ? "green.50" : "gray.50"} border="1px" borderColor={mappingStep >= 3 ? "green.200" : "gray.200"}>
                  <CardBody textAlign="center">
                    <Icon as={Satellite} size={24} color={mappingStep >= 3 ? "green.600" : "gray.400"} />
                    <Text fontSize="sm" fontWeight="bold" mt={2}>3. Analysis</Text>
                    <Text fontSize="xs" color="gray.600">Crop health</Text>
                  </CardBody>
                </Card>

                {/* Step 4: Save */}
                <Card bg={mappingStep >= 4 ? "green.50" : "gray.50"} border="1px" borderColor={mappingStep >= 4 ? "green.200" : "gray.200"}>
                  <CardBody textAlign="center">
                    <Icon as={Save} size={24} color={mappingStep >= 4 ? "green.600" : "gray.400"} />
                    <Text fontSize="sm" fontWeight="bold" mt={2}>4. Save</Text>
                    <Text fontSize="xs" color="gray.600">Complete mapping</Text>
                  </CardBody>
                </Card>
              </SimpleGrid>
            </VStack>
          </CardBody>
        </Card>

        {/* Field Boundary Info */}
        {fieldBoundary && (
          <Card bg="green.50" border="1px" borderColor="green.200">
            <CardBody>
              <HStack spacing={4} alignItems="center">
                <Icon as={CheckCircle} size={24} color="green.600" />
                <VStack align="start" spacing={0}>
                  <Text fontWeight="bold">Field Boundary Created</Text>
                  <Text fontSize="sm">
                    Area: {fieldBoundary.area} acres | Accuracy: {fieldBoundary.accuracy}%
                  </Text>
                </VStack>
              </HStack>
            </CardBody>
          </Card>
        )}

        {/* Crop Analysis Results */}
        {cropAnalysis && (
          <Card bg="purple.50" border="1px" borderColor="purple.200">
            <CardBody>
              <VStack spacing={4} align="stretch">
                <HStack spacing={4} alignItems="center">
                  <Icon as={BarChart3} size={24} color="purple.600" />
                  <Text fontWeight="bold">Crop Analysis Results</Text>
                </HStack>
                
                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                  <Stat>
                    <StatLabel>Health Score</StatLabel>
                    <StatNumber color="green.600">{cropAnalysis.healthScore.toFixed(1)}%</StatNumber>
                    <StatHelpText>Overall crop health</StatHelpText>
                  </Stat>
                  
                  <Stat>
                    <StatLabel>Expected Yield</StatLabel>
                    <StatNumber color="blue.600">{cropAnalysis.expectedYield.toFixed(1)} tons/acre</StatNumber>
                    <StatHelpText>Predicted harvest</StatHelpText>
                  </Stat>
                  
                  <Stat>
                    <StatLabel>Confidence</StatLabel>
                    <StatNumber color="purple.600">{cropAnalysis.confidence.toFixed(1)}%</StatNumber>
                    <StatHelpText>Analysis confidence</StatHelpText>
                  </Stat>
                </SimpleGrid>

                {cropAnalysis.recommendations.length > 0 && (
                  <Box>
                    <Text fontWeight="bold" mb={2}>Recommendations:</Text>
                    <VStack align="start" spacing={1}>
                      {cropAnalysis.recommendations.map((rec, index) => (
                        <Text key={index} fontSize="sm">• {rec}</Text>
                      ))}
                    </VStack>
                  </Box>
                )}
              </VStack>
            </CardBody>
          </Card>
        )}
      </VStack>

      {/* Field Creation Modal */}
      <Modal isOpen={isOpen} onClose={onClose} size="lg">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Map New Field</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <VStack spacing={4}>
              {/* Step 1: Basic Information */}
              {mappingStep === 1 && (
                <VStack spacing={4} width="full">
                  <Alert status="info">
                    <AlertIcon />
                    <AlertDescription>
                      Step 1: Enter basic information about your field
                    </AlertDescription>
                  </Alert>
                  
                  <FormControl isRequired>
                    <FormLabel>Field Name (खेत का नाम)</FormLabel>
                    <Input
                      placeholder="e.g., North Rice Field"
                      value={newFieldData.name}
                      onChange={(e) => setNewFieldData({ ...newFieldData, name: e.target.value })}
                    />
                  </FormControl>
                  
                  <FormControl isRequired>
                    <FormLabel>Crop Type (फसल का प्रकार)</FormLabel>
                    <Select
                      placeholder="Select crop"
                      value={newFieldData.crop_type}
                      onChange={(e) => setNewFieldData({ ...newFieldData, crop_type: e.target.value })}
                    >
                      <option value="Rice">Rice (चावल)</option>
                      <option value="Maize">Maize (मक्का)</option>
                      <option value="Cotton">Cotton (कपास)</option>
                    </Select>
                  </FormControl>
                  
                  <FormControl isRequired>
                    <FormLabel>Field Size (खेत का आकार) - acres</FormLabel>
                    <NumberInput
                      value={newFieldData.field_size}
                      onChange={(value) => setNewFieldData({ ...newFieldData, field_size: value })}
                      min={0.1}
                      max={10}
                      step={0.1}
                    >
                      <NumberInputField placeholder="e.g., 1.5" />
                    </NumberInput>
                  </FormControl>
                  
                  <HStack spacing={4} width="full">
                    <FormControl>
                      <FormLabel>Planting Date</FormLabel>
                      <Input
                        type="date"
                        value={newFieldData.planting_date}
                        onChange={(e) => setNewFieldData({ ...newFieldData, planting_date: e.target.value })}
                      />
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel>Expected Harvest</FormLabel>
                      <Input
                        type="date"
                        value={newFieldData.expected_harvest}
                        onChange={(e) => setNewFieldData({ ...newFieldData, expected_harvest: e.target.value })}
                      />
                    </FormControl>
                  </HStack>
                  
                  <Button
                    colorScheme="blue"
                    onClick={() => setMappingStep(2)}
                    isDisabled={!newFieldData.name || !newFieldData.crop_type || !newFieldData.field_size}
                    width="full"
                  >
                    Next: Set Location
                  </Button>
                </VStack>
              )}

              {/* Step 2: Location */}
              {mappingStep === 2 && (
                <VStack spacing={4} width="full">
                  <Alert status="info">
                    <AlertIcon />
                    <AlertDescription>
                      Step 2: Confirm your field location using GPS
                    </AlertDescription>
                  </Alert>
                  
                  <Card bg="blue.50" border="1px" borderColor="blue.200" width="full">
                    <CardBody>
                      <HStack spacing={4} alignItems="center">
                        <Icon as={MapPin} size={24} color="blue.600" />
                        <VStack align="start" spacing={0}>
                          <Text fontWeight="bold">GPS Location</Text>
                          {currentLocation ? (
                            <Text fontSize="sm">
                              Lat: {currentLocation.lat.toFixed(6)}, Lon: {currentLocation.lon.toFixed(6)}
                            </Text>
                          ) : (
                            <Text fontSize="sm" color="gray.500">
                              Getting location...
                            </Text>
                          )}
                        </VStack>
                      </HStack>
                    </CardBody>
                  </Card>
                  
                  <HStack spacing={4} width="full">
                    <Button
                      colorScheme="orange"
                      onClick={createFieldBoundary}
                      leftIcon={<Icon as={Ruler} />}
                      isDisabled={!currentLocation || !newFieldData.field_size}
                      flex={1}
                    >
                      Create Field Boundary
                    </Button>
                    
                    <Button
                      variant="outline"
                      onClick={() => setMappingStep(1)}
                      flex={1}
                    >
                      Back
                    </Button>
                  </HStack>
                </VStack>
              )}

              {/* Step 3: Analysis */}
              {mappingStep === 3 && (
                <VStack spacing={4} width="full">
                  <Alert status="info">
                    <AlertIcon />
                    <AlertDescription>
                      Step 3: Analyze your crop health with satellite data
                    </AlertDescription>
                  </Alert>
                  
                  {fieldBoundary && (
                    <Card bg="green.50" border="1px" borderColor="green.200" width="full">
                      <CardBody>
                        <HStack spacing={4} alignItems="center">
                          <Icon as={CheckCircle} size={24} color="green.600" />
                          <VStack align="start" spacing={0}>
                            <Text fontWeight="bold">Field Boundary Ready</Text>
                            <Text fontSize="sm">
                              Area: {fieldBoundary.area} acres | Accuracy: {fieldBoundary.accuracy}%
                            </Text>
                          </VStack>
                        </HStack>
                      </CardBody>
                    </Card>
                  )}
                  
                  <HStack spacing={4} width="full">
                    <Button
                      colorScheme="purple"
                      onClick={analyzeCrop}
                      isLoading={isLoading}
                      loadingText="Analyzing..."
                      leftIcon={<Icon as={Satellite} />}
                      flex={1}
                    >
                      Analyze Crop Health
                    </Button>
                    
                    <Button
                      variant="outline"
                      onClick={() => setMappingStep(2)}
                      flex={1}
                    >
                      Back
                    </Button>
                  </HStack>
                </VStack>
              )}

              {/* Step 4: Save */}
              {mappingStep === 4 && (
                <VStack spacing={4} width="full">
                  <Alert status="success">
                    <AlertIcon />
                    <AlertDescription>
                      Step 4: Review and save your field
                    </AlertDescription>
                  </Alert>
                  
                  <Card bg="purple.50" border="1px" borderColor="purple.200" width="full">
                    <CardBody>
                      <VStack spacing={2} align="start">
                        <Text fontWeight="bold">Field Summary:</Text>
                        <Text fontSize="sm">Name: {newFieldData.name}</Text>
                        <Text fontSize="sm">Crop: {newFieldData.crop_type}</Text>
                        <Text fontSize="sm">Size: {newFieldData.field_size} acres</Text>
                        {cropAnalysis && (
                          <>
                            <Text fontSize="sm">Health Score: {cropAnalysis.healthScore.toFixed(1)}%</Text>
                            <Text fontSize="sm">Expected Yield: {cropAnalysis.expectedYield.toFixed(1)} tons/acre</Text>
                          </>
                        )}
                      </VStack>
                    </CardBody>
                  </Card>
                  
                  <HStack spacing={4} width="full">
                    <Button
                      colorScheme="green"
                      onClick={saveField}
                      isLoading={createFieldMutation.isPending}
                      loadingText="Saving..."
                      leftIcon={<Icon as={Save} />}
                      flex={1}
                    >
                      Save Field
                    </Button>
                    
                    <Button
                      variant="outline"
                      onClick={() => setMappingStep(3)}
                      flex={1}
                    >
                      Back
                    </Button>
                  </HStack>
                </VStack>
              )}
            </VStack>
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default SimpleFieldMapper;
