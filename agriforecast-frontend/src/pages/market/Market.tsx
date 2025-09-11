import {
  Box,
  Heading,
  Text as ChakraText,
  VStack,
  HStack,
  useColorModeValue,
  SimpleGrid,
  Card,
  CardBody,
  Badge,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Skeleton,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { marketApi } from '../../services/marketApi'
import { useErrorHandler } from '../../hooks/useErrorHandler'
import { TrendingUp, TrendingDown, Minus, RefreshCw } from 'lucide-react'

const Market = () => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')
  const { handleError } = useErrorHandler()

  // Fetch real-time market data
  const { data: marketData, isLoading: marketLoading, error: marketError, refetch: refetchMarket } = useQuery({
    queryKey: ['market-data'],
    queryFn: marketApi.getCommodityPrices,
    refetchInterval: 2 * 60 * 1000, // Refetch every 2 minutes
    retry: 1,
  })

  const { data: marketOverview, isLoading: overviewLoading, error: overviewError, refetch: refetchOverview } = useQuery({
    queryKey: ['market-overview'],
    queryFn: marketApi.getMarketOverview,
    refetchInterval: 2 * 60 * 1000, // Refetch every 2 minutes
    retry: 1,
  })

  // Handle errors
  if (marketError) {
    handleError(marketError, { showToast: true })
  }
  if (overviewError) {
    handleError(overviewError, { showToast: true })
  }

  const isLoading = marketLoading || overviewLoading

  const handleRefresh = () => {
    refetchMarket()
    refetchOverview()
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return TrendingUp
      case 'down': return TrendingDown
      default: return Minus
    }
  }

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up': return 'green'
      case 'down': return 'red'
      default: return 'gray'
    }
  }

  if (isLoading) {
    return (
      <Box>
        <VStack align="start" spacing={4} mb={8}>
          <Skeleton height="40px" width="300px" />
          <Skeleton height="20px" width="500px" />
        </VStack>
        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6} mb={8}>
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} height="120px" />
          ))}
        </SimpleGrid>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} height="200px" />
          ))}
        </SimpleGrid>
      </Box>
    )
  }

  if (!marketData || !marketOverview) {
    return (
      <Alert status="error" borderRadius="xl">
        <AlertIcon />
        <Box>
          <AlertTitle>Market Data Unavailable</AlertTitle>
          <AlertDescription>
            Unable to fetch market data. Please try again later.
          </AlertDescription>
        </Box>
      </Alert>
    )
  }

  return (
    <Box>
      <VStack align="start" spacing={4} mb={8}>
        <HStack justify="space-between" w="full">
          <VStack align="start" spacing={2}>
            <Heading size="lg">Market Intelligence</Heading>
            <ChakraText color="gray.600">
              Real-time commodity prices and market trends
            </ChakraText>
          </VStack>
          <HStack>
            <ChakraText fontSize="sm" color="gray.500">
              Last updated: {new Date(marketData[0]?.lastUpdated || Date.now()).toLocaleTimeString()}
            </ChakraText>
            <RefreshCw 
              size={16} 
              color="#3182ce" 
              cursor="pointer"
              onClick={handleRefresh}
              style={{ marginLeft: '8px' }}
            />
          </HStack>
        </HStack>
      </VStack>

      {/* Market Overview */}
      <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6} mb={8}>
        <Stat bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
          <StatLabel>Market Index</StatLabel>
          <StatNumber>{marketOverview.marketIndex.toFixed(1)}</StatNumber>
          <StatHelpText>
            <StatArrow type="increase" />
            2.3% today
          </StatHelpText>
        </Stat>

        <Stat bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
          <StatLabel>Avg Price</StatLabel>
          <StatNumber>${marketOverview.averagePrice.toFixed(2)}</StatNumber>
          <StatHelpText>
            <StatArrow type="increase" />
            1.8% this week
          </StatHelpText>
        </Stat>

        <Stat bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
          <StatLabel>Volume</StatLabel>
          <StatNumber>{marketOverview.totalVolume}</StatNumber>
          <StatHelpText>
            <StatArrow type="increase" />
            12% higher
          </StatHelpText>
        </Stat>

        <Stat bg={bg} p={6} borderRadius="xl" border="1px" borderColor={borderColor}>
          <StatLabel>Volatility</StatLabel>
          <StatNumber>{marketOverview.volatility.toFixed(1)}%</StatNumber>
          <StatHelpText>
            <StatArrow type="decrease" />
            Low risk
          </StatHelpText>
        </Stat>
      </SimpleGrid>

      {/* Commodity Prices */}
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
        {marketData.map((commodity) => {
          const TrendIcon = getTrendIcon(commodity.trend)
          const trendColor = getTrendColor(commodity.trend)
          
          return (
            <Card key={commodity.commodity} bg={bg} border="1px" borderColor={borderColor}>
              <CardBody>
                <HStack justify="space-between" mb={4}>
                  <VStack align="start" spacing={1}>
                    <Heading size="md">{commodity.commodity}</Heading>
                    <ChakraText fontSize="sm" color="gray.600">
                      Volume: {commodity.volume}
                    </ChakraText>
                  </VStack>
                  <Badge colorScheme={trendColor} variant="subtle">
                    {commodity.trend}
                  </Badge>
                </HStack>

                <VStack spacing={3} align="stretch">
                  <HStack justify="space-between">
                    <ChakraText fontSize="2xl" fontWeight="bold">
                      ${commodity.currentPrice}
                    </ChakraText>
                    <HStack spacing={1}>
                      <TrendIcon 
                        size={20} 
                        color={trendColor === 'green' ? '#22c55e' : trendColor === 'red' ? '#ef4444' : '#6b7280'} 
                      />
                      <ChakraText 
                        fontSize="sm" 
                        color={trendColor === 'green' ? 'green.500' : trendColor === 'red' ? 'red.500' : 'gray.500'}
                        fontWeight="semibold"
                      >
                        {commodity.change > 0 ? '+' : ''}{commodity.change} ({commodity.changePercent > 0 ? '+' : ''}{commodity.changePercent}%)
                      </ChakraText>
                    </HStack>
                  </HStack>

                  <ChakraText fontSize="sm" color="gray.600">
                    Last updated: {new Date(commodity.lastUpdated).toLocaleTimeString()}
                  </ChakraText>
                </VStack>
              </CardBody>
            </Card>
          )
        })}
      </SimpleGrid>
    </Box>
  )
}

export default Market
