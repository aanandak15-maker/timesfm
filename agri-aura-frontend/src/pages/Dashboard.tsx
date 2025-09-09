import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { 
  HomeIcon, 
  ChartBarIcon, 
  CloudIcon, 
  CurrencyDollarIcon,
  SparklesIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  MapPinIcon
} from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'

import { apiService, type Farm, type Field } from '../lib/api'
import { useAuth } from '../hooks/useAuth'
import QuickActions from '../components/QuickActions'
import WeatherWidget from '../components/WeatherWidget'
import AIInsights from '../components/AIInsights'

interface DashboardStats {
  totalFarms: number
  totalFields: number
  totalAcres: number
  averageYield: number
  riskScore: number
  marketTrend: 'up' | 'down' | 'stable'
}

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState<DashboardStats>({
    totalFarms: 0,
    totalFields: 0,
    totalAcres: 0,
    averageYield: 0,
    riskScore: 0,
    marketTrend: 'stable'
  })

  // Fetch farms
  const { data: farms = [], isLoading: farmsLoading, error: farmsError } = useQuery({
    queryKey: ['farms'],
    queryFn: apiService.getFarms,
    onError: (error) => {
      console.warn('Farms API error:', error)
    }
  })

  // Fetch all fields
  const { data: fields = [], isLoading: fieldsLoading } = useQuery({
    queryKey: ['fields'],
    queryFn: () => apiService.getFields(),
    onError: (error) => {
      console.warn('Fields API error:', error)
    }
  })

  // Calculate stats
  useEffect(() => {
    if (farms.length >= 0 && fields.length >= 0) {
      const totalAcres = fields.reduce((sum, field) => sum + (field.area_acres || 0), 0)
      
      setStats({
        totalFarms: farms.length,
        totalFields: fields.length,
        totalAcres,
        averageYield: 4.2, // This would come from actual yield calculations
        riskScore: 25, // This would come from risk assessment API
        marketTrend: 'up' as const
      })
    }
  }, [farms, fields])

  const isLoading = farmsLoading || fieldsLoading

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <motion.div 
        className="aura-card aura-fade-in"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="aura-card-header">
          <h1 className="aura-card-title text-2xl">
            <SparklesIcon className="h-8 w-8" />
            Welcome to AgriForecast.ai, {user?.name || 'Farmer'}! 🌾
          </h1>
        </div>
        <div className="aura-card-content">
          <p className="text-gray-600 text-lg">
            Your AI-powered agricultural intelligence platform. Monitor crops, predict yields, 
            and make data-driven decisions for optimal farming outcomes.
          </p>
          <div className="mt-4 flex items-center gap-4 text-sm text-gray-500">
            <span className="flex items-center gap-1">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              TimesFM AI Models Active
            </span>
            <span className="flex items-center gap-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              Real-time Data Sync
            </span>
            <span className="flex items-center gap-1">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              Market Intelligence Connected
            </span>
          </div>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Farms"
          value={stats.totalFarms}
          icon={<HomeIcon className="h-6 w-6" />}
          color="bg-blue-500"
          loading={isLoading}
          trend={stats.totalFarms > 0 ? 'up' : 'stable'}
        />
        <StatCard
          title="Active Fields"
          value={stats.totalFields}
          icon={<ChartBarIcon className="h-6 w-6" />}
          color="bg-field-500"
          loading={isLoading}
          trend={stats.totalFields > 2 ? 'up' : 'stable'}
        />
        <StatCard
          title="Total Area"
          value={`${stats.totalAcres.toFixed(1)} acres`}
          icon={<MapPinIcon className="h-6 w-6" />}
          color="bg-crop-500"
          loading={isLoading}
          trend="stable"
        />
        <StatCard
          title="Avg. Yield"
          value={`${stats.averageYield} t/ha`}
          icon={<CurrencyDollarIcon className="h-6 w-6" />}
          color="bg-green-500"
          loading={isLoading}
          trend="up"
        />
      </div>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="lg:col-span-2">
          <QuickActions />
        </div>
        
        {/* Weather Widget */}
        <div>
          <WeatherWidget />
        </div>
      </div>

      {/* AI Insights and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI Insights */}
        <AIInsights />
        
        {/* Recent Farms */}
        <RecentFarms farms={farms.slice(0, 3)} isLoading={isLoading} />
      </div>

      {/* Performance Metrics */}
      <motion.div 
        className="aura-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <div className="aura-card-header">
          <h2 className="aura-card-title">
            <ChartBarIcon className="h-6 w-6" />
            Performance Overview
          </h2>
        </div>
        <div className="aura-card-content">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <PerformanceMetric
              label="AI Prediction Accuracy"
              value="94.2%"
              change="+2.1%"
              color="text-green-600"
            />
            <PerformanceMetric
              label="Risk Mitigation"
              value="87%"
              change="+5.3%"
              color="text-blue-600"
            />
            <PerformanceMetric
              label="Profit Optimization"
              value="23.4%"
              change="+8.7%"
              color="text-purple-600"
            />
          </div>
        </div>
      </motion.div>

      {/* Error State */}
      {farmsError && (
        <div className="aura-alert-warning">
          <CloudIcon className="h-5 w-5" />
          <div>
            <p className="font-medium">Backend Connection Issue</p>
            <p className="text-sm">Running in demo mode. Some features may be limited.</p>
          </div>
        </div>
      )}
    </div>
  )
}

