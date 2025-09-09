import { Bars3Icon, UserCircleIcon, BellIcon } from '@heroicons/react/24/outline'
import { useAuth } from '../hooks/useAuth'

interface HeaderProps {
  user: any
  onMenuClick: () => void
  backendConnected: boolean
  isMobile: boolean
}

export default function Header({ user, onMenuClick, backendConnected, isMobile }: HeaderProps) {
  const { logout } = useAuth()

  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="flex items-center justify-between">
        {/* Left side */}
        <div className="flex items-center gap-4">
          {isMobile && (
            <button
              onClick={onMenuClick}
              className="p-2 rounded-lg hover:bg-gray-100"
            >
              <Bars3Icon className="h-6 w-6" />
            </button>
          )}
          
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              Welcome back, {user?.name || 'Farmer'}!
            </h2>
            <p className="text-sm text-gray-600">
              {new Date().toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </p>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <button className="p-2 rounded-lg hover:bg-gray-100 relative">
            <BellIcon className="h-6 w-6 text-gray-600" />
            <div className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></div>
          </button>

          {/* User menu */}
          <div className="flex items-center gap-3">
            <UserCircleIcon className="h-8 w-8 text-gray-600" />
            <div className="hidden md:block">
              <p className="text-sm font-medium text-gray-900">{user?.name}</p>
              <p className="text-xs text-gray-600">{user?.email}</p>
            </div>
            <button
              onClick={logout}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
