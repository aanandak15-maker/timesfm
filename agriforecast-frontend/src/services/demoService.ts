// Demo Service for Hackathon Presentation
// Provides realistic data simulation for impressive demonstrations

import {
  demoFarms,
  demoFields,
  generateDemoSensorData,
  demoWeatherData,
  demoMarketData,
  demoYieldPredictions,
  demoAnalytics,
  demoAlerts,
  demoAIInsights,
  type DemoFarm,
  type DemoField,
  type DemoSensorData,
  type DemoWeatherData,
  type DemoMarketData,
  type DemoYieldPrediction
} from '../data/demoData';

class DemoService {
  private isSimulationRunning = false;
  private simulationInterval: NodeJS.Timeout | null = null;
  private sensorDataCache = new Map<string, DemoSensorData[]>();

  // Simulate real-time data updates
  startSimulation() {
    if (this.isSimulationRunning) return;
    
    this.isSimulationRunning = true;
    this.simulationInterval = setInterval(() => {
      // Update sensor data for all fields
      demoFields.forEach(field => {
        const newSensorData = generateDemoSensorData(field.id);
        const existingData = this.sensorDataCache.get(field.id) || [];
        existingData.push(newSensorData);
        
        // Keep only last 50 readings
        if (existingData.length > 50) {
          existingData.shift();
        }
        
        this.sensorDataCache.set(field.id, existingData);
      });
    }, 5000); // Update every 5 seconds
  }

  stopSimulation() {
    if (this.simulationInterval) {
      clearInterval(this.simulationInterval);
      this.simulationInterval = null;
    }
    this.isSimulationRunning = false;
  }

