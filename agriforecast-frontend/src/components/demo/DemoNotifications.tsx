// Demo Notifications for Hackathon Presentation
// Shows realistic agricultural alerts and updates

import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Icon,
  useToast,
  Button,
  Collapse,
  useDisclosure
} from '@chakra-ui/react';
import {
  Bell,
  AlertTriangle,
  CheckCircle,
  Info,
  Leaf,
  Droplets,
  Thermometer,
  DollarSign,
  TrendingUp,
  Wifi,
  Battery
} from 'lucide-react';
import demoService from '../../services/demoService';

interface DemoNotification {
  id: string;
  type: 'success' | 'warning' | 'info' | 'error';
  title: string;
  message: string;
  timestamp: string;
  icon: any;
  color: string;
}

const DemoNotifications: React.FC = () => {
  const [notifications, setNotifications] = useState<DemoNotification[]>([]);
  const [isRunning, setIsRunning] = useState(true);
  const toast = useToast();
  const { isOpen, onToggle } = useDisclosure();

  const notificationTypes = [
    {
      type: 'success' as const,
      icon: CheckCircle,
      color: 'green.500',
      templates: [
        { title: 'Irrigation Complete', message: 'Field 1 irrigation completed successfully. Soil moisture now optimal.' },
        { title: 'Harvest Ready', message: 'Field 2 maize is ready for harvest. Estimated yield: 3.8 tons/acre.' },
        { title: 'Fertilizer Applied', message: 'Nitrogen fertilizer applied to Field 3. Growth rate improved by 15%.' },
        { title: 'Pest Control Success', message: 'Integrated pest management reduced pest damage by 40% this season.' }
      ]
    },
    {
      type: 'warning' as const,
      icon: AlertTriangle,
      color: 'orange.500',
      templates: [
        { title: 'Soil Moisture Low', message: 'Field 1 soil moisture is below optimal level (35%). Consider irrigation.' },
        { title: 'Temperature Alert', message: 'High temperature detected (38°C). Monitor for heat stress in crops.' },
        { title: 'pH Level Warning', message: 'Field 2 soil pH is 5.8. Consider lime application to increase pH.' },
        { title: 'Battery Low', message: 'IoT sensor battery at 20%. Schedule maintenance visit.' }
      ]
    },
    {
      type: 'info' as const,
      icon: Info,
      color: 'blue.500',
      templates: [
        { title: 'Weather Update', message: 'Rain expected in 2 hours. Irrigation system will pause automatically.' },
        { title: 'Market Price Alert', message: 'Rice prices increased by 2.3% today. Consider selling timing.' },
        { title: 'AI Insight Available', message: 'New AI recommendation: Optimize irrigation schedule for 15% water savings.' },
        { title: 'Data Sync Complete', message: 'All sensor data synchronized successfully. 150 new data points added.' }
      ]
    }
  ];

  const generateNotification = (): DemoNotification => {
    const typeConfig = notificationTypes[Math.floor(Math.random() * notificationTypes.length)];
    const template = typeConfig.templates[Math.floor(Math.random() * typeConfig.templates.length)];
    
    return {
      id: `notification-${Date.now()}-${Math.random()}`,
      type: typeConfig.type,
      title: template.title,
      message: template.message,
      timestamp: new Date().toISOString(),
      icon: typeConfig.icon,
      color: typeConfig.color
    };
  };

  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(() => {
      const newNotification = generateNotification();
      setNotifications(prev => [newNotification, ...prev.slice(0, 9)]); // Keep last 10
      
      // Show toast notification
      toast({
        title: newNotification.title,
        description: newNotification.message,
        status: newNotification.type,
        duration: 4000,
        isClosable: true,
        position: 'top-right'
      });
    }, 15000); // Generate notification every 15 seconds

    return () => clearInterval(interval);
  }, [isRunning, toast]);

  const clearNotifications = () => {
    setNotifications([]);
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'success': return CheckCircle;
      case 'warning': return AlertTriangle;
      case 'info': return Info;
      default: return Bell;
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'success': return 'green.500';
      case 'warning': return 'orange.500';
      case 'info': return 'blue.500';
      default: return 'gray.500';
    }
  };

  return (
    <Box position="fixed" top={4} right={4} zIndex={1000} maxW="400px">
      <VStack spacing={2} align="stretch">
        {/* Notification Toggle Button */}
        <Button
          size="sm"
          colorScheme="blue"
          variant="outline"
          onClick={onToggle}
          leftIcon={<Bell />}
        >
          Notifications ({notifications.length})
        </Button>

        {/* Notifications Panel */}
        <Collapse in={isOpen} animateOpacity>
          <Box
            bg="white"
            border="1px solid"
            borderColor="gray.200"
            borderRadius="md"
            shadow="lg"
            maxH="400px"
            overflowY="auto"
          >
            <VStack spacing={0} align="stretch">
              {/* Header */}
              <Box p={3} borderBottom="1px solid" borderColor="gray.200">
                <HStack justify="space-between">
                  <Text fontWeight="bold" fontSize="sm">
                    Live Notifications
                  </Text>
                  <HStack spacing={2}>
                    <Button
                      size="xs"
                      colorScheme={isRunning ? "red" : "green"}
                      onClick={() => setIsRunning(!isRunning)}
                    >
                      {isRunning ? "Stop" : "Start"}
                    </Button>
                    <Button size="xs" variant="outline" onClick={clearNotifications}>
                      Clear
                    </Button>
                  </HStack>
                </HStack>
              </Box>

              {/* Notifications List */}
              {notifications.length === 0 ? (
                <Box p={4} textAlign="center">
                  <Text color="gray.500" fontSize="sm">
                    No notifications yet. They will appear here as the system runs.
                  </Text>
                </Box>
              ) : (
                notifications.map((notification) => (
                  <Box
                    key={notification.id}
                    p={3}
                    borderBottom="1px solid"
                    borderColor="gray.100"
                    _last={{ borderBottom: "none" }}
                  >
                    <VStack spacing={2} align="stretch">
                      <HStack>
                        <Icon
                          as={getNotificationIcon(notification.type)}
                          color={getNotificationColor(notification.type)}
                          boxSize={4}
                        />
                        <Text fontWeight="bold" fontSize="sm" flex={1}>
                          {notification.title}
                        </Text>
                        <Badge
                          size="sm"
                          colorScheme={
                            notification.type === 'success' ? 'green' :
                            notification.type === 'warning' ? 'orange' :
                            notification.type === 'info' ? 'blue' : 'gray'
                          }
                        >
                          {notification.type}
                        </Badge>
                      </HStack>
                      <Text fontSize="xs" color="gray.600">
                        {notification.message}
                      </Text>
                      <Text fontSize="xs" color="gray.400">
                        {new Date(notification.timestamp).toLocaleTimeString()}
                      </Text>
                    </VStack>
                  </Box>
                ))
              )}
            </VStack>
          </Box>
        </Collapse>
      </VStack>
    </Box>
  );
};

export default DemoNotifications;
