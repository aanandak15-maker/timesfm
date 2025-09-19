// Quick test to verify demo data is working
import demoService from '../services/demoService';

export const testDemo = async () => {
  console.log('🧪 Testing Demo Data...');
  
  try {
    const farms = await demoService.getFarms();
    const fields = await demoService.getFields();
    
    console.log('✅ Demo Data Test Results:');
    console.log(`📋 Farms: ${farms.length} (${farms.map(f => f.name).join(', ')})`);
    console.log(`🌾 Fields: ${fields.length} (${fields.map(f => f.crop_type).join(', ')})`);
    
    if (farms.length > 0 && fields.length > 0) {
      console.log('🎉 Demo data is working correctly!');
      return true;
    } else {
      console.log('❌ Demo data is empty');
      return false;
    }
  } catch (error) {
    console.error('❌ Demo data test failed:', error);
    return false;
  }
};

// Auto-run test
testDemo();
