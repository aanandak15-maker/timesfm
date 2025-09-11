import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { Box, Text, useColorModeValue } from '@chakra-ui/react'

interface YieldTrendData {
  month: string
  yield: number
  target: number
}

interface YieldTrendChartProps {
  data: YieldTrendData[]
}

const YieldTrendChart: React.FC<YieldTrendChartProps> = ({ data }) => {
  const textColor = useColorModeValue('gray.600', 'gray.300')

  if (!data || data.length === 0) {
    return (
      <Box height="300px" display="flex" alignItems="center" justifyContent="center">
        <Text color={textColor}>No data available</Text>
      </Box>
    )
  }

  return (
    <Box height="300px">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis 
            dataKey="month" 
            stroke={textColor}
            fontSize={12}
          />
          <YAxis 
            stroke={textColor}
            fontSize={12}
            label={{ value: 'Tons/Acre', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="yield" 
            stroke="#3182ce" 
            strokeWidth={3}
            dot={{ fill: '#3182ce', strokeWidth: 2, r: 4 }}
            name="Actual Yield"
          />
          <Line 
            type="monotone" 
            dataKey="target" 
            stroke="#38a169" 
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#38a169', strokeWidth: 2, r: 4 }}
            name="Target Yield"
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  )
}

export default YieldTrendChart
