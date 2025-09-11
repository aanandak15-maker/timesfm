import {
  Box,
  Heading,
  Text as ChakraText,
  VStack,
  Input,
  Button,
  FormControl,
  FormLabel,
  useColorModeValue,
  Card,
  CardBody,
} from '@chakra-ui/react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  })
  const navigate = useNavigate()
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    // For demo purposes, accept any credentials
    localStorage.setItem('auth_token', 'demo-token')
    navigate('/')
  }

  return (
    <Box minH="100vh" bg="gray.50" display="flex" alignItems="center" justifyContent="center">
      <Card maxW="md" w="full" bg={bg} border="1px" borderColor={borderColor}>
        <CardBody p={8}>
          <VStack spacing={6} align="stretch">
            {/* Logo */}
            <VStack spacing={2}>
              <Box
                w={16}
                h={16}
                bg="brand.500"
                borderRadius="xl"
                display="flex"
                alignItems="center"
                justifyContent="center"
              >
                <ChakraText color="white" fontWeight="bold" fontSize="2xl">
                  🌾
                </ChakraText>
              </Box>
              <Heading size="lg">AgriForecast.ai</Heading>
              <ChakraText color="gray.600" textAlign="center">
                AI-Powered Agricultural Intelligence Platform
              </ChakraText>
            </VStack>

            {/* Login Form */}
            <form onSubmit={handleLogin}>
              <VStack spacing={4} align="stretch">
                <FormControl>
                  <FormLabel>Username</FormLabel>
                  <Input
                    type="text"
                    value={credentials.username}
                    onChange={(e) => setCredentials(prev => ({ ...prev, username: e.target.value }))}
                    placeholder="Enter your username"
                  />
                </FormControl>

                <FormControl>
                  <FormLabel>Password</FormLabel>
                  <Input
                    type="password"
                    value={credentials.password}
                    onChange={(e) => setCredentials(prev => ({ ...prev, password: e.target.value }))}
                    placeholder="Enter your password"
                  />
                </FormControl>

                <Button type="submit" colorScheme="green" size="lg">
                  Sign In
                </Button>
              </VStack>
            </form>

            {/* Demo Info */}
            <Box p={4} bg="blue.50" borderRadius="lg">
              <ChakraText fontSize="sm" color="blue.700" textAlign="center">
                <strong>Demo Mode:</strong> Enter any username and password to continue
              </ChakraText>
            </Box>
          </VStack>
        </CardBody>
      </Card>
    </Box>
  )
}

export default Login