interface StatCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  color: string
  loading: boolean
  trend: 'up' | 'down' | 'stable'
}

function StatCard({ title, value, icon, color, loading, trend }: StatCardProps) {
  const trendIcon = {
    up: <ArrowUpIcon className="h-4 w-4 text-green-500" />,
    down: <ArrowDownIcon className="h-4 w-4 text-red-500" />,
    stable: <div className="h-4 w-4" />
  }

  return (
    <motion.div 
      className="aura-metric-card"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="aura-metric-label">{title}</p>
          <div className="flex items-center gap-2">
            <div className="aura-metric-value text-2xl">
              {loading ? (
                <div className="aura-skeleton h-8 w-16"></div>
              ) : (
                value
              )}
            </div>
            {!loading && trendIcon[trend]}
          </div>
        </div>
        <div className={`aura-metric-icon ${color}`}>
          {icon}
        </div>
      </div>
    </motion.div>
  )
}

interface RecentFarmsProps {
  farms: Farm[]
  isLoading: boolean
}

function RecentFarms({ farms, isLoading }: RecentFarmsProps) {
  return (
    <motion.div 
      className="aura-card"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <div className="aura-card-header">
        <h2 className="aura-card-title">
          <HomeIcon className="h-6 w-6" />
          Recent Farms
        </h2>
      </div>
      <div className="aura-card-content">
        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="aura-skeleton h-16 rounded-lg"></div>
            ))}
          </div>
        ) : farms.length > 0 ? (
          <div className="space-y-3">
            {farms.map((farm) => (
              <div key={farm.id} className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">{farm.name}</h3>
                    <p className="text-sm text-gray-600">{farm.location}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">{farm.total_area_acres} acres</p>
                    <p className="text-xs text-green-600">Active</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <HomeIcon className="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600">No farms yet</p>
            <button className="aura-btn-primary mt-3">
              Create Your First Farm
            </button>
          </div>
        )}
      </div>
    </motion.div>
  )
}

interface PerformanceMetricProps {
  label: string
  value: string
  change: string
  color: string
}

function PerformanceMetric({ label, value, change, color }: PerformanceMetricProps) {
  return (
    <div className="text-center">
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-sm text-gray-600 mb-1">{label}</p>
      <p className={`text-sm font-medium ${color}`}>{change} from last month</p>
    </div>
  )
}
