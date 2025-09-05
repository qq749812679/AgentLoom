import React from 'react';
import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: string | number;
  total?: number;
  icon: LucideIcon;
  color: string;
  change?: string;
}

const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  total,
  icon: Icon,
  color,
  change
}) => {
  const displayValue = typeof value === 'number' && total 
    ? `${value}/${total}` 
    : value;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="card hover:bg-white/5 transition-all"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <Icon className={`w-5 h-5 ${color}`} />
            <h3 className="text-sm font-medium text-gray-400">{title}</h3>
          </div>
          
          <div className="flex items-baseline space-x-2">
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="text-2xl font-bold text-white"
            >
              {displayValue}
            </motion.span>
          </div>
          
          {change && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="text-xs text-green-400 mt-2"
            >
              {change}
            </motion.p>
          )}
        </div>
        
        {/* Progress Circle for ratio values */}
        {typeof value === 'number' && total && (
          <div className="relative w-12 h-12">
            <svg className="w-12 h-12 transform -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-dark-700"
                stroke="currentColor"
                strokeWidth="3"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <motion.path
                className={color.replace('text-', 'text-')}
                stroke="currentColor"
                strokeWidth="3"
                fill="none"
                strokeLinecap="round"
                initial={{ strokeDasharray: `0, 100` }}
                animate={{ strokeDasharray: `${(value / total) * 100}, 100` }}
                transition={{ duration: 1, delay: 0.3 }}
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={`text-xs font-semibold ${color}`}>
                {Math.round((value / total) * 100)}%
              </span>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default StatsCard;
