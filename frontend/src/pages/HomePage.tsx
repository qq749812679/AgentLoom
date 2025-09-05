import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Palette, 
  Bot, 
  Lightbulb, 
  Video, 
  Music, 
  Image,
  Zap,
  TrendingUp,
  Clock,
  Award
} from 'lucide-react';
import { useAppStore } from '../store/appStore';
import AgentStatusCard from '../components/Agents/AgentStatusCard';
import QuickActionCard from '../components/Dashboard/QuickActionCard';
import StatsCard from '../components/Dashboard/StatsCard';
import RecentActivityCard from '../components/Dashboard/RecentActivityCard';

const HomePage: React.FC = () => {
  const { agents, jobs, devices, setCurrentPage } = useAppStore();

  useEffect(() => {
    setCurrentPage('home');
  }, [setCurrentPage]);

  const quickActions = [
    {
      title: 'Text to Everything',
      description: 'Generate image, music, lighting & video from text',
      icon: Palette,
      color: 'from-blue-500 to-purple-500',
      action: () => window.location.href = '/studio?mode=text-to-all'
    },
    {
      title: 'Image to Music',
      description: 'Create matching soundtrack from your images',
      icon: Music,
      color: 'from-green-500 to-teal-500',
      action: () => window.location.href = '/studio?mode=image-to-music'
    },
    {
      title: 'Smart Lighting',
      description: 'Control your smart devices with AI',
      icon: Lightbulb,
      color: 'from-yellow-500 to-orange-500',
      action: () => window.location.href = '/devices'
    },
    {
      title: 'Video Creation',
      description: 'Compose videos with synchronized audio',
      icon: Video,
      color: 'from-pink-500 to-red-500',
      action: () => window.location.href = '/studio?mode=video'
    }
  ];

  const stats = [
    {
      title: 'Active Agents',
      value: agents.filter(a => a.status !== 'error').length,
      total: agents.length,
      icon: Bot,
      color: 'text-blue-400',
      change: '+2 this week'
    },
    {
      title: 'Completed Tasks',
      value: agents.reduce((sum, agent) => sum + agent.metrics.tasksCompleted, 0),
      icon: Award,
      color: 'text-green-400',
      change: '+47 today'
    },
    {
      title: 'Connected Devices',
      value: devices.filter(d => d.status === 'online').length,
      total: devices.length,
      icon: Lightbulb,
      color: 'text-yellow-400',
      change: 'All online'
    },
    {
      title: 'Avg Response Time',
      value: '2.4s',
      icon: Clock,
      color: 'text-purple-400',
      change: '-0.3s improved'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary-600/20 via-secondary-600/20 to-accent-600/20 p-8"
      >
        <div className="relative z-10">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold gradient-text">
                Welcome to Multi-Modal AI
              </h1>
              <p className="text-gray-300">
                Your intelligent creative companion is ready to create amazing experiences
              </p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
            {quickActions.map((action, index) => (
              <QuickActionCard key={index} {...action} />
            ))}
          </div>
        </div>
        
        {/* Background Animation */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-primary-500 rounded-full animate-pulse" />
          <div className="absolute bottom-1/4 right-1/4 w-24 h-24 bg-secondary-500 rounded-full animate-pulse delay-1000" />
          <div className="absolute top-3/4 left-3/4 w-16 h-16 bg-accent-500 rounded-full animate-pulse delay-2000" />
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Status */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="card"
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <Bot className="w-6 h-6 text-primary-400" />
                <h2 className="text-xl font-semibold">AI Agents Status</h2>
              </div>
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full"
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {agents.slice(0, 6).map((agent) => (
                <AgentStatusCard key={agent.id} agent={agent} />
              ))}
            </div>
          </motion.div>
        </div>

        {/* Recent Activity */}
        <div className="space-y-6">
          <RecentActivityCard />
          
          {/* System Health */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="card"
          >
            <div className="flex items-center space-x-3 mb-4">
              <TrendingUp className="w-5 h-5 text-green-400" />
              <h3 className="text-lg font-semibold">System Health</h3>
            </div>
            
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-400">CPU Usage</span>
                  <span className="text-green-400">23%</span>
                </div>
                <div className="w-full bg-dark-700 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '23%' }}
                    transition={{ duration: 1, delay: 0.5 }}
                    className="bg-green-400 h-2 rounded-full"
                  />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-400">Memory</span>
                  <span className="text-blue-400">67%</span>
                </div>
                <div className="w-full bg-dark-700 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '67%' }}
                    transition={{ duration: 1, delay: 0.7 }}
                    className="bg-blue-400 h-2 rounded-full"
                  />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-400">Network</span>
                  <span className="text-purple-400">89%</span>
                </div>
                <div className="w-full bg-dark-700 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '89%' }}
                    transition={{ duration: 1, delay: 0.9 }}
                    className="bg-purple-400 h-2 rounded-full"
                  />
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
