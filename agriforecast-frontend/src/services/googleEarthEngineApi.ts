// Google Earth Engine API Service for Satellite Data
// Simplified and optimized for small and marginal farmers

export interface GEESatelliteImage {
  id: string;
  date: string;
  cloudCover: number;
  satellite: 'Sentinel-2' | 'Landsat';
  bands: {
    red: number;
    nir: number;
    blue: number;
    green: number;
  };
  ndvi: number;
  evi: number;
  savi: number;
  imageUrl?: string;
}

export interface GEETimeSeries {
  dates: string[];
  ndvi: number[];
  evi: number[];
  savi: number[];
  temperature: number[];
  precipitation: number[];
  soilMoisture: number[];
}

export interface GEEData {
  satelliteImages: GEESatelliteImage[];
  timeSeriesData: GEETimeSeries;
}

export class GoogleEarthEngineApiService {
  constructor() {
    console.log("GoogleEarthEngineApiService initialized for small farmers");
  }

  /**
   * Get satellite images for a specific location
   * Optimized for small field analysis
   */
  async getSatelliteImages(lat: number, lon: number, startDate?: string, endDate?: string): Promise<GEESatelliteImage[]> {
    try {
      console.log(`Fetching satellite data for location: ${lat}, ${lon}`);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Generate realistic satellite data for small farmers
      const images = this.generateMockSatelliteData(lat, lon, startDate, endDate);
      
      console.log(`Generated ${images.length} satellite images`);
      return images;
    } catch (error) {
      console.error('Error fetching satellite images:', error);
      return [];
    }
  }

  /**
   * Get time series data for vegetation analysis
   */
  async getTimeSeriesData(lat: number, lon: number, startDate?: string, endDate?: string): Promise<GEETimeSeries> {
    try {
      console.log(`Fetching time series data for location: ${lat}, ${lon}`);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Generate realistic time series data
      const timeSeries = this.generateMockTimeSeriesData(lat, lon);
      
      console.log(`Generated time series with ${timeSeries.dates.length} data points`);
      return timeSeries;
    } catch (error) {
      console.error('Error fetching time series data:', error);
      return {
        dates: [],
        ndvi: [],
        evi: [],
        savi: [],
        temperature: [],
        precipitation: [],
        soilMoisture: []
      };
    }
  }

  /**
   * Generate mock satellite data optimized for small farmers
   */
  private generateMockSatelliteData(lat: number, lon: number, startDate?: string, endDate?: string): GEESatelliteImage[] {
    const images: GEESatelliteImage[] = [];
    const baseDate = new Date(startDate || '2024-01-01');
    
    // Generate 5 recent images (weekly intervals)
    for (let i = 0; i < 5; i++) {
      const imageDate = new Date(baseDate);
      imageDate.setDate(baseDate.getDate() + (i * 7));
      
      // Generate realistic values for small farms
      const ndvi = 0.3 + Math.random() * 0.4; // 0.3-0.7 (healthy vegetation)
      const evi = 0.2 + Math.random() * 0.3;  // 0.2-0.5
      const savi = 0.25 + Math.random() * 0.35; // 0.25-0.6
      
      images.push({
        id: `image-${i + 1}`,
        date: imageDate.toISOString(),
        cloudCover: Math.random() * 15, // Low cloud cover for small areas
        satellite: 'Sentinel-2',
        bands: {
          red: 0.2 + Math.random() * 0.1,
          nir: 0.4 + Math.random() * 0.2,
          blue: 0.15 + Math.random() * 0.1,
          green: 0.3 + Math.random() * 0.15
        },
        ndvi,
        evi,
        savi,
        imageUrl: `https://via.placeholder.com/300x200?text=Satellite+${i + 1}`
      });
    }
    
    return images;
  }

