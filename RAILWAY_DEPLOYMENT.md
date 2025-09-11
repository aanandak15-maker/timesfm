# 🚂 Railway Deployment Guide

## **Step 1: Deploy Backend to Railway**

### **1.1 Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your GitHub account

### **1.2 Deploy from GitHub**
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `timesfm` repository
4. Railway will automatically detect it's a Python project

### **1.3 Configure Environment Variables**
In Railway dashboard, go to Variables tab and add:
```
PORT=8000
PYTHON_VERSION=3.11
```

### **1.4 Deploy**
1. Railway will automatically build and deploy
2. You'll get a URL like: `https://your-app-name.railway.app`
3. Test the health endpoint: `https://your-app-name.railway.app/health`

## **Step 2: Update Frontend for Production**

### **2.1 Update API Base URL**
In `agriforecast-frontend/src/lib/api.ts`:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-app-name.railway.app'
```

### **2.2 Add Environment Variable**
Create `agriforecast-frontend/.env.production`:
```
VITE_API_URL=https://your-app-name.railway.app
```

## **Step 3: Deploy Frontend to Vercel**

### **3.1 Create Vercel Account**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Connect your GitHub account

### **3.2 Deploy Frontend**
1. Click "New Project"
2. Select your `timesfm` repository
3. Set Root Directory to `agriforecast-frontend`
4. Vercel will automatically detect it's a React project

### **3.3 Configure Environment Variables**
In Vercel dashboard, go to Settings > Environment Variables:
```
VITE_API_URL=https://your-app-name.railway.app
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
VITE_OPENWEATHER_API_KEY=your-openweather-key
VITE_ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
VITE_NASA_API_KEY=your-nasa-token
VITE_MAPBOX_API_KEY=your-mapbox-token
```

## **Step 4: Test Production**

### **4.1 Test Backend**
```bash
curl https://your-app-name.railway.app/health
```

### **4.2 Test Frontend**
Visit your Vercel URL and check:
- API calls are working
- Real data is loading
- No CORS errors

## **Step 5: Custom Domain (Optional)**

### **5.1 Railway Custom Domain**
1. Go to Railway project settings
2. Add custom domain
3. Update DNS records

### **5.2 Vercel Custom Domain**
1. Go to Vercel project settings
2. Add custom domain
3. Update DNS records

## **Troubleshooting**

### **Common Issues:**
1. **CORS errors**: Check allowed origins in `api_server_production.py`
2. **Environment variables**: Make sure all are set in both Railway and Vercel
3. **Build failures**: Check logs in Railway dashboard
4. **API not responding**: Check Railway logs for errors

### **Useful Commands:**
```bash
# Check Railway logs
railway logs

# Check Railway status
railway status

# Deploy to Railway
railway up
```

## **Costs:**
- **Railway**: Free tier (500 hours/month)
- **Vercel**: Free tier (unlimited static sites)
- **Total**: $0/month for development use
