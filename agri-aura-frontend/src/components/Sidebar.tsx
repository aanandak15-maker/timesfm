import { Fragment } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  HomeIcon, 
  BuildingOfficeIcon, 
  MapIcon,
  SparklesIcon,
  ChartBarIcon,
  BoltIcon,
  CloudIcon,
  CurrencyDollarIcon,
  DocumentTextIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline'

interface SidebarProps {
  open: boolean
  setOpen: (open: boolean) => void
  backendConnected: boolean
}

export default function Sidebar({ open, setOpen, backendConnected }: SidebarProps) {
  const location = useLocation()

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Farms', href: '/farms', icon: BuildingOfficeIcon },
    { name: 'Fields', href: '/fields', icon: MapIcon },
    { name: 'AI Forecast', href: '/ai-forecast', icon: SparklesIcon },
    { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
    { name: 'Real-time', href: '/realtime', icon: BoltIcon },
    { name: 'Weather', href: '/weather', icon: CloudIcon },
    { name: 'Market', href: '/market', icon: CurrencyDollarIcon },
    { name: 'Reports', href: '/reports', icon: DocumentTextIcon },
    { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
  ]

  return (
    <div className="flex">
      <div className="flex flex-col w-64 bg-white border-r border-gray-200 min-h-screen">
        {/* Logo */}
        <div className="flex items-center gap-3 px-6 py-4 border-b border-gray-200">
          <div className="w-8 h-8 bg-gradient-to-r from-field-500 to-crop-500 rounded-lg flex items-center justify-center">
            <SparklesIcon className="h-5 w-5 text-white" />
          </div>
          <h1 className="text-xl font-bold text-gray-900">AgriForecast.ai</h1>
        </div>

        {/* Status */}
        <div className="px-6 py-3 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${backendConnected ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
            <span className="text-sm text-gray-600">
              {backendConnected ? 'Backend Connected' : 'Demo Mode'}
            </span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-4 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`aura-nav-item ${isActive ? 'active' : ''}`}
              >
                <item.icon className="h-5 w-5" />
                {item.name}
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-200">
          <p className="text-xs text-gray-500">AgriForecast.ai v2.0</p>
          <p className="text-xs text-gray-500">Powered by TimesFM</p>
        </div>
      </div>
    </div>
  )
}
