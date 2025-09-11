import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { Box, Text, useColorModeValue } from '@chakra-ui/react'

interface FieldPerformanceData {
  name: string
  yield: number
  efficiency: number
  area: number
}

interface FieldPerformanceChartProps {
  data: FieldPerformanceData[]
}

const FieldPerformanceChart: React.FC<FieldPerformanceChartProps> = ({ data }) => {
  const textColor = useColorModeValue('gray.600', 'gray.300')

  if (!data || data.length === 0) {
    return (
      <Box height="300px" display="flex" alignItems="center" justifyContent="center">
        <Text color={textColor}>No data available</Text>
      </Box>
    )
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <Box
          bg="white"
          p={3}
          borderRadius="md"
          border="1px solid #e2e8f0"
          boxShadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)"
        >
          <Text fontWeight="semibold" color="gray.700">
            {label}
          </Text>
          <Text color="gray.600">
            Yield: {data.yield.toFixed(1)} tons/acre
          </Text>
          <Text color="gray.600">
            Efficiency: {data.efficiency.toFixed(0)}%
          </Text>
          <Text color="gray.600">
            Area: {data.area.toFixed(1)} acres
          </Text>
        </Box>
      )
    }
    return null
  }

  return (
    <Box height="300px">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis 
            dataKey="name" 
            stroke={textColor}
            fontSize={12}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis 
            stroke={textColor}
            fontSize={12}
            label={{ value: 'Yield (tons/acre)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar 
            dataKey="yield" 
            fill="#3182ce" 
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  )
}

export default FieldPerformanceChart
