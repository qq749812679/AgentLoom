import React from 'react';
import { motion } from 'framer-motion';
import { Clock, CheckCircle, XCircle, Loader, Image, Music, Lightbulb, Video } from 'lucide-react';

interface ActivityItem {
  id: string;
  type: 'image' | 'music' | 'lighting' | 'video';
  title: string;
  status: 'completed' | 'processing' | 'failed';
  timestamp: Date;
  details?: string;
}

const mockActivities: ActivityItem[] = [
  {
    id: '1',
    type: 'image',
    title: 'Generated "Sunset Beach" scene',
    status: 'completed',
    timestamp: new Date(Date.now() - 2 * 60 * 1000),
    details: '1024x768 • Style: Photorealistic'
  },
  {
    id: '2',
    type: 'music',
    title: 'Composed ambient soundtrack',
    status: 'processing',
    timestamp: new Date(Date.now() - 5 * 60 * 1000),
    details: '30s • Genre: Ambient'
  },
  {
    id: '3',
    type: 'lighting',
    title: 'Synchronized Hue lights',
    status: 'completed',
    timestamp: new Date(Date.now() - 8 * 60 * 1000),
    details: '3 devices • Living room'
  },
  {
    id: '4',
    type: 'video',
    title: 'Video composition failed',
    status: 'failed',
    timestamp: new Date(Date.now() - 12 * 60 * 1000),
    details: 'Encoding error'
  },
  {
    id: '5',
    type: 'image',
    title: 'Created cyberpunk cityscape',
    status: 'completed',
    timestamp: new Date(Date.now() - 20 * 60 * 1000),
    details: '1024x768 • Style: Cyberpunk'
  }
];

const RecentActivityCard: React.FC = () => {
  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'image': return Image;
      case 'music': return Music;
      case 'lighting': return Lightbulb;
      case 'video': return Video;
      default: return CheckCircle;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return CheckCircle;
      case 'processing': return Loader;
      case 'failed': return XCircle;
      default: return CheckCircle;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-400';
      case 'processing': return 'text-yellow-400';
      case 'failed': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const formatTimeAgo = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / (1000 * 60));
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.3 }}
      className="card"
    >
      <div className="flex items-center space-x-3 mb-6">
        <Clock className="w-5 h-5 text-blue-400" />
        <h3 className="text-lg font-semibold">Recent Activity</h3>
      </div>

      <div className="space-y-4">
        {mockActivities.map((activity, index) => {
          const ActivityIcon = getActivityIcon(activity.type);
          const StatusIcon = getStatusIcon(activity.status);
          
          return (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="flex items-start space-x-3 p-3 rounded-lg hover:bg-white/5 transition-colors"
            >
              <div className="flex-shrink-0">
                <div className="relative">
                  <ActivityIcon className="w-5 h-5 text-gray-400" />
                  <div className="absolute -bottom-1 -right-1">
                    <StatusIcon 
                      className={`w-3 h-3 ${getStatusColor(activity.status)} ${
                        activity.status === 'processing' ? 'animate-spin' : ''
                      }`} 
                    />
                  </div>
                </div>
              </div>
              
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">
                  {activity.title}
                </p>
                {activity.details && (
                  <p className="text-xs text-gray-400 mt-1">
                    {activity.details}
                  </p>
                )}
                <p className="text-xs text-gray-500 mt-1">
                  {formatTimeAgo(activity.timestamp)}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Show More Button */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="w-full mt-4 py-2 text-sm text-gray-400 hover:text-white transition-colors border-t border-white/5 pt-4"
      >
        View all activity
      </motion.button>
    </motion.div>
  );
};

export default RecentActivityCard;
