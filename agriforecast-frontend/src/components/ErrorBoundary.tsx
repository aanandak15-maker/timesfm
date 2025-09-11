import React, { Component, type ErrorInfo, type ReactNode } from 'react'
import {
  Box,
  VStack,
  Heading,
  Text,
  Button,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Code,
  useColorModeValue,
} from '@chakra-ui/react'
import { RefreshCw, Bug, Home } from 'lucide-react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    }
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({
      error,
      errorInfo,
    })

    // Log error to console in development
    if (import.meta.env.DEV) {
      console.error('ErrorBoundary caught an error:', error, errorInfo)
    }

    // Call custom error handler if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo)
    }

    // In production, you might want to send this to an error reporting service
    // Example: Sentry.captureException(error, { extra: errorInfo })
  }

  handleRetry = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    })
  }

  handleGoHome = () => {
    window.location.href = '/'
  }

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback
      }

      return <ErrorFallback 
        error={this.state.error} 
        errorInfo={this.state.errorInfo}
        onRetry={this.handleRetry}
        onGoHome={this.handleGoHome}
      />
    }

    return this.props.children
  }
}

interface ErrorFallbackProps {
  error: Error | null
  errorInfo: ErrorInfo | null
  onRetry: () => void
  onGoHome: () => void
}

const ErrorFallback: React.FC<ErrorFallbackProps> = ({ 
  error, 
  errorInfo, 
  onRetry, 
  onGoHome 
}) => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('red.200', 'red.800')

  return (
    <Box minH="100vh" bg="gray.50" display="flex" alignItems="center" justifyContent="center" p={4}>
      <Box maxW="600px" w="full" bg={bg} borderRadius="xl" border="1px" borderColor={borderColor} p={8}>
        <VStack spacing={6} align="stretch">
          <VStack spacing={4} textAlign="center">
            <Box p={4} bg="red.100" borderRadius="full" display="inline-flex">
              <Bug size={48} color="#e53e3e" />
            </Box>
            <Heading size="lg" color="red.600">
              Oops! Something went wrong
            </Heading>
            <Text color="gray.600">
              We encountered an unexpected error. Don't worry, our team has been notified.
            </Text>
          </VStack>

          <Alert status="error" borderRadius="lg">
            <AlertIcon />
            <Box>
              <AlertTitle>Error Details</AlertTitle>
              <AlertDescription>
                {error?.message || 'An unknown error occurred'}
              </AlertDescription>
            </Box>
          </Alert>

          {import.meta.env.DEV && errorInfo && (
            <Box>
              <Text fontSize="sm" fontWeight="semibold" mb={2} color="gray.700">
                Stack Trace:
              </Text>
              <Code 
                p={4} 
                borderRadius="md" 
                bg="gray.100" 
                fontSize="xs" 
                whiteSpace="pre-wrap"
                overflow="auto"
                maxH="200px"
              >
                {error?.stack}
              </Code>
            </Box>
          )}

          <VStack spacing={3}>
            <Button
              leftIcon={<RefreshCw />}
              colorScheme="blue"
              onClick={onRetry}
              size="lg"
              w="full"
            >
              Try Again
            </Button>
            <Button
              leftIcon={<Home />}
              variant="outline"
              onClick={onGoHome}
              size="lg"
              w="full"
            >
              Go to Dashboard
            </Button>
          </VStack>

          <Text fontSize="sm" color="gray.500" textAlign="center">
            If this problem persists, please contact support.
          </Text>
        </VStack>
      </Box>
    </Box>
  )
}

export default ErrorBoundary
