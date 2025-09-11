import {
  Box,
  Heading,
  VStack,
  HStack,
  Text as ChakraText,
  Badge,
  useColorModeValue,
  Skeleton,
  Divider,
} from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { apiService } from '../../services/api'
import { format } from 'date-fns'
import { MapPin, Droplets, TrendingUp, AlertCircle } from 'lucide-react'

const RecentActivity = () => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  const { data: fields, isLoading } = useQuery({
    queryKey: ['fields'],
    queryFn: () => apiService.getFields(),
  })

  // Suppress unused variable warning
  console.log('Fields loaded:', fields?.length || 0)

  // Mock recent activity data
  const mockActivities = [
    {
      id: 1,
      type: 'field',
      title: 'Field "North Field" updated',
      description: 'Crop status changed to growing',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      icon: MapPin,
      color: 'blue'
    },
    {
      id: 2,
      type: 'weather',
      title: 'Weather alert',
      description: 'Rain expected in 2 days',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
      icon: Droplets,
      color: 'cyan'
    },
    {
      id: 3,
      type: 'yield',
      title: 'Yield prediction updated',
      description: 'New AI prediction: 4.2 tons/acre',
      timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
      icon: TrendingUp,
      color: 'green'
    },
    {
      id: 4,
      type: 'alert',
      title: 'Irrigation needed',
      description: 'Soil moisture below optimal level',
      timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000), // 8 hours ago
      icon: AlertCircle,
      color: 'orange'
    }
  ]

  return (
    <Box bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
      <Heading size="md" mb={4}>Recent Activity</Heading>
      
      {isLoading ? (
        <VStack spacing={3} align="stretch">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} height="60px" />
          ))}
        </VStack>
      ) : (
        <VStack spacing={3} align="stretch">
          {mockActivities.map((activity, index) => (
            <Box key={activity.id}>
              <HStack spacing={3} align="start">
                <Box
                  p={2}
                  borderRadius="lg"
                  bg={`${activity.color}.50`}
                  color={`${activity.color}.600`}
                >
                  <activity.icon size={16} />
                </Box>
                <VStack align="start" spacing={1} flex="1">
                  <ChakraText fontSize="sm" fontWeight="semibold">
                    {activity.title}
                  </ChakraText>
                  <ChakraText fontSize="xs" color="gray.600">
                    {activity.description}
                  </ChakraText>
                  <ChakraText fontSize="xs" color="gray.500">
                    {format(activity.timestamp, 'MMM d, h:mm a')}
                  </ChakraText>
                </VStack>
                <Badge
                  colorScheme={activity.color}
                  variant="subtle"
                  fontSize="xs"
                >
                  {activity.type}
                </Badge>
              </HStack>
              {index < mockActivities.length - 1 && <Divider mt={3} />}
            </Box>
          ))}
        </VStack>
      )}
    </Box>
  )
}

export default RecentActivity
