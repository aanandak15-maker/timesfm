import { CloudIcon, SunIcon } from '@heroicons/react/24/outline'

export default function WeatherWidget() {
  const weatherData = {
    current: {
      temperature: 28,
      condition: 'Partly Cloudy',
      humidity: 65,
      windSpeed: 12
    },
    forecast: [
      { day: 'Today', high: 32, low: 24, condition: 'Sunny' },
      { day: 'Tomorrow', high: 30, low: 22, condition: 'Cloudy' },
      { day: 'Wednesday', high: 28, low: 20, condition: 'Rain' }
    ]
  }

  return (
    <div className="aura-card">
      <div className="aura-card-header">
        <h2 className="aura-card-title">
          <CloudIcon className="h-6 w-6" />
          Weather Conditions
        </h2>
      </div>
      <div className="aura-card-content">
        <div className="text-center mb-4">
          <div className="flex items-center justify-center mb-2">
            <SunIcon className="h-12 w-12 text-yellow-500" />
          </div>
          <p className="text-3xl font-bold text-gray-900">{weatherData.current.temperature}°C</p>
          <p className="text-gray-600">{weatherData.current.condition}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center">
            <p className="text-sm text-gray-600">Humidity</p>
            <p className="font-semibold">{weatherData.current.humidity}%</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">Wind</p>
            <p className="font-semibold">{weatherData.current.windSpeed} km/h</p>
          </div>
        </div>

        <div className="space-y-2">
          <h4 className="font-medium text-gray-900">3-Day Forecast</h4>
          {weatherData.forecast.map((day) => (
            <div key={day.day} className="flex justify-between items-center p-2 bg-gray-50 rounded">
              <span className="text-sm font-medium">{day.day}</span>
              <span className="text-sm text-gray-600">{day.condition}</span>
              <span className="text-sm font-medium">{day.high}°/{day.low}°</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
