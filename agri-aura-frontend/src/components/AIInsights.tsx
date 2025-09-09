import { SparklesIcon, ArrowTrendingUpIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

export default function AIInsights() {
  const insights = [
    {
      type: 'success',
      title: 'Optimal Yield Predicted',
      message: 'AI models predict 18% higher yields this season based on current conditions and weather patterns.',
      icon: ArrowTrendingUpIcon,
      color: 'text-green-600 bg-green-50 border-green-200'
    },
    {
      type: 'warning',
      title: 'Irrigation Alert',
      message: 'Consider adjusting irrigation schedule. Soil moisture levels are trending below optimal.',
      icon: ExclamationTriangleIcon,
      color: 'text-yellow-600 bg-yellow-50 border-yellow-200'
    },
    {
      type: 'info',
      title: 'Market Opportunity',
      message: 'Rice prices are expected to increase by 12% next month. Optimal selling window identified.',
      icon: SparklesIcon,
      color: 'text-blue-600 bg-blue-50 border-blue-200'
    }
  ]

  return (
    <div className="aura-card">
      <div className="aura-card-header">
        <h2 className="aura-card-title">
          <SparklesIcon className="h-6 w-6" />
          AI Insights
        </h2>
      </div>
      <div className="aura-card-content">
        <div className="space-y-4">
          {insights.map((insight, index) => (
            <div key={index} className={`p-4 rounded-lg border ${insight.color}`}>
              <div className="flex items-start gap-3">
                <insight.icon className="h-5 w-5 mt-0.5" />
                <div>
                  <h4 className="font-medium mb-1">{insight.title}</h4>
                  <p className="text-sm">{insight.message}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-6 p-4 bg-gradient-to-r from-field-50 to-crop-50 rounded-lg border border-field-200">
          <div className="flex items-center gap-2 mb-2">
            <SparklesIcon className="h-5 w-5 text-field-600" />
            <h4 className="font-medium text-field-800">TimesFM AI Status</h4>
          </div>
          <p className="text-sm text-field-700">
            AI models are actively monitoring your fields and providing real-time insights based on 
            weather patterns, soil conditions, and historical data.
          </p>
        </div>
      </div>
    </div>
  )
}
