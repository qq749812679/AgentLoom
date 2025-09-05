import React from 'react';
import { motion } from 'framer-motion';
import { Bot, Palette, Music, Lightbulb, Video, Shield, Brain } from 'lucide-react';
import { Agent } from '../../store/appStore';

interface AgentStatusCardProps {
  agent: Agent;
  onClick?: () => void;
}

const AgentStatusCard: React.FC<AgentStatusCardProps> = ({ agent, onClick }) => {
  const getAgentIcon = (type: string) => {
    switch (type) {
      case 'image': return Palette;
      case 'music': return Music;
      case 'lighting': return Lightbulb;
      case 'video': return Video;
      case 'safety': return Shield;
      case 'orchestrator': return Brain;
      default: return Bot;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'working': return 'text-yellow-400';
      case 'completed': return 'text-green-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'working': return 'bg-yellow-500/20 border-yellow-500/30';
      case 'completed': return 'bg-green-500/20 border-green-500/30';
      case 'error': return 'bg-red-500/20 border-red-500/30';
      default: return 'bg-gray-500/20 border-gray-500/30';
    }
  };

  const Icon = getAgentIcon(agent.type);

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`agent-card cursor-pointer ${getStatusBg(agent.status)}`}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg ${getStatusBg(agent.status)}`}>
            <Icon className={`w-5 h-5 ${getStatusColor(agent.status)}`} />
          </div>
          <div>
            <h3 className="font-semibold text-white">{agent.name}</h3>
            <p className="text-xs text-gray-400 capitalize">{agent.type} Agent</p>
          </div>
        </div>
        
        <div className={`status-indicator ${
          agent.status === 'idle' ? 'status-idle' :
          agent.status === 'working' ? 'status-working' :
          agent.status === 'completed' ? 'status-completed' :
          'status-error'
        }`} />
      </div>

      {/* Progress Bar */}
      {agent.status === 'working' && (
        <div className="mb-3">
          <div className="flex justify-between text-xs mb-1">
            <span className="text-gray-400">Progress</span>
            <span className={getStatusColor(agent.status)}>{agent.progress}%</span>
          </div>
          <div className="w-full bg-dark-700 rounded-full h-1.5">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${agent.progress}%` }}
              transition={{ duration: 0.5 }}
              className={`h-1.5 rounded-full ${
                agent.status === 'working' ? 'bg-yellow-400' : 'bg-green-400'
              }`}
            />
          </div>
        </div>
      )}

      {/* Metrics */}
      <div className="grid grid-cols-3 gap-2 text-xs">
        <div className="text-center">
          <p className="text-gray-400">Tasks</p>
          <p className="font-semibold text-white">{agent.metrics.tasksCompleted}</p>
        </div>
        <div className="text-center">
          <p className="text-gray-400">Avg Time</p>
          <p className="font-semibold text-white">{agent.metrics.avgResponseTime}s</p>
        </div>
        <div className="text-center">
          <p className="text-gray-400">Success</p>
          <p className="font-semibold text-green-400">{agent.metrics.successRate}%</p>
        </div>
      </div>

      {/* Capabilities Preview */}
      <div className="mt-3 pt-3 border-t border-white/5">
        <div className="flex flex-wrap gap-1">
          {agent.capabilities.slice(0, 2).map((capability, index) => (
            <span
              key={index}
              className="px-2 py-1 text-xs bg-white/5 rounded-md text-gray-300"
            >
              {capability.replace('-', ' ')}
            </span>
          ))}
          {agent.capabilities.length > 2 && (
            <span className="px-2 py-1 text-xs bg-white/5 rounded-md text-gray-400">
              +{agent.capabilities.length - 2}
            </span>
          )}
        </div>
      </div>

      {/* Last Active */}
      <div className="mt-2 text-xs text-gray-500">
        Last active: {new Date(agent.lastActive).toLocaleTimeString()}
      </div>
    </motion.div>
  );
};

export default AgentStatusCard;
