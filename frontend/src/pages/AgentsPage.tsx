import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Bot, Activity, Settings, BarChart3, Zap } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import AgentDetailCard from '../components/Agents/AgentDetailCard';
import AgentNetworkVisualization from '../components/Agents/AgentNetworkVisualization';
import AgentMetricsChart from '../components/Agents/AgentMetricsChart';

const AgentsPage: React.FC = () => {
  const { agents, setCurrentPage } = useAppStore();

  useEffect(() => {
    setCurrentPage('agents');
  }, [setCurrentPage]);

  const activeAgents = agents.filter(agent => agent.status === 'working').length;
  const totalTasks = agents.reduce((sum, agent) => sum + agent.metrics.tasksCompleted, 0);
  const avgSuccessRate = agents.reduce((sum, agent) => sum + agent.metrics.successRate, 0) / agents.length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold gradient-text">AI Agents</h1>
          <p className="text-gray-400 mt-2">
            Monitor and manage your intelligent agent workforce
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          <button className="button-secondary">
            <Settings className="w-4 h-4 mr-2" />
            Configure
          </button>
          <button className="button-primary">
            <Zap className="w-4 h-4 mr-2" />
            Deploy Agent
          </button>
        </div>
      </motion.div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-500/20 rounded-lg">
              <Bot className="w-6 h-6 text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{agents.length}</p>
              <p className="text-sm text-gray-400">Total Agents</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-green-500/20 rounded-lg">
              <Activity className="w-6 h-6 text-green-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{activeAgents}</p>
              <p className="text-sm text-gray-400">Active Now</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-purple-500/20 rounded-lg">
              <BarChart3 className="w-6 h-6 text-purple-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{totalTasks}</p>
              <p className="text-sm text-gray-400">Tasks Completed</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-yellow-500/20 rounded-lg">
              <Zap className="w-6 h-6 text-yellow-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{avgSuccessRate.toFixed(1)}%</p>
              <p className="text-sm text-gray-400">Success Rate</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Network Visualization */}
        <div className="lg:col-span-2">
          <AgentNetworkVisualization agents={agents} />
        </div>

        {/* Metrics Chart */}
        <div>
          <AgentMetricsChart agents={agents} />
        </div>
      </div>

      {/* Agent Details Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent, index) => (
          <AgentDetailCard
            key={agent.id}
            agent={agent}
            index={index}
          />
        ))}
      </div>
    </div>
  );
};

export default AgentsPage;
