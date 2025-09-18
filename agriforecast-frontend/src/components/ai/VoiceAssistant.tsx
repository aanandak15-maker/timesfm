/**
 * AI Voice Assistant Component
 * Provides natural language interaction with Gemini 2.0 Flash
 */

import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Button,
  VStack,
  HStack,
  Text,
  Card,
  CardBody,
  CardHeader,
  Heading,
  IconButton,
  Tooltip,
  useToast,
  Badge,
  Alert,
  AlertIcon,
  AlertDescription,
  Spinner,
  Textarea,
  Select,
  Switch,
  FormControl,
  FormLabel
} from '@chakra-ui/react';
import { 
  Mic, 
  MicOff, 
  Volume2, 
  Send,
  MessageCircle,
  RefreshCw
} from 'lucide-react';
import { processVoiceQuery, type VoiceAssistantResponse } from '../../services/geminiApi';
import { generateAgriculturalVoiceResponse } from '../../services/elevenLabsApi';

interface VoiceAssistantProps {
  farmerContext?: {
    location: string;
    crop_type?: string;
    field_history?: any[];
    weather_conditions?: any;
  };
  onResponse?: (response: VoiceAssistantResponse) => void;
}

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  audio_url?: string;
  language: 'hindi' | 'english';
}

const VoiceAssistant: React.FC<VoiceAssistantProps> = ({
  farmerContext,
  onResponse
}) => {
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentQuery, setCurrentQuery] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState<'hindi' | 'english'>('hindi');
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [isRecording, setIsRecording] = useState(false);

  const recognitionRef = useRef<any>(null);
  const audioRef = useRef<HTMLAudioElement>(null);
  const toast = useToast();

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = selectedLanguage === 'hindi' ? 'hi-IN' : 'en-US';

      recognitionRef.current.onstart = () => {
        setIsListening(true);
        setIsRecording(true);
      };

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setCurrentQuery(transcript);
        setIsListening(false);
        setIsRecording(false);
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        setIsRecording(false);
        toast({
          title: 'Speech Recognition Error',
          description: 'Failed to recognize speech. Please try again.',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
        setIsRecording(false);
      };
    }
  }, [selectedLanguage, toast]);

  const startListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.start();
      } catch (error) {
        console.error('Error starting speech recognition:', error);
        toast({
          title: 'Microphone Error',
          description: 'Unable to access microphone. Please check permissions.',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      }
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  const processQuery = async (query: string) => {
    if (!query.trim()) return;

    setIsProcessing(true);
    
    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: query,
      timestamp: new Date(),
      language: selectedLanguage
    };
    
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await processVoiceQuery(query, {
        location: farmerContext?.location || 'India',
        crop_type: farmerContext?.crop_type,
        field_history: farmerContext?.field_history,
        weather_conditions: farmerContext?.weather_conditions,
        language: selectedLanguage
      });

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: selectedLanguage === 'hindi' ? response.hindi_response : response.text_response,
        timestamp: new Date(),
        language: selectedLanguage
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Generate voice response if enabled
      if (voiceEnabled && response.text_response) {
        try {
          const voiceResponse = await generateAgriculturalVoiceResponse(
            response.text_response,
            selectedLanguage,
            'general'
          );
          
          assistantMessage.audio_url = voiceResponse.audio_url;
          
          if (audioRef.current) {
            audioRef.current.src = voiceResponse.audio_url;
            audioRef.current.play();
            setIsPlayingAudio(true);
          }
        } catch (voiceError) {
          console.error('Voice generation error:', voiceError);
        }
      }

      if (onResponse) {
        onResponse(response);
      }

      setCurrentQuery('');

    } catch (error) {
      console.error('Query processing error:', error);
      toast({
        title: 'Processing Error',
        description: 'Failed to process your query. Please try again.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSendMessage = () => {
    if (currentQuery.trim()) {
      processQuery(currentQuery);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
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

  const clearChat = () => {
    setMessages([]);
    setCurrentQuery('');
  };

  const getLanguageFlag = (lang: 'hindi' | 'english') => {
    return lang === 'hindi' ? '🇮🇳' : '🇺🇸';
  };

  return (
    <Box p={6} maxW="4xl" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <Box textAlign="center">
          <Heading size="lg" color="green.600" mb={2}>
            🤖 AI Voice Assistant
          </Heading>
          <Text color="gray.600">
            Ask questions about farming, get instant AI-powered answers
          </Text>
        </Box>

        {/* Settings Panel */}
        <Card>
          <CardHeader>
            <Heading size="md">⚙️ Assistant Settings</Heading>
          </CardHeader>
          <CardBody>
            <HStack spacing={6} wrap="wrap">
              <FormControl display="flex" alignItems="center">
                <FormLabel htmlFor="language-select" mb="0">
                  Language:
                </FormLabel>
                <Select
                  id="language-select"
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value as 'hindi' | 'english')}
                  width="150px"
                >
                  <option value="hindi">🇮🇳 Hindi</option>
                  <option value="english">🇺🇸 English</option>
                </Select>
              </FormControl>

              <FormControl display="flex" alignItems="center">
                <FormLabel htmlFor="voice-enabled" mb="0">
                  Voice Response:
                </FormLabel>
                <Switch
                  id="voice-enabled"
                  isChecked={voiceEnabled}
                  onChange={(e) => setVoiceEnabled(e.target.checked)}
                  colorScheme="green"
                />
              </FormControl>

              <Button
                leftIcon={<RefreshCw />}
                onClick={clearChat}
                size="sm"
                variant="outline"
                colorScheme="gray"
              >
                Clear Chat
              </Button>
            </HStack>
          </CardBody>
        </Card>

        {/* Chat Messages */}
        <Card maxH="400px" overflowY="auto">
          <CardBody>
            <VStack spacing={4} align="stretch">
              {messages.length === 0 ? (
                <Box textAlign="center" py={8}>
                  <MessageCircle size={48} color="#68D391" />
                  <Text mt={2} color="gray.600">
                    Start a conversation with your AI farming assistant
                  </Text>
                  <Text fontSize="sm" color="gray.500">
                    Ask about crops, diseases, weather, or market prices
                  </Text>
                </Box>
              ) : (
                messages.map((message) => (
                  <Box
                    key={message.id}
                    alignSelf={message.type === 'user' ? 'flex-end' : 'flex-start'}
                    maxW="80%"
                  >
                    <Card
                      bg={message.type === 'user' ? 'blue.50' : 'green.50'}
                      borderColor={message.type === 'user' ? 'blue.200' : 'green.200'}
                    >
                      <CardBody p={3}>
                        <HStack justify="space-between" mb={2}>
                          <Badge
                            colorScheme={message.type === 'user' ? 'blue' : 'green'}
                            variant="subtle"
                          >
                            {message.type === 'user' ? 'You' : 'AI Assistant'}
                          </Badge>
                          <HStack spacing={2}>
                            <Text fontSize="xs" color="gray.500">
                              {getLanguageFlag(message.language)}
                            </Text>
                            <Text fontSize="xs" color="gray.500">
                              {message.timestamp.toLocaleTimeString()}
                            </Text>
                            {message.audio_url && voiceEnabled && (
                              <Tooltip label="Play audio">
                                <IconButton
                                  aria-label="Play audio"
                                  icon={<Volume2 />}
                                  size="xs"
                                  variant="ghost"
                                  onClick={() => {
                                    if (audioRef.current) {
                                      audioRef.current.src = message.audio_url!;
                                      audioRef.current.play();
                                    }
                                  }}
                                />
                              </Tooltip>
                            )}
                          </HStack>
                        </HStack>
                        <Text fontSize="sm">{message.content}</Text>
                      </CardBody>
                    </Card>
                  </Box>
                ))
              )}

              {isProcessing && (
                <Box alignSelf="flex-start">
                  <Card bg="gray.50">
                    <CardBody p={3}>
                      <HStack>
                        <Spinner size="sm" color="green.500" />
                        <Text fontSize="sm" color="gray.600">
                          AI is thinking...
                        </Text>
                      </HStack>
                    </CardBody>
                  </Card>
                </Box>
              )}
            </VStack>
          </CardBody>
        </Card>

        {/* Input Section */}
        <Card>
          <CardBody>
            <VStack spacing={4}>
              {/* Text Input */}
              <HStack width="100%" spacing={3}>
                <Textarea
                  value={currentQuery}
                  onChange={(e) => setCurrentQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={
                    selectedLanguage === 'hindi' 
                      ? 'अपना सवाल लिखें... (e.g., मेरी फसल में रोग दिख रहा है)'
                      : 'Type your question... (e.g., My crop is showing disease symptoms)'
                  }
                  resize="none"
                  rows={2}
                  isDisabled={isProcessing}
                />
                <VStack spacing={2}>
                  <Button
                    onClick={handleSendMessage}
                    leftIcon={<Send />}
                    colorScheme="green"
                    isDisabled={!currentQuery.trim() || isProcessing}
                    isLoading={isProcessing}
                  >
                    Send
                  </Button>
                </VStack>
              </HStack>

              {/* Voice Input */}
              <HStack spacing={4} justify="center">
                <Text fontSize="sm" color="gray.600">
                  Or use voice input:
                </Text>
                <Button
                  leftIcon={isListening ? <MicOff /> : <Mic />}
                  onClick={isListening ? stopListening : startListening}
                  colorScheme={isListening ? 'red' : 'blue'}
                  variant={isListening ? 'solid' : 'outline'}
                  isLoading={isRecording}
                  loadingText="Listening..."
                  isDisabled={isProcessing}
                >
                  {isListening ? 'Stop Listening' : 'Start Voice Input'}
                </Button>
              </HStack>

              {/* Quick Actions */}
              <HStack spacing={2} wrap="wrap" justify="center">
                <Text fontSize="sm" color="gray.600">Quick questions:</Text>
                {selectedLanguage === 'hindi' ? (
                  <>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setCurrentQuery('मेरी फसल में रोग दिख रहा है')}
                    >
                      रोग की जांच
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setCurrentQuery('आज का मौसम कैसा है')}
                    >
                      मौसम जानकारी
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setCurrentQuery('बाजार में कीमत कितनी है')}
                    >
                      बाजार कीमत
                    </Button>
                  </>
                ) : (
                  <>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setCurrentQuery('My crop is showing disease symptoms')}
                    >
                      Disease Check
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setCurrentQuery('What is today\'s weather')}
                    >
                      Weather Info
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setCurrentQuery('What are current market prices')}
                    >
                      Market Prices
                    </Button>
                  </>
                )}
              </HStack>
            </VStack>
          </CardBody>
        </Card>

        {/* Audio Player */}
        <audio
          ref={audioRef}
          onEnded={() => setIsPlayingAudio(false)}
          onError={() => {
            setIsPlayingAudio(false);
            toast({
              title: 'Audio Error',
              description: 'Failed to play audio response',
              status: 'error',
              duration: 3000,
              isClosable: true,
            });
          }}
        />

        {/* Farmer Context Display */}
        {farmerContext && (
          <Alert status="info" borderRadius="md">
            <AlertIcon />
            <AlertDescription>
              <Text fontSize="sm">
                <strong>Context:</strong> {farmerContext.location}
                {farmerContext.crop_type && ` • ${farmerContext.crop_type}`}
              </Text>
            </AlertDescription>
          </Alert>
        )}
      </VStack>
    </Box>
  );
};

export default VoiceAssistant;
