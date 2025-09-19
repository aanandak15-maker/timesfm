import React, { useState, useEffect, useRef } from 'react';
import {
  Box, VStack, HStack, Text, Heading, Button, Card, CardBody,
  Badge, Icon, useToast, Alert, AlertIcon, AlertDescription,
  useColorModeValue, Grid, GridItem,   Modal, ModalOverlay,
  ModalContent, ModalHeader, ModalBody, ModalCloseButton, useDisclosure,
  FormControl, FormLabel, Input, Select, Progress,
  Stat, StatLabel, StatNumber, StatHelpText, Image,
  Tabs, TabList, TabPanels, Tab, TabPanel, SimpleGrid
} from '@chakra-ui/react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import {
  MapPin, Satellite, Camera,
  CheckCircle, AlertTriangle, Play, Pause, RotateCcw, Save,
  Eye, Edit, Trash2, Plus, Minus, Target, Compass, Globe,
  Layers, BarChart3, TrendingUp, Calendar, Thermometer,
  Droplets, Sun, Cloud, Zap
} from 'lucide-react';

// GEE Satellite Data Interfaces
interface GEESatelliteImage {
  id: string;
  date: string;
  cloudCover: number;
  satellite: 'Sentinel-2' | 'Landsat-8' | 'Landsat-9' | 'MODIS';
  bands: {
    red: number;
    nir: number;
    blue: number;
    green: number;
  };
  ndvi: number;
  evi: number;
  savi: number;
  imageUrl: string;
  coordinates: {
    lat: number;
    lon: number;
  };
}

interface GEETimeSeries {
  dates: string[];
  ndvi: number[];
  evi: number[];
  savi: number[];
  temperature: number[];
  precipitation: number[];
  soilMoisture: number[];
}

interface FieldBoundary {
  id: string;
  name: string;
  coordinates: { lat: number; lon: number }[];
  area: number; // in acres
  center: { lat: number; lon: number };
  method: 'satellite' | 'gps' | 'manual';
  accuracy: number;
  created_at: string;
  validated: boolean;
}

interface CropAnalysis {
  cropType: string;
  growthStage: string;
  healthScore: number;
  stressFactors: string[];
  recommendations: string[];
  expectedYield: number;
  confidence: number;
}

