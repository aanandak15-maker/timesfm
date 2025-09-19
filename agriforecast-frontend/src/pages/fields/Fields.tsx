import {
  Box,
  Heading,
  Text as ChakraText,
  Text,
  Button,
  HStack,
  VStack,
  useColorModeValue,
  SimpleGrid,
  Card,
  CardBody,
  Badge,
  Icon,
  Skeleton,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  FormControl,
  FormLabel,
  Input,
  Select,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  useToast,
} from '@chakra-ui/react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiService } from '../../services/api'
import demoService from '../../services/demoService'
import { Plus, MapPin, Calendar, Droplets, Edit, Trash2, Eye } from 'lucide-react'
import LocationPicker from '../../components/location/LocationPicker'
import FieldBoundaryDetector from '../../components/location/FieldBoundaryDetector'
import React, { useState } from 'react'

const Fields = () => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')
  const { isOpen, onOpen, onClose } = useDisclosure()
  const toast = useToast()
  const queryClient = useQueryClient()

  const [selectedField, setSelectedField] = useState<any>(null)
  const [isEditing, setIsEditing] = useState(false)

  // Fetch real data from FastAPI backend
  const { data: fields, isLoading, error } = useQuery({
    queryKey: ['fields'],
    queryFn: () => demoService.getFields(),
  })

  // Debug logging
  console.log('Fields data:', fields)
  console.log('Is loading:', isLoading)
  console.log('Error:', error)

  const { data: farms, isLoading: farmsLoading, error: farmsError } = useQuery({
    queryKey: ['farms'],
    queryFn: () => demoService.getFarms(),
  })

  // Debug logging for farms
  console.log('Farms data:', farms)
  console.log('Farms loading:', farmsLoading)
  console.log('Farms error:', farmsError)

  // Create field mutation
  const createFieldMutation = useMutation({
    mutationFn: apiService.createField,
    onSuccess: (data) => {
      console.log('Field created successfully:', data)
      queryClient.invalidateQueries({ queryKey: ['fields'] })
      toast({
        title: 'Field created successfully!',
        status: 'success',
        duration: 3000,
      })
      onClose()
    },
    onError: (error) => {
      console.error('Error creating field:', error)
      toast({
        title: 'Error creating field',
        description: error.message,
        status: 'error',
        duration: 5000,
      })
    },
  })

  // Update field mutation
  const updateFieldMutation = useMutation({
    mutationFn: (data: { id: string; updates: any }) => apiService.updateField(data.id, data.updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fields'] })
      toast({
        title: 'Field updated successfully!',
        status: 'success',
        duration: 3000,
      })
      onClose()
    },
    onError: (error) => {
      toast({
        title: 'Error updating field',
        description: error.message,
        status: 'error',
        duration: 5000,
      })
    },
  })

  // Delete field mutation
  const deleteFieldMutation = useMutation({
    mutationFn: apiService.deleteField,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fields'] })
      toast({
        title: 'Field deleted successfully!',
        status: 'success',
        duration: 3000,
      })
    },
    onError: (error) => {
      toast({
        title: 'Error deleting field',
        description: error.message,
        status: 'error',
        duration: 5000,
      })
    },
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'planted': return 'blue'
      case 'growing': return 'green'
      case 'harvesting': return 'orange'
      case 'harvested': return 'purple'
      default: return 'gray'
    }
  }

  const handleAddField = () => {
    setSelectedField(null)
    setIsEditing(false)
    onOpen()
  }

  const handleEditField = (field: any) => {
    setSelectedField(field)
    setIsEditing(true)
    onOpen()
  }

  const handleDeleteField = (fieldId: string) => {
    if (window.confirm('Are you sure you want to delete this field?')) {
      deleteFieldMutation.mutate(fieldId)
    }
  }

  const handleSubmit = (formData: any) => {
    console.log('handleSubmit called with:', formData)
    console.log('isEditing:', isEditing, 'selectedField:', selectedField)
    
    if (isEditing && selectedField) {
      console.log('Updating field:', selectedField.id)
      updateFieldMutation.mutate({
        id: selectedField?.id || '',
        updates: formData,
      })
    } else {
      console.log('Creating new field with data:', formData)
      createFieldMutation.mutate(formData)
    }
  }

  return (
    <Box>
      <HStack justify="space-between" mb={8}>
        <VStack align="start" spacing={2}>
          <Heading size="lg">Field Management</Heading>
          <ChakraText color="gray.600">
            Monitor and manage your agricultural fields
          </ChakraText>
        </VStack>
        <Button colorScheme="green" leftIcon={<Plus />} onClick={handleAddField}>
          Add Field
        </Button>
      </HStack>

      {/* Debug info */}
      <Box mb={4} p={4} bg="yellow.100" borderRadius="md">
        <ChakraText fontSize="sm">
          Debug: Fields count: {fields?.length || 0}, Loading: {isLoading ? 'Yes' : 'No'}, Error: {error ? 'Yes' : 'No'}
        </ChakraText>
      </Box>

      {isLoading ? (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} height="200px" />
          ))}
        </SimpleGrid>
      ) : (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
          {fields?.map((field) => (
            <Card key={field.id} bg={bg} border="1px" borderColor={borderColor}>
              <CardBody>
                <VStack align="start" spacing={4}>
                  <HStack justify="space-between" w="full">
                    <Heading size="md">{field.name}</Heading>
                    <Badge colorScheme={getStatusColor(field.status || 'active')}>
                      {field.status || 'active'}
                    </Badge>
                  </HStack>

                  <VStack spacing={2} align="start" w="full">
                    <HStack>
                      <Icon as={MapPin} w={4} h={4} color="gray.500" />
                      <ChakraText fontSize="sm" color="gray.600">
                        {field.crop_type || 'Unknown'}
                      </ChakraText>
                    </HStack>
                    <HStack>
                      <Icon as={Calendar} w={4} h={4} color="gray.500" />
                      <ChakraText fontSize="sm" color="gray.600">
                        {field.area_acres} acres
                      </ChakraText>
                    </HStack>
                    {field.soil_type && (
                      <HStack>
                        <Icon as={Droplets} w={4} h={4} color="gray.500" />
                        <ChakraText fontSize="sm" color="gray.600">
                          {field.soil_type}
                        </ChakraText>
                      </HStack>
                    )}
                    {field.farm_id && (
                      <ChakraText fontSize="sm" color="gray.500">
                        Farm ID: {field.farm_id}
                      </ChakraText>
                    )}
                  </VStack>

                  <HStack spacing={2} w="full">
                    <Button 
                      size="sm" 
                      variant="outline" 
                      flex="1"
                      leftIcon={<Eye />}
                    >
                      View
                    </Button>
                    <Button 
                      size="sm" 
                      colorScheme="blue" 
                      flex="1"
                      leftIcon={<Edit />}
                      onClick={() => handleEditField(field)}
                    >
                      Edit
                    </Button>
                    <Button 
                      size="sm" 
                      colorScheme="red" 
                      variant="outline"
                      onClick={() => handleDeleteField(field.id)}
                      leftIcon={<Trash2 />}
                    >
                      Delete
                    </Button>
                  </HStack>
                </VStack>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>
      )}

      {/* Add/Edit Field Modal */}
      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {isEditing ? 'Edit Field' : 'Add New Field'}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FieldForm
              field={selectedField}
              farms={farms || []}
              farmsLoading={farmsLoading}
              onSubmit={handleSubmit}
              isLoading={createFieldMutation.isPending || updateFieldMutation.isPending}
            />
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  )
}

