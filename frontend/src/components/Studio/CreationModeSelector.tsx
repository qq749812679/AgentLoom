import React from 'react';
import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';

interface CreationMode {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
  color: string;
}

interface CreationModeSelectorProps {
  modes: CreationMode[];
  currentMode: string;
  onModeChange: (mode: string) => void;
}

const CreationModeSelector: React.FC<CreationModeSelectorProps> = ({
  modes,
  currentMode,
  onModeChange
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {modes.map((mode, index) => {
        const Icon = mode.icon;
        const isSelected = currentMode === mode.id;

        return (
          <motion.div
            key={mode.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onModeChange(mode.id)}
            className={`cursor-pointer p-6 rounded-xl border transition-all ${
              isSelected
                ? 'bg-white/10 border-primary-500/50 ring-2 ring-primary-500/20'
                : 'bg-white/5 border-white/10 hover:border-white/20 hover:bg-white/10'
            }`}
          >
            <div className="flex flex-col items-center text-center space-y-3">
              <div className={`p-4 rounded-xl bg-gradient-to-br ${mode.color} shadow-lg`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              
              <div>
                <h3 className={`font-semibold ${
                  isSelected ? 'text-white' : 'text-gray-200'
                }`}>
                  {mode.title}
                </h3>
                <p className="text-sm text-gray-400 mt-1 leading-relaxed">
                  {mode.description}
                </p>
              </div>
              
              {isSelected && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="w-2 h-2 bg-primary-500 rounded-full"
                />
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};

export default CreationModeSelector;
