import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { Box, Text, useColorModeValue } from '@chakra-ui/react'

interface WeatherImpactData {
  month: string
  temperature: number
  precipitation: number
  yield: number
}

interface WeatherImpactChartProps {
  data: WeatherImpactData[]
}

const WeatherImpactChart: React.FC<WeatherImpactChartProps> = ({ data }) => {
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
          {payload.map((entry: any, index: number) => (
            <Text key={index} color={entry.color}>
              {entry.name}: {entry.value}{entry.dataKey === 'temperature' ? '°F' : entry.dataKey === 'precipitation' ? '%' : ' tons/acre'}
            </Text>
          ))}
        </Box>
      )
    }
    return null
  }

  return (
    <Box height="300px">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis 
            dataKey="month" 
            stroke={textColor}
            fontSize={12}
          />
          <YAxis 
            yAxisId="left"
            stroke={textColor}
            fontSize={12}
            label={{ value: 'Temperature (°F)', angle: -90, position: 'insideLeft' }}
          />
          <YAxis 
            yAxisId="right"
            orientation="right"
            stroke={textColor}
            fontSize={12}
            label={{ value: 'Yield (tons/acre)', angle: 90, position: 'insideRight' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar 
            yAxisId="left"
            dataKey="precipitation" 
            fill="#3182ce" 
            name="Precipitation (%)"
            radius={[4, 4, 0, 0]}
          />
          <Line 
            yAxisId="left"
            type="monotone" 
            dataKey="temperature" 
            stroke="#e53e3e" 
            strokeWidth={2}
            name="Temperature (°F)"
          />
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="yield" 
            stroke="#38a169" 
            strokeWidth={3}
            name="Yield (tons/acre)"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </Box>
  )
}

export default WeatherImpactChart