  // Get farms data
  async getFarms(): Promise<any[]> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Map demo farms to expected interface
    return demoFarms.map(farm => ({
      id: farm.id,
      name: farm.name,
      location: farm.location,
      total_area_acres: farm.total_area, // Map total_area to total_area_acres
      description: farm.description,
      owner: farm.owner,
      established: farm.established,
      image: farm.image,
      latitude: 28.368911 + (Math.random() - 0.5) * 0.1, // Add some variation
      longitude: 77.541033 + (Math.random() - 0.5) * 0.1, // Add some variation
      created_at: "2024-01-15T10:30:00Z",
      updated_at: "2024-01-15T10:30:00Z"
    }));
  }

  // Get fields data
  async getFields(): Promise<DemoField[]> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 200));
    return demoFields;
  }

  // Get sensor data for a specific field
  async getSensorData(fieldId: string): Promise<DemoSensorData[]> {
    await new Promise(resolve => setTimeout(resolve, 100));
    return this.sensorDataCache.get(fieldId) || [generateDemoSensorData(fieldId)];
  }

  // Get latest sensor data for a field
  async getLatestSensorData(fieldId: string): Promise<DemoSensorData> {
    await new Promise(resolve => setTimeout(resolve, 50));
    const data = this.sensorDataCache.get(fieldId);
    return data && data.length > 0 ? data[data.length - 1] : generateDemoSensorData(fieldId);
  }

  // Get weather data
  async getWeatherData(): Promise<DemoWeatherData> {
    await new Promise(resolve => setTimeout(resolve, 400));
    return demoWeatherData;
  }

  // Get market data
  async getMarketData(): Promise<DemoMarketData[]> {
    await new Promise(resolve => setTimeout(resolve, 250));
    return demoMarketData;
  }

  // Get yield predictions
  async getYieldPredictions(): Promise<DemoYieldPrediction[]> {
    await new Promise(resolve => setTimeout(resolve, 350));
    return demoYieldPredictions;
  }

  // Get analytics data
  async getAnalytics() {
    await new Promise(resolve => setTimeout(resolve, 200));
    return demoAnalytics;
  }

  // Get alerts
  async getAlerts() {
    await new Promise(resolve => setTimeout(resolve, 150));
    return demoAlerts;
  }

  // Get AI insights
  async getAIInsights() {
    await new Promise(resolve => setTimeout(resolve, 300));
    return demoAIInsights;
  }

  // Create a new field (for demo purposes)
  async createField(fieldData: Partial<DemoField>): Promise<DemoField> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const newField: DemoField = {
      id: `field-${Date.now()}`,
      name: fieldData.name || 'New Field',
      farm_id: fieldData.farm_id || 'farm-1',
      area_acres: fieldData.area_acres || 1.0,
      crop_type: fieldData.crop_type || 'Rice',
      latitude: fieldData.latitude || 28.368911,
      longitude: fieldData.longitude || 77.541033,
      soil_type: fieldData.soil_type || 'Loamy',
      planting_date: fieldData.planting_date || new Date().toISOString().split('T')[0],
      harvest_date: fieldData.harvest_date || new Date(Date.now() + 120 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      status: fieldData.status || 'growing',
      created_at: new Date().toISOString(),
      yield_prediction: 3.5 + Math.random() * 1.5,
      health_score: 80 + Math.random() * 20
    };

    // Add to demo fields
    demoFields.push(newField);
    
    // Initialize sensor data cache for new field
    this.sensorDataCache.set(newField.id, [generateDemoSensorData(newField.id)]);
    
    return newField;
  }

  // Update field data
  async updateField(fieldId: string, updates: Partial<DemoField>): Promise<DemoField> {
    await new Promise(resolve => setTimeout(resolve, 300));
    
    const fieldIndex = demoFields.findIndex(f => f.id === fieldId);
    if (fieldIndex === -1) {
      throw new Error('Field not found');
    }
    
    demoFields[fieldIndex] = { ...demoFields[fieldIndex], ...updates };
    return demoFields[fieldIndex];
  }

  // Delete field
  async deleteField(fieldId: string): Promise<boolean> {
    await new Promise(resolve => setTimeout(resolve, 200));
    
    const fieldIndex = demoFields.findIndex(f => f.id === fieldId);
    if (fieldIndex === -1) {
      return false;
    }
    
    demoFields.splice(fieldIndex, 1);
    this.sensorDataCache.delete(fieldId);
    return true;
  }

  // Get field status based on sensor data
  getFieldStatus(fieldId: string): string {
    const sensorData = this.sensorDataCache.get(fieldId);
    if (!sensorData || sensorData.length === 0) return 'unknown';
    
    const latest = sensorData[sensorData.length - 1];
    
    // Determine status based on sensor readings
    if (latest.soil_moisture < 30) return 'needs_water';
    if (latest.ph < 6.0 || latest.ph > 7.5) return 'ph_alert';
    if (latest.nitrogen < 60) return 'needs_fertilizer';
    if (latest.temperature > 35) return 'heat_stress';
    if (latest.device_health < 80) return 'device_issue';
    
    return 'healthy';
  }

  // Get field recommendations based on sensor data
  getFieldRecommendations(fieldId: string): string[] {
    const sensorData = this.sensorDataCache.get(fieldId);
    if (!sensorData || sensorData.length === 0) return [];
    
    const latest = sensorData[sensorData.length - 1];
    const recommendations: string[] = [];
    
    if (latest.soil_moisture < 30) {
      recommendations.push('Irrigate field immediately - soil moisture is low');
    }
    if (latest.ph < 6.0) {
      recommendations.push('Apply lime to increase soil pH');
    }
    if (latest.ph > 7.5) {
      recommendations.push('Apply sulfur to decrease soil pH');
    }
    if (latest.nitrogen < 60) {
      recommendations.push('Apply nitrogen fertilizer');
    }
    if (latest.phosphorus < 40) {
      recommendations.push('Apply phosphorus fertilizer');
    }
    if (latest.potassium < 50) {
      recommendations.push('Apply potassium fertilizer');
    }
    if (latest.temperature > 35) {
      recommendations.push('Consider shade or cooling measures');
    }
    if (latest.wind_speed > 15) {
      recommendations.push('Monitor for wind damage');
    }
    
    if (recommendations.length === 0) {
      recommendations.push('Field conditions are optimal');
    }
    
    return recommendations;
  }

  // Get historical data for charts
  getHistoricalData(fieldId: string, days: number = 7) {
    const sensorData = this.sensorDataCache.get(fieldId) || [];
    const now = new Date();
    const startDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
    
    return sensorData.filter(data => new Date(data.timestamp) >= startDate);
  }

  // Generate demo notifications
  generateDemoNotification() {
    const notifications = [
      "🌱 Field 1 soil moisture is optimal for rice growth",
      "🌤️ Weather forecast shows ideal conditions for next 3 days", 
      "📈 Yield prediction updated - 15% increase expected",
      "💰 Market prices for rice increased by 2.3%",
      "🔋 IoT device battery levels are good across all fields",
      "🌾 Field 2 maize is ready for harvest in 5 days",
      "💧 Irrigation system activated automatically",
      "📊 Monthly analytics report is ready",
      "🤖 AI detected optimal fertilizer application window",
      "📱 New field mapping completed successfully"
    ];
    
    return notifications[Math.floor(Math.random() * notifications.length)];
  }

  // Get demo statistics for dashboard
  getDemoStats() {
    return {
      totalFields: demoFields.length,
      activeSensors: demoFields.length * 12, // 12 sensors per field
      dataPoints: this.sensorDataCache.size * 50, // Approximate data points
      uptime: "99.8%",
      lastUpdate: new Date().toISOString(),
      alerts: demoAlerts.length,
      recommendations: demoAIInsights.length
    };
  }
}

// Create singleton instance
const demoService = new DemoService();

// Start simulation automatically
demoService.startSimulation();

export default demoService;
