import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  HomeIcon,
  ChartBarIcon,
  CloudIcon,
  CurrencyDollarIcon,
} from '@heroicons/react/24/outline'
import { api, Farm, Field } from '../lib/supabase'
import { useAuth } from '../hooks/useAuth'

interface DashboardStats {
  totalFarms: number
  totalFields: number
  totalAcres: number
  averageYield: number
}

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState<DashboardStats>({
    totalFarms: 0,
    totalFields: 0,
    totalAcres: 0,
    averageYield: 0,
  })

  // Fetch farms data
  const { data: farms = [], isLoading: farmsLoading } = useQuery({
    queryKey: ['farms', user?.id],
    queryFn: () => api.getFarms(user!.id),
    enabled: !!user?.id,
  })

  // Fetch all fields for all farms
  const { data: allFields = [], isLoading: fieldsLoading } = useQuery({
    queryKey: ['allFields', farms],
    queryFn: async () => {
      const fieldsPromises = farms.map(farm => api.getFields(farm.id))
      const fieldsArrays = await Promise.all(fieldsPromises)
      return fieldsArrays.flat()
    },
    enabled: farms.length > 0,
  })

  // Calculate stats when data changes
  useEffect(() => {
    if (farms.length > 0 && allFields.length > 0) {
      const totalAcres = allFields.reduce((sum, field) => sum + field.area_acres, 0)
      
      setStats({
        totalFarms: farms.length,
        totalFields: allFields.length,
        totalAcres,
        averageYield: 4.2, // Mock data - would come from yield calculations
      })
    }
  }, [farms, allFields])

  const isLoading = farmsLoading || fieldsLoading

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="ag-card ag-fade-in">
        <div className="ag-card-header">
          <h1 className="ag-card-title">
            <HomeIcon className="h-8 w-8" />
            Welcome back, {user?.user_metadata?.full_name || 'Farmer'}! 🌾
          </h1>
        </div>
        <div className="ag-card-content">
          <p className="text-gray-600">
            Your agricultural intelligence dashboard powered by AI and real-time data.
            Monitor your farms, track yields, and make data-driven decisions.
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Farms"
          value={stats.totalFarms}
          icon={<HomeIcon className="h-6 w-6" />}
          color="bg-blue-500"
          loading={isLoading}
        />
        <StatCard
          title="Total Fields"
          value={stats.totalFields}
          icon={<ChartBarIcon className="h-6 w-6" />}
          color="bg-green-500"
          loading={isLoading}
        />
        <StatCard
          title="Total Acres"
          value={`${stats.totalAcres.toFixed(1)} acres`}
          icon={<CloudIcon className="h-6 w-6" />}
          color="bg-yellow-500"
          loading={isLoading}
        />
        <StatCard
          title="Avg. Yield"
          value={`${stats.averageYield} t/ha`}
          icon={<CurrencyDollarIcon className="h-6 w-6" />}
          color="bg-purple-500"
          loading={isLoading}
        />
      </div>

      {/* Quick Actions */}
      <div className="ag-card">
        <div className="ag-card-header">
          <h2 className="ag-card-title">
            <ChartBarIcon className="h-6 w-6" />
            Quick Actions
          </h2>
        </div>
        <div className="ag-card-content">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <QuickActionButton
              title="Add New Field"
              description="Create a new field for monitoring"
              icon="🌾"
              href="/fields"
            />
            <QuickActionButton
              title="AI Forecast"
              description="Get AI-powered yield predictions"
              icon="🤖"
              href="/ai-forecast"
            />
            <QuickActionButton
              title="Weather Alerts"
              description="Check current weather conditions"
              icon="🌤️"
              href="/realtime"
            />
            <QuickActionButton
              title="Market Prices"
              description="View current market trends"
              icon="💰"
              href="/analytics"
            />
            <QuickActionButton
              title="Field Analysis"
              description="Detailed field performance"
              icon="📊"
              href="/analytics"
            />
            <QuickActionButton
              title="Settings"
              description="Configure your preferences"
              icon="⚙️"
              href="/settings"
            />
          </div>
        </div>
      </div>

      {/* Recent Farms */}
      {farms.length > 0 && (
        <div className="ag-card">
          <div className="ag-card-header">
            <h2 className="ag-card-title">
              <HomeIcon className="h-6 w-6" />
              Your Farms
            </h2>
          </div>
          <div className="ag-card-content">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {farms.slice(0, 6).map((farm) => (
                <FarmCard key={farm.id} farm={farm} />
              ))}
            </div>
          </div>
        </div>
      )}

      {/* AI Insights Preview */}
      <div className="ag-card">
        <div className="ag-card-header">
          <h2 className="ag-card-title">
            <ChartBarIcon className="h-6 w-6" />
            AI Insights
          </h2>
        </div>
        <div className="ag-card-content">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-green-600 text-lg">🤖</span>
                <h3 className="font-semibold text-green-800">Yield Prediction</h3>
              </div>
              <p className="text-green-700 text-sm">
                AI models predict 15% higher yields this season based on current conditions.
              </p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-blue-600 text-lg">🌤️</span>
                <h3 className="font-semibold text-blue-800">Weather Alert</h3>
              </div>
              <p className="text-blue-700 text-sm">
                Optimal weather conditions expected for the next 7 days. Perfect for crop growth.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

interface StatCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  color: string
  loading: boolean
}

function StatCard({ title, value, icon, color, loading }: StatCardProps) {
  return (
    <div className="ag-metric-card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">
            {loading ? '...' : value}
          </p>
        </div>
        <div className={`p-3 rounded-full ${color} text-white`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

interface QuickActionButtonProps {
  title: string
  description: string
  icon: string
  href: string
}

function QuickActionButton({ title, description, icon, href }: QuickActionButtonProps) {
  return (
    <a
      href={href}
      className="p-4 bg-white rounded-lg border border-gray-200 hover:border-green-300 hover:shadow-md transition-all duration-200 group"
    >
      <div className="flex items-center gap-3 mb-2">
        <span className="text-2xl">{icon}</span>
        <h3 className="font-semibold text-gray-900 group-hover:text-green-700">
          {title}
        </h3>
      </div>
      <p className="text-sm text-gray-600">{description}</p>
    </a>
  )
}

interface FarmCardProps {
  farm: Farm
}

function FarmCard({ farm }: FarmCardProps) {
  return (
    <div className="p-4 bg-white rounded-lg border border-gray-200 hover:border-green-300 hover:shadow-md transition-all duration-200">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-green-600 text-lg">🏭</span>
        <h3 className="font-semibold text-gray-900">{farm.name}</h3>
      </div>
      <p className="text-sm text-gray-600 mb-2">{farm.location}</p>
      <p className="text-sm text-gray-500">{farm.total_area_acres} acres</p>
    </div>
  )
}
