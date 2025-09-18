/**
 * AI Market Intelligence Component
 * Provides intelligent market analysis and price predictions
 */

import React, { useState, useEffect } from 'react';
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
  Badge,
  Alert,
  AlertIcon,
  AlertDescription,
  Grid,
  GridItem,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  IconButton,
  Tooltip,
  useToast,
  Spinner,
  Select,
  FormControl,
  FormLabel,
} from '@chakra-ui/react';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  BarChart3, 
  Volume2,
  Download,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  Info
} from 'lucide-react';
import { getMarketIntelligence, type MarketIntelligence } from '../../services/geminiApi';
import { generateMarketIntelligenceVoice } from '../../services/elevenLabsApi';

interface MarketIntelligenceProps {
  selectedCrop?: string;
  selectedRegion?: string;
  onIntelligenceUpdate?: (data: MarketIntelligence) => void;
}

const CROP_OPTIONS = [
  'Rice', 'Wheat', 'Corn', 'Soybean', 'Cotton', 'Sugarcane',
  'Potato', 'Tomato', 'Onion', 'Chili', 'Turmeric', 'Ginger'
];

const REGION_OPTIONS = [
  'Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Maharashtra',
  'Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'West Bengal', 'Bihar',
  'Rajasthan', 'Gujarat', 'Odisha', 'Assam', 'Kerala'
];