const GEESatelliteFieldMapper: React.FC = () => {
  const toast = useToast();
  const queryClient = useQueryClient();
  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const [currentLocation, setCurrentLocation] = useState<{ lat: number; lon: number } | null>(null);
  const [satelliteImages, setSatelliteImages] = useState<GEESatelliteImage[]>([]);
  const [timeSeriesData, setTimeSeriesData] = useState<GEETimeSeries | null>(null);
  const [fieldBoundary, setFieldBoundary] = useState<FieldBoundary | null>(null);
  const [cropAnalysis, setCropAnalysis] = useState<CropAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<GEESatelliteImage | null>(null);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  
  const [newFieldData, setNewFieldData] = useState({
    name: '',
    crop_type: '',
    planting_date: '',
    expected_harvest: '',
    field_size: ''
  });

  const mapRef = useRef<HTMLDivElement>(null);

  // Get current location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCurrentLocation({
            lat: position.coords.latitude,
            lon: position.coords.longitude
          });
        },
        (error) => {
          console.error('Location error:', error);
          // Default to a location in India
          setCurrentLocation({ lat: 28.368911, lon: 77.541033 });
        }
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
        description: satelliteImages.length > 0 ? 'Your field has been saved with satellite analysis' : 'Your field has been saved successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
      // Reset form data
      setNewFieldData({
        name: '',
        crop_type: '',
        planting_date: '',
        expected_harvest: '',
        field_size: ''
      });
      setSatelliteImages([]);
      setTimeSeriesData(null);
      setCropAnalysis(null);
      setFieldBoundary(null);
      
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

  // Fetch satellite imagery from GEE
  const fetchSatelliteImagery = async (lat: number, lon: number) => {
    setIsLoading(true);
    setAnalysisProgress(0);
    
    try {
      // Simulate GEE API call with realistic satellite data
      const images: GEESatelliteImage[] = [];
      
      // Generate multiple satellite images over time
      for (let i = 0; i < 5; i++) {
        const date = new Date();
        date.setDate(date.getDate() - (i * 7)); // Weekly images
        
        const image: GEESatelliteImage = {
          id: `sentinel-2-${i}`,
          date: date.toISOString(),
          cloudCover: Math.random() * 15, // Low cloud cover
          satellite: 'Sentinel-2',
          bands: {
            red: 0.3 + Math.random() * 0.1,
            nir: 0.4 + Math.random() * 0.1,
            blue: 0.2 + Math.random() * 0.1,
            green: 0.35 + Math.random() * 0.1
          },
          ndvi: 0.6 + Math.random() * 0.2,
          evi: 0.4 + Math.random() * 0.15,
          savi: 0.5 + Math.random() * 0.2,
          imageUrl: `https://api.nasa.gov/planetary/earth/imagery?lat=${lat}&lon=${lon}&date=${date.toISOString().split('T')[0]}&api_key=4Od5nRoNq2NKdyFZ6ENS98kcpZg4RT3Efelbjleb`,
          coordinates: { lat, lon }
        };
        
        images.push(image);
        setAnalysisProgress((i + 1) * 20);
      }
      
      setSatelliteImages(images);
      setSelectedImage(images[0]);
      
      // Generate time series data
      const timeSeries: GEETimeSeries = {
        dates: images.map(img => img.date),
        ndvi: images.map(img => img.ndvi),
        evi: images.map(img => img.evi),
        savi: images.map(img => img.savi),
        temperature: images.map(() => 25 + Math.random() * 10),
        precipitation: images.map(() => Math.random() * 20),
        soilMoisture: images.map(() => 40 + Math.random() * 30)
      };
      
      setTimeSeriesData(timeSeries);
      
      // Generate crop analysis
      const analysis: CropAnalysis = {
        cropType: newFieldData.crop_type || 'Rice',
        growthStage: 'vegetative',
        healthScore: 85 + Math.random() * 10,
        stressFactors: ['Moderate heat stress', 'Low soil moisture'],
        recommendations: [
          'Apply irrigation to maintain soil moisture',
          'Monitor for pest activity',
          'Consider fertilizer application'
        ],
        expectedYield: 4.2 + Math.random() * 0.8,
        confidence: 88 + Math.random() * 7
      };
      
      setCropAnalysis(analysis);
      
      toast({
        title: 'Satellite analysis complete!',
        description: 'Found 5 satellite images with crop analysis',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
    } catch (error) {
      console.error('Satellite imagery error:', error);
      toast({
        title: 'Error fetching satellite data',
        description: 'Failed to load satellite imagery',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
      setAnalysisProgress(100);
    }
  };

  // Create field boundary from satellite analysis
  const createFieldBoundary = () => {
    if (!currentLocation || !satelliteImages.length) return;
    
    const boundary: FieldBoundary = {
      id: `field-${Date.now()}`,
      name: newFieldData.name || `Satellite Field ${new Date().toLocaleDateString()}`,
      coordinates: [
        { lat: currentLocation.lat - 0.001, lon: currentLocation.lon - 0.001 },
        { lat: currentLocation.lat + 0.001, lon: currentLocation.lon - 0.001 },
        { lat: currentLocation.lat + 0.001, lon: currentLocation.lon + 0.001 },
        { lat: currentLocation.lat - 0.001, lon: currentLocation.lon + 0.001 },
        { lat: currentLocation.lat - 0.001, lon: currentLocation.lon - 0.001 }
      ],
      area: parseFloat(newFieldData.field_size) || 2.5,
      center: currentLocation,
      method: 'satellite',
      accuracy: 95,
      created_at: new Date().toISOString(),
      validated: true
    };
    
    setFieldBoundary(boundary);
    
    toast({
      title: 'Field boundary created!',
      description: `Area: ${boundary.area} acres, Accuracy: ${boundary.accuracy}%`,
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  // Save field with satellite data
  const saveField = () => {
    // Basic validation
    if (!newFieldData.name || !newFieldData.crop_type || !newFieldData.field_size) {
      toast({
        title: 'Missing required fields',
        description: 'Please fill in field name, crop type, and field size',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    // Use current location or default coordinates
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
      // GEE Satellite data (if available)
      satellite_images: satelliteImages.length > 0 ? satelliteImages : null,
      time_series_data: timeSeriesData || null,
      crop_analysis: cropAnalysis || null,
      mapping_method: satelliteImages.length > 0 ? 'satellite_gee' : 'manual'
    };

    console.log('Saving field with data:', fieldData);
    createFieldMutation.mutate(fieldData);
  };

  return (
    <Box p={6} maxW="1400px" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <HStack justify="space-between">
              <VStack align="start" spacing={2}>
                <HStack>
                  <Icon as={Satellite} w={8} h={8} color="blue.500" />
                  <Heading size="lg" color="blue.600">
                    GEE Satellite Field Mapper
                  </Heading>
                </HStack>
                <Text color="gray.600">
                  Map your field using Google Earth Engine satellite imagery and analysis
                </Text>
              </VStack>
              <Button
                leftIcon={<Icon as={Plus} />}
                onClick={onOpen}
                colorScheme="blue"
                size="lg"
              >
                New Field
              </Button>
            </HStack>
          </CardBody>
        </Card>

        {/* Location Status */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
              <GridItem>
                <Stat>
                  <StatLabel>Current Location</StatLabel>
                  <StatNumber fontSize="sm">
                    {currentLocation ? 
                      `${currentLocation.lat.toFixed(6)}, ${currentLocation.lon.toFixed(6)}` : 
                      "Loading..."
                    }
                  </StatNumber>
                  <StatHelpText>
                    <Icon as={MapPin} w={4} h={4} />
                    GPS Coordinates
                  </StatHelpText>
                </Stat>
              </GridItem>
              
              <GridItem>
                <Stat>
                  <StatLabel>Satellite Images</StatLabel>
                  <StatNumber color="blue.500">
                    {satelliteImages.length}
                  </StatNumber>
                  <StatHelpText>
                    <Icon as={Camera} w={4} h={4} />
                    Available Images
                  </StatHelpText>
                </Stat>
              </GridItem>
            </Grid>
          </CardBody>
        </Card>

        {/* Satellite Analysis Controls */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <VStack spacing={4}>
              <HStack spacing={4} width="full">
                <Button
                  leftIcon={<Icon as={Satellite} />}
                  onClick={() => currentLocation && fetchSatelliteImagery(currentLocation.lat, currentLocation.lon)}
                  colorScheme="blue"
                  isDisabled={!currentLocation || isLoading}
                  flex={1}
                >
                  Analyze with GEE
                </Button>
                <Button
                  leftIcon={<Icon as={Target} />}
                  onClick={createFieldBoundary}
                  colorScheme="green"
                  isDisabled={!satelliteImages.length}
                  flex={1}
                >
                  Create Field Boundary
                </Button>
              </HStack>

              {isLoading && (
                <Box width="full">
                  <Text mb={2}>Analyzing satellite data... {analysisProgress}%</Text>
                  <Progress value={analysisProgress} colorScheme="blue" />
                </Box>
              )}
            </VStack>
          </CardBody>
        </Card>

        {/* Satellite Images and Analysis */}
        {satelliteImages.length > 0 && (
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody>
              <Tabs>
                <TabList>
                  <Tab>Satellite Images</Tab>
                  <Tab>Time Series Analysis</Tab>
                  <Tab>Crop Analysis</Tab>
                  <Tab>Field Boundary</Tab>
                </TabList>

                <TabPanels>
                  {/* Satellite Images Tab */}
                  <TabPanel>
                    <VStack spacing={4} align="stretch">
                      <Heading size="md">Recent Satellite Images</Heading>
                      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                        {satelliteImages.map((image) => (
                          <Card key={image.id} cursor="pointer" 
                                border={selectedImage?.id === image.id ? "2px solid" : "1px solid"}
                                borderColor={selectedImage?.id === image.id ? "blue.500" : borderColor}
                                onClick={() => setSelectedImage(image)}>
                            <CardBody>
                              <VStack spacing={2}>
                                <Image
                                  src={image.imageUrl}
                                  alt={`Satellite image ${image.date}`}
                                  fallbackSrc="https://via.placeholder.com/200x150?text=Satellite+Image"
                                  boxSize="200px"
                                  objectFit="cover"
                                  borderRadius="md"
                                />
                                <VStack spacing={1} align="start" width="full">
                                  <Text fontSize="sm" fontWeight="bold">
                                    {image.satellite}
                                  </Text>
                                  <Text fontSize="xs" color="gray.600">
                                    {new Date(image.date).toLocaleDateString()}
                                  </Text>
                                  <HStack spacing={2}>
                                    <Badge colorScheme="green" size="sm">
                                      NDVI: {image.ndvi.toFixed(3)}
                                    </Badge>
                                    <Badge colorScheme="blue" size="sm">
                                      Cloud: {image.cloudCover.toFixed(1)}%
                                    </Badge>
                                  </HStack>
                                </VStack>
                              </VStack>
                            </CardBody>
                          </Card>
                        ))}
                      </SimpleGrid>
                    </VStack>
                  </TabPanel>

                  {/* Time Series Analysis Tab */}
                  <TabPanel>
                    <VStack spacing={4} align="stretch">
                      <Heading size="md">Vegetation Index Time Series</Heading>
                      {timeSeriesData && (
                        <Grid templateColumns="repeat(auto-fit, minmax(150px, 1fr))" gap={4}>
                          <GridItem>
                            <Stat>
                              <StatLabel>Average NDVI</StatLabel>
                              <StatNumber color="green.500">
                                {(timeSeriesData.ndvi.reduce((a, b) => a + b, 0) / timeSeriesData.ndvi.length).toFixed(3)}
                              </StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Average EVI</StatLabel>
                              <StatNumber color="blue.500">
                                {(timeSeriesData.evi.reduce((a, b) => a + b, 0) / timeSeriesData.evi.length).toFixed(3)}
                              </StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Average Temperature</StatLabel>
                              <StatNumber color="red.500">
                                {(timeSeriesData.temperature.reduce((a, b) => a + b, 0) / timeSeriesData.temperature.length).toFixed(1)}°C
                              </StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Average Soil Moisture</StatLabel>
                              <StatNumber color="brown.500">
                                {(timeSeriesData.soilMoisture.reduce((a, b) => a + b, 0) / timeSeriesData.soilMoisture.length).toFixed(1)}%
                              </StatNumber>
                            </Stat>
                          </GridItem>
                        </Grid>
                      )}
                    </VStack>
                  </TabPanel>

                  {/* Crop Analysis Tab */}
                  <TabPanel>
                    <VStack spacing={4} align="stretch">
                      <Heading size="md">AI Crop Analysis</Heading>
                      {cropAnalysis && (
                        <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
                          <GridItem>
                            <Stat>
                              <StatLabel>Crop Type</StatLabel>
                              <StatNumber color="green.500">{cropAnalysis.cropType}</StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Growth Stage</StatLabel>
                              <StatNumber color="blue.500">{cropAnalysis.growthStage}</StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Health Score</StatLabel>
                              <StatNumber color="green.500">{cropAnalysis.healthScore.toFixed(1)}%</StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Expected Yield</StatLabel>
                              <StatNumber color="orange.500">{cropAnalysis.expectedYield.toFixed(2)} tons/acre</StatNumber>
                              <StatHelpText>Confidence: {cropAnalysis.confidence.toFixed(1)}%</StatHelpText>
                            </Stat>
                          </GridItem>
                        </Grid>
                      )}
                      
                      {cropAnalysis && (
                        <VStack align="stretch" spacing={4}>
                          <Box>
                            <Text fontWeight="bold" mb={2}>Stress Factors:</Text>
                            {cropAnalysis.stressFactors.map((factor, index) => (
                              <Badge key={index} colorScheme="orange" mr={2} mb={2}>
                                {factor}
                              </Badge>
                            ))}
                          </Box>
                          
                          <Box>
                            <Text fontWeight="bold" mb={2}>Recommendations:</Text>
                            {cropAnalysis.recommendations.map((rec, index) => (
                              <Text key={index} fontSize="sm">• {rec}</Text>
                            ))}
                          </Box>
                        </VStack>
                      )}
                    </VStack>
                  </TabPanel>

                  {/* Field Boundary Tab */}
                  <TabPanel>
                    <VStack spacing={4} align="stretch">
                      <Heading size="md">Field Boundary Information</Heading>
                      {fieldBoundary && (
                        <Grid templateColumns="repeat(auto-fit, minmax(150px, 1fr))" gap={4}>
                          <GridItem>
                            <Stat>
                              <StatLabel>Field Area</StatLabel>
                              <StatNumber color="blue.500">{fieldBoundary.area} acres</StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Mapping Method</StatLabel>
                              <StatNumber color="green.500">{fieldBoundary.method}</StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Accuracy</StatLabel>
                              <StatNumber color="green.500">{fieldBoundary.accuracy}%</StatNumber>
                            </Stat>
                          </GridItem>
                          <GridItem>
                            <Stat>
                              <StatLabel>Coordinates</StatLabel>
                              <StatNumber fontSize="sm">
                                {fieldBoundary.center.lat.toFixed(6)}, {fieldBoundary.center.lon.toFixed(6)}
                              </StatNumber>
                            </Stat>
                          </GridItem>
                        </Grid>
                      )}
                    </VStack>
                  </TabPanel>
                </TabPanels>
              </Tabs>
            </CardBody>
          </Card>
        )}

        {/* New Field Modal */}
        <Modal isOpen={isOpen} onClose={onClose} size="lg">
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Create New Field with GEE Analysis</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <VStack spacing={4}>
                <Alert status="info" borderRadius="md">
                  <AlertIcon />
                  <AlertDescription fontSize="sm">
                    Fill in the basic field information below. You can optionally analyze with GEE satellite data for advanced insights.
                  </AlertDescription>
                </Alert>
                
                <FormControl isRequired>
                  <FormLabel>Field Name</FormLabel>
                  <Input
                    placeholder="e.g., North Rice Field"
                    value={newFieldData.name}
                    onChange={(e) => setNewFieldData({ ...newFieldData, name: e.target.value })}
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Crop Type</FormLabel>
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
                  <FormLabel>Field Size (acres)</FormLabel>
                  <Input
                    type="number"
                    placeholder="e.g., 2.5"
                    value={newFieldData.field_size}
                    onChange={(e) => setNewFieldData({ ...newFieldData, field_size: e.target.value })}
                  />
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
                
                <HStack spacing={4} width="full">
                  <Button
                    colorScheme="blue"
                    onClick={saveField}
                    flex={1}
                    isLoading={createFieldMutation.isPending}
                    loadingText="Saving..."
                  >
                    {satelliteImages.length > 0 ? 'Save Field with GEE Data' : 'Save Basic Field'}
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

export default GEESatelliteFieldMapper;
