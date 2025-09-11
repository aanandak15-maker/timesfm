import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from 'recharts'
import { Box, Text, useColorModeValue } from '@chakra-ui/react'

interface CropDistributionChartProps {
  data: Record<string, number>
}

const COLORS = ['#3182ce', '#38a169', '#d69e2e', '#e53e3e', '#805ad5', '#dd6b20']

const CropDistributionChart: React.FC<CropDistributionChartProps> = ({ data }) => {
  const textColor = useColorModeValue('gray.600', 'gray.300')

  // Transform data for the pie chart
  const chartData = Object.entries(data).map(([name, value], index) => ({
    name,
    value,
    color: COLORS[index % COLORS.length],
  }))

  if (!chartData || chartData.length === 0) {
    return (
      <Box height="300px" display="flex" alignItems="center" justifyContent="center">
        <Text color={textColor}>No data available</Text>
      </Box>
    )
  }

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0]
      return (
        <Box
          bg="white"
          p={3}
          borderRadius="md"
          border="1px solid #e2e8f0"
          boxShadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)"
        >
          <Text fontWeight="semibold" color="gray.700">
            {data.name}
          </Text>
          <Text color="gray.600">
            Fields: {data.value}
          </Text>
        </Box>
      )
    }
    return null
  }

  return (
    <Box height="300px">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value }) => `${name} ${value}`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Box>
  )
}

export default CropDistributionChart
