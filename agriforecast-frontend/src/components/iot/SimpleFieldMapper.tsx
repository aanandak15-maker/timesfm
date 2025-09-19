import React, { useState } from 'react';
import {
  Box, VStack, HStack, Text, Button, Card, CardBody, 
  Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, 
  ModalCloseButton, useDisclosure, FormControl, FormLabel, 
  Input, Select, Textarea, useToast, SimpleGrid, Badge,
  Icon, useColorModeValue
} from '@chakra-ui/react';
import { MapPin, Plus, Edit, Trash2, Eye, Crop } from 'lucide-react';

interface SimpleField {
  id: string;
  name: string;
  crop: string;
  size: string;
  location: string;
  shape: 'rectangle' | 'circle' | 'triangle' | 'irregular';
  status: 'healthy' | 'needs_water' | 'needs_fertilizer' | 'pest_alert' | 'harvest_ready';
}

const SimpleFieldMapper: React.FC = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();
  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  const [fields, setFields] = useState<SimpleField[]>([
    {
      id: '1',
      name: 'मेरा धान का खेत',
      crop: 'Rice',
      size: '2 acres',
      location: 'Village: Ramgarh',
      shape: 'rectangle',
      status: 'healthy'
    },
    {
      id: '2',
      name: 'गेहूं का खेत',
      crop: 'Wheat',
      size: '1.5 acres',
      location: 'Village: Ramgarh',
      shape: 'circle',
      status: 'needs_water'
    }
  ]);
  
  const [editingField, setEditingField] = useState<SimpleField | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    crop: '',
    size: '',
    location: '',
    shape: 'rectangle' as const
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
      case 'healthy': return 'स्वस्थ';
      case 'needs_water': return 'पानी चाहिए';
      case 'needs_fertilizer': return 'खाद चाहिए';
      case 'pest_alert': return 'कीट चेतावनी';
      case 'harvest_ready': return 'कटाई तैयार';
      default: return 'अज्ञात';
    }
  };

  const getShapeIcon = (shape: string) => {
    switch (shape) {
      case 'rectangle': return '⬜';
      case 'circle': return '⭕';
      case 'triangle': return '🔺';
      case 'irregular': return '🔶';
      default: return '⬜';
    }
  };

  const handleAddField = () => {
    setEditingField(null);
    setFormData({
      name: '',
      crop: '',
      size: '',
      location: '',
      shape: 'rectangle'
    });
    onOpen();
  };

  const handleEditField = (field: SimpleField) => {
    setEditingField(field);
    setFormData({
      name: field.name,
      crop: field.crop,
      size: field.size,
      location: field.location,
      shape: field.shape
    });
    onOpen();
  };

  const handleSaveField = () => {
    if (!formData.name || !formData.crop || !formData.size || !formData.location) {
      toast({
        title: 'Please fill all fields',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    if (editingField) {
      // Update existing field
      setFields(prev => prev.map(field => 
        field.id === editingField.id 
          ? { ...field, ...formData }
          : field
      ));
      toast({
        title: 'Field updated successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } else {
      // Add new field
      const newField: SimpleField = {
        id: Date.now().toString(),
        ...formData,
        status: 'healthy'
      };
      setFields(prev => [...prev, newField]);
      toast({
        title: 'Field added successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    }

    onClose();
  };

  const handleDeleteField = (fieldId: string) => {
    setFields(prev => prev.filter(field => field.id !== fieldId));
    toast({
      title: 'Field deleted',
      status: 'info',
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Box>
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <Card bg={bg} border="1px" borderColor={borderColor}>
          <CardBody>
            <HStack justify="space-between">
              <HStack>
                <Icon as={MapPin} w={6} h={6} color="green.500" />
                <Text fontSize="xl" fontWeight="bold">
                  Field Mapping (खेत मैपिंग)
                </Text>
              </HStack>
              <Button
                leftIcon={<Icon as={Plus} />}
                onClick={handleAddField}
                colorScheme="green"
                size="sm"
              >
                Add Field
              </Button>
            </HStack>
          </CardBody>
        </Card>

        {/* Fields Grid */}
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
          {fields.map(field => (
            <Card
              key={field.id}
              bg={bg}
              border="1px"
              borderColor={borderColor}
              _hover={{ shadow: 'md' }}
            >
              <CardBody>
                <VStack spacing={3} align="stretch">
                  {/* Field Shape Visual */}
                  <Box textAlign="center" py={4}>
                    <Text fontSize="4xl">{getShapeIcon(field.shape)}</Text>
                    <Text fontSize="sm" color="gray.600" textTransform="capitalize">
                      {field.shape} shape
                    </Text>
                  </Box>

                  {/* Field Info */}
                  <VStack spacing={2} align="stretch">
                    <Text fontWeight="bold" fontSize="lg">{field.name}</Text>
                    <HStack justify="space-between">
                      <Text fontSize="sm" color="gray.600">{field.crop}</Text>
                      <Text fontSize="sm" color="gray.600">{field.size}</Text>
                    </HStack>
                    <Text fontSize="sm" color="gray.500">{field.location}</Text>
                    
                    <Badge 
                      colorScheme={getStatusColor(field.status)} 
                      alignSelf="center"
                      size="sm"
                    >
                      {getStatusText(field.status)}
                    </Badge>
                  </VStack>

                  {/* Actions */}
                  <HStack justify="center" spacing={2}>
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
                      onClick={() => handleEditField(field)}
                    >
                      Edit
                    </Button>
                    <Button
                      size="sm"
                      leftIcon={<Icon as={Trash2} />}
                      colorScheme="red"
                      variant="outline"
                      onClick={() => handleDeleteField(field.id)}
                    >
                      Delete
                    </Button>
                  </HStack>
                </VStack>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>

        {/* Add/Edit Field Modal */}
        <Modal isOpen={isOpen} onClose={onClose} size="lg">
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>
              {editingField ? 'Edit Field' : 'Add New Field'}
            </ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <VStack spacing={4}>
                <FormControl>
                  <FormLabel>Field Name (खेत का नाम)</FormLabel>
                  <Input
                    placeholder="e.g., मेरा धान का खेत"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </FormControl>
                
                <FormControl>
                  <FormLabel>Crop Type (फसल का प्रकार)</FormLabel>
                  <Select
                    value={formData.crop}
                    onChange={(e) => setFormData({ ...formData, crop: e.target.value })}
                  >
                    <option value="">Select crop</option>
                    <option value="Rice">Rice (धान)</option>
                    <option value="Wheat">Wheat (गेहूं)</option>
                    <option value="Corn">Corn (मक्का)</option>
                    <option value="Vegetables">Vegetables (सब्जियां)</option>
                    <option value="Sugarcane">Sugarcane (गन्ना)</option>
                    <option value="Cotton">Cotton (कपास)</option>
                    <option value="Soybean">Soybean (सोयाबीन)</option>
                  </Select>
                </FormControl>
                
                <FormControl>
                  <FormLabel>Field Size (खेत का आकार)</FormLabel>
                  <Input
                    placeholder="e.g., 2 acres, 1.5 bigha"
                    value={formData.size}
                    onChange={(e) => setFormData({ ...formData, size: e.target.value })}
                  />
                </FormControl>
                
                <FormControl>
                  <FormLabel>Location (स्थान)</FormLabel>
                  <Input
                    placeholder="e.g., Village: Ramgarh, District: XYZ"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  />
                </FormControl>
                
                <FormControl>
                  <FormLabel>Field Shape (खेत का आकार)</FormLabel>
                  <Select
                    value={formData.shape}
                    onChange={(e) => setFormData({ ...formData, shape: e.target.value as any })}
                  >
                    <option value="rectangle">Rectangle (आयताकार)</option>
                    <option value="circle">Circle (गोल)</option>
                    <option value="triangle">Triangle (त्रिकोण)</option>
                    <option value="irregular">Irregular (अनियमित)</option>
                  </Select>
                </FormControl>
                
                <HStack spacing={4} width="full">
                  <Button
                    colorScheme="green"
                    onClick={handleSaveField}
                    flex={1}
                  >
                    {editingField ? 'Update Field' : 'Add Field'}
                  </Button>
                  <Button
                    variant="outline"
                    onClick={onClose}
                    flex={1}
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

export default SimpleFieldMapper;
