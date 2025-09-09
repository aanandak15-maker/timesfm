import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import { useEffect, useState } from 'react'

// Layout Components
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import MobileNav from './components/MobileNav'

// Pages
import Dashboard from './pages/Dashboard'
import Farms from './pages/Farms'
import Fields from './pages/Fields'
import AIForecast from './pages/AIForecast'
import Analytics from './pages/Analytics'
import RealTime from './pages/RealTime'
import Weather from './pages/Weather'
import Market from './pages/Market'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import Login from './pages/Login'

// Hooks & Utils
import { useAuth } from './hooks/useAuth'
import { AuthProvider } from './contexts/AuthContext'
import { apiService } from './lib/api'

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      retry: (failureCount, error: any) => {
        if (error?.response?.status === 401) return false
        return failureCount < 2
      },
    },
    mutations: {
      retry: 1,
    },
  },
})

function AppContent() {
  const { user, isAuthenticated, isLoading } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [isMobile, setIsMobile] = useState(false)
  const [backendConnected, setBackendConnected] = useState(false)

  // Check mobile screen
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Check backend connection
  useEffect(() => {
    const checkBackend = async () => {
      try {
        await apiService.healthCheck()
        setBackendConnected(true)
      } catch (error) {
        setBackendConnected(false)
        console.warn('Backend not available - using demo mode')
      }
    }
    
    checkBackend()
    const interval = setInterval(checkBackend, 30000) // Check every 30s
    return () => clearInterval(interval)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="aura-loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading AgriForecast.ai...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Login />
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar - Desktop */}
      {!isMobile && (
        <Sidebar 
          open={sidebarOpen} 
          setOpen={setSidebarOpen}
          backendConnected={backendConnected}
        />
      )}
      
      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header 
          user={user} 
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
          backendConnected={backendConnected}
          isMobile={isMobile}
        />
        
        {/* Main content area */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-4 md:p-6">
          <div className="max-w-7xl mx-auto">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/farms" element={<Farms />} />
              <Route path="/fields" element={<Fields />} />
              <Route path="/ai-forecast" element={<AIForecast />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/realtime" element={<RealTime />} />
              <Route path="/weather" element={<Weather />} />
              <Route path="/market" element={<Market />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </div>
        </main>
        
        {/* Mobile Navigation */}
        {isMobile && <MobileNav />}
      </div>
      
      {/* Connection Status Toast */}
      {!backendConnected && (
        <div className="fixed top-4 right-4 z-50 bg-yellow-100 border border-yellow-400 text-yellow-800 px-4 py-2 rounded-lg shadow-lg">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium">Demo Mode - Backend Offline</span>
          </div>
        </div>
      )}
    </div>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <AppContent />
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#f9fafb',
                color: '#374151',
                border: '1px solid #d1d5db',
              },
              success: {
                style: {
                  background: '#f0fdf4',
                  color: '#166534',
                  border: '1px solid #bbf7d0',
                },
              },
              error: {
                style: {
                  background: '#fef2f2',
                  color: '#dc2626',
                  border: '1px solid #fecaca',
                },
              },
            }}
          />
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App