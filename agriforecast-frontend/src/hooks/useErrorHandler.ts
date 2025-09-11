import { useCallback } from 'react'
import { useToast } from '@chakra-ui/react'

export interface ErrorHandlerOptions {
  showToast?: boolean
  logError?: boolean
  fallbackMessage?: string
}

export const useErrorHandler = () => {
  const toast = useToast()

  const handleError = useCallback((
    error: Error | unknown,
    options: ErrorHandlerOptions = {}
  ) => {
    const {
      showToast = true,
      logError = true,
      fallbackMessage = 'An unexpected error occurred'
    } = options

    // Extract error message
    let errorMessage = fallbackMessage
    if (error instanceof Error) {
      errorMessage = error.message
    } else if (typeof error === 'string') {
      errorMessage = error
    }

    // Log error in development
    if (logError && import.meta.env.DEV) {
      console.error('Error caught by useErrorHandler:', error)
    }

    // Show toast notification
    if (showToast) {
      toast({
        title: 'Error',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    }

    // In production, you might want to send this to an error reporting service
    // Example: Sentry.captureException(error)
  }, [toast])

  return { handleError }
}

export default useErrorHandler
