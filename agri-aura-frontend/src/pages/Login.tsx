import { useState } from 'react'
import { SparklesIcon } from '@heroicons/react/24/outline'
import { useAuth } from '../hooks/useAuth'
import toast from 'react-hot-toast'

export default function Login() {
  const [credentials, setCredentials] = useState({ username: 'anand', password: 'password123' })
  const [isLoading, setIsLoading] = useState(false)
  const { login } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      await login(credentials)
      toast.success('Welcome to AgriForecast.ai!')
    } catch (error) {
      toast.error('Login failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-field-50 to-crop-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="aura-card">
          <div className="aura-card-content">
            {/* Logo */}
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-r from-field-500 to-crop-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
                <SparklesIcon className="h-8 w-8 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">AgriForecast.ai</h1>
              <p className="text-gray-600">AI-Powered Agricultural Intelligence</p>
            </div>

            {/* Login Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="aura-label">Username</label>
                <input
                  type="text"
                  value={credentials.username}
                  onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                  className="aura-input"
                  placeholder="Enter your username"
                  required
                />
              </div>

              <div>
                <label className="aura-label">Password</label>
                <input
                  type="password"
                  value={credentials.password}
                  onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                  className="aura-input"
                  placeholder="Enter your password"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="aura-btn-primary w-full"
              >
                {isLoading ? (
                  <div className="aura-loading-spinner w-5 h-5"></div>
                ) : (
                  'Sign In'
                )}
              </button>
            </form>

            {/* Demo credentials */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-sm text-blue-800 font-medium mb-1">Demo Credentials:</p>
              <p className="text-sm text-blue-700">Username: anand</p>
              <p className="text-sm text-blue-700">Password: password123</p>
            </div>

            {/* Features */}
            <div className="mt-6 space-y-2">
              <p className="text-sm text-gray-600 font-medium">Platform Features:</p>
              <div className="space-y-1">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <div className="w-1.5 h-1.5 bg-field-500 rounded-full"></div>
                  AI-powered yield predictions
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <div className="w-1.5 h-1.5 bg-crop-500 rounded-full"></div>
                  Real-time weather monitoring
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                  Market intelligence insights
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
