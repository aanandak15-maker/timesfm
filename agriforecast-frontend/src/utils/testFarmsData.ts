// Test script to verify farms and fields data structure
import demoService from '../services/demoService';

export const testFarmsAndFieldsData = async () => {
  console.log('🧪 Testing Farms and Fields Data Structure...');
  
  try {
    const farms = await demoService.getFarms();
    const fields = await demoService.getFields();
    
    console.log('✅ Farms Data:');
    farms.forEach((farm, index) => {
      console.log(`Farm ${index + 1}:`, {
        id: farm.id,
        name: farm.name,
        location: farm.location,
        total_area_acres: farm.total_area_acres,
        description: farm.description,
        owner: farm.owner,
        established: farm.established,
        hasImage: !!farm.image,
        hasCoordinates: !!(farm.latitude && farm.longitude),
        hasTimestamps: !!(farm.created_at && farm.updated_at)
      });
    });
    
    console.log('✅ Fields Data:');
    fields.forEach((field, index) => {
      console.log(`Field ${index + 1}:`, {
        id: field.id,
        name: field.name,
        farm_id: field.farm_id,
        area_acres: field.area_acres,
        crop_type: field.crop_type,
        status: field.status,
        soil_type: field.soil_type,
        hasCoordinates: !!(field.latitude && field.longitude),
        hasDates: !!(field.planting_date && field.harvest_date),
        hasPredictions: !!(field.yield_prediction && field.health_score)
      });
    });
    
    console.log('🎉 Data structure test completed!');
    return true;
  } catch (error) {
    console.error('❌ Data structure test failed:', error);
    return false;
  }
};

// Auto-run test
testFarmsAndFieldsData();
