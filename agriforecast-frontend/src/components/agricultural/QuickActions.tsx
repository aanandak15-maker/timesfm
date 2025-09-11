import {
  Box,
  Heading,
  Text as ChakraText,
  VStack,
  Button,
  Icon,
  useColorModeValue,
  SimpleGrid,
} from '@chakra-ui/react'
import { Link } from 'react-router-dom'
import { 
  Plus, 
  MapPin, 
  BarChart3, 
  Cloud, 
  TrendingUp, 
  FileText 
} from 'lucide-react'

const QuickActions = () => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  const actions = [
    {
      name: 'Add Field',
      icon: Plus,
      href: '/fields?action=add',
      color: 'green',
      description: 'Create a new field'
    },
    {
      name: 'View Fields',
      icon: MapPin,
      href: '/fields',
      color: 'blue',
      description: 'Manage your fields'
    },
    {
      name: 'Analytics',
      icon: BarChart3,
      href: '/analytics',
      color: 'purple',
      description: 'View detailed analytics'
    },
    {
      name: 'Weather',
      icon: Cloud,
      href: '/weather',
      color: 'cyan',
      description: 'Check weather forecast'
    },
    {
      name: 'Market Data',
      icon: TrendingUp,
      href: '/market',
      color: 'orange',
      description: 'View market prices'
    },
    {
      name: 'Reports',
      icon: FileText,
      href: '/reports',
      color: 'gray',
      description: 'Generate reports'
    }
  ]

  return (
    <Box bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
      <Heading size="md" mb={4}>Quick Actions</Heading>
      
      <SimpleGrid columns={2} spacing={3}>
        {actions.map((action) => (
          <Link key={action.name} to={action.href}>
            <Button
              variant="outline"
              size="sm"
              w="full"
              h="auto"
              p={3}
              flexDirection="column"
              alignItems="center"
              gap={2}
              _hover={{
                bg: `${action.color}.50`,
                borderColor: `${action.color}.300`,
              }}
            >
              <Icon as={action.icon} w={5} h={5} color={`${action.color}.500`} />
              <VStack spacing={1}>
                <ChakraText fontSize="sm" fontWeight="semibold">
                  {action.name}
                </ChakraText>
                <ChakraText fontSize="xs" color="gray.600" textAlign="center">
                  {action.description}
                </ChakraText>
              </VStack>
            </Button>
          </Link>
        ))}
      </SimpleGrid>
    </Box>
  )
}

export default QuickActions
