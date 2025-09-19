import { Routes, Route } from 'react-router-dom'
import { Box, ChakraProvider } from '@chakra-ui/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import ErrorBoundary from './components/ErrorBoundary'
import Layout from './components/layout/Layout'
import Dashboard from './pages/dashboard/Dashboard'
import DemoDashboard from './components/demo/DemoDashboard'
import FarmerFriendlyIoT from './pages/iot/FarmerFriendlyIoT'
import EnhancedIoT from './pages/iot/EnhancedIoT'
import Fields from './pages/fields/Fields'
import Farms from './pages/farms/Farms'
import ProductionFieldMapper from './components/mapping/ProductionFieldMapper'
import GEESatelliteFieldMapper from './components/mapping/GEESatelliteFieldMapper'
import SimpleFieldMapper from './components/mapping/SimpleFieldMapper'
import Analytics from './pages/analytics/Analytics'
import Weather from './pages/weather/Weather'
import Market from './pages/market/Market'
import Login from './pages/auth/Login'
import theme from './theme/index'
import './utils/testDemo' // Test demo data on app start
import './utils/testFarmsData' // Test farms and fields data structure

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ChakraProvider theme={theme}>
          <Box minH="100vh" bg="gray.50">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<Layout />}>
                <Route index element={<DemoDashboard />} />
                       <Route path="farms" element={<Farms />} />
                       <Route path="mapping" element={<SimpleFieldMapper />} />
                       <Route path="advanced-mapping" element={<ProductionFieldMapper />} />
                       <Route path="gee-mapping" element={<GEESatelliteFieldMapper />} />
                <Route path="iot" element={<EnhancedIoT />} />
                <Route path="simple-iot" element={<FarmerFriendlyIoT />} />
                <Route path="fields" element={<Fields />} />
                <Route path="analytics" element={<Analytics />} />
                <Route path="weather" element={<Weather />} />
                <Route path="market" element={<Market />} />
              </Route>
            </Routes>
          </Box>
          {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
        </ChakraProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  )
}

export default App