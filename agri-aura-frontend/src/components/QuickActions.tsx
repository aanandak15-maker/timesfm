import { PlusIcon, ChartBarIcon, CloudIcon, CurrencyDollarIcon } from '@heroicons/react/24/outline'
import { Link } from 'react-router-dom'

export default function QuickActions() {
  const actions = [
    {
      title: 'Add New Field',
      description: 'Create a new field for monitoring',
      icon: PlusIcon,
      href: '/fields',
      color: 'bg-field-500'
    },
    {
      title: 'AI Forecast',
      description: 'Get AI-powered yield predictions',
      icon: ChartBarIcon,
      href: '/ai-forecast',
      color: 'bg-purple-500'
    },
    {
      title: 'Weather Alerts',
      description: 'Check current weather conditions',
      icon: CloudIcon,
      href: '/weather',
      color: 'bg-blue-500'
    },
    {
      title: 'Market Prices',
      description: 'View current market trends',
      icon: CurrencyDollarIcon,
      href: '/market',
      color: 'bg-green-500'
    }
  ]

  return (
    <div className="aura-card">
      <div className="aura-card-header">
        <h2 className="aura-card-title">
          <ChartBarIcon className="h-6 w-6" />
          Quick Actions
        </h2>
      </div>
      <div className="aura-card-content">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {actions.map((action) => (
            <Link
              key={action.title}
              to={action.href}
              className="p-4 bg-white rounded-lg border border-gray-200 hover:border-field-300 hover:shadow-md transition-all duration-200 group"
            >
              <div className="flex items-center gap-3 mb-2">
                <div className={`p-2 rounded-lg ${action.color} text-white`}>
                  <action.icon className="h-5 w-5" />
                </div>
                <h3 className="font-semibold text-gray-900 group-hover:text-field-700">
                  {action.title}
                </h3>
              </div>
              <p className="text-sm text-gray-600">{action.description}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
