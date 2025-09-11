import {
  Box,
  VStack,
  HStack,
  Text as ChakraText,
  Icon,
  useDisclosure,
  Drawer,
  DrawerContent,
  DrawerOverlay,
  IconButton,
  useBreakpointValue,
} from '@chakra-ui/react'
import { Link, useLocation } from 'react-router-dom'
import {
  Home,
  MapPin,
  BarChart3,
  Cloud,
  TrendingUp,
  Menu,
  X,
} from 'lucide-react'

const navigationItems = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Fields', href: '/fields', icon: MapPin },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Weather', href: '/weather', icon: Cloud },
  { name: 'Market', href: '/market', icon: TrendingUp },
]

const Sidebar = () => {
  const { isOpen, onOpen, onClose } = useDisclosure()
  const location = useLocation()
  const isMobile = useBreakpointValue({ base: true, lg: false })

  const sidebarContent = (
    <Box
      w="280px"
      h="full"
      bg="white"
      borderRight="1px"
      borderColor="gray.200"
      p={6}
    >
      {/* Logo */}
      <HStack mb={8}>
        <Box
          w={8}
          h={8}
          bg="brand.500"
          borderRadius="lg"
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <ChakraText color="white" fontWeight="bold" fontSize="lg">
            🌾
          </ChakraText>
        </Box>
        <ChakraText fontSize="xl" fontWeight="bold" color="gray.800">
          AgriForecast
        </ChakraText>
      </HStack>

      {/* Navigation */}
      <VStack spacing={2} align="stretch">
        {navigationItems.map((item) => {
          const isActive = location.pathname === item.href
          return (
            <Link key={item.name} to={item.href}>
              <HStack
                p={3}
                borderRadius="lg"
                bg={isActive ? 'brand.50' : 'transparent'}
                color={isActive ? 'brand.600' : 'gray.600'}
                _hover={{
                  bg: isActive ? 'brand.50' : 'gray.50',
                }}
                transition="all 0.2s"
              >
                <Icon as={item.icon} w={5} h={5} />
                <ChakraText fontWeight={isActive ? 'semibold' : 'medium'}>
                  {item.name}
                </ChakraText>
              </HStack>
            </Link>
          )
        })}
      </VStack>
    </Box>
  )

  if (isMobile) {
    return (
      <>
        <IconButton
          aria-label="Open menu"
          icon={<Menu />}
          onClick={onOpen}
          position="fixed"
          top={4}
          left={4}
          zIndex={1000}
          bg="white"
          shadow="md"
        />
        <Drawer isOpen={isOpen} onClose={onClose} placement="left">
          <DrawerOverlay />
          <DrawerContent>
            <Box position="relative">
              <IconButton
                aria-label="Close menu"
                icon={<X />}
                onClick={onClose}
                position="absolute"
                top={4}
                right={4}
                zIndex={1000}
              />
              {sidebarContent}
            </Box>
          </DrawerContent>
        </Drawer>
      </>
    )
  }

  return sidebarContent
}

export default Sidebar
