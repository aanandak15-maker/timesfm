/**
 * ElevenLabs Voice API Integration for Natural Voice Synthesis
 * Provides high-quality voice responses for agricultural AI assistant
 */

// ElevenLabs API Configuration
const ELEVENLABS_API_KEY = 'sk_beb9c483b360922f206f4c660cff5af2abe27f3e706ff8a5';
const ELEVENLABS_BASE_URL = 'https://api.elevenlabs.io/v1';

/**
 * Voice settings for different languages and contexts
 */
export const VOICE_SETTINGS = {
  hindi: {
    voice_id: 'pNInz6obpgDQGcFmaJgB', // Adam voice for Hindi
    stability: 0.75,
    similarity_boost: 0.75,
    style: 0.0,
    use_speaker_boost: true
  },
  english: {
    voice_id: 'EXAVITQu4vr4xnSDxMaL', // Bella voice for English
    stability: 0.75,
    similarity_boost: 0.75,
    style: 0.0,
    use_speaker_boost: true
  },
  agricultural_expert: {
    voice_id: 'VR6AewLTigWG4xSOukaG', // Arnold voice for expert advice
    stability: 0.8,
    similarity_boost: 0.8,
    style: 0.2,
    use_speaker_boost: true
  }
};

/**
 * Interface for voice synthesis request
 */
export interface VoiceSynthesisRequest {
  text: string;
  language: 'hindi' | 'english' | 'agricultural_expert';
  voice_settings?: any;
  model_id?: string;
}

/**
 * Interface for voice synthesis response
 */
export interface VoiceSynthesisResponse {
  audio_url: string;
  audio_data?: ArrayBuffer;
  duration: number;
  voice_id: string;
  language: string;
}

/**
 * Convert text to speech using ElevenLabs
 */
export async function textToSpeech(
  request: VoiceSynthesisRequest
): Promise<VoiceSynthesisResponse> {
  try {
    const voiceConfig = VOICE_SETTINGS[request.language];
    const modelId = request.model_id || 'eleven_multilingual_v2';

    const response = await fetch(`${ELEVENLABS_BASE_URL}/text-to-speech/${voiceConfig.voice_id}`, {
      method: 'POST',
      headers: {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': ELEVENLABS_API_KEY
      },
      body: JSON.stringify({
        text: request.text,
        model_id: modelId,
        voice_settings: {
          stability: voiceConfig.stability,
          similarity_boost: voiceConfig.similarity_boost,
          style: voiceConfig.style,
          use_speaker_boost: voiceConfig.use_speaker_boost
        }
      })
    });

    if (!response.ok) {
      throw new Error(`ElevenLabs API error: ${response.status} ${response.statusText}`);
    }

    const audioData = await response.arrayBuffer();
    
    // Create blob URL for audio playback
    const audioBlob = new Blob([audioData], { type: 'audio/mpeg' });
    const audioUrl = URL.createObjectURL(audioBlob);

    return {
      audio_url: audioUrl,
      audio_data: audioData,
      duration: audioData.byteLength / 16000, // Approximate duration
      voice_id: voiceConfig.voice_id,
      language: request.language
    };

  } catch (error) {
    console.error('❌ Error in text-to-speech conversion:', error);
    throw new Error('Failed to convert text to speech. Please try again.');
  }
}

/**
 * Generate voice response for agricultural advice
 */
export async function generateAgriculturalVoiceResponse(
  text: string,
  language: 'hindi' | 'english' = 'hindi',
  context: 'general' | 'expert' | 'emergency' = 'general'
): Promise<VoiceSynthesisResponse> {
  try {
    // Select appropriate voice based on context
    let voiceType: 'hindi' | 'english' | 'agricultural_expert';
    
    if (context === 'expert') {
      voiceType = 'agricultural_expert';
    } else {
      voiceType = language;
    }

    // Enhance text for better voice synthesis
    const enhancedText = enhanceTextForVoice(text, context);

    return await textToSpeech({
      text: enhancedText,
      language: voiceType
    });

  } catch (error) {
    console.error('❌ Error generating agricultural voice response:', error);
    throw new Error('Failed to generate voice response. Please try again.');
  }
}

/**
 * Enhance text for better voice synthesis
 */
function enhanceTextForVoice(text: string, context: string): string {
  let enhancedText = text;

  // Add appropriate pauses and emphasis for agricultural content
  if (context === 'expert') {
    enhancedText = `Agricultural Expert Advice: ${text}`;
  } else if (context === 'emergency') {
    enhancedText = `Important Alert: ${text}`;
  }

  // Add natural pauses for better comprehension
  enhancedText = enhancedText
    .replace(/\./g, '. ')
    .replace(/:/g, ': ')
    .replace(/;/g, '; ')
    .replace(/\n/g, ' ');

  return enhancedText;
}

/**
 * Generate voice for crop disease diagnosis
 */
export async function generateDiseaseDiagnosisVoice(
  diagnosis: {
    disease_name: string;
    treatment: string[];
    prevention: string[];
    language: 'hindi' | 'english';
  }
): Promise<VoiceSynthesisResponse> {
  try {
    const { disease_name, treatment, prevention, language } = diagnosis;
    
    let voiceText: string;
    
    if (language === 'hindi') {
      voiceText = `
आपकी फसल में ${disease_name} रोग की पहचान हुई है।
उपचार के लिए: ${treatment.join(', ')}
रोकथाम के लिए: ${prevention.join(', ')}
कृपया तुरंत कार्यवाही करें।
      `;
    } else {
      voiceText = `
Your crop has been diagnosed with ${disease_name}.
For treatment: ${treatment.join(', ')}
For prevention: ${prevention.join(', ')}
Please take immediate action.
      `;
    }

    return await generateAgriculturalVoiceResponse(
      voiceText,
      language,
      'expert'
    );

  } catch (error) {
    console.error('❌ Error generating disease diagnosis voice:', error);
    throw new Error('Failed to generate disease diagnosis voice. Please try again.');
  }
}

