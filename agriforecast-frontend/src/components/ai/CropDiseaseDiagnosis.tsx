/**
 * AI-Powered Crop Disease Diagnosis Component
 * Uses Gemini 2.0 Flash for intelligent photo analysis
 */

import React, { useState, useRef } from 'react';
import {
  Box,
  Button,
  VStack,
  HStack,
  Text,
  Image,
  Progress,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Badge,
  Card,
  CardBody,
  CardHeader,
  Heading,
  Divider,
  IconButton,
  Tooltip,
  useToast,
  Spinner,
  Flex,
  Grid,
  GridItem
} from '@chakra-ui/react';
import { 
  Camera, 
  Upload, 
  Play, 
  Pause, 
  Volume2, 
  Download,
  CheckCircle,
  AlertTriangle,
  Info,
  RefreshCw
} from 'lucide-react';
import { analyzeCropDisease, CropAnalysisResult } from '../../services/geminiApi';
import { generateDiseaseDiagnosisVoice } from '../../services/elevenLabsApi';

interface CropDiseaseDiagnosisProps {
  fieldId?: string;
  onDiagnosisComplete?: (result: CropAnalysisResult) => void;
}

const CropDiseaseDiagnosis: React.FC<CropDiseaseDiagnosisProps> = ({
  fieldId,
  onDiagnosisComplete
}) => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<CropAnalysisResult | null>(null);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [cropContext, setCropContext] = useState({
    crop_type: '',
    growth_stage: '',
    location: '',
    symptoms: ''
  });

  const fileInputRef = useRef<HTMLInputElement>(null);
  const audioRef = useRef<HTMLAudioElement>(null);
  const toast = useToast();

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCameraCapture = () => {
    // This would integrate with device camera
    // For now, we'll trigger file input
    fileInputRef.current?.click();
  };

  const analyzeImage = async () => {
    if (!selectedImage) {
      toast({
        title: 'No image selected',
        description: 'Please select an image to analyze',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsAnalyzing(true);
    try {
      const result = await analyzeCropDisease(selectedImage, cropContext);
      setAnalysisResult(result);
      
      if (onDiagnosisComplete) {
        onDiagnosisComplete(result);
      }

      toast({
        title: 'Analysis Complete',
        description: `Disease identified: ${result.disease_identified}`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

    } catch (error) {
      console.error('Analysis error:', error);
      toast({
        title: 'Analysis Failed',
        description: 'Failed to analyze the image. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const generateVoiceExplanation = async () => {
    if (!analysisResult) return;

    try {
      const voiceResponse = await generateDiseaseDiagnosisVoice({
        disease_name: analysisResult.disease_identified,
        treatment: analysisResult.treatment_recommendations.immediate_actions,
        prevention: analysisResult.treatment_recommendations.preventive_measures,
        language: 'hindi'
      });

      setAudioUrl(voiceResponse.audio_url);
      
      if (audioRef.current) {
        audioRef.current.src = voiceResponse.audio_url;
        audioRef.current.play();
        setIsPlayingAudio(true);
      }

    } catch (error) {
      console.error('Voice generation error:', error);
      toast({
        title: 'Voice Generation Failed',
        description: 'Failed to generate voice explanation',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const toggleAudio = () => {
    if (audioRef.current) {
      if (isPlayingAudio) {
        audioRef.current.pause();
        setIsPlayingAudio(false);
      } else {
        audioRef.current.play();
        setIsPlayingAudio(true);
      }
    }
  };

  const resetAnalysis = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setAnalysisResult(null);
    setAudioUrl(null);
    setIsPlayingAudio(false);
    setCropContext({
      crop_type: '',
      growth_stage: '',
      location: '',
      symptoms: ''
    });
  };

  return (
    <Box p={6} maxW="4xl" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <Box textAlign="center">
          <Heading size="lg" color="green.600" mb={2}>
            🌾 AI Crop Disease Diagnosis
          </Heading>
          <Text color="gray.600">
            Upload a photo of your crop to get instant AI-powered disease diagnosis
          </Text>
        </Box>

        {/* Image Upload Section */}
        <Card>
          <CardHeader>
            <Heading size="md">📸 Upload Crop Photo</Heading>
          </CardHeader>
          <CardBody>
            <VStack spacing={4}>
              {!imagePreview ? (
                <Box
                  border="2px dashed"
                  borderColor="gray.300"
                  borderRadius="lg"
                  p={8}
                  textAlign="center"
                  cursor="pointer"
                  _hover={{ borderColor: "green.400" }}
                  onClick={handleCameraCapture}
                >
                  <Camera size={48} color="#68D391" />
                  <Text mt={2} color="gray.600">
                    Click to capture or upload photo
                  </Text>
                  <Text fontSize="sm" color="gray.500">
                    Supports JPG, PNG formats
                  </Text>
                </Box>
              ) : (
                <Box position="relative">
                  <Image
                    src={imagePreview}
                    alt="Crop photo"
                    maxH="300px"
                    borderRadius="lg"
                    objectFit="cover"
                  />
                  <IconButton
                    aria-label="Remove image"
                    icon={<RefreshCw />}
                    size="sm"
                    position="absolute"
                    top={2}
                    right={2}
                    colorScheme="red"
                    variant="solid"
                    onClick={resetAnalysis}
                  />
                </Box>
              )}

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                style={{ display: 'none' }}
              />

              <HStack spacing={4}>
                <Button
                  leftIcon={<Camera />}
                  onClick={handleCameraCapture}
                  colorScheme="green"
                  variant="outline"
                >
                  Take Photo
                </Button>
                <Button
                  leftIcon={<Upload />}
                  onClick={() => fileInputRef.current?.click()}
                  colorScheme="blue"
                  variant="outline"
                >
                  Upload Image
                </Button>
              </HStack>
            </VStack>
          </CardBody>
        </Card>

        {/* Crop Context Form */}
        <Card>
          <CardHeader>
            <Heading size="md">📋 Crop Information</Heading>
          </CardHeader>
          <CardBody>
            <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
              <GridItem>
                <Text mb={2} fontWeight="medium">Crop Type</Text>
                <input
                  type="text"
                  placeholder="e.g., Rice, Wheat, Corn"
                  value={cropContext.crop_type}
                  onChange={(e) => setCropContext({...cropContext, crop_type: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #E2E8F0',
                    borderRadius: '6px',
                    fontSize: '14px'
                  }}
                />
              </GridItem>
              <GridItem>
                <Text mb={2} fontWeight="medium">Growth Stage</Text>
                <input
                  type="text"
                  placeholder="e.g., Seedling, Flowering, Maturity"
                  value={cropContext.growth_stage}
                  onChange={(e) => setCropContext({...cropContext, growth_stage: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #E2E8F0',
                    borderRadius: '6px',
                    fontSize: '14px'
                  }}
                />
              </GridItem>
              <GridItem>
                <Text mb={2} fontWeight="medium">Location</Text>
                <input
                  type="text"
                  placeholder="e.g., Punjab, India"
                  value={cropContext.location}
                  onChange={(e) => setCropContext({...cropContext, location: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #E2E8F0',
                    borderRadius: '6px',
                    fontSize: '14px'
                  }}
                />
              </GridItem>
              <GridItem colSpan={2}>
                <Text mb={2} fontWeight="medium">Symptoms (Optional)</Text>
                <textarea
                  placeholder="Describe any visible symptoms or concerns..."
                  value={cropContext.symptoms}
                  onChange={(e) => setCropContext({...cropContext, symptoms: e.target.value})}
                  rows={3}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #E2E8F0',
                    borderRadius: '6px',
                    fontSize: '14px',
                    resize: 'vertical'
                  }}
                />
              </GridItem>
            </Grid>
          </CardBody>
        </Card>

        {/* Analysis Button */}
        <Button
          onClick={analyzeImage}
          isLoading={isAnalyzing}
          loadingText="Analyzing..."
          colorScheme="green"
          size="lg"
          leftIcon={<CheckCircle />}
          isDisabled={!selectedImage}
        >
          {isAnalyzing ? 'AI Analyzing...' : 'Analyze Disease'}
        </Button>

        {/* Analysis Results */}
        {analysisResult && (
          <Card>
            <CardHeader>
              <HStack justify="space-between">
                <Heading size="md">🔍 Analysis Results</Heading>
                <HStack>
                  <Badge
                    colorScheme={analysisResult.confidence_score > 0.8 ? 'green' : 'yellow'}
                    fontSize="sm"
                  >
                    {Math.round(analysisResult.confidence_score * 100)}% Confidence
                  </Badge>
                  <Tooltip label="Listen to Hindi explanation">
                    <IconButton
                      aria-label="Play voice explanation"
                      icon={isPlayingAudio ? <Pause /> : <Volume2 />}
                      onClick={toggleAudio}
                      colorScheme="blue"
                      variant="outline"
                    />
                  </Tooltip>
                </HStack>
              </HStack>
            </CardHeader>
            <CardBody>
              <VStack spacing={4} align="stretch">
                {/* Disease Identification */}
                <Alert status="info" borderRadius="md">
                  <AlertIcon />
                  <Box>
                    <AlertTitle>Disease Identified: {analysisResult.disease_identified}</AlertTitle>
                    <AlertDescription>
                      {analysisResult.hindi_translation.disease_name}
                    </AlertDescription>
                  </Box>
                </Alert>

                {/* Symptoms */}
                <Box>
                  <Text fontWeight="bold" mb={2}>🔍 Observed Symptoms:</Text>
                  <HStack wrap="wrap" spacing={2}>
                    {analysisResult.symptoms.map((symptom, index) => (
                      <Badge key={index} colorScheme="orange" variant="subtle">
                        {symptom}
                      </Badge>
                    ))}
                  </HStack>
                </Box>

                {/* Treatment Recommendations */}
                <Box>
                  <Text fontWeight="bold" mb={2}>💊 Immediate Treatment:</Text>
                  <VStack align="stretch" spacing={2}>
                    {analysisResult.treatment_recommendations.immediate_actions.map((action, index) => (
                      <HStack key={index} p={3} bg="red.50" borderRadius="md">
                        <CheckCircle size={16} color="#E53E3E" />
                        <Text fontSize="sm">{action}</Text>
                      </HStack>
                    ))}
                  </VStack>
                </Box>

                {/* Preventive Measures */}
                <Box>
                  <Text fontWeight="bold" mb={2}>🛡️ Prevention Measures:</Text>
                  <VStack align="stretch" spacing={2}>
                    {analysisResult.treatment_recommendations.preventive_measures.map((measure, index) => (
                      <HStack key={index} p={3} bg="green.50" borderRadius="md">
                        <CheckCircle size={16} color="#38A169" />
                        <Text fontSize="sm">{measure}</Text>
                      </HStack>
                    ))}
                  </VStack>
                </Box>

                {/* Timeline and Cost */}
                <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
                  <GridItem>
                    <Text fontWeight="bold" mb={2}>⏰ Recovery Timeline:</Text>
                    <Text fontSize="sm" color="gray.600">
                      {analysisResult.treatment_recommendations.timeline}
                    </Text>
                  </GridItem>
                  <GridItem>
                    <Text fontWeight="bold" mb={2}>💰 Cost Estimate:</Text>
                    <Text fontSize="sm" color="gray.600">
                      {analysisResult.treatment_recommendations.cost_estimate}
                    </Text>
                  </GridItem>
                </Grid>

                {/* Alternative Treatments */}
                {analysisResult.alternative_treatments.length > 0 && (
                  <Box>
                    <Text fontWeight="bold" mb={2}>🔄 Alternative Treatments:</Text>
                    <VStack align="stretch" spacing={1}>
                      {analysisResult.alternative_treatments.map((treatment, index) => (
                        <Text key={index} fontSize="sm" color="gray.600">
                          • {treatment}
                        </Text>
                      ))}
                    </VStack>
                  </Box>
                )}

                {/* Follow-up Actions */}
                <Box>
                  <Text fontWeight="bold" mb={2}>📋 Follow-up Actions:</Text>
                  <VStack align="stretch" spacing={1}>
                    {analysisResult.follow_up_actions.map((action, index) => (
                      <HStack key={index}>
                        <Text fontSize="sm">•</Text>
                        <Text fontSize="sm">{action}</Text>
                      </HStack>
                    ))}
                  </VStack>
                </Box>

                {/* Hindi Translation */}
                <Box p={4} bg="blue.50" borderRadius="md">
                  <Text fontWeight="bold" mb={2}>🇮🇳 Hindi Summary:</Text>
                  <VStack align="stretch" spacing={2}>
                    <Text fontSize="sm">
                      <strong>रोग:</strong> {analysisResult.hindi_translation.disease_name}
                    </Text>
                    <Text fontSize="sm">
                      <strong>उपचार:</strong> {analysisResult.hindi_translation.treatment.join(', ')}
                    </Text>
                    <Text fontSize="sm">
                      <strong>रोकथाम:</strong> {analysisResult.hindi_translation.prevention.join(', ')}
                    </Text>
                  </VStack>
                </Box>
              </VStack>
            </CardBody>
          </Card>
        )}

        {/* Audio Player */}
        <audio
          ref={audioRef}
          onEnded={() => setIsPlayingAudio(false)}
          onError={() => {
            setIsPlayingAudio(false);
            toast({
              title: 'Audio Error',
              description: 'Failed to play audio explanation',
              status: 'error',
              duration: 3000,
              isClosable: true,
            });
          }}
        />
      </VStack>
    </Box>
  );
};

export default CropDiseaseDiagnosis;
