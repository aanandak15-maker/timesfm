import React, { useState } from 'react';
import {
  Box, VStack, HStack, Text, Heading, Button, SimpleGrid, Card, CardBody,
  Badge, Icon, useToast, Alert, AlertIcon, AlertDescription,
  useColorModeValue, Grid, GridItem, Spinner, Modal, ModalOverlay,
  ModalContent, ModalHeader, ModalBody, ModalCloseButton, useDisclosure,
  FormControl, FormLabel, Input, Select, Textarea, Table, Thead, Tbody,
  Tr, Th, Td, TableContainer, Stat, StatLabel, StatNumber, StatHelpText
} from '@chakra-ui/react';
import {
  MapPin, Plus, Edit, Trash2, Eye, Building2, Users, Calendar,
  TrendingUp, AlertTriangle, CheckCircle
} from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import demoService from '../../services/demoService';

interface Farm {
  id: string;
  name: string;
  location: string;
  total_area_acres: number;
  description?: string;
  latitude?: number;
  longitude?: number;
  created_at: string;
  updated_at: string;
}

const Farms: React.FC = () => {
  const toast = useToast();
  const queryClient = useQueryClient();
  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const [editingFarm, setEditingFarm] = useState<Farm | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    total_area_acres: 0,
    description: '',
    latitude: 0,
    longitude: 0
  });

  // Fetch farms from API
  const { data: farms, isLoading: farmsLoading, error: farmsError } = useQuery({
    queryKey: ['farms'],
    queryFn: () => demoService.getFarms(),
  });

  // Fetch fields to show farm statistics
  const { data: fields } = useQuery({
    queryKey: ['fields'],
    queryFn: () => demoService.getFields(),
  });

  // Create farm mutation
  const createFarmMutation = useMutation({
    mutationFn: apiService.createFarm,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farms'] });
      toast({
        title: 'Farm created successfully!',
        description: 'Your new farm has been added to the system',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      resetForm();
      onClose();
    },
    onError: (error: any) => {
      toast({
        title: 'Error creating farm',
        description: error.message || 'Failed to create farm',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  // Update farm mutation
  const updateFarmMutation = useMutation({
    mutationFn: ({ id, updates }: { id: string; updates: Partial<Farm> }) => 
      apiService.updateFarm(id, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farms'] });
      toast({
        title: 'Farm updated successfully!',
        description: 'Farm information has been updated',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      resetForm();
      onClose();
    },
    onError: (error: any) => {
      toast({
        title: 'Error updating farm',
        description: error.message || 'Failed to update farm',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  const resetForm = () => {
    setFormData({
      name: '',
      location: '',
      total_area_acres: 0,
      description: '',
      latitude: 0,
      longitude: 0
    });
    setEditingFarm(null);
  };

  const handleAddFarm = () => {
    resetForm();
    onOpen();
  };

  const handleEditFarm = (farm: Farm) => {
    setEditingFarm(farm);
    setFormData({
      name: farm.name,
      location: farm.location,
      total_area_acres: farm.total_area_acres,
      description: farm.description || '',
      latitude: farm.latitude || 0,
      longitude: farm.longitude || 0
    });
    onOpen();
  };

  const handleSubmit = () => {
    if (!formData.name || !formData.location || formData.total_area_acres <= 0) {
      toast({
        title: 'Please fill all required fields',
        description: 'Name, location, and area are required',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    if (editingFarm) {
      updateFarmMutation.mutate({
        id: editingFarm.id,
        updates: formData
      });
    } else {
      createFarmMutation.mutate(formData);
    }
  };

  const getFarmStats = (farmId: string) => {
    const farmFields = fields?.filter(field => field.farm_id === farmId) || [];
    const totalFieldArea = farmFields.reduce((sum, field) => sum + (field.area || 0), 0);
    
    return {
      fieldCount: farmFields.length,
      totalFieldArea,
      utilizationRate: farms?.find(f => f.id === farmId)?.total_area_acres 
        ? (totalFieldArea / farms.find(f => f.id === farmId)!.total_area_acres) * 100 
        : 0
    };
  };

  if (farmsLoading) {
    return (
      <VStack p={8} spacing={4} align="center">
        <Spinner size="xl" color="green.500" />
        <Text fontSize="xl">Loading farms...</Text>
      </VStack>
    );
  }

  if (farmsError) {
    return (
      <VStack p={8} spacing={4} align="center">
        <Alert status="error">
          <AlertIcon />
          <AlertDescription>
            Error loading farms: {farmsError.message}
          </AlertDescription>
        </Alert>
      </VStack>
    );
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
                  <Icon as={Building2} w={8} h={8} color="green.500" />
                  <Heading size="lg" color="green.600">
                    Farm Management (खेत प्रबंधन)
                  </Heading>
                </HStack>
                <Text color="gray.600">
                  Manage your farms and monitor field distribution
                </Text>
              </VStack>
              <Button
                leftIcon={<Icon as={Plus} />}
                onClick={handleAddFarm}
                colorScheme="green"
                size="lg"
              >
                Add Farm
              </Button>
            </HStack>
          </CardBody>
        </Card>

        {/* Statistics */}
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody>
              <Stat>
                <StatLabel>Total Farms</StatLabel>
                <StatNumber color="green.500">{farms?.length || 0}</StatNumber>
                <StatHelpText>
                  <Icon as={TrendingUp} w={4} h={4} />
                  Active farms
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
          
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody>
              <Stat>
                <StatLabel>Total Area</StatLabel>
                <StatNumber color="blue.500">
                  {farms?.reduce((sum, farm) => sum + farm.total_area_acres, 0) || 0} acres
                </StatNumber>
                <StatHelpText>
                  <Icon as={MapPin} w={4} h={4} />
                  Combined area
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
          
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody>
              <Stat>
                <StatLabel>Total Fields</StatLabel>
                <StatNumber color="orange.500">{fields?.length || 0}</StatNumber>
                <StatHelpText>
                  <Icon as={Users} w={4} h={4} />
                  Across all farms
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
        </SimpleGrid>

        {/* Farms List */}
        {farms && farms.length > 0 ? (
          <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={6}>
            {farms.map(farm => {
              const stats = getFarmStats(farm.id);
              return (
                <Card
                  key={farm.id}
                  bg={bg}
                  border="1px"
                  borderColor={borderColor}
                  _hover={{ shadow: 'md' }}
                >
                  <CardBody>
                    <VStack spacing={4} align="stretch">
                      <HStack justify="space-between">
                        <VStack align="start" spacing={1}>
                          <Heading size="md">{farm.name}</Heading>
                          <HStack>
                            <Icon as={MapPin} w={4} h={4} color="gray.500" />
                            <Text fontSize="sm" color="gray.600">{farm.location}</Text>
                          </HStack>
                        </VStack>
                        <HStack spacing={2}>
                          <Button
                            size="sm"
                            leftIcon={<Icon as={Eye} />}
                            colorScheme="blue"
                            variant="outline"
                          >
                            View
                          </Button>
                          <Button
                            size="sm"
                            leftIcon={<Icon as={Edit} />}
                            colorScheme="orange"
                            variant="outline"
                            onClick={() => handleEditFarm(farm)}
                          >
                            Edit
                          </Button>
                        </HStack>
                      </HStack>

                      <Grid templateColumns="repeat(3, 1fr)" gap={4}>
                        <GridItem>
                          <VStack spacing={1}>
                            <Text fontSize="sm" color="gray.500">Total Area</Text>
                            <Text fontWeight="bold">{farm.total_area_acres} acres</Text>
                          </VStack>
                        </GridItem>
                        <GridItem>
                          <VStack spacing={1}>
                            <Text fontSize="sm" color="gray.500">Fields</Text>
                            <Text fontWeight="bold">{stats.fieldCount}</Text>
                          </VStack>
                        </GridItem>
                        <GridItem>
                          <VStack spacing={1}>
                            <Text fontSize="sm" color="gray.500">Utilization</Text>
                            <Text fontWeight="bold">{stats.utilizationRate.toFixed(1)}%</Text>
                          </VStack>
                        </GridItem>
                      </Grid>

                      {farm.description && (
                        <Text fontSize="sm" color="gray.600" noOfLines={2}>
                          {farm.description}
                        </Text>
                      )}

                      <HStack justify="space-between">
                        <Text fontSize="xs" color="gray.400">
                          Created: {new Date(farm.created_at).toLocaleDateString()}
                        </Text>
                        <Badge colorScheme={stats.utilizationRate > 80 ? 'green' : 'orange'}>
                          {stats.utilizationRate > 80 ? 'High Usage' : 'Moderate Usage'}
                        </Badge>
                      </HStack>
                    </VStack>
                  </CardBody>
                </Card>
              );
            })}
          </SimpleGrid>
        ) : (
          <Card bg={bg} border="1px" borderColor={borderColor}>
            <CardBody textAlign="center" py={12}>
              <Icon as={Building2} w={16} h={16} color="gray.400" mb={4} />
              <Heading size="md" color="gray.600" mb={2}>
                No Farms Found
              </Heading>
              <Text color="gray.500" mb={6}>
                Get started by creating your first farm
              </Text>
              <Button
                leftIcon={<Icon as={Plus} />}
                onClick={handleAddFarm}
                colorScheme="green"
                size="lg"
              >
                Create Your First Farm
              </Button>
            </CardBody>
          </Card>
        )}

        {/* Add/Edit Farm Modal */}
        <Modal isOpen={isOpen} onClose={onClose} size="lg">
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>
              {editingFarm ? 'Edit Farm' : 'Add New Farm'}
            </ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <VStack spacing={4}>
                <FormControl isRequired>
                  <FormLabel>Farm Name (खेत का नाम)</FormLabel>
                  <Input
                    placeholder="e.g., Ramgarh Farm"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Location (स्थान)</FormLabel>
                  <Input
                    placeholder="e.g., Village: Ramgarh, District: XYZ"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Total Area in Acres (कुल क्षेत्रफल)</FormLabel>
                  <Input
                    type="number"
                    placeholder="e.g., 10"
                    value={formData.total_area_acres}
                    onChange={(e) => setFormData({ ...formData, total_area_acres: parseFloat(e.target.value) || 0 })}
                  />
                </FormControl>
                
                <FormControl>
                  <FormLabel>Description (विवरण)</FormLabel>
                  <Textarea
                    placeholder="Optional description of the farm..."
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  />
                </FormControl>
                
                <HStack spacing={4} width="full">
                  <FormControl>
                    <FormLabel>Latitude (अक्षांश)</FormLabel>
                    <Input
                      type="number"
                      step="any"
                      placeholder="e.g., 28.368911"
                      value={formData.latitude}
                      onChange={(e) => setFormData({ ...formData, latitude: parseFloat(e.target.value) || 0 })}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Longitude (देशांतर)</FormLabel>
                    <Input
                      type="number"
                      step="any"
                      placeholder="e.g., 77.541033"
                      value={formData.longitude}
                      onChange={(e) => setFormData({ ...formData, longitude: parseFloat(e.target.value) || 0 })}
                    />
                  </FormControl>
                </HStack>
                
                <HStack spacing={4} width="full">
                  <Button
                    colorScheme="green"
                    onClick={handleSubmit}
                    flex={1}
                    isLoading={createFarmMutation.isPending || updateFarmMutation.isPending}
                    loadingText={editingFarm ? 'Updating...' : 'Creating...'}
                  >
                    {editingFarm ? 'Update Farm' : 'Create Farm'}
                  </Button>
                  <Button
                    variant="outline"
                    onClick={onClose}
                    flex={1}
                    isDisabled={createFarmMutation.isPending || updateFarmMutation.isPending}
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

export default Farms;