  /**
   * Generate mock time series data for small farms
   */
  private generateMockTimeSeriesData(lat: number, lon: number): GEETimeSeries {
    const dates: string[] = [];
    const ndvi: number[] = [];
    const evi: number[] = [];
    const savi: number[] = [];
    const temperature: number[] = [];
    const precipitation: number[] = [];
    const soilMoisture: number[] = [];

    // Generate 12 months of data
    for (let i = 0; i < 12; i++) {
      const date = new Date();
      date.setMonth(date.getMonth() - (11 - i));
      dates.push(date.toISOString().split('T')[0]);

      // Seasonal variations for small farms
      const month = date.getMonth();
      const seasonalFactor = Math.sin((month / 12) * 2 * Math.PI);
      
      ndvi.push(0.4 + seasonalFactor * 0.2 + Math.random() * 0.1);
      evi.push(0.3 + seasonalFactor * 0.15 + Math.random() * 0.08);
      savi.push(0.35 + seasonalFactor * 0.18 + Math.random() * 0.09);
      
      // Temperature based on Indian climate
      temperature.push(20 + seasonalFactor * 10 + Math.random() * 5);
      
      // Precipitation (monsoon pattern)
      precipitation.push(month >= 5 && month <= 9 ? Math.random() * 100 : Math.random() * 20);
      
      // Soil moisture
      soilMoisture.push(15 + seasonalFactor * 15 + Math.random() * 10);
    }

    return { dates, ndvi, evi, savi, temperature, precipitation, soilMoisture };
  }

  /**
   * Calculate vegetation indices
   */
  private calculateNDVI(nir: number, red: number): number {
    return (nir - red) / (nir + red);
  }

  private calculateEVI(nir: number, red: number, blue: number): number {
    return 2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1));
  }

  private calculateSAVI(nir: number, red: number, L: number = 0.5): number {
    return (nir - red) * (1 + L) / (nir + red + L);
  }

  /**
   * Get crop health analysis for small farms
   */
  async getCropHealthAnalysis(lat: number, lon: number, cropType: string): Promise<any> {
    try {
      console.log(`Analyzing crop health for ${cropType} at ${lat}, ${lon}`);
      
      // Simulate analysis delay
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Generate crop-specific analysis
      const analysis = this.generateCropHealthAnalysis(cropType);
      
      return analysis;
    } catch (error) {
      console.error('Error analyzing crop health:', error);
      return null;
    }
  }

  /**
   * Generate crop health analysis for small farmers
   */
  private generateCropHealthAnalysis(cropType: string): any {
    const baseHealth = {
      'Rice': { health: 85, stress: ['Water stress'], recommendations: ['Increase irrigation', 'Monitor soil moisture'] },
      'Maize': { health: 78, stress: ['Nutrient deficiency'], recommendations: ['Apply nitrogen fertilizer', 'Check soil pH'] },
      'Cotton': { health: 82, stress: ['Pest pressure'], recommendations: ['Monitor for bollworm', 'Apply integrated pest management'] }
    };

    const cropData = baseHealth[cropType as keyof typeof baseHealth] || baseHealth['Rice'];
    
    return {
      cropType,
      healthScore: cropData.health + Math.random() * 10,
      stressFactors: cropData.stress,
      recommendations: cropData.recommendations,
      expectedYield: this.getExpectedYield(cropType),
      confidence: 85 + Math.random() * 10,
      lastUpdated: new Date().toISOString()
    };
  }

  /**
   * Get expected yield for small farms
   */
  private getExpectedYield(cropType: string): number {
    const yields = {
      'Rice': 3.5 + Math.random() * 1.0,    // 3.5-4.5 tons/acre
      'Maize': 2.8 + Math.random() * 0.8,   // 2.8-3.6 tons/acre
      'Cotton': 1.5 + Math.random() * 0.5   // 1.5-2.0 tons/acre
    };
    
    return yields[cropType as keyof typeof yields] || 3.0;
  }
}

// Export singleton instance
export const geeService = new GoogleEarthEngineApiService();