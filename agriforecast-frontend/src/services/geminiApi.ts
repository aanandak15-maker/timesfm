/**
 * Google Gemini 2.0 Flash API Integration for Agricultural Intelligence
 * Provides AI-powered crop analysis, voice assistance, and market intelligence
 */

import { GoogleGenerativeAI } from '@google/generative-ai';

// API Configuration
const GEMINI_API_KEY = 'AIzaSyAmc78NU-vGwvjajje2YBD3LI2uYqub3tE';
const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

// Initialize Gemini 2.0 Flash model
const model = genAI.getGenerativeModel({ 
  model: "gemini-2.0-flash-exp",
  systemInstruction: getAgriculturistInstruction()
});

/**
 * System instruction for agricultural AI assistant
 */
function getAgriculturistInstruction(): string {
  return `
You are an expert agricultural AI assistant specializing in Indian farming conditions. Your expertise includes:

🌾 CROP DISEASE DIAGNOSIS:
- Identify diseases from photos with 95%+ accuracy
- Provide treatment recommendations in Hindi and English
- Consider local weather and soil conditions
- Suggest preventive measures

🌤️ WEATHER IMPACT ANALYSIS:
- Interpret weather data for farming decisions
- Predict weather impact on crops
- Provide irrigation and harvesting timing advice
- Consider monsoon patterns and seasonal variations

💰 MARKET INTELLIGENCE:
- Analyze commodity price trends
- Predict optimal selling times
- Consider government policies (MGNREGA, MSP, etc.)
- Provide regional market insights

🌱 FARMING BEST PRACTICES:
- Sustainable agriculture techniques
- Organic farming methods
- Water conservation strategies
- Soil health improvement
- Crop rotation planning

🎯 RISK ASSESSMENT:
- Climate risk evaluation
- Pest and disease outbreak prediction
- Market volatility analysis
- Financial impact assessment

Always provide:
✅ Actionable, farmer-friendly recommendations
✅ Local/regional agricultural context
✅ Preventive measures and long-term strategies
✅ Cost-effective solutions
✅ Environmentally sustainable practices
✅ Responses in both Hindi and English when requested
`;
}

/**
 * Interface for crop analysis results
 */
export interface CropAnalysisResult {
  disease_identified: string;
  confidence_score: number;
  symptoms: string[];
  treatment_recommendations: {
    immediate_actions: string[];
    preventive_measures: string[];
    timeline: string;
    cost_estimate: string;
  };
  alternative_treatments: string[];
  expected_recovery: string;
  follow_up_actions: string[];
  hindi_translation: {
    disease_name: string;
    treatment: string[];
    prevention: string[];
  };
}

/**
 * Interface for market intelligence
 */
export interface MarketIntelligence {
  current_price: number;
  price_trend: 'rising' | 'falling' | 'stable';
  price_prediction: {
    next_week: number;
    next_month: number;
    confidence: number;
  };
  market_factors: string[];
  recommendations: {
    sell_timing: string;
    hold_period: string;
    alternative_crops: string[];
  };
  government_policies: string[];
  regional_insights: string[];
}

/**
 * Interface for voice assistant response
 */
export interface VoiceAssistantResponse {
  text_response: string;
  hindi_response: string;
  audio_url?: string;
  follow_up_questions: string[];
  action_items: string[];
  confidence_score: number;
}

/**
 * Analyze crop disease from uploaded photo
 */
export async function analyzeCropDisease(
  imageFile: File,
  context: {
    crop_type: string;
    growth_stage: string;
    location: string;
    symptoms?: string;
  }
): Promise<CropAnalysisResult> {
  try {
    // Convert image to base64
    const imageData = await fileToBase64(imageFile);
    
    const prompt = `
Analyze this ${context.crop_type} crop photo for disease identification.

Context:
- Crop: ${context.crop_type}
- Growth Stage: ${context.growth_stage}
- Location: ${context.location}
- Symptoms: ${context.symptoms || 'Not specified'}

Please provide:
1. Disease identification with confidence score
2. Detailed symptoms observed
3. Immediate treatment recommendations
4. Preventive measures
5. Expected recovery timeline
6. Cost-effective alternatives
7. Follow-up actions
8. Hindi translations for key recommendations

Format response as JSON with the structure:
{
  "disease_identified": "disease name",
  "confidence_score": 0.95,
  "symptoms": ["symptom1", "symptom2"],
  "treatment_recommendations": {
    "immediate_actions": ["action1", "action2"],
    "preventive_measures": ["prevention1", "prevention2"],
    "timeline": "recovery timeline",
    "cost_estimate": "estimated cost"
  },
  "alternative_treatments": ["alt1", "alt2"],
  "expected_recovery": "recovery details",
  "follow_up_actions": ["follow1", "follow2"],
  "hindi_translation": {
    "disease_name": "रोग का नाम",
    "treatment": ["उपचार 1", "उपचार 2"],
    "prevention": ["रोकथाम 1", "रोकथाम 2"]
  }
}
`;

    const result = await model.generateContent([
      prompt,
      {
        inlineData: {
          data: imageData,
          mimeType: imageFile.type
        }
      }
    ]);

    const response = await result.response;
    const text = response.text();
    
    // Parse JSON response
    const analysisResult = JSON.parse(text) as CropAnalysisResult;
    
    console.log('🌾 Crop Analysis Result:', analysisResult);
    return analysisResult;
    
  } catch (error) {
    console.error('❌ Error analyzing crop disease:', error);
    throw new Error('Failed to analyze crop disease. Please try again.');
  }
}

/**
 * Get market intelligence for specific crop
 */
export async function getMarketIntelligence(
  cropType: string,
  region: string,
  timeRange: string = 'current_month'
): Promise<MarketIntelligence> {
  try {
    const prompt = `
Provide comprehensive market intelligence for ${cropType} in ${region} for ${timeRange}.

Include:
1. Current market price and trend analysis
2. Price predictions for next week and month
3. Key market factors affecting prices
4. Optimal selling timing recommendations
5. Alternative crop suggestions
6. Government policy impacts (MSP, MGNREGA, etc.)
7. Regional market insights

Consider:
- Seasonal demand patterns
- Weather impact on supply
- Government procurement policies
- Export/import trends
- Local market dynamics

Format as JSON:
{
  "current_price": 2500,
  "price_trend": "rising",
  "price_prediction": {
    "next_week": 2600,
    "next_month": 2800,
    "confidence": 0.85
  },
  "market_factors": ["factor1", "factor2"],
  "recommendations": {
    "sell_timing": "recommendation",
    "hold_period": "period",
    "alternative_crops": ["crop1", "crop2"]
  },
  "government_policies": ["policy1", "policy2"],
  "regional_insights": ["insight1", "insight2"]
}
`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    const marketData = JSON.parse(text) as MarketIntelligence;
    
    console.log('💰 Market Intelligence:', marketData);
    return marketData;
    
  } catch (error) {
    console.error('❌ Error getting market intelligence:', error);
    throw new Error('Failed to get market intelligence. Please try again.');
  }
}

/**
 * Process voice query from farmer
 */
export async function processVoiceQuery(
  query: string,
  farmerContext: {
    location: string;
    crop_type?: string;
    field_history?: any[];
    weather_conditions?: any;
    language: 'hindi' | 'english';
  }
): Promise<VoiceAssistantResponse> {
  try {
    const prompt = `
You are an agricultural AI assistant helping a farmer. Respond to their query in a helpful, actionable way.

Farmer Query: "${query}"

Farmer Context:
- Location: ${farmerContext.location}
- Crop Type: ${farmerContext.crop_type || 'Not specified'}
- Language Preference: ${farmerContext.language}
- Weather: ${JSON.stringify(farmerContext.weather_conditions || {})}

Provide:
1. Clear, actionable response in ${farmerContext.language}
2. Translation in the other language
3. Follow-up questions to gather more info
4. Specific action items
5. Confidence score for your response

Format as JSON:
{
  "text_response": "response in requested language",
  "hindi_response": "response in Hindi",
  "follow_up_questions": ["question1", "question2"],
  "action_items": ["action1", "action2"],
  "confidence_score": 0.9
}
`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    const voiceResponse = JSON.parse(text) as VoiceAssistantResponse;
    
    console.log('🎤 Voice Assistant Response:', voiceResponse);
    return voiceResponse;
    
  } catch (error) {
    console.error('❌ Error processing voice query:', error);
    throw new Error('Failed to process voice query. Please try again.');
  }
}

/**
 * Generate personalized farming recommendations
 */
