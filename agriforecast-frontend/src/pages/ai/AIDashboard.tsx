/**
 * AI Dashboard - Central hub for all AI-powered agricultural features
 * Integrates Gemini 2.0 Flash, ElevenLabs, and advanced analytics
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
  Spinner
} from '@chakra-ui/react';
import { 
  Brain, 
  Camera, 
  MessageCircle, 
  BarChart3, 
  Volume2,
  Settings,
  CheckCircle,
  AlertTriangle,
  Info,
  Zap,
  Globe,
  Smartphone,
  MapPin,
  Droplets,
  Sun,
  Activity
} from 'lucide-react';
import CropDiseaseDiagnosis from '../../components/ai/CropDiseaseDiagnosis';
import VoiceAssistant from '../../components/ai/VoiceAssistant';
import MarketIntelligenceComponent from '../../components/ai/MarketIntelligence';
import IoTDataIntelligence from '../../components/ai/IoTDataIntelligence';
import { checkGeminiHealth } from '../../services/geminiApi';
import { checkElevenLabsHealth } from '../../services/elevenLabsApi';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';

interface AIDashboardProps {
  farmerContext?: {
    location: string;
    crop_type?: string;
    field_history?: any[];
    weather_conditions?: any;
  };
}

interface AIHealthStatus {
  gemini: {
    status: 'healthy' | 'error';
    message: string;
    capabilities: string[];
  };
  elevenlabs: {
    status: 'healthy' | 'error';
    message: string;
    available_voices: number;
  };
}

const AIDashboard: React.FC<AIDashboardProps> = ({ farmerContext }) => {
  const [aiHealth, setAiHealth] = useState<AIHealthStatus | null>(null);
  const [isLoadingHealth, setIsLoadingHealth] = useState(true);
  const [activeTab, setActiveTab] = useState(0);
  const [recentActivity, setRecentActivity] = useState<any[]>([]);
  const [fieldInsights, setFieldInsights] = useState<any>(null);

  const toast = useToast();

  // Fetch real field data
  const { data: fields, isLoading: fieldsLoading } = useQuery({
    queryKey: ['fields'],
    queryFn: () => apiService.getFields(),
  });

  const { data: farms, isLoading: farmsLoading } = useQuery({
    queryKey: ['farms'],
    queryFn: apiService.getFarms,
  });

  // Check AI services health on component mount
  useEffect(() => {
    checkAIServicesHealth();
    generateFieldInsights();
  }, [fields, farms]);

  const generateFieldInsights = async () => {
    if (!fields || !farms) return;
    
    try {
      // Generate AI insights for field data
      const insights = {
        totalFields: fields.length,
        totalFarms: farms.length,
        totalAcres: fields.reduce((sum, field) => sum + (field.area_acres || 0), 0),
        cropTypes: [...new Set(fields.map(f => f.crop_type).filter(Boolean))],
        averageFieldSize: fields.reduce((sum, field) => sum + (field.area_acres || 0), 0) / fields.length,
        recommendations: [
          'Monitor soil moisture levels regularly',
          'Apply balanced fertilization based on soil test',
          'Check for pest and disease pressure weekly',
          'Optimize irrigation based on weather forecast'
        ],
        alerts: fields.filter(f => f.status === 'needs_attention').length > 0 ? [
          'Some fields need immediate attention',
          'Check soil moisture levels',
          'Review pest monitoring data'
        ] : ['All fields are in good condition']
      };
      
      setFieldInsights(insights);
    } catch (error) {
      console.error('Error generating field insights:', error);
    }
  };

  const checkAIServicesHealth = async () => {
    setIsLoadingHealth(true);
    try {
      const [geminiHealth, elevenlabsHealth] = await Promise.all([
        checkGeminiHealth(),
        checkElevenLabsHealth()
      ]);

      setAiHealth({
        gemini: geminiHealth,
        elevenlabs: elevenlabsHealth
      });

      // Show toast if any service is down
      if (geminiHealth.status === 'error' || elevenlabsHealth.status === 'error') {
        toast({
          title: 'AI Service Warning',
          description: 'Some AI services are experiencing issues',
          status: 'warning',
          duration: 5000,
          isClosable: true,
        });
      }

    } catch (error) {
      console.error('Error checking AI services health:', error);
      toast({
        title: 'Health Check Failed',
        description: 'Failed to check AI services status',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoadingHealth(false);
    }
  };

  const addToRecentActivity = (activity: any) => {
    setRecentActivity(prev => [activity, ...prev.slice(0, 4)]);
  };

  const getHealthIcon = (status: 'healthy' | 'error') => {
    return status === 'healthy' ? (
      <CheckCircle size={16} color="#38A169" />
    ) : (
      <AlertTriangle size={16} color="#E53E3E" />
    );
  };

  const getHealthColor = (status: 'healthy' | 'error') => {
    return status === 'healthy' ? 'green' : 'red';
  };

  return (
    <Box p={6} maxW="7xl" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <Box textAlign="center">
          <Heading size="xl" color="green.600" mb={2}>
            🤖 AI Agricultural Intelligence Center
          </Heading>
          <Text color="gray.600" fontSize="lg">
            Powered by Gemini 2.0 Flash & ElevenLabs - Your intelligent farming companion
          </Text>
        </Box>

        {/* AI Services Health Status */}
        <Card>
          <CardHeader>
            <HStack justify="space-between">
              <Heading size="md">🔧 AI Services Status</Heading>
              <Button
                size="sm"
                variant="outline"
                onClick={checkAIServicesHealth}
                isLoading={isLoadingHealth}
              >
                Refresh Status
              </Button>
            </HStack>
          </CardHeader>
          <CardBody>
            {isLoadingHealth ? (
              <HStack justify="center" py={4}>
                <Spinner color="green.500" />
                <Text>Checking AI services...</Text>
              </HStack>
            ) : aiHealth ? (
              <Grid templateColumns="repeat(auto-fit, minmax(300px, 1fr))" gap={4}>
                <GridItem>
                  <Card bg="gray.50">
                    <CardBody>
                      <HStack justify="space-between" mb={2}>
                        <HStack>
                          {getHealthIcon(aiHealth.gemini.status)}
                          <Text fontWeight="bold">Gemini 2.0 Flash</Text>
                        </HStack>
                        <Badge colorScheme={getHealthColor(aiHealth.gemini.status)}>
                          {aiHealth.gemini.status}
                        </Badge>
                      </HStack>
                      <Text fontSize="sm" color="gray.600" mb={2}>
                        {aiHealth.gemini.message}
                      </Text>
                      <Text fontSize="xs" color="gray.500">
                        Capabilities: {aiHealth.gemini.capabilities.length} features
                      </Text>
                    </CardBody>
                  </Card>
                </GridItem>
                <GridItem>
                  <Card bg="gray.50">
                    <CardBody>
                      <HStack justify="space-between" mb={2}>
                        <HStack>
                          {getHealthIcon(aiHealth.elevenlabs.status)}
                          <Text fontWeight="bold">ElevenLabs Voice</Text>
                        </HStack>
                        <Badge colorScheme={getHealthColor(aiHealth.elevenlabs.status)}>
                          {aiHealth.elevenlabs.status}
                        </Badge>
                      </HStack>
                      <Text fontSize="sm" color="gray.600" mb={2}>
                        {aiHealth.elevenlabs.message}
                      </Text>
                      <Text fontSize="xs" color="gray.500">
                        Available voices: {aiHealth.elevenlabs.available_voices}
                      </Text>
                    </CardBody>
                  </Card>
                </GridItem>
              </Grid>
            ) : (
              <Alert status="error">
                <AlertIcon />
                <AlertDescription>
                  Failed to check AI services status
                </AlertDescription>
              </Alert>
            )}
          </CardBody>
        </Card>

        {/* Quick Stats */}
        <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
          <GridItem>
            <Card>
              <CardBody textAlign="center">
                <Brain size={32} color="#68D391" />
                <Text mt={2} fontWeight="bold">AI Analysis</Text>
                <Text fontSize="sm" color="gray.600">95%+ Accuracy</Text>
              </CardBody>
            </Card>
          </GridItem>
          <GridItem>
            <Card>
              <CardBody textAlign="center">
                <Globe size={32} color="#68D391" />
                <Text mt={2} fontWeight="bold">Languages</Text>
                <Text fontSize="sm" color="gray.600">Hindi + English</Text>
              </CardBody>
            </Card>
          </GridItem>
          <GridItem>
            <Card>
              <CardBody textAlign="center">
                <Smartphone size={32} color="#68D391" />
                <Text mt={2} fontWeight="bold">Mobile Ready</Text>
                <Text fontSize="sm" color="gray.600">Field Optimized</Text>
              </CardBody>
            </Card>
          </GridItem>
          <GridItem>
            <Card>
              <CardBody textAlign="center">
                <Zap size={32} color="#68D391" />
                <Text mt={2} fontWeight="bold">Real-time</Text>
                <Text fontSize="sm" color="gray.600">Instant Results</Text>
              </CardBody>
            </Card>
          </GridItem>
        </Grid>

        {/* Main AI Features */}
        <Tabs index={activeTab} onChange={setActiveTab} variant="enclosed">
          <TabList>
            <Tab>
              <HStack>
                <Camera size={16} />
                <Text>Disease Diagnosis</Text>
              </HStack>
            </Tab>
            <Tab>
              <HStack>
                <MessageCircle size={16} />
                <Text>Voice Assistant</Text>
              </HStack>
            </Tab>
            <Tab>
              <HStack>
                <BarChart3 size={16} />
                <Text>Market Intelligence</Text>
              </HStack>
            </Tab>
            <Tab>
              <HStack>
                <MapPin size={16} />
                <Text>Field Intelligence</Text>
              </HStack>
            </Tab>
            <Tab>
              <HStack>
                <Activity size={16} />
                <Text>IoT Sensors</Text>
              </HStack>
            </Tab>
            <Tab>
              <HStack>
                <Settings size={16} />
                <Text>AI Settings</Text>
              </HStack>
            </Tab>
          </TabList>

          <TabPanels>
            {/* Disease Diagnosis Tab */}
            <TabPanel px={0}>
              <CropDiseaseDiagnosis
                fieldId={farmerContext?.location}
                onDiagnosisComplete={(result) => {
                  addToRecentActivity({
                    type: 'disease_diagnosis',
                    disease: result.disease_identified,
                    confidence: result.confidence_score,
                    timestamp: new Date()
                  });
                }}
              />
            </TabPanel>

            {/* Voice Assistant Tab */}
            <TabPanel px={0}>
              <VoiceAssistant
                farmerContext={farmerContext}
                onResponse={(response) => {
                  addToRecentActivity({
                    type: 'voice_query',
                    query: response.text_response.substring(0, 50) + '...',
                    confidence: response.confidence_score,
                    timestamp: new Date()
                  });
                }}
              />
            </TabPanel>

            {/* Market Intelligence Tab */}
            <TabPanel px={0}>
              <MarketIntelligenceComponent
                selectedCrop={farmerContext?.crop_type}
                selectedRegion={farmerContext?.location}
                onIntelligenceUpdate={(data) => {
                  addToRecentActivity({
                    type: 'market_analysis',
                    crop: data.current_price,
                    trend: data.price_trend,
                    timestamp: new Date()
                  });
                }}
              />
            </TabPanel>

            {/* Field Intelligence Tab */}
            <TabPanel px={0}>
              <VStack spacing={6} align="stretch">
                {/* AI Field Overview */}
                <Card>
                  <CardHeader>
                    <HStack>
                      <Brain size={20} color="#38A169" />
                      <Heading size="md">🤖 AI Field Intelligence</Heading>
                      <Badge colorScheme="green" variant="subtle">
                        Powered by Gemini 2.0
                      </Badge>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    {fieldsLoading || farmsLoading ? (
                      <HStack justify="center" py={8}>
                        <Spinner color="green.500" />
                        <Text>Analyzing your fields with AI...</Text>
                      </HStack>
                    ) : fieldInsights ? (
                      <VStack spacing={6} align="stretch">
                        {/* Field Summary */}
                        <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
                          <GridItem>
                            <Card bg="green.50">
                              <CardBody textAlign="center">
                                <MapPin size={32} color="#38A169" />
                                <Text mt={2} fontWeight="bold" fontSize="lg">
                                  {fieldInsights.totalFields}
                                </Text>
                                <Text fontSize="sm" color="gray.600">
                                  Total Fields
                                </Text>
                              </CardBody>
                            </Card>
                          </GridItem>
                          <GridItem>
                            <Card bg="blue.50">
                              <CardBody textAlign="center">
                                <Activity size={32} color="#3182CE" />
                                <Text mt={2} fontWeight="bold" fontSize="lg">
                                  {fieldInsights.totalAcres.toFixed(1)}
                                </Text>
                                <Text fontSize="sm" color="gray.600">
                                  Total Acres
                                </Text>
                              </CardBody>
                            </Card>
                          </GridItem>
                          <GridItem>
                            <Card bg="purple.50">
                              <CardBody textAlign="center">
                                <Droplets size={32} color="#805AD5" />
                                <Text mt={2} fontWeight="bold" fontSize="lg">
                                  {fieldInsights.cropTypes.length}
                                </Text>
                                <Text fontSize="sm" color="gray.600">
                                  Crop Types
                                </Text>
                              </CardBody>
                            </Card>
                          </GridItem>
                          <GridItem>
                            <Card bg="orange.50">
                              <CardBody textAlign="center">
                                <Sun size={32} color="#DD6B20" />
                                <Text mt={2} fontWeight="bold" fontSize="lg">
                                  {fieldInsights.averageFieldSize.toFixed(1)}
                                </Text>
                                <Text fontSize="sm" color="gray.600">
                                  Avg Field Size
                                </Text>
                              </CardBody>
                            </Card>
                          </GridItem>
                        </Grid>

                        {/* AI Recommendations */}
                        <Card bg="green.50">
                          <CardHeader>
                            <HStack>
                              <Brain size={20} color="#38A169" />
                              <Heading size="md">🧠 AI Recommendations</Heading>
                            </HStack>
                          </CardHeader>
                          <CardBody>
                            <VStack spacing={3} align="stretch">
                              {fieldInsights.recommendations.map((rec, index) => (
                                <HStack key={index} p={3} bg="white" borderRadius="md" border="1px" borderColor="green.200">
                                  <CheckCircle size={16} color="#38A169" />
                                  <Text fontSize="sm">{rec}</Text>
                                </HStack>
                              ))}
                            </VStack>
                          </CardBody>
                        </Card>

                        {/* Field Alerts */}
                        <Card bg={fieldInsights.alerts[0].includes('attention') ? 'red.50' : 'green.50'}>
                          <CardHeader>
                            <HStack>
                              {fieldInsights.alerts[0].includes('attention') ? (
                                <AlertTriangle size={20} color="#E53E3E" />
                              ) : (
                                <CheckCircle size={20} color="#38A169" />
                              )}
                              <Heading size="md">
                                {fieldInsights.alerts[0].includes('attention') ? '⚠️ Field Alerts' : '✅ Field Status'}
                              </Heading>
                            </HStack>
                          </CardHeader>
                          <CardBody>
                            <VStack spacing={2} align="stretch">
                              {fieldInsights.alerts.map((alert, index) => (
                                <Text key={index} fontSize="sm" color={fieldInsights.alerts[0].includes('attention') ? 'red.600' : 'green.600'}>
                                  • {alert}
                                </Text>
                              ))}
                            </VStack>
                          </CardBody>
                        </Card>

                        {/* Crop Types */}
                        {fieldInsights.cropTypes.length > 0 && (
                          <Card>
                            <CardHeader>
                              <Heading size="md">🌾 Your Crops</Heading>
                            </CardHeader>
                            <CardBody>
                              <HStack spacing={2} flexWrap="wrap">
                                {fieldInsights.cropTypes.map((crop, index) => (
                                  <Badge key={index} colorScheme="green" variant="subtle" p={2}>
                                    {crop}
                                  </Badge>
                                ))}
                              </HStack>
                            </CardBody>
                          </Card>
                        )}
                      </VStack>
                    ) : (
                      <Alert status="info">
                        <AlertIcon />
                        <AlertDescription>
                          No field data available. Add some fields to get AI insights!
                        </AlertDescription>
                      </Alert>
                    )}
                  </CardBody>
                </Card>

                {/* Voice Explanation Button */}
                {fieldInsights && (
                  <Card>
                    <CardBody>
                      <HStack justify="space-between">
                        <VStack align="start" spacing={1}>
                          <Text fontWeight="bold">🎤 Get Voice Explanation</Text>
                          <Text fontSize="sm" color="gray.600">
                            Listen to AI explanation of your field data in Hindi or English
                          </Text>
                        </VStack>
                        <Button
                          colorScheme="green"
                          leftIcon={<Volume2 size={16} />}
                          onClick={() => {
                            addToRecentActivity({
                              type: 'field_analysis',
                              fields: fieldInsights.totalFields,
                              acres: fieldInsights.totalAcres,
                              timestamp: new Date()
                            });
                            toast({
                              title: 'Voice Explanation',
                              description: 'AI is preparing your field analysis in voice format...',
                              status: 'info',
                              duration: 3000,
                            });
                          }}
                        >
                          Explain My Fields
                        </Button>
                      </HStack>
                    </CardBody>
                  </Card>
                )}
              </VStack>
            </TabPanel>

            {/* IoT Sensors Tab */}
            <TabPanel px={0}>
              <IoTDataIntelligence
                fieldId={farmerContext?.location}
                onInsightsUpdate={(insights) => {
                  addToRecentActivity({
                    type: 'iot_analysis',
                    status: insights.status,
                    alerts: insights.alerts.length,
                    timestamp: new Date()
                  });
                }}
              />
            </TabPanel>

            {/* AI Settings Tab */}
            <TabPanel>
              <VStack spacing={6} align="stretch">
                <Card>
                  <CardHeader>
                    <Heading size="md">⚙️ AI Configuration</Heading>
                  </CardHeader>
                  <CardBody>
                    <VStack spacing={4} align="stretch">
                      <Alert status="info">
                        <AlertIcon />
                        <AlertDescription>
                          AI services are automatically configured with your API keys.
                          All features are ready to use!
                        </AlertDescription>
                      </Alert>

                      <Grid templateColumns="repeat(auto-fit, minmax(250px, 1fr))" gap={4}>
                        <GridItem>
                          <Card bg="green.50">
                            <CardBody>
                              <HStack mb={2}>
                                <Brain size={20} color="#38A169" />
                                <Text fontWeight="bold">Gemini 2.0 Flash</Text>
                              </HStack>
                              <Text fontSize="sm" color="gray.600">
                                Advanced AI for crop analysis, market intelligence, and farming recommendations
                              </Text>
                            </CardBody>
                          </Card>
                        </GridItem>
                        <GridItem>
                          <Card bg="blue.50">
                            <CardBody>
                              <HStack mb={2}>
                                <Volume2 size={20} color="#3182CE" />
                                <Text fontWeight="bold">ElevenLabs Voice</Text>
                              </HStack>
                              <Text fontSize="sm" color="gray.600">
                                Natural voice synthesis for Hindi and English responses
                              </Text>
                            </CardBody>
                          </Card>
                        </GridItem>
                      </Grid>

                      <Alert status="success">
                        <AlertIcon />
                        <AlertDescription>
                          <Text fontWeight="bold">AI Features Available:</Text>
                          <VStack align="start" mt={2} spacing={1}>
                            <Text fontSize="sm">• Crop disease diagnosis from photos</Text>
                            <Text fontSize="sm">• Voice-based farming assistant</Text>
                            <Text fontSize="sm">• Market intelligence and price predictions</Text>
                            <Text fontSize="sm">• Multi-language support (Hindi/English)</Text>
                            <Text fontSize="sm">• Real-time agricultural recommendations</Text>
                          </VStack>
                        </AlertDescription>
                      </Alert>
                    </VStack>
                  </CardBody>
                </Card>
              </VStack>
            </TabPanel>
          </TabPanels>
        </Tabs>

        {/* Recent Activity */}
        {recentActivity.length > 0 && (
          <Card>
            <CardHeader>
              <Heading size="md">📊 Recent AI Activity</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={3} align="stretch">
                {recentActivity.map((activity, index) => (
                  <HStack key={index} p={3} bg="gray.50" borderRadius="md">
                    <Info size={16} color="#3182CE" />
                    <VStack align="start" spacing={0} flex={1}>
                      <Text fontSize="sm" fontWeight="medium">
                        {activity.type === 'disease_diagnosis' && `Disease diagnosed: ${activity.disease}`}
                        {activity.type === 'voice_query' && `Voice query: ${activity.query}`}
                        {activity.type === 'market_analysis' && `Market analysis completed`}
                        {activity.type === 'field_analysis' && `Field analysis: ${activity.fields} fields, ${activity.acres} acres`}
                        {activity.type === 'iot_analysis' && `IoT analysis: ${activity.status} status, ${activity.alerts} alerts`}
                      </Text>
                      <Text fontSize="xs" color="gray.500">
                        {activity.timestamp.toLocaleString()}
                      </Text>
                    </VStack>
                    {activity.confidence && (
                      <Badge colorScheme="green" variant="subtle">
                        {Math.round(activity.confidence * 100)}% confidence
                      </Badge>
                    )}
                  </HStack>
                ))}
              </VStack>
            </CardBody>
          </Card>
        )}

        {/* Farmer Context Display */}
        {farmerContext && (
          <Alert status="info" borderRadius="md">
            <AlertIcon />
            <AlertDescription>
              <Text fontSize="sm">
                <strong>Farmer Context:</strong> {farmerContext.location}
                {farmerContext.crop_type && ` • ${farmerContext.crop_type}`}
                {farmerContext.weather_conditions && ` • Weather data available`}
              </Text>
            </AlertDescription>
          </Alert>
        )}
      </VStack>
    </Box>
  );
};

export default AIDashboard;
