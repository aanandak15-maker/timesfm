import {
  Box,
  HStack,
  Text as ChakraText,
  IconButton,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  useColorModeValue,
  Badge,
} from '@chakra-ui/react'
import { Bell, Settings, LogOut, User } from 'lucide-react'

const Header = () => {
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  return (
    <Box
      bg={bg}
      borderBottom="1px"
      borderColor={borderColor}
      px={6}
      py={4}
      display="flex"
      alignItems="center"
      justifyContent="space-between"
    >
      {/* Page Title */}
      <ChakraText fontSize="2xl" fontWeight="bold" color="gray.800">
        Agricultural Intelligence Platform
      </ChakraText>

      {/* Right Side */}
      <HStack spacing={4}>
        {/* Notifications */}
        <IconButton
          aria-label="Notifications"
          icon={<Bell />}
          variant="ghost"
          position="relative"
        >
          <Badge
            position="absolute"
            top={1}
            right={1}
            colorScheme="red"
            borderRadius="full"
            w={5}
            h={5}
            fontSize="xs"
          >
            3
          </Badge>
        </IconButton>

        {/* User Menu */}
        <Menu>
          <MenuButton
            as={IconButton}
            aria-label="User menu"
            icon={<Avatar size="sm" name="Farmer" />}
            variant="ghost"
          />
          <MenuList>
            <MenuItem icon={<User />}>Profile</MenuItem>
            <MenuItem icon={<Settings />}>Settings</MenuItem>
            <MenuItem icon={<LogOut />} color="red.500">
              Logout
            </MenuItem>
          </MenuList>
        </Menu>
      </HStack>
    </Box>
  )
}

export default Header
