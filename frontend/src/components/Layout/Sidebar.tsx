import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Home, 
  Palette, 
  Bot, 
  Lightbulb, 
  Users, 
  Settings,
  ChevronLeft,
  ChevronRight,
  Zap,
  Activity
} from 'lucide-react';
import { useAppStore } from '../../store/appStore';

const menuItems = [
  { id: 'home', path: '/', icon: Home, label: 'Home', description: 'Overview & Dashboard' },
  { id: 'studio', path: '/studio', icon: Palette, label: 'Creative Studio', description: 'Multi-modal Creation' },
  { id: 'agents', path: '/agents', icon: Bot, label: 'AI Agents', description: 'Agent Management' },
  { id: 'devices', path: '/devices', icon: Lightbulb, label: 'Smart Devices', description: 'Device Control' },
  { id: 'community', path: '/community', icon: Users, label: 'Community', description: 'Share & Collaborate' },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { sidebarOpen, toggleSidebar, agents, connectionStatus } = useAppStore();

  const activeAgents = agents.filter(agent => agent.status === 'working').length;
  const isConnected = connectionStatus === 'connected';

  return (
    <motion.div
      animate={{ width: sidebarOpen ? 256 : 64 }}
      transition={{ duration: 0.3 }}
      className="fixed left-0 top-0 h-full bg-dark-800/80 backdrop-blur-xl border-r border-white/10 z-50"
    >
      {/* Header */}
      <div className="p-4 border-b border-white/10">
        <div className="flex items-center justify-between">
          {sidebarOpen && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
              className="flex items-center space-x-3"
            >
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold gradient-text">MultiModal AI</h1>
                <p className="text-xs text-gray-400">Orchestrator v1.0</p>
              </div>
            </motion.div>
          )}
          
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            {sidebarOpen ? (
              <ChevronLeft className="w-5 h-5" />
            ) : (
              <ChevronRight className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>

      {/* Status Indicator */}
      <div className="p-4">
        <div className={`flex items-center space-x-3 p-3 rounded-lg ${
          isConnected ? 'bg-green-500/20' : 'bg-red-500/20'
        }`}>
          <div className={`w-3 h-3 rounded-full ${
            isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'
          }`} />
          {sidebarOpen && (
            <div>
              <p className="text-sm font-medium">
                {isConnected ? 'Connected' : 'Disconnected'}
              </p>
              <p className="text-xs text-gray-400">
                {activeAgents} agents active
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="px-4 space-y-2">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;

          return (
            <motion.button
              key={item.id}
              onClick={() => navigate(item.path)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-all ${
                isActive
                  ? 'bg-primary-600/20 text-primary-400 border border-primary-500/30'
                  : 'hover:bg-white/5 text-gray-300 hover:text-white'
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? 'text-primary-400' : ''}`} />
              {sidebarOpen && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.1 }}
                  className="flex-1 text-left"
                >
                  <p className="font-medium">{item.label}</p>
                  <p className="text-xs text-gray-500">{item.description}</p>
                </motion.div>
              )}
            </motion.button>
          );
        })}
      </nav>

      {/* Quick Stats */}
      {sidebarOpen && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="absolute bottom-4 left-4 right-4"
        >
          <div className="glass-effect rounded-lg p-4 space-y-3">
            <h3 className="text-sm font-semibold text-gray-300">System Status</h3>
            
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Agents Online</span>
                <span className="text-xs font-medium text-green-400">
                  {agents.filter(a => a.status !== 'error').length}/{agents.length}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Active Tasks</span>
                <span className="text-xs font-medium text-yellow-400">{activeAgents}</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Devices</span>
                <div className="flex items-center space-x-1">
                  <Activity className="w-3 h-3 text-green-400" />
                  <span className="text-xs font-medium text-green-400">2</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default Sidebar;
