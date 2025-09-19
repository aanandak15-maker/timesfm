// Test script to verify demo data is working
import demoService from '../services/demoService';

export const testDemoData = async () => {
  console.log('🧪 Testing Demo Data...');
  
  try {
    // Test farms
    const farms = await demoService.getFarms();
    console.log('✅ Farms loaded:', farms.length);
    console.log('📋 Farm names:', farms.map(f => f.name));
    
    // Test fields
    const fields = await demoService.getFields();
    console.log('✅ Fields loaded:', fields.length);
    console.log('🌾 Field crops:', fields.map(f => f.crop_type));
    
    // Test weather
    const weather = await demoService.getWeatherData();
    console.log('✅ Weather loaded:', weather.location, weather.temperature + '°C');
    
    // Test market data
    const market = await demoService.getMarketData();
    console.log('✅ Market data loaded:', market.length, 'commodities');
    
    // Test analytics
    const analytics = await demoService.getAnalytics();
    console.log('✅ Analytics loaded:', analytics.totalFarms, 'farms');
    
    // Test alerts
    const alerts = await demoService.getAlerts();
    console.log('✅ Alerts loaded:', alerts.length);
    
    // Test AI insights
    const insights = await demoService.getAIInsights();
    console.log('✅ AI insights loaded:', insights.length);
    
    console.log('🎉 All demo data tests passed!');
    return true;
  } catch (error) {
    console.error('❌ Demo data test failed:', error);
    return false;
  }
};

// Auto-run test when imported
if (typeof window !== 'undefined') {
  testDemoData();
}