export async function generateFarmingPlan(
  farmerProfile: {
    experience_level: 'beginner' | 'intermediate' | 'expert';
    farm_size: string;
    location: string;
    risk_tolerance: 'low' | 'medium' | 'high';
    objectives: string[];
    constraints: string[];
  }
): Promise<any> {
  try {
    const prompt = `
Create a comprehensive farming plan for this farmer profile:

Profile:
- Experience: ${farmerProfile.experience_level}
- Farm Size: ${farmerProfile.farm_size}
- Location: ${farmerProfile.location}
- Risk Tolerance: ${farmerProfile.risk_tolerance}
- Objectives: ${farmerProfile.objectives.join(', ')}
- Constraints: ${farmerProfile.constraints.join(', ')}

Generate:
1. Crop rotation calendar
2. Pest management schedule
3. Irrigation optimization plan
4. Financial projections
5. Risk mitigation strategies
6. Seasonal recommendations
7. Technology adoption plan

Format as comprehensive JSON with detailed sections.
`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    const farmingPlan = JSON.parse(text);
    
    console.log('🌱 Farming Plan Generated:', farmingPlan);
    return farmingPlan;
    
  } catch (error) {
    console.error('❌ Error generating farming plan:', error);
    throw new Error('Failed to generate farming plan. Please try again.');
  }
}

/**
 * Analyze multi-modal agricultural data
 */
export async function analyzeMultiModalData(
  data: {
    satellite_images?: any[];
    field_photos?: File[];
    soil_analysis?: any;
    weather_forecast?: any;
    farmer_notes?: string;
    market_data?: any;
  }
): Promise<any> {
  try {
    const prompt = `
Analyze this comprehensive agricultural dataset and provide integrated insights:

Data Available:
- Satellite Images: ${data.satellite_images?.length || 0} images
- Field Photos: ${data.field_photos?.length || 0} photos
- Soil Analysis: ${JSON.stringify(data.soil_analysis || {})}
- Weather Forecast: ${JSON.stringify(data.weather_forecast || {})}
- Farmer Notes: ${data.farmer_notes || 'None'}
- Market Data: ${JSON.stringify(data.market_data || {})}

Provide:
1. Integrated analysis combining all data sources
2. Yield prediction with confidence intervals
3. Risk assessment and mitigation strategies
4. Optimization recommendations
5. Actionable next steps
6. Timeline for implementation

Format as comprehensive JSON with detailed analysis.
`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    const analysis = JSON.parse(text);
    
    console.log('🔍 Multi-Modal Analysis:', analysis);
    return analysis;
    
  } catch (error) {
    console.error('❌ Error analyzing multi-modal data:', error);
    throw new Error('Failed to analyze multi-modal data. Please try again.');
  }
}

/**
 * Generate proactive farm monitoring alerts
 */
export async function generateProactiveAlerts(
  fieldData: {
    field_id: string;
    crop_type: string;
    growth_stage: string;
    weather_conditions: any;
    soil_conditions: any;
    pest_pressure: any;
    market_conditions: any;
  }
): Promise<any[]> {
  try {
    const prompt = `
Analyze this field data and generate proactive alerts for potential issues:

Field Data:
${JSON.stringify(fieldData, null, 2)}

Generate alerts for:
1. Pest pressure increasing
2. Weather risks (drought, flood, frost)
3. Irrigation needs
4. Market price volatility
5. Disease risk factors
6. Harvest timing optimization

Each alert should include:
- Alert type and severity
- Description of the issue
- Recommended actions
- Timeline for action
- Expected impact if not addressed

Format as JSON array of alert objects.
`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    const alerts = JSON.parse(text);
    
    console.log('🚨 Proactive Alerts Generated:', alerts);
    return alerts;
    
  } catch (error) {
    console.error('❌ Error generating proactive alerts:', error);
    throw new Error('Failed to generate proactive alerts. Please try again.');
  }
}

/**
 * Utility function to convert file to base64
 */
async function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const base64 = reader.result as string;
      // Remove data URL prefix
      const base64Data = base64.split(',')[1];
      resolve(base64Data);
    };
    reader.onerror = error => reject(error);
  });
}

/**
 * Check Gemini API health and availability
 */
export async function checkGeminiHealth(): Promise<{
  status: 'healthy' | 'error';
  message: string;
  capabilities: string[];
}> {
  try {
    const result = await model.generateContent('Hello, are you working?');
    const response = await result.response;
    const text = response.text();
    
    return {
      status: 'healthy',
      message: 'Gemini 2.0 Flash is operational',
      capabilities: [
        'Crop disease diagnosis',
        'Market intelligence',
        'Voice assistance',
        'Multi-modal analysis',
        'Proactive monitoring',
        'Farming recommendations'
      ]
    };
  } catch (error) {
    return {
      status: 'error',
      message: `Gemini API error: ${error}`,
      capabilities: []
    };
  }
}

export default {
  analyzeCropDisease,
  getMarketIntelligence,
  processVoiceQuery,
  generateFarmingPlan,
  analyzeMultiModalData,
  generateProactiveAlerts,
  checkGeminiHealth
};
