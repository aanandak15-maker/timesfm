// Hindi and English translations for farmer interface

export const translations = {
  en: {
    // Navigation
    dashboard: 'Dashboard',
    fields: 'Fields',
    analytics: 'Analytics',
    settings: 'Settings',
    
    // Soil Analysis
    soilAnalysis: 'Soil Analysis',
    phLevel: 'pH Level',
    organicCarbon: 'Organic Carbon',
    nitrogen: 'Nitrogen',
    phosphorus: 'Phosphorus',
    potassium: 'Potassium',
    moisture: 'Moisture',
    
    // Health Status
    excellent: 'Excellent',
    good: 'Good',
    fair: 'Fair',
    poor: 'Poor',
    needsAttention: 'Needs Attention',
    
    // Actions
    refresh: 'Refresh',
    save: 'Save',
    cancel: 'Cancel',
    submit: 'Submit',
    
    // Weather
    weather: 'Weather',
    temperature: 'Temperature',
    humidity: 'Humidity',
    rainfall: 'Rainfall',
    windSpeed: 'Wind Speed',
    
    // Crops
    crop: 'Crop',
    rice: 'Rice',
    wheat: 'Wheat',
    corn: 'Corn',
    soybean: 'Soybean',
    
    // Time
    today: 'Today',
    tomorrow: 'Tomorrow',
    thisWeek: 'This Week',
    thisMonth: 'This Month',
    
    // Status
    loading: 'Loading...',
    error: 'Error',
    success: 'Success',
    warning: 'Warning',
    
    // Recommendations
    recommendations: 'Recommendations',
    addLime: 'Add lime to increase pH',
    addOrganicMatter: 'Add organic matter',
    applyFertilizer: 'Apply fertilizer',
    irrigate: 'Irrigate the field',
    
    // Units
    mgPerKg: 'mg/kg',
    percent: '%',
    celsius: '°C',
    mm: 'mm',
    kmh: 'km/h'
  },
  
  hi: {
    // Navigation
    dashboard: 'डैशबोर्ड',
    fields: 'खेत',
    analytics: 'विश्लेषण',
    settings: 'सेटिंग्स',
    
    // Soil Analysis
    soilAnalysis: 'मिट्टी का विश्लेषण',
    phLevel: 'pH स्तर',
    organicCarbon: 'कार्बन',
    nitrogen: 'नाइट्रोजन',
    phosphorus: 'फॉस्फोरस',
    potassium: 'पोटैशियम',
    moisture: 'नमी',
    
    // Health Status
    excellent: 'उत्तम',
    good: 'अच्छा',
    fair: 'ठीक',
    poor: 'खराब',
    needsAttention: 'ध्यान दें',
    
    // Actions
    refresh: 'रिफ्रेश करें',
    save: 'सेव करें',
    cancel: 'रद्द करें',
    submit: 'जमा करें',
    
    // Weather
    weather: 'मौसम',
    temperature: 'तापमान',
    humidity: 'नमी',
    rainfall: 'बारिश',
    windSpeed: 'हवा की गति',
    
    // Crops
    crop: 'फसल',
    rice: 'चावल',
    wheat: 'गेहूं',
    corn: 'मक्का',
    soybean: 'सोयाबीन',
    
    // Time
    today: 'आज',
    tomorrow: 'कल',
    thisWeek: 'इस सप्ताह',
    thisMonth: 'इस महीने',
    
    // Status
    loading: 'लोड हो रहा है...',
    error: 'त्रुटि',
    success: 'सफल',
    warning: 'चेतावनी',
    
    // Recommendations
    recommendations: 'सुझाव',
    addLime: 'pH बढ़ाने के लिए चूना डालें',
    addOrganicMatter: 'जैविक खाद डालें',
    applyFertilizer: 'उर्वरक डालें',
    irrigate: 'खेत की सिंचाई करें',
    
    // Units
    mgPerKg: 'मिलीग्राम/किलो',
    percent: '%',
    celsius: '°से',
    mm: 'मिमी',
    kmh: 'किमी/घंटा'
  }
}

export type Language = 'en' | 'hi'
export type TranslationKey = keyof typeof translations.en

export const getTranslation = (key: TranslationKey, language: Language = 'hi'): string => {
  return translations[language][key] || translations.en[key] || key
}

export const getCurrentLanguage = (): Language => {
  const saved = localStorage.getItem('agriforecast-language')
  return (saved as Language) || 'hi'
}

export const setLanguage = (language: Language): void => {
  localStorage.setItem('agriforecast-language', language)
}

export default translations
