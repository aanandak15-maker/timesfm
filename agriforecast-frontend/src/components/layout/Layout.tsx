import { Outlet } from 'react-router-dom'
import { Box, Flex } from '@chakra-ui/react'
import Sidebar from './Sidebar'
import Header from './Header'
import DemoNotifications from '../demo/DemoNotifications'

const Layout = () => {
  return (
    <Flex h="100vh" bg="gray.50">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <Flex direction="column" flex="1" overflow="hidden">
        <Header />
        <Box flex="1" overflow="auto" p={6}>
          <Outlet />
        </Box>
      </Flex>
      
      {/* Demo Notifications */}
      <DemoNotifications />
    </Flex>
  )
}

export default Layout

