import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'

// Components
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import Fields from './pages/Fields'
import AIForecast from './pages/AIForecast'
import Analytics from './pages/Analytics'
import RealTime from './pages/RealTime'
import Settings from './pages/Settings'
import Login from './pages/Login'

// Hooks
import { useAuth } from './hooks/useAuth'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      retry: 2,
    },
  },
})

function AppContent() {
  const { isAuthenticated, user } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  if (!isAuthenticated) {
    return <Login />
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
      
      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header 
          user={user} 
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
        />
        
        {/* Main content area */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-6">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/fields" element={<Fields />} />
            <Route path="/ai-forecast" element={<AIForecast />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/realtime" element={<RealTime />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
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
          }}
        />
      </Router>
    </QueryClientProvider>
  )
}

export default App