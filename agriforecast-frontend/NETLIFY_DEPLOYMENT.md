# Netlify Deployment Guide for AgriForecast

## Prerequisites

1. **Netlify Account**: Sign up at [netlify.com](https://netlify.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Backend API**: Your backend should be deployed (Heroku, Railway, or similar)

## Step 1: Prepare Your Repository

### 1.1 Environment Variables
Create a `.env.production` file with your production API keys:

```bash
# API Configuration
VITE_API_BASE_URL=https://your-backend-url.herokuapp.com
VITE_API_TIMEOUT=10000

# Weather API
VITE_OPENWEATHER_API_KEY=your_openweather_api_key

# Market Data API
VITE_ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key

# NASA Earthdata
VITE_NASA_EARTHDATA_TOKEN=your_nasa_earthdata_token

# Google Generative AI (Gemini)
VITE_GOOGLE_AI_API_KEY=your_google_ai_api_key

# ElevenLabs (Voice)
VITE_ELEVENLABS_API_KEY=your_elevenlabs_api_key

# App Configuration
VITE_APP_NAME=AgriForecast
VITE_APP_VERSION=1.0.0
VITE_APP_ENVIRONMENT=production
```

### 1.2 Update API Base URL
Update your API service to use environment variables:

```typescript
// src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

## Step 2: Deploy to Netlify

### Method 1: Netlify Dashboard (Recommended)

1. **Connect Repository**:
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub account
   - Select your AgriForecast repository

2. **Build Settings**:
   - **Base directory**: `agriforecast-frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `agriforecast-frontend/dist`

3. **Environment Variables**:
   - Go to Site settings → Environment variables
   - Add all your production environment variables
   - Make sure to use `VITE_` prefix for client-side variables

4. **Deploy**:
   - Click "Deploy site"
   - Wait for build to complete

### Method 2: Netlify CLI

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**:
   ```bash
   netlify login
   ```

3. **Initialize Site**:
   ```bash
   cd agriforecast-frontend
   netlify init
   ```

4. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

## Step 3: Configure Custom Domain (Optional)

1. Go to Site settings → Domain management
2. Add your custom domain
3. Configure DNS settings as instructed by Netlify

## Step 4: Set Up Continuous Deployment

1. **Automatic Deploys**: Enabled by default when connected to Git
2. **Branch Deploys**: Configure in Site settings → Build & deploy
3. **Deploy Previews**: Automatically created for pull requests

## Step 5: Environment Variables in Netlify

Add these environment variables in Netlify dashboard:

### Required Variables:
```
VITE_API_BASE_URL=https://your-backend-url.herokuapp.com
VITE_OPENWEATHER_API_KEY=your_openweather_api_key
VITE_ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
VITE_NASA_EARTHDATA_TOKEN=your_nasa_earthdata_token
VITE_GOOGLE_AI_API_KEY=your_google_ai_api_key
VITE_ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

### Optional Variables:
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_MAPBOX_ACCESS_TOKEN=your_mapbox_token
VITE_GOOGLE_EARTH_ENGINE_PROJECT=your_gee_project_id
```

## Step 6: Backend Deployment

Your backend needs to be deployed separately. Options:

### Option 1: Heroku
```bash
# In your backend directory
heroku create your-app-name
git push heroku main
```

### Option 2: Railway
```bash
# Connect your repository to Railway
# Railway will auto-deploy from your main branch
```

### Option 3: Render
```bash
# Connect your repository to Render
# Set build command: pip install -r requirements.txt
# Set start command: python api_server_production.py
```

## Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check Node.js version (should be 18+)
   - Verify all dependencies are in package.json
   - Check build logs in Netlify dashboard

2. **API Calls Fail**:
   - Verify VITE_API_BASE_URL is correct
   - Check CORS settings on your backend
   - Ensure backend is deployed and accessible

3. **Environment Variables Not Working**:
   - Make sure variables start with `VITE_`
   - Redeploy after adding new variables
   - Check variable names match exactly

4. **Routing Issues**:
   - The netlify.toml file includes SPA redirect rules
   - Make sure all routes redirect to index.html

## Performance Optimization

1. **Enable Netlify Analytics** (paid feature)
2. **Use Netlify Edge Functions** for serverless functions
3. **Enable Image Optimization** in Netlify dashboard
4. **Set up CDN** for global distribution

## Security

1. **Environment Variables**: Never commit API keys to Git
2. **HTTPS**: Automatically enabled by Netlify
3. **Headers**: Configured in netlify.toml for security
4. **CORS**: Configure your backend to allow your Netlify domain

## Monitoring

1. **Netlify Analytics**: Monitor site performance
2. **Error Tracking**: Consider adding Sentry or similar
3. **Uptime Monitoring**: Use services like UptimeRobot

## Support

- **Netlify Docs**: [docs.netlify.com](https://docs.netlify.com)
- **Netlify Community**: [community.netlify.com](https://community.netlify.com)
- **Vite Docs**: [vitejs.dev](https://vitejs.dev)
