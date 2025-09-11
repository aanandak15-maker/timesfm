// Market API service for real-time commodity prices
export interface MarketData {
  commodity: string
  currentPrice: number
  change: number
  changePercent: number
  trend: 'up' | 'down' | 'stable'
  volume: string
  lastUpdated: string
  high52Week: number
  low52Week: number
  marketCap?: string
}

export interface MarketOverview {
  marketIndex: number
  averagePrice: number
  totalVolume: string
  volatility: number
  lastUpdated: string
}

class MarketApiService {
  private apiKey: string
  private baseUrl: string

  constructor() {
    // Using Alpha Vantage API (free tier)
    this.apiKey = import.meta.env.VITE_ALPHA_VANTAGE_API_KEY || 'demo'
    this.baseUrl = 'https://www.alphavantage.co/query'
    
    if (this.apiKey === 'demo') {
      console.warn('⚠️ Using demo market data. Alpha Vantage API key not found!')
    } else {
      console.log('✅ Real market API key detected. Fetching live commodity prices...')
    }
  }

  async getCommodityPrices(): Promise<MarketData[]> {
    try {
      // Always try real API first, fallback to mock if it fails
      console.log('Attempting to fetch real commodity prices...')
      
      const commodities = ['WHEAT', 'CORN', 'SOYBEAN', 'RICE']
      const promises = commodities.map(commodity => this.fetchCommodityPrice(commodity))
      const results = await Promise.allSettled(promises)
      
      const realData = results
        .filter((result): result is PromiseFulfilledResult<MarketData> => result.status === 'fulfilled')
        .map(result => result.value)
      
      if (realData.length > 0) {
        console.log('Real commodity data received:', realData)
        return realData
      } else {
        throw new Error('No real data received')
      }
    } catch (error) {
      console.warn('Real market API failed, using mock data:', error)
      return this.getMockMarketData()
    }
  }

  async getMarketOverview(): Promise<MarketOverview> {
    try {
      // If no API key, return mock data
      if (this.apiKey === 'demo') {
        return this.getMockMarketOverview()
      }

      // In a real implementation, you'd fetch from a market index API
      return this.getMockMarketOverview()
    } catch (error) {
      console.warn('Market overview API failed, using mock data:', error)
      return this.getMockMarketOverview()
    }
  }

  private async fetchCommodityPrice(commodity: string): Promise<MarketData> {
    const response = await fetch(
      `${this.baseUrl}?function=COMMODITY&symbol=${commodity}&apikey=${this.apiKey}`
    )

    if (!response.ok) {
      throw new Error(`Market API error: ${response.status}`)
    }

    const data = await response.json()
    return this.transformCommodityData(commodity, data)
  }

  private transformCommodityData(commodity: string, data: any): MarketData {
    const price = parseFloat(data.data?.value || '0')
    const change = Math.random() * 2 - 1 // Mock change for demo
    const changePercent = (change / price) * 100

    return {
      commodity: commodity.charAt(0) + commodity.slice(1).toLowerCase(),
      currentPrice: price,
      change,
      changePercent,
      trend: change > 0.1 ? 'up' : change < -0.1 ? 'down' : 'stable',
      volume: this.formatVolume(Math.random() * 2000000 + 100000),
      lastUpdated: new Date().toISOString(),
      high52Week: price * 1.2,
      low52Week: price * 0.8,
    }
  }

  private getMockMarketData(): MarketData[] {
    const commodities = [
      { name: 'Wheat', basePrice: 6.25 },
      { name: 'Corn', basePrice: 4.85 },
      { name: 'Soybeans', basePrice: 12.40 },
      { name: 'Rice', basePrice: 18.75 },
    ]

    return commodities.map(commodity => {
      const change = (Math.random() - 0.5) * 0.5 // -0.25 to +0.25
      const changePercent = (change / commodity.basePrice) * 100
      
      return {
        commodity: commodity.name,
        currentPrice: commodity.basePrice + change,
        change,
        changePercent,
        trend: change > 0.1 ? 'up' : change < -0.1 ? 'down' : 'stable',
        volume: this.formatVolume(Math.random() * 2000000 + 100000),
        lastUpdated: new Date().toISOString(),
        high52Week: commodity.basePrice * 1.2,
        low52Week: commodity.basePrice * 0.8,
      }
    })
  }

  private getMockMarketOverview(): MarketOverview {
    return {
      marketIndex: 1247.5 + (Math.random() - 0.5) * 50,
      averagePrice: 10.56 + (Math.random() - 0.5) * 2,
      totalVolume: this.formatVolume(Math.random() * 10000000 + 5000000),
      volatility: 2.1 + (Math.random() - 0.5) * 1,
      lastUpdated: new Date().toISOString(),
    }
  }

  private formatVolume(volume: number): string {
    if (volume >= 1000000) {
      return `${(volume / 1000000).toFixed(1)}M`
    } else if (volume >= 1000) {
      return `${(volume / 1000).toFixed(1)}K`
    }
    return volume.toFixed(0)
  }
}

export const marketApi = new MarketApiService()
export default marketApi