const MarketIntelligenceComponent: React.FC<MarketIntelligenceProps> = ({
  selectedCrop,
  selectedRegion,
  onIntelligenceUpdate
}) => {
  const [crop, setCrop] = useState(selectedCrop || 'Rice');
  const [region, setRegion] = useState(selectedRegion || 'Punjab');
  const [timeRange, setTimeRange] = useState('current_month');
  const [isLoading, setIsLoading] = useState(false);
  const [marketData, setMarketData] = useState<MarketIntelligence | null>(null);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const toast = useToast();

  // Load market data on component mount or when parameters change
  useEffect(() => {
    if (crop && region) {
      loadMarketIntelligence();
    }
  }, [crop, region, timeRange]);

  const loadMarketIntelligence = async () => {
    setIsLoading(true);
    try {
      const data = await getMarketIntelligence(crop, region, timeRange);
      setMarketData(data);
      
      if (onIntelligenceUpdate) {
        onIntelligenceUpdate(data);
      }

      toast({
        title: 'Market Intelligence Updated',
        description: `Latest data for ${crop} in ${region}`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });

    } catch (error) {
      console.error('Market intelligence error:', error);
      toast({
        title: 'Market Data Error',
        description: 'Failed to load market intelligence. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const generateVoiceReport = async () => {
    if (!marketData) return;

    try {
      const voiceResponse = await generateMarketIntelligenceVoice({
        crop_type: crop,
        current_price: marketData.current_price,
        trend: marketData.price_trend,
        recommendation: marketData.recommendations.sell_timing,
        language: 'hindi'
      });

      // setAudioUrl(voiceResponse.audio_url);
      
      const audio = new Audio(voiceResponse.audio_url);
      audio.play();
      setIsPlayingAudio(true);

      audio.onended = () => setIsPlayingAudio(false);

    } catch (error) {
      console.error('Voice generation error:', error);
      toast({
        title: 'Voice Generation Failed',
        description: 'Failed to generate voice report',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'rising':
        return <TrendingUp color="#38A169" />;
      case 'falling':
        return <TrendingDown color="#E53E3E" />;
      default:
        return <BarChart3 color="#3182CE" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'rising':
        return 'green';
      case 'falling':
        return 'red';
      default:
        return 'blue';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'green';
    if (confidence >= 0.6) return 'yellow';
    return 'red';
  };

  return (
    <Box p={6} maxW="6xl" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <Box textAlign="center">
          <Heading size="lg" color="green.600" mb={2}>
            💰 AI Market Intelligence
          </Heading>
          <Text color="gray.600">
            Get intelligent market analysis and price predictions for your crops
          </Text>
        </Box>

        {/* Controls */}
        <Card>
          <CardHeader>
            <Heading size="md">📊 Market Analysis Settings</Heading>
          </CardHeader>
          <CardBody>
            <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
              <GridItem>
                <FormControl>
                  <FormLabel>Crop Type</FormLabel>
                  <Select value={crop} onChange={(e) => setCrop(e.target.value)}>
                    {CROP_OPTIONS.map((cropOption) => (
                      <option key={cropOption} value={cropOption}>
                        {cropOption}
                      </option>
                    ))}
                  </Select>
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Region</FormLabel>
                  <Select value={region} onChange={(e) => setRegion(e.target.value)}>
                    {REGION_OPTIONS.map((regionOption) => (
                      <option key={regionOption} value={regionOption}>
                        {regionOption}
                      </option>
                    ))}
                  </Select>
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Time Range</FormLabel>
                  <Select value={timeRange} onChange={(e) => setTimeRange(e.target.value)}>
                    <option value="current_week">This Week</option>
                    <option value="current_month">This Month</option>
                    <option value="last_3_months">Last 3 Months</option>
                    <option value="last_6_months">Last 6 Months</option>
                  </Select>
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Actions</FormLabel>
                  <HStack spacing={2}>
                    <Button
                      onClick={loadMarketIntelligence}
                      isLoading={isLoading}
                      leftIcon={<RefreshCw />}
                      colorScheme="green"
                      size="sm"
                    >
                      Refresh
                    </Button>
                    {marketData && (
                      <Tooltip label="Listen to market report">
                        <IconButton
                          aria-label="Play voice report"
                          icon={<Volume2 />}
                          onClick={generateVoiceReport}
                          colorScheme="blue"
                          variant="outline"
                          size="sm"
                          isLoading={isPlayingAudio}
                        />
                      </Tooltip>
                    )}
                  </HStack>
                </FormControl>
              </GridItem>
            </Grid>
          </CardBody>
        </Card>

        {/* Loading State */}
        {isLoading && (
          <Card>
            <CardBody textAlign="center" py={8}>
              <Spinner size="lg" color="green.500" />
              <Text mt={4} color="gray.600">
                Analyzing market data for {crop} in {region}...
              </Text>
            </CardBody>
          </Card>
        )}

        {/* Market Intelligence Results */}
        {marketData && !isLoading && (
          <VStack spacing={6} align="stretch">
            {/* Price Overview */}
            <Card>
              <CardHeader>
                <HStack justify="space-between">
                  <Heading size="md">📈 Price Overview</Heading>
                  <Badge colorScheme={getTrendColor(marketData.price_trend)} size="lg">
                    {marketData.price_trend.toUpperCase()}
                  </Badge>
                </HStack>
              </CardHeader>
              <CardBody>
                <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={6}>
                  <GridItem>
                    <Stat>
                      <StatLabel>Current Price</StatLabel>
                      <StatNumber color="green.600">
                        ₹{marketData.current_price.toLocaleString()}
                      </StatNumber>
                      <StatHelpText>per quintal</StatHelpText>
                    </Stat>
                  </GridItem>
                  <GridItem>
                    <Stat>
                      <StatLabel>Next Week</StatLabel>
                      <StatNumber color="blue.600">
                        ₹{marketData.price_prediction.next_week.toLocaleString()}
                      </StatNumber>
                      <StatHelpText>
                        <StatArrow type={marketData.price_prediction.next_week > marketData.current_price ? 'increase' : 'decrease'} />
                        {Math.abs(((marketData.price_prediction.next_week - marketData.current_price) / marketData.current_price) * 100).toFixed(1)}%
                      </StatHelpText>
                    </Stat>
                  </GridItem>
                  <GridItem>
                    <Stat>
                      <StatLabel>Next Month</StatLabel>
                      <StatNumber color="purple.600">
                        ₹{marketData.price_prediction.next_month.toLocaleString()}
                      </StatNumber>
                      <StatHelpText>
                        <StatArrow type={marketData.price_prediction.next_month > marketData.current_price ? 'increase' : 'decrease'} />
                        {Math.abs(((marketData.price_prediction.next_month - marketData.current_price) / marketData.current_price) * 100).toFixed(1)}%
                      </StatHelpText>
                    </Stat>
                  </GridItem>
                  <GridItem>
                    <Stat>
                      <StatLabel>Confidence</StatLabel>
                      <StatNumber color={`${getConfidenceColor(marketData.price_prediction.confidence)}.600`}>
                        {Math.round(marketData.price_prediction.confidence * 100)}%
                      </StatNumber>
                      <StatHelpText>prediction accuracy</StatHelpText>
                    </Stat>
                  </GridItem>
                </Grid>
              </CardBody>
            </Card>

            {/* Market Factors */}
            <Card>
              <CardHeader>
                <Heading size="md">🔍 Market Factors</Heading>
              </CardHeader>
              <CardBody>
                <VStack spacing={3} align="stretch">
                  {marketData.market_factors.map((factor, index) => (
                    <HStack key={index} p={3} bg="blue.50" borderRadius="md">
                      <Info size={16} color="#3182CE" />
                      <Text fontSize="sm">{factor}</Text>
                    </HStack>
                  ))}
                </VStack>
              </CardBody>
            </Card>

            {/* Recommendations */}
            <Card>
              <CardHeader>
                <Heading size="md">💡 AI Recommendations</Heading>
              </CardHeader>
              <CardBody>
                <Grid templateColumns="repeat(auto-fit, minmax(300px, 1fr))" gap={4}>
                  <GridItem>
                    <VStack align="stretch" spacing={3}>
                      <Text fontWeight="bold" color="green.600">🎯 Selling Strategy</Text>
                      <Alert status="info" borderRadius="md">
                        <AlertIcon />
                        <AlertDescription fontSize="sm">
                          {marketData.recommendations.sell_timing}
                        </AlertDescription>
                      </Alert>
                    </VStack>
                  </GridItem>
                  <GridItem>
                    <VStack align="stretch" spacing={3}>
                      <Text fontWeight="bold" color="blue.600">⏰ Hold Period</Text>
                      <Alert status="warning" borderRadius="md">
                        <AlertIcon />
                        <AlertDescription fontSize="sm">
                          {marketData.recommendations.hold_period}
                        </AlertDescription>
                      </Alert>
                    </VStack>
                  </GridItem>
                </Grid>

                {marketData.recommendations.alternative_crops.length > 0 && (
                  <Box mt={4}>
                    <Text fontWeight="bold" color="purple.600" mb={2}>
                      🌾 Alternative Crops
                    </Text>
                    <HStack wrap="wrap" spacing={2}>
                      {marketData.recommendations.alternative_crops.map((crop, index) => (
                        <Badge key={index} colorScheme="purple" variant="subtle">
                          {crop}
                        </Badge>
                      ))}
                    </HStack>
                  </Box>
                )}
              </CardBody>
            </Card>

            {/* Government Policies */}
            {marketData.government_policies.length > 0 && (
              <Card>
                <CardHeader>
                  <Heading size="md">🏛️ Government Policies</Heading>
                </CardHeader>
                <CardBody>
                  <VStack spacing={3} align="stretch">
                    {marketData.government_policies.map((policy, index) => (
                      <HStack key={index} p={3} bg="yellow.50" borderRadius="md">
                        <CheckCircle size={16} color="#D69E2E" />
                        <Text fontSize="sm">{policy}</Text>
                      </HStack>
                    ))}
                  </VStack>
                </CardBody>
              </Card>
            )}

            {/* Regional Insights */}
            {marketData.regional_insights.length > 0 && (
              <Card>
                <CardHeader>
                  <Heading size="md">🗺️ Regional Insights</Heading>
                </CardHeader>
                <CardBody>
                  <VStack spacing={3} align="stretch">
                    {marketData.regional_insights.map((insight, index) => (
                      <HStack key={index} p={3} bg="green.50" borderRadius="md">
                        <AlertTriangle size={16} color="#38A169" />
                        <Text fontSize="sm">{insight}</Text>
                      </HStack>
                    ))}
                  </VStack>
                </CardBody>
              </Card>
            )}

            {/* Action Buttons */}
            <HStack spacing={4} justify="center">
              <Button
                leftIcon={<Download />}
                colorScheme="green"
                variant="outline"
                onClick={() => {
                  // Export market data
                  const dataStr = JSON.stringify(marketData, null, 2);
                  const dataBlob = new Blob([dataStr], { type: 'application/json' });
                  const url = URL.createObjectURL(dataBlob);
                  const link = document.createElement('a');
                  link.href = url;
                  link.download = `market-intelligence-${crop}-${region}.json`;
                  link.click();
                }}
              >
                Export Data
              </Button>
              <Button
                leftIcon={<Volume2 />}
                colorScheme="blue"
                onClick={generateVoiceReport}
                isLoading={isPlayingAudio}
              >
                Voice Report
              </Button>
            </HStack>
          </VStack>
        )}

        {/* No Data State */}
        {!marketData && !isLoading && (
          <Card>
            <CardBody textAlign="center" py={8}>
              <DollarSign size={48} color="#68D391" />
              <Text mt={4} color="gray.600">
                Select a crop and region to get market intelligence
              </Text>
              <Button
                mt={4}
                onClick={loadMarketIntelligence}
                colorScheme="green"
                leftIcon={<BarChart3 />}
              >
                Load Market Data
              </Button>
            </CardBody>
          </Card>
        )}
      </VStack>
    </Box>
  );
};

export default MarketIntelligenceComponent;
