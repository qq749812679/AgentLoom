import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Palette, 
  Upload, 
  Music, 
  Video, 
  Settings, 
  Play, 
  Download,
  Share2,
  Wand2
} from 'lucide-react';
import { useAppStore } from '../store/appStore';
import CreationModeSelector from '../components/Studio/CreationModeSelector';
import TextToAllPanel from '../components/Studio/TextToAllPanel';
import ImageToMusicPanel from '../components/Studio/ImageToMusicPanel';
import VideoCreationPanel from '../components/Studio/VideoCreationPanel';
import GenerationProgress from '../components/Studio/GenerationProgress';
import ResultsDisplay from '../components/Studio/ResultsDisplay';

type CreationMode = 'text-to-all' | 'image-to-music' | 'music-to-lights' | 'video';

const StudioPage: React.FC = () => {
  const { setCurrentPage, currentJob, agents } = useAppStore();
  const [currentMode, setCurrentMode] = useState<CreationMode>('text-to-all');
  const [showAdvancedSettings, setShowAdvancedSettings] = useState(false);

  useEffect(() => {
    setCurrentPage('studio');
  }, [setCurrentPage]);

  const creationModes = [
    {
      id: 'text-to-all' as CreationMode,
      title: 'Text to Everything',
      description: 'Generate complete multi-modal experience from text',
      icon: Palette,
      color: 'from-blue-500 to-purple-500'
    },
    {
      id: 'image-to-music' as CreationMode,
      title: 'Image to Music',
      description: 'Create soundtrack matching your image',
      icon: Music,
      color: 'from-green-500 to-teal-500'
    },
    {
      id: 'music-to-lights' as CreationMode,
      title: 'Music to Lights',
      description: 'Generate lighting choreography from audio',
      icon: Upload,
      color: 'from-yellow-500 to-orange-500'
    },
    {
      id: 'video' as CreationMode,
      title: 'Video Creation',
      description: 'Compose synchronized audio-visual content',
      icon: Video,
      color: 'from-pink-500 to-red-500'
    }
  ];

  const renderCreationPanel = () => {
    switch (currentMode) {
      case 'text-to-all':
        return <TextToAllPanel />;
      case 'image-to-music':
        return <ImageToMusicPanel />;
      case 'music-to-lights':
        return <div className="text-center py-8 text-gray-400">Music to Lights panel coming soon...</div>;
      case 'video':
        return <VideoCreationPanel />;
      default:
        return null;
    }
  };

  const isGenerating = currentJob?.status === 'processing';
  const workingAgents = agents.filter(agent => agent.status === 'working');

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold gradient-text">Creative Studio</h1>
          <p className="text-gray-400 mt-2">
            Transform your ideas into immersive multi-modal experiences
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowAdvancedSettings(!showAdvancedSettings)}
            className={`p-3 rounded-lg transition-all ${
              showAdvancedSettings 
                ? 'bg-primary-600/20 text-primary-400 border border-primary-500/30' 
                : 'bg-white/5 text-gray-400 hover:text-white'
            }`}
          >
            <Settings className="w-5 h-5" />
          </motion.button>
          
          {currentJob?.results && (
            <>
              <button className="button-secondary">
                <Share2 className="w-4 h-4 mr-2" />
                Share
              </button>
              <button className="button-primary">
                <Download className="w-4 h-4 mr-2" />
                Download
              </button>
            </>
          )}
        </div>
      </motion.div>

      {/* Creation Mode Selector */}
      <CreationModeSelector
        modes={creationModes}
        currentMode={currentMode}
        onModeChange={setCurrentMode}
      />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Creation Panel */}
        <div className="lg:col-span-2 space-y-6">
          <motion.div
            key={currentMode}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            className="card"
          >
            <div className="flex items-center space-x-3 mb-6">
              <Wand2 className="w-6 h-6 text-primary-400" />
              <h2 className="text-xl font-semibold">
                {creationModes.find(mode => mode.id === currentMode)?.title}
              </h2>
            </div>
            
            {renderCreationPanel()}
          </motion.div>

          {/* Advanced Settings */}
          {showAdvancedSettings && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="card"
            >
              <h3 className="text-lg font-semibold mb-4">Advanced Settings</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Quality Priority
                  </label>
                  <select className="w-full p-3 bg-white/5 border border-white/10 rounded-lg text-white">
                    <option value="fast">Speed</option>
                    <option value="balanced" selected>Balanced</option>
                    <option value="quality">Quality</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Output Resolution
                  </label>
                  <select className="w-full p-3 bg-white/5 border border-white/10 rounded-lg text-white">
                    <option value="512">512x512</option>
                    <option value="768" selected>768x768</option>
                    <option value="1024">1024x1024</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Style Strength
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="20"
                    defaultValue="7"
                    className="w-full"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Creativity Level
                  </label>
                  <input
                    type="range"
                    min="0.1"
                    max="2"
                    step="0.1"
                    defaultValue="1"
                    className="w-full"
                  />
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Generation Progress */}
          {isGenerating && (
            <GenerationProgress 
              currentJob={currentJob}
              workingAgents={workingAgents}
            />
          )}

          {/* Results Display */}
          {currentJob?.results && (
            <ResultsDisplay results={currentJob.results} />
          )}

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card"
          >
            <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
            
            <div className="space-y-3">
              <button className="w-full flex items-center space-x-3 p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                <Play className="w-4 h-4 text-green-400" />
                <span>Preview Generation</span>
              </button>
              
              <button className="w-full flex items-center space-x-3 p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                <Upload className="w-4 h-4 text-blue-400" />
                <span>Import Template</span>
              </button>
              
              <button className="w-full flex items-center space-x-3 p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                <Download className="w-4 h-4 text-purple-400" />
                <span>Save as Template</span>
              </button>
            </div>
          </motion.div>

          {/* Recent Templates */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="card"
          >
            <h3 className="text-lg font-semibold mb-4">Recent Templates</h3>
            
            <div className="space-y-2">
              {['Sunset Beach', 'Cyberpunk City', 'Forest Ambience'].map((template, index) => (
                <button
                  key={template}
                  className="w-full text-left p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors"
                >
                  <p className="font-medium text-white">{template}</p>
                  <p className="text-xs text-gray-400">Used {3 - index} times</p>
                </button>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default StudioPage;
