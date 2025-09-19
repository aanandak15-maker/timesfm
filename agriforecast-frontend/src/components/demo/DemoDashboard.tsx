// Demo Dashboard for Hackathon Presentation
// Showcases all features with realistic data simulation

import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardBody,
  Text,
  Heading,
  Badge,
  Progress,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  VStack,
  HStack,
  Icon,
  Button,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  useColorModeValue,
  Flex,
  Spacer,
  Divider
} from '@chakra-ui/react';
import {
  Tractor,
  Sprout,
  Thermometer,
  Droplets,
  TrendingUp,
  DollarSign,
  CloudRain,
  Leaf,
  Wifi,
  Battery,
  AlertTriangle,
  CheckCircle,
  Info
} from 'lucide-react';
import demoService from '../../services/demoService';

interface DemoDashboardProps {
  onNavigate?: (path: string) => void;
}

const DemoDashboard: React.FC<DemoDashboardProps> = ({ onNavigate }) => {
  const [stats, setStats] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [aiInsights, setAIInsights] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  useEffect(() => {
    const loadDemoData = async () => {
      try {
        const [statsData, alertsData, insightsData] = await Promise.all([
          demoService.getDemoStats(),
          demoService.getAlerts(),
          demoService.getAIInsights()
        ]);
        
        setStats(statsData);
        setAlerts(alertsData);
        setAIInsights(insightsData);
        setIsLoading(false);
      } catch (error) {
        console.error('Error loading demo data:', error);
        setIsLoading(false);
      }
    };

    loadDemoData();
  }, []);

  if (isLoading) {
    return (
      <Box p={6}>
        <Text>Loading demo data...</Text>
      </Box>
    );
  }

  return (
    <Box p={6} maxW="1400px" mx="auto">
      {/* Header */}
      <VStack spacing={4} align="stretch" mb={8}>
        <Flex align="center" justify="space-between">
          <VStack align="start" spacing={2}>
            <Heading size="lg" color="green.600">
              🌾 AgriForecast Demo Dashboard
            </Heading>
            <Text color="gray.600" fontSize="lg">
              Real-time agricultural intelligence for small and marginal farmers
            </Text>
          </VStack>
          <Badge colorScheme="green" fontSize="md" px={3} py={1}>
            DEMO MODE
          </Badge>
        </Flex>
        
        <Alert status="info" borderRadius="md">
          <AlertIcon />
          <Box>
            <AlertTitle>Hackathon Demo Mode!</AlertTitle>
            <AlertDescription>
              This dashboard showcases real-time agricultural data simulation with IoT sensors, 
              AI predictions, and market intelligence for small farmers in India.
            </AlertDescription>
          </Box>
        </Alert>
      </VStack>

      {/* Key Statistics */}
      <Grid templateColumns={{ base: "1fr", md: "repeat(2, 1fr)", lg: "repeat(4, 1fr)" }} gap={6} mb={8}>
        <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
          <CardBody>
            <Stat>
              <StatLabel>Total Fields</StatLabel>
              <StatNumber color="green.600">{stats?.totalFields || 3}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                3 active fields
              </StatHelpText>
            </Stat>
          </CardBody>
        </Card>

        <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
          <CardBody>
            <Stat>
              <StatLabel>IoT Sensors</StatLabel>
              <StatNumber color="blue.600">{stats?.activeSensors || 36}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                12 sensors per field
              </StatHelpText>
            </Stat>
          </CardBody>
        </Card>

        <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
          <CardBody>
            <Stat>
              <StatLabel>Data Points</StatLabel>
              <StatNumber color="purple.600">{stats?.dataPoints || 150}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                Real-time updates
              </StatHelpText>
            </Stat>
          </CardBody>
        </Card>

        <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
          <CardBody>
            <Stat>
              <StatLabel>System Uptime</StatLabel>
              <StatNumber color="green.600">{stats?.uptime || "99.8%"}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                Excellent reliability
              </StatHelpText>
            </Stat>
          </CardBody>
        </Card>
      </Grid>

      {/* Main Content Grid */}
      <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={8} mb={8}>
        {/* Left Column - Main Features */}
        <VStack spacing={6} align="stretch">
          {/* IoT Sensor Status */}
          <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
            <CardBody>
              <VStack spacing={4} align="stretch">
                <HStack>
                  <Icon as={Wifi} color="green.500" boxSize={5} />
                  <Heading size="md">IoT Sensor Network</Heading>
                  <Spacer />
                  <Badge colorScheme="green">All Online</Badge>
                </HStack>
                
                <Grid templateColumns="repeat(3, 1fr)" gap={4}>
                  <VStack spacing={2}>
                    <Icon as={Thermometer} color="red.500" boxSize={6} />
                    <Text fontSize="sm" fontWeight="bold">Temperature</Text>
                    <Text fontSize="lg" color="red.600">32°C</Text>
                    <Progress value={80} colorScheme="red" size="sm" />
                  </VStack>
                  
                  <VStack spacing={2}>
                    <Icon as={Droplets} color="blue.500" boxSize={6} />
                    <Text fontSize="sm" fontWeight="bold">Soil Moisture</Text>
                    <Text fontSize="lg" color="blue.600">45%</Text>
                    <Progress value={45} colorScheme="blue" size="sm" />
                  </VStack>
                  
                  <VStack spacing={2}>
                    <Icon as={Leaf} color="green.500" boxSize={6} />
                    <Text fontSize="sm" fontWeight="bold">pH Level</Text>
                    <Text fontSize="lg" color="green.600">6.8</Text>
                    <Progress value={85} colorScheme="green" size="sm" />
                  </VStack>
                </Grid>
              </VStack>
            </CardBody>
          </Card>

          {/* AI Insights */}
          <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
            <CardBody>
              <VStack spacing={4} align="stretch">
                <HStack>
                  <Icon as={TrendingUp} color="purple.500" boxSize={5} />
                  <Heading size="md">AI Agricultural Insights</Heading>
                  <Spacer />
                  <Badge colorScheme="purple">Powered by Gemini 2.0</Badge>
                </HStack>
                
                {aiInsights.slice(0, 3).map((insight, index) => (
                  <Box key={insight.id} p={4} bg="gray.50" borderRadius="md" borderLeft="4px" borderLeftColor="purple.500">
                    <VStack spacing={2} align="stretch">
                      <HStack>
                        <Badge colorScheme={insight.type === 'optimization' ? 'green' : insight.type === 'prediction' ? 'blue' : 'orange'}>
                          {insight.type}
                        </Badge>
                        <Text fontSize="sm" color="gray.600">Confidence: {insight.confidence}%</Text>
                      </HStack>
                      <Text fontWeight="bold">{insight.title}</Text>
                      <Text fontSize="sm" color="gray.700">{insight.description}</Text>
                      <Text fontSize="sm" color="green.600" fontWeight="bold">
                        💰 Potential Savings: ₹{insight.cost_savings?.toLocaleString()}
                      </Text>
                    </VStack>
                  </Box>
                ))}
              </VStack>
            </CardBody>
          </Card>
        </VStack>

        {/* Right Column - Alerts & Quick Actions */}
        <VStack spacing={6} align="stretch">
          {/* Alerts */}
          <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
            <CardBody>
              <VStack spacing={4} align="stretch">
                <HStack>
                  <Icon as={AlertTriangle} color="orange.500" boxSize={5} />
                  <Heading size="md">Field Alerts</Heading>
                  <Spacer />
                  <Badge colorScheme="orange">{alerts.length}</Badge>
                </HStack>
                
                {alerts.map((alert) => (
                  <Alert key={alert.id} status={alert.type} borderRadius="md">
                    <AlertIcon />
                    <Box>
                      <AlertTitle fontSize="sm">{alert.title}</AlertTitle>
                      <AlertDescription fontSize="xs">{alert.message}</AlertDescription>
                    </Box>
                  </Alert>
                ))}
              </VStack>
            </CardBody>
          </Card>

          {/* Quick Actions */}
          <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
            <CardBody>
              <VStack spacing={4} align="stretch">
                <Heading size="md">Quick Actions</Heading>
                
                <VStack spacing={3} align="stretch">
                  <Button 
                    leftIcon={<Tractor />} 
                    colorScheme="green" 
                    variant="outline"
                    onClick={() => onNavigate?.('/farms')}
                  >
                    Manage Farms
                  </Button>
                  
                  <Button 
                    leftIcon={<Sprout />} 
                    colorScheme="blue" 
                    variant="outline"
                    onClick={() => onNavigate?.('/fields')}
                  >
                    View Fields
                  </Button>
                  
                  <Button 
                    leftIcon={<TrendingUp />} 
                    colorScheme="purple" 
                    variant="outline"
                    onClick={() => onNavigate?.('/iot')}
                  >
                    IoT Dashboard
                  </Button>
                  
                  <Button 
                    leftIcon={<DollarSign />} 
                    colorScheme="orange" 
                    variant="outline"
                    onClick={() => onNavigate?.('/market')}
                  >
                    Market Intelligence
                  </Button>
                </VStack>
              </VStack>
            </CardBody>
          </Card>

          {/* System Status */}
          <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
            <CardBody>
              <VStack spacing={4} align="stretch">
                <Heading size="md">System Status</Heading>
                
                <VStack spacing={3} align="stretch">
                  <HStack justify="space-between">
                    <HStack>
                      <Icon as={Wifi} color="green.500" />
                      <Text fontSize="sm">Network</Text>
                    </HStack>
                    <Badge colorScheme="green">Online</Badge>
                  </HStack>
                  
                  <HStack justify="space-between">
                    <HStack>
                      <Icon as={Battery} color="green.500" />
                      <Text fontSize="sm">Battery</Text>
                    </HStack>
                    <Badge colorScheme="green">85%</Badge>
                  </HStack>
                  
                  <HStack justify="space-between">
                    <HStack>
                      <Icon as={CloudRain} color="blue.500" />
                      <Text fontSize="sm">Weather API</Text>
                    </HStack>
                    <Badge colorScheme="green">Active</Badge>
                  </HStack>
                  
                  <HStack justify="space-between">
                    <HStack>
                      <Icon as={TrendingUp} color="purple.500" />
                      <Text fontSize="sm">AI Engine</Text>
                    </HStack>
                    <Badge colorScheme="green">Running</Badge>
                  </HStack>
                </VStack>
              </VStack>
            </CardBody>
          </Card>
        </VStack>
      </Grid>

      {/* Bottom Section - Market Data */}
      <Card bg={cardBg} borderColor={borderColor} borderWidth="1px">
        <CardBody>
          <VStack spacing={4} align="stretch">
            <HStack>
              <Icon as={DollarSign} color="green.500" boxSize={5} />
              <Heading size="md">Live Market Prices</Heading>
              <Spacer />
              <Text fontSize="sm" color="gray.600">Updated 2 minutes ago</Text>
            </HStack>
            
            <Grid templateColumns={{ base: "1fr", md: "repeat(3, 1fr)" }} gap={6}>
              <Box p={4} bg="green.50" borderRadius="md" borderLeft="4px" borderLeftColor="green.500">
                <VStack spacing={2} align="stretch">
                  <Text fontWeight="bold" color="green.700">Rice</Text>
                  <Text fontSize="2xl" color="green.600">₹2,850</Text>
                  <HStack>
                    <Text fontSize="sm" color="green.600">+₹45 (+1.6%)</Text>
                    <Icon as={TrendingUp} color="green.500" />
                  </HStack>
                </VStack>
              </Box>
              
              <Box p={4} bg="blue.50" borderRadius="md" borderLeft="4px" borderLeftColor="blue.500">
                <VStack spacing={2} align="stretch">
                  <Text fontWeight="bold" color="blue.700">Maize</Text>
                  <Text fontSize="2xl" color="blue.600">₹1,950</Text>
                  <HStack>
                    <Text fontSize="sm" color="red.600">-₹25 (-1.3%)</Text>
                    <Icon as={TrendingUp} color="red.500" />
                  </HStack>
                </VStack>
              </Box>
              
              <Box p={4} bg="purple.50" borderRadius="md" borderLeft="4px" borderLeftColor="purple.500">
                <VStack spacing={2} align="stretch">
                  <Text fontWeight="bold" color="purple.700">Cotton</Text>
                  <Text fontSize="2xl" color="purple.600">₹7,200</Text>
                  <HStack>
                    <Text fontSize="sm" color="green.600">+₹120 (+1.7%)</Text>
                    <Icon as={TrendingUp} color="green.500" />
                  </HStack>
                </VStack>
              </Box>
            </Grid>
          </VStack>
        </CardBody>
      </Card>
    </Box>
  );
};

export default DemoDashboard;
