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
  Smartphone
} from 'lucide-react';
import CropDiseaseDiagnosis from '../../components/ai/CropDiseaseDiagnosis';
import VoiceAssistant from '../../components/ai/VoiceAssistant';
import MarketIntelligenceComponent from '../../components/ai/MarketIntelligence';
import { checkGeminiHealth } from '../../services/geminiApi';
import { checkElevenLabsHealth } from '../../services/elevenLabsApi';

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

  const toast = useToast();

  // Check AI services health on component mount
  useEffect(() => {
    checkAIServicesHealth();
  }, []);

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
