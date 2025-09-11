import { extendTheme } from '@chakra-ui/react'

// Agricultural theme colors
const colors = {
  brand: {
    50: '#f0f9f0',
    100: '#dcf2dc',
    200: '#bce5bc',
    300: '#8dd18d',
    400: '#5bb85b',
    500: '#3a9d3a', // Primary green
    600: '#2d7d2d',
    700: '#256325',
    800: '#215021',
    900: '#1e421e',
  },
  earth: {
    50: '#faf7f0',
    100: '#f3ede0',
    200: '#e6d9c1',
    300: '#d4c19e',
    400: '#c2a97b',
    500: '#b08f58', // Earth brown
    600: '#9a7a4a',
    700: '#7d623c',
    800: '#604a2e',
    900: '#433220',
  },
  sky: {
    50: '#f0f9ff',
    100: '#e0f2fe',
    200: '#bae6fd',
    300: '#7dd3fc',
    400: '#38bdf8',
    500: '#0ea5e9', // Sky blue
    600: '#0284c7',
    700: '#0369a1',
    800: '#075985',
    900: '#0c4a6e',
  },
  harvest: {
    50: '#fffbeb',
    100: '#fef3c7',
    200: '#fde68a',
    300: '#fcd34d',
    400: '#fbbf24',
    500: '#f59e0b', // Harvest gold
    600: '#d97706',
    700: '#b45309',
    800: '#92400e',
    900: '#78350f',
  }
}

const fonts = {
  heading: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  body: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
}

const components = {
  Button: {
    baseStyle: {
      fontWeight: 'semibold',
      borderRadius: 'lg',
    },
    variants: {
      solid: {
        bg: 'brand.500',
        color: 'white',
        _hover: {
          bg: 'brand.600',
        },
      },
      outline: {
        borderColor: 'brand.500',
        color: 'brand.500',
        _hover: {
          bg: 'brand.50',
        },
      },
    },
  },
  Card: {
    baseStyle: {
      container: {
        borderRadius: 'xl',
        boxShadow: 'sm',
        border: '1px solid',
        borderColor: 'gray.100',
      },
    },
  },
}

const theme = extendTheme({
  colors,
  fonts,
  components,
  config: {
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
})

export default theme