/**
 * Generate voice for market intelligence
 */
export async function generateMarketIntelligenceVoice(
  marketData: {
    crop_type: string;
    current_price: number;
    trend: string;
    recommendation: string;
    language: 'hindi' | 'english';
  }
): Promise<VoiceSynthesisResponse> {
  try {
    const { crop_type, current_price, trend, recommendation, language } = marketData;
    
    let voiceText: string;
    
    if (language === 'hindi') {
      voiceText = `
${crop_type} की वर्तमान कीमत ${current_price} रुपये प्रति क्विंटल है।
बाजार में ${trend} की प्रवृत्ति है।
सुझाव: ${recommendation}
      `;
    } else {
      voiceText = `
Current price of ${crop_type} is ${current_price} rupees per quintal.
Market trend is ${trend}.
Recommendation: ${recommendation}
      `;
    }

    return await generateAgriculturalVoiceResponse(
      voiceText,
      language,
      'general'
    );

  } catch (error) {
    console.error('❌ Error generating market intelligence voice:', error);
    throw new Error('Failed to generate market intelligence voice. Please try again.');
  }
}

/**
 * Generate voice for weather alerts
 */
export async function generateWeatherAlertVoice(
  alert: {
    alert_type: string;
    severity: 'low' | 'medium' | 'high';
    message: string;
    language: 'hindi' | 'english';
  }
): Promise<VoiceSynthesisResponse> {
  try {
    const { alert_type, severity, message, language } = alert;
    
    let voiceText: string;
    
    if (language === 'hindi') {
      const severityText = severity === 'high' ? 'उच्च' : severity === 'medium' ? 'मध्यम' : 'निम्न';
      voiceText = `
मौसम चेतावनी: ${alert_type}
गंभीरता: ${severityText}
संदेश: ${message}
कृपया सावधानी बरतें।
      `;
    } else {
      voiceText = `
Weather Alert: ${alert_type}
Severity: ${severity}
Message: ${message}
Please take precautions.
      `;
    }

    return await generateAgriculturalVoiceResponse(
      voiceText,
      language,
      severity === 'high' ? 'emergency' : 'general'
    );

  } catch (error) {
    console.error('❌ Error generating weather alert voice:', error);
    throw new Error('Failed to generate weather alert voice. Please try again.');
  }
}

/**
 * Generate voice for farming recommendations
 */
export async function generateFarmingRecommendationVoice(
  recommendation: {
    title: string;
    description: string;
    actions: string[];
    language: 'hindi' | 'english';
  }
): Promise<VoiceSynthesisResponse> {
  try {
    const { title, description, actions, language } = recommendation;
    
    let voiceText: string;
    
    if (language === 'hindi') {
      voiceText = `
कृषि सुझाव: ${title}
विवरण: ${description}
कार्य: ${actions.join(', ')}
      `;
    } else {
      voiceText = `
Farming Recommendation: ${title}
Description: ${description}
Actions: ${actions.join(', ')}
      `;
    }

    return await generateAgriculturalVoiceResponse(
      voiceText,
      language,
      'expert'
    );

  } catch (error) {
    console.error('❌ Error generating farming recommendation voice:', error);
    throw new Error('Failed to generate farming recommendation voice. Please try again.');
  }
}

/**
 * Check ElevenLabs API health
 */
export async function checkElevenLabsHealth(): Promise<{
  status: 'healthy' | 'error';
  message: string;
  available_voices: number;
}> {
  try {
    const response = await fetch(`${ELEVENLABS_BASE_URL}/voices`, {
      headers: {
        'xi-api-key': ELEVENLABS_API_KEY
      }
    });

    if (!response.ok) {
      throw new Error(`ElevenLabs API error: ${response.status}`);
    }

    const data = await response.json();
    
    return {
      status: 'healthy',
      message: 'ElevenLabs API is operational',
      available_voices: data.voices?.length || 0
    };

  } catch (error) {
    return {
      status: 'error',
      message: `ElevenLabs API error: ${error}`,
      available_voices: 0
    };
  }
}

/**
 * Get available voices from ElevenLabs
 */
export async function getAvailableVoices(): Promise<any[]> {
  try {
    const response = await fetch(`${ELEVENLABS_BASE_URL}/voices`, {
      headers: {
        'xi-api-key': ELEVENLABS_API_KEY
      }
    });

    if (!response.ok) {
      throw new Error(`ElevenLabs API error: ${response.status}`);
    }

    const data = await response.json();
    return data.voices || [];

  } catch (error) {
    console.error('❌ Error fetching available voices:', error);
    return [];
  }
}

export default {
  textToSpeech,
  generateAgriculturalVoiceResponse,
  generateDiseaseDiagnosisVoice,
  generateMarketIntelligenceVoice,
  generateWeatherAlertVoice,
  generateFarmingRecommendationVoice,
  checkElevenLabsHealth,
  getAvailableVoices
};
