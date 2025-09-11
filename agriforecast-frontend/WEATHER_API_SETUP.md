# Weather API Setup Guide

## Get Real Weather Data for Your Field

### Step 1: Get OpenWeatherMap API Key (FREE)

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Replace `demo` in `.env` file with your actual API key

### Step 2: Update Environment File

```bash
# In agriforecast-frontend/.env
VITE_OPENWEATHER_API_KEY=your_actual_api_key_here
```

### Step 3: Restart Development Server

```bash
npm run dev
```

## What You'll Get

✅ **Real Weather Data** for your exact field coordinates
✅ **Accurate Temperature** in Celsius
✅ **Real Humidity, Wind, Pressure** data
✅ **5-Day Forecast** for your location
✅ **Current Conditions** for your field

## API Limits (Free Tier)

- 1,000 calls per day
- 60 calls per minute
- Perfect for development and small farms

## Fallback Behavior

If API fails or reaches limits, the system automatically falls back to mock data with your correct location name.

## Testing

1. Open Weather page: http://localhost:3002/weather
2. Check browser console for "Real weather data received" message
3. Verify location shows your actual area (Uttar Pradesh, India)
