import React from 'react';
import { motion } from 'framer-motion';
import { 
  Bell, 
  Search, 
  User, 
  Settings, 
  Moon, 
  Sun,
  Wifi,
  WifiOff,
  Activity
} from 'lucide-react';
import { useAppStore } from '../../store/appStore';

const Header: React.FC = () => {
  const { 
    theme, 
    setTheme, 
    connectionStatus, 
    agents, 
    jobs 
  } = useAppStore();

  const activeJobs = jobs.filter(job => job.status === 'processing').length;
  const workingAgents = agents.filter(agent => agent.status === 'working').length;

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 right-0 left-64 h-20 bg-dark-800/80 backdrop-blur-xl border-b border-white/10 z-40"
    >
      <div className="flex items-center justify-between h-full px-6">
        {/* Left: Current Page Info */}
        <div className="flex items-center space-x-4">
          <div>
            <h2 className="text-xl font-semibold text-white">Creative Studio</h2>
            <p className="text-sm text-gray-400">Multi-modal AI creation platform</p>
          </div>
          
          {/* Real-time Activity Indicator */}
          {(activeJobs > 0 || workingAgents > 0) && (
            <motion.div
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="flex items-center space-x-2 px-3 py-2 bg-primary-600/20 rounded-lg border border-primary-500/30"
            >
              <Activity className="w-4 h-4 text-primary-400 animate-pulse" />
              <span className="text-sm text-primary-300">
                {workingAgents} agents • {activeJobs} jobs
              </span>
            </motion.div>
          )}
        </div>

        {/* Center: Search */}
        <div className="flex-1 max-w-md mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search agents, jobs, devices..."
              className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-white placeholder-gray-400"
            />
          </div>
        </div>

        {/* Right: Status & Controls */}
        <div className="flex items-center space-x-4">
          {/* Connection Status */}
          <div className="flex items-center space-x-2">
            {connectionStatus === 'connected' ? (
              <Wifi className="w-5 h-5 text-green-400" />
            ) : (
              <WifiOff className="w-5 h-5 text-red-400" />
            )}
            <span className={`text-sm ${
              connectionStatus === 'connected' ? 'text-green-400' : 'text-red-400'
            }`}>
              {connectionStatus}
            </span>
          </div>

          {/* Theme Toggle */}
          <button
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            className="p-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            {theme === 'dark' ? (
              <Sun className="w-5 h-5 text-yellow-400" />
            ) : (
              <Moon className="w-5 h-5 text-blue-400" />
            )}
          </button>

          {/* Notifications */}
          <button className="relative p-2 rounded-lg hover:bg-white/10 transition-colors">
            <Bell className="w-5 h-5 text-gray-300" />
            {(activeJobs > 0 || workingAgents > 0) && (
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="absolute -top-1 -right-1 w-3 h-3 bg-primary-500 rounded-full"
              />
            )}
          </button>

          {/* Settings */}
          <button className="p-2 rounded-lg hover:bg-white/10 transition-colors">
            <Settings className="w-5 h-5 text-gray-300" />
          </button>

          {/* User Profile */}
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
            <div className="hidden md:block">
              <p className="text-sm font-medium text-white">AI Creator</p>
              <p className="text-xs text-gray-400">Premium User</p>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar for Active Jobs */}
      {activeJobs > 0 && (
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: '100%' }}
          className="absolute bottom-0 left-0 h-1 bg-gradient-to-r from-primary-500 to-secondary-500"
        />
      )}
    </motion.header>
  );
};

export default Header;
