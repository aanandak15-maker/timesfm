# 🚀 Render Deployment Guide

## **Step 1: Deploy Backend to Render**

### **1.1 Create Render Account**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Connect your GitHub account

### **1.2 Deploy Backend**
1. Click "New +" → "Web Service"
2. Connect your `timesfm` repository
3. Render will auto-detect Python
4. Configure:
   - **Name**: `agriforecast-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api_server_production.py`
   - **Plan**: `Free`

### **1.3 Environment Variables**
In Render dashboard, go to Environment tab:
```
PORT=8000
PYTHON_VERSION=3.11
```

### **1.4 Deploy**
1. Click "Create Web Service"
2. Render will build and deploy
3. You'll get a URL like: `https://agriforecast-api.onrender.com`
4. Test: `https://agriforecast-api.onrender.com/health`

## **Step 2: Deploy Frontend to Vercel**

### **2.1 Create Vercel Account**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Connect your GitHub account

### **2.2 Deploy Frontend**
1. Click "New Project"
2. Select your `timesfm` repository
3. Set Root Directory to `agriforecast-frontend`
4. Vercel will auto-detect React

### **2.3 Environment Variables**
In Vercel dashboard, go to Settings > Environment Variables:
```
VITE_API_URL=https://agriforecast-api.onrender.com
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
VITE_OPENWEATHER_API_KEY=your-openweather-key
VITE_ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
VITE_NASA_API_KEY=your-nasa-token
VITE_MAPBOX_API_KEY=your-mapbox-token
```

## **Step 3: Test Production**

### **3.1 Test Backend**
```bash
curl https://agriforecast-api.onrender.com/health
```

### **3.2 Test Frontend**
Visit your Vercel URL and check:
- API calls are working
- Real data is loading
- No CORS errors

## **Costs:**
- **Render**: Free tier (750 hours/month)
- **Vercel**: Free tier (unlimited static sites)
- **Total**: $0/month for development use

## **Troubleshooting:**

### **Common Issues:**
1. **CORS errors**: Check allowed origins in `api_server_production.py`
2. **Environment variables**: Make sure all are set in both Render and Vercel
3. **Build failures**: Check logs in Render dashboard
4. **API not responding**: Check Render logs for errors

### **Render Free Tier Limits:**
- 750 hours/month
- Sleeps after 15 minutes of inactivity
- Cold start takes ~30 seconds
- Perfect for development and demos
