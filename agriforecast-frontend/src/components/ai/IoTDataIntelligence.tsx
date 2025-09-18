/**
 * IoT Data Intelligence Component
 * Uses AI to present IoT sensor data in farmer-friendly way
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
  Alert,
  AlertIcon,
  AlertDescription,
  Progress,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  useColorModeValue,
  Spinner
} from '@chakra-ui/react';
import { 
  Thermometer, 
  Droplets, 
  Sun, 
  Wind, 
  Activity, 
  AlertTriangle, 
  CheckCircle,
  Volume2,
  Brain,
  Zap
} from 'lucide-react';

interface IoTData {
  temperature: number;
  humidity: number;
  soil_moisture: number;
  light_intensity: number;
  wind_speed: number;
  timestamp: string;
  location: string;
}

interface IoTInsights {
  status: 'optimal' | 'warning' | 'critical';
  recommendations: string[];
  alerts: string[];
  summary: string;
}

interface IoTDataIntelligenceProps {
  fieldId?: string;
  onInsightsUpdate?: (insights: IoTInsights) => void;
}

const IoTDataIntelligence: React.FC<IoTDataIntelligenceProps> = ({ 
  fieldId, 
  onInsightsUpdate 
}) => {
  const [iotData, setIotData] = useState<IoTData | null>(null);
  const [insights, setInsights] = useState<IoTInsights | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGeneratingVoice, setIsGeneratingVoice] = useState(false);

  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  useEffect(() => {
    loadIoTData();
  }, [fieldId]);

  const loadIoTData = async () => {
    setIsLoading(true);
    try {
      // Simulate IoT data from sensors
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const data: IoTData = {
        temperature: 28 + Math.random() * 8, // 28-36°C
        humidity: 60 + Math.random() * 30, // 60-90%
        soil_moisture: 40 + Math.random() * 40, // 40-80%
        light_intensity: 800 + Math.random() * 400, // 800-1200 lux
        wind_speed: 5 + Math.random() * 10, // 5-15 km/h
        timestamp: new Date().toISOString(),
        location: fieldId || 'Field-1'
      };
      
      setIotData(data);
      generateAIInsights(data);
    } catch (error) {
      console.error('Error loading IoT data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const generateAIInsights = (data: IoTData) => {
    const recommendations: string[] = [];
    const alerts: string[] = [];
    let status: 'optimal' | 'warning' | 'critical' = 'optimal';

    // AI analysis of IoT data
    if (data.temperature > 35) {
      alerts.push('High temperature detected - crops may be stressed');
      recommendations.push('Increase irrigation frequency');
      status = 'warning';
    } else if (data.temperature < 20) {
      alerts.push('Low temperature - growth may slow down');
      recommendations.push('Consider protective measures');
      status = 'warning';
    }

    if (data.soil_moisture < 30) {
      alerts.push('Soil moisture is critically low');
      recommendations.push('Irrigate immediately');
      status = 'critical';
    } else if (data.soil_moisture > 80) {
      alerts.push('Soil is oversaturated');
      recommendations.push('Reduce irrigation');
      status = 'warning';
    }

    if (data.humidity > 85) {
      alerts.push('High humidity - risk of fungal diseases');
      recommendations.push('Improve air circulation');
      status = 'warning';
    }

    if (data.wind_speed > 15) {
      alerts.push('Strong winds detected');
      recommendations.push('Check for crop damage');
      status = 'warning';
    }

    if (recommendations.length === 0) {
      recommendations.push('All conditions are optimal for crop growth');
      recommendations.push('Continue current farming practices');
    }

    const summary = status === 'optimal' 
      ? 'Your field conditions are excellent for crop growth'
      : status === 'warning'
      ? 'Some conditions need attention but crops are generally healthy'
      : 'Immediate action required to protect your crops';

    const aiInsights: IoTInsights = {
      status,
      recommendations,
      alerts,
      summary
    };

    setInsights(aiInsights);
    onInsightsUpdate?.(aiInsights);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'optimal': return 'green';
      case 'warning': return 'yellow';
      case 'critical': return 'red';
      default: return 'gray';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'optimal': return CheckCircle;
      case 'warning': return AlertTriangle;
      case 'critical': return AlertTriangle;
      default: return Activity;
    }
  };

  const generateVoiceExplanation = async () => {
    if (!iotData || !insights) return;
    
    setIsGeneratingVoice(true);
    try {
      // Simulate voice generation
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // In real implementation, this would call ElevenLabs API
      console.log('Generating voice explanation for IoT data:', {
        temperature: iotData.temperature,
        soil_moisture: iotData.soil_moisture,
        status: insights.status,
        summary: insights.summary
      });
      
    } catch (error) {
      console.error('Error generating voice explanation:', error);
    } finally {
      setIsGeneratingVoice(false);
    }
  };

  if (isLoading) {
    return (
      <Card>
        <CardBody>
          <VStack spacing={4} py={8}>
            <Spinner size="xl" color="green.500" />
            <Text>🤖 AI is analyzing your IoT sensor data...</Text>
            <Text fontSize="sm" color="gray.600">
              Processing temperature, humidity, soil moisture, and more
            </Text>
          </VStack>
        </CardBody>
      </Card>
    );
  }

  if (!iotData || !insights) {
    return (
      <Alert status="error">
        <AlertIcon />
        <AlertDescription>
          Unable to load IoT sensor data. Please check your sensors.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <VStack spacing={6} align="stretch">
      {/* AI Status Header */}
      <Card bg={`${getStatusColor(insights.status)}.50`}>
        <CardHeader>
          <HStack justify="space-between">
            <HStack>
              <Brain size={20} color="#38A169" />
              <Heading size="md">🤖 AI IoT Analysis</Heading>
              <Badge colorScheme={getStatusColor(insights.status)} variant="subtle">
                {insights.status.toUpperCase()}
              </Badge>
            </HStack>
            <Button
              size="sm"
              variant="outline"
              onClick={loadIoTData}
            >
              Refresh Data
            </Button>
          </HStack>
        </CardHeader>
        <CardBody>
          <VStack spacing={4} align="stretch">
            <HStack>
              {React.createElement(getStatusIcon(insights.status), { 
                size: 24, 
                color: getStatusColor(insights.status) === 'green' ? '#38A169' : 
                       getStatusColor(insights.status) === 'yellow' ? '#D69E2E' : '#E53E3E'
              })}
              <Text fontWeight="bold" fontSize="lg">
                {insights.summary}
              </Text>
            </HStack>
            
            <Text fontSize="sm" color="gray.600">
              Last updated: {new Date(iotData.timestamp).toLocaleString()}
            </Text>
          </VStack>
        </CardBody>
      </Card>

      {/* IoT Sensor Data */}
      <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
        <GridItem>
          <Card>
            <CardBody>
              <Stat>
                <StatLabel>
                  <HStack>
                    <Thermometer size={16} color="#E53E3E" />
                    <Text>Temperature</Text>
                  </HStack>
                </StatLabel>
                <StatNumber color={iotData.temperature > 35 ? 'red.500' : 'green.500'}>
                  {iotData.temperature.toFixed(1)}°C
                </StatNumber>
                <StatHelpText>
                  {iotData.temperature > 35 ? 'Hot - irrigate more' : 
                   iotData.temperature < 20 ? 'Cool - growth slow' : 'Optimal'}
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
        </GridItem>

        <GridItem>
          <Card>
            <CardBody>
              <Stat>
                <StatLabel>
                  <HStack>
                    <Droplets size={16} color="#3182CE" />
                    <Text>Soil Moisture</Text>
                  </HStack>
                </StatLabel>
                <StatNumber color={iotData.soil_moisture < 30 ? 'red.500' : 
                                 iotData.soil_moisture > 80 ? 'yellow.500' : 'green.500'}>
                  {iotData.soil_moisture.toFixed(0)}%
                </StatNumber>
                <StatHelpText>
                  {iotData.soil_moisture < 30 ? 'Too dry' : 
                   iotData.soil_moisture > 80 ? 'Too wet' : 'Perfect'}
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
        </GridItem>

        <GridItem>
          <Card>
            <CardBody>
              <Stat>
                <StatLabel>
                  <HStack>
                    <Wind size={16} color="#805AD5" />
                    <Text>Humidity</Text>
                  </HStack>
                </StatLabel>
                <StatNumber color={iotData.humidity > 85 ? 'yellow.500' : 'green.500'}>
                  {iotData.humidity.toFixed(0)}%
                </StatNumber>
                <StatHelpText>
                  {iotData.humidity > 85 ? 'High - watch diseases' : 'Good'}
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
        </GridItem>

        <GridItem>
          <Card>
            <CardBody>
              <Stat>
                <StatLabel>
                  <HStack>
                    <Sun size={16} color="#D69E2E" />
                    <Text>Light</Text>
                  </HStack>
                </StatLabel>
                <StatNumber color="green.500">
                  {iotData.light_intensity.toFixed(0)} lux
                </StatNumber>
                <StatHelpText>
                  {iotData.light_intensity > 1000 ? 'Bright' : 'Moderate'}
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
        </GridItem>

        <GridItem>
          <Card>
            <CardBody>
              <Stat>
                <StatLabel>
                  <HStack>
                    <Wind size={16} color="#38A169" />
                    <Text>Wind Speed</Text>
                  </HStack>
                </StatLabel>
                <StatNumber color={iotData.wind_speed > 15 ? 'red.500' : 'green.500'}>
                  {iotData.wind_speed.toFixed(1)} km/h
                </StatNumber>
                <StatHelpText>
                  {iotData.wind_speed > 15 ? 'Strong winds' : 'Calm'}
                </StatHelpText>
              </Stat>
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
            {insights.recommendations.map((rec, index) => (
              <HStack key={index} p={3} bg="white" borderRadius="md" border="1px" borderColor="green.200">
                <CheckCircle size={16} color="#38A169" />
                <Text fontSize="sm">{rec}</Text>
              </HStack>
            ))}
          </VStack>
        </CardBody>
      </Card>

      {/* Alerts */}
      {insights.alerts.length > 0 && (
        <Card bg="red.50">
          <CardHeader>
            <HStack>
              <AlertTriangle size={20} color="#E53E3E" />
              <Heading size="md">⚠️ Important Alerts</Heading>
            </HStack>
          </CardHeader>
          <CardBody>
            <VStack spacing={2} align="stretch">
              {insights.alerts.map((alert, index) => (
                <Text key={index} fontSize="sm" color="red.600">
                  • {alert}
                </Text>
              ))}
            </VStack>
          </CardBody>
        </Card>
      )}

      {/* Voice Explanation */}
      <Card>
        <CardBody>
          <HStack justify="space-between">
            <VStack align="start" spacing={1}>
              <Text fontWeight="bold">🎤 Get Voice Explanation</Text>
              <Text fontSize="sm" color="gray.600">
                Listen to AI explanation of your IoT data in Hindi or English
              </Text>
            </VStack>
            <Button
              colorScheme="green"
              leftIcon={<Volume2 size={16} />}
              onClick={generateVoiceExplanation}
              isLoading={isGeneratingVoice}
              loadingText="Generating..."
            >
              Explain IoT Data
            </Button>
          </HStack>
        </CardBody>
      </Card>
    </VStack>
  );
};

export default IoTDataIntelligence;
