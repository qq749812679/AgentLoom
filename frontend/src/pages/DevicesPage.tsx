import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Lightbulb, Plus, Settings, Wifi, WifiOff } from 'lucide-react';
import { useAppStore } from '../store/appStore';

const DevicesPage: React.FC = () => {
  const { devices, setCurrentPage } = useAppStore();

  useEffect(() => {
    setCurrentPage('devices');
  }, [setCurrentPage]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold gradient-text">Smart Devices</h1>
          <p className="text-gray-400 mt-2">
            Control and monitor your connected lighting devices
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          <button className="button-secondary">
            <Settings className="w-4 h-4 mr-2" />
            Settings
          </button>
          <button className="button-primary">
            <Plus className="w-4 h-4 mr-2" />
            Add Device
          </button>
        </div>
      </motion.div>

      {/* Device Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {devices.map((device, index) => (
          <motion.div
            key={device.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card hover:bg-white/10 transition-all cursor-pointer"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className={`p-3 rounded-lg ${
                  device.status === 'online' ? 'bg-green-500/20' : 'bg-red-500/20'
                }`}>
                  <Lightbulb className={`w-6 h-6 ${
                    device.status === 'online' ? 'text-green-400' : 'text-red-400'
                  }`} />
                </div>
                <div>
                  <h3 className="font-semibold text-white">{device.name}</h3>
                  <p className="text-sm text-gray-400 capitalize">{device.type}</p>
                </div>
              </div>
              
              {device.status === 'online' ? (
                <Wifi className="w-5 h-5 text-green-400" />
              ) : (
                <WifiOff className="w-5 h-5 text-red-400" />
              )}
            </div>

            {device.ip && (
              <p className="text-xs text-gray-500 mb-3">IP: {device.ip}</p>
            )}

            {device.currentState && (
              <div className="space-y-2 mb-4">
                {device.currentState.brightness && (
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-400">Brightness</span>
                      <span className="text-white">{device.currentState.brightness}%</span>
                    </div>
                    <div className="w-full bg-dark-700 rounded-full h-2">
                      <div 
                        className="bg-yellow-400 h-2 rounded-full"
                        style={{ width: `${device.currentState.brightness}%` }}
                      />
                    </div>
                  </div>
                )}
                
                {device.currentState.color && (
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-400">Color:</span>
                    <div 
                      className="w-6 h-6 rounded border border-white/20"
                      style={{ backgroundColor: device.currentState.color }}
                    />
                    <span className="text-sm text-white">{device.currentState.color}</span>
                  </div>
                )}
              </div>
            )}

            <div className="flex flex-wrap gap-1">
              {device.capabilities.map((capability) => (
                <span
                  key={capability}
                  className="px-2 py-1 text-xs bg-white/10 rounded text-gray-300"
                >
                  {capability.replace('-', ' ')}
                </span>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default DevicesPage;