// Field Form Component
const FieldForm = ({ field, farms, farmsLoading, onSubmit, isLoading }: any) => {
  const [formData, setFormData] = useState({
    name: field?.name || '',
    farm_id: field?.farm_id || '',
    crop_type: field?.crop_type || 'Rice',
    area_acres: field?.area_acres || 1.0,
    latitude: field?.latitude || 28.368911,
    longitude: field?.longitude || 77.541033,
    soil_type: field?.soil_type || 'Loamy',
    planting_date: field?.planting_date || '',
    harvest_date: field?.harvest_date || '',
  })

  // Set default farm if none selected and farms are available
  React.useEffect(() => {
    if (!formData.farm_id && farms && farms.length > 0) {
      setFormData(prev => ({ ...prev, farm_id: farms[0].id }))
    }
  }, [farms, formData.farm_id])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    // Ensure farm_id is set - use first available farm or default
    const submitData = {
      ...formData,
      farm_id: formData.farm_id || (farms && farms.length > 0 ? farms[0].id : 'farm-1')
    }
    
    console.log('Submitting field data:', submitData)
    onSubmit(submitData)
  }

  return (
    <form onSubmit={handleSubmit}>
      <VStack spacing={4} align="stretch">
        <FormControl isRequired>
          <FormLabel>Field Name</FormLabel>
          <Input
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="e.g., Rice Field 1"
          />
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Farm</FormLabel>
          <Select
            value={formData.farm_id}
            onChange={(e) => setFormData({ ...formData, farm_id: e.target.value })}
            placeholder="Select a farm"
            disabled={farmsLoading}
          >
            <option value="">Select a farm</option>
            {farmsLoading ? (
              <option value="" disabled>Loading farms...</option>
            ) : farms && farms.length > 0 ? (
              farms.map((farm: any) => (
                <option key={farm.id} value={farm.id}>
                  {farm.name} - {farm.location}
                </option>
              ))
            ) : (
              <option value="farm-1" disabled>
                No farms available - Using default farm
              </option>
            )}
          </Select>
          {farmsLoading ? (
            <Text fontSize="sm" color="blue.500" mt={1}>
              Loading farms...
            </Text>
          ) : !farms || farms.length === 0 ? (
            <Text fontSize="sm" color="orange.500" mt={1}>
              No farms found. Please create a farm first or contact support.
            </Text>
          ) : null}
        </FormControl>

        <HStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Crop Type</FormLabel>
            <Select
              value={formData.crop_type}
              onChange={(e) => setFormData({ ...formData, crop_type: e.target.value })}
            >
              <option value="Rice">Rice (चावल)</option>
              <option value="Maize">Maize (मक्का)</option>
              <option value="Cotton">Cotton (कपास)</option>
            </Select>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Area (acres)</FormLabel>
            <NumberInput
              value={formData.area_acres}
              onChange={(_, value) => setFormData({ ...formData, area_acres: value || 0 })}
              min={0.1}
              step={0.1}
            >
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </FormControl>
        </HStack>

        <FormControl>
          <FormLabel>Soil Type</FormLabel>
          <Select
            value={formData.soil_type}
            onChange={(e) => setFormData({ ...formData, soil_type: e.target.value })}
          >
            <option value="Loamy">Loamy</option>
            <option value="Clay">Clay</option>
            <option value="Sandy">Sandy</option>
            <option value="Silty">Silty</option>
            <option value="Other">Other</option>
          </Select>
        </FormControl>

        {/* Enhanced Location Picker */}
        <FormControl>
          <FormLabel>Field Location</FormLabel>
          <LocationPicker
            latitude={formData.latitude}
            longitude={formData.longitude}
            onLocationChange={(lat, lng) => {
              setFormData({ ...formData, latitude: lat, longitude: lng })
            }}
            disabled={false}
          />
        </FormControl>

        {/* Field Boundary Detection */}
        <FormControl>
          <FormLabel>Field Boundary Detection</FormLabel>
          <FieldBoundaryDetector
            fieldId="new"
            currentArea={formData.area_acres || 0}
            onBoundaryUpdate={(boundary) => {
              // Update form data with detected boundary
              setFormData({ 
                ...formData, 
                area_acres: boundary.area,
                latitude: boundary.center.lat,
                longitude: boundary.center.lng
              })
            }}
            disabled={false}
          />
        </FormControl>

        <HStack spacing={4}>
          <FormControl>
            <FormLabel>Planting Date</FormLabel>
            <Input
              type="date"
              value={formData.planting_date}
              onChange={(e) => setFormData({ ...formData, planting_date: e.target.value })}
            />
          </FormControl>

          <FormControl>
            <FormLabel>Expected Harvest Date</FormLabel>
            <Input
              type="date"
              value={formData.harvest_date}
              onChange={(e) => setFormData({ ...formData, harvest_date: e.target.value })}
            />
          </FormControl>
        </HStack>

        <Button
          type="submit"
          colorScheme="green"
          isLoading={isLoading}
          loadingText={field ? 'Updating...' : 'Creating...'}
        >
          {field ? 'Update Field' : 'Create Field'}
        </Button>
      </VStack>
    </form>
  )
}

export default Fields