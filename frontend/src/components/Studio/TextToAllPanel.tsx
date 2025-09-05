import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Wand2, 
  Mic, 
  Sparkles, 
  RefreshCw,
  Image,
  Music,
  Lightbulb,
  Video
} from 'lucide-react';
import { useAppStore } from '../../store/appStore';
import toast from 'react-hot-toast';

const TextToAllPanel: React.FC = () => {
  const { addJob, updateAgent } = useAppStore();
  const [prompt, setPrompt] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [selectedStyle, setSelectedStyle] = useState('photorealistic');
  const [selectedMood, setSelectedMood] = useState('balanced');

  const presetPrompts = [
    'Cozy fireplace with warm ambient lighting',
    'Futuristic cyberpunk cityscape at night',
    'Peaceful sunrise over mountain lake',
    'Energetic dance party with colorful lights',
    'Mystical forest with ethereal glow',
    'Vintage jazz club atmosphere'
  ];

  const styles = [
    { id: 'photorealistic', name: 'Photorealistic', color: 'from-blue-500 to-cyan-500' },
    { id: 'artistic', name: 'Artistic', color: 'from-purple-500 to-pink-500' },
    { id: 'anime', name: 'Anime', color: 'from-red-500 to-orange-500' },
    { id: 'abstract', name: 'Abstract', color: 'from-green-500 to-teal-500' }
  ];

  const moods = [
    { id: 'energetic', name: 'Energetic', emoji: '⚡' },
    { id: 'calm', name: 'Calm', emoji: '🧘' },
    { id: 'romantic', name: 'Romantic', emoji: '💕' },
    { id: 'mysterious', name: 'Mysterious', emoji: '🌙' },
    { id: 'festive', name: 'Festive', emoji: '🎉' },
    { id: 'balanced', name: 'Balanced', emoji: '⚖️' }
  ];

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a description');
      return;
    }

    // Create new job
    const newJob = {
      type: 'text-to-all' as const,
      prompt: prompt.trim(),
      status: 'processing' as const,
      progress: 0,
      agents: ['orchestrator', 'vision-agent', 'audio-agent', 'lighting-agent', 'video-agent']
    };

    addJob(newJob);
    toast.success('Generation started!');

    // Simulate agent work
    setTimeout(() => {
      updateAgent('orchestrator', { status: 'working', progress: 20 });
    }, 500);

    setTimeout(() => {
      updateAgent('vision-agent', { status: 'working', progress: 0 });
    }, 1000);

    setTimeout(() => {
      updateAgent('audio-agent', { status: 'working', progress: 0 });
    }, 2000);
  };

  const handleVoiceRecord = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      toast.success('Voice recording started');
      // Simulate voice recognition
      setTimeout(() => {
        setIsRecording(false);
        setPrompt('Cozy Christmas living room with fireplace');
        toast.success('Voice recognized!');
      }, 3000);
    }
  };

  return (
    <div className="space-y-6">
      {/* Main Input */}
      <div className="space-y-4">
        <div className="relative">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the scene you want to create... (e.g., 'A cozy winter cabin with warm lighting and snow falling outside')"
            className="w-full p-4 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 min-h-[120px]"
          />
          
          <div className="absolute bottom-4 right-4 flex items-center space-x-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleVoiceRecord}
              className={`p-2 rounded-lg transition-all ${
                isRecording 
                  ? 'bg-red-500 text-white animate-pulse' 
                  : 'bg-white/10 text-gray-400 hover:text-white'
              }`}
            >
              <Mic className="w-4 h-4" />
            </motion.button>
            
            <span className="text-sm text-gray-500">
              {prompt.length}/500
            </span>
          </div>
        </div>

        {/* Preset Prompts */}
        <div>
          <h4 className="text-sm font-medium text-gray-300 mb-3">Quick Start Templates</h4>
          <div className="flex flex-wrap gap-2">
            {presetPrompts.map((preset, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setPrompt(preset)}
                className="px-3 py-2 text-sm bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-colors text-gray-300"
              >
                {preset}
              </motion.button>
            ))}
          </div>
        </div>
      </div>

      {/* Style and Mood Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Visual Style */}
        <div>
          <h4 className="text-sm font-medium text-gray-300 mb-3">Visual Style</h4>
          <div className="grid grid-cols-2 gap-2">
            {styles.map((style) => (
              <motion.button
                key={style.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelectedStyle(style.id)}
                className={`p-3 rounded-lg border transition-all ${
                  selectedStyle === style.id
                    ? 'border-primary-500 bg-primary-500/20'
                    : 'border-white/10 bg-white/5 hover:bg-white/10'
                }`}
              >
                <div className={`w-full h-8 bg-gradient-to-r ${style.color} rounded mb-2`} />
                <span className="text-sm font-medium">{style.name}</span>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Mood */}
        <div>
          <h4 className="text-sm font-medium text-gray-300 mb-3">Mood & Atmosphere</h4>
          <div className="grid grid-cols-3 gap-2">
            {moods.map((mood) => (
              <motion.button
                key={mood.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelectedMood(mood.id)}
                className={`p-3 rounded-lg border transition-all text-center ${
                  selectedMood === mood.id
                    ? 'border-primary-500 bg-primary-500/20'
                    : 'border-white/10 bg-white/5 hover:bg-white/10'
                }`}
              >
                <div className="text-lg mb-1">{mood.emoji}</div>
                <span className="text-xs font-medium">{mood.name}</span>
              </motion.button>
            ))}
          </div>
        </div>
      </div>

      {/* Output Options */}
      <div>
        <h4 className="text-sm font-medium text-gray-300 mb-3">Generated Content</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { icon: Image, label: 'Image', enabled: true },
            { icon: Music, label: 'Music', enabled: true },
            { icon: Lightbulb, label: 'Lighting', enabled: true },
            { icon: Video, label: 'Video', enabled: false }
          ].map((output, index) => (
            <div
              key={index}
              className={`flex items-center space-x-2 p-3 rounded-lg border ${
                output.enabled
                  ? 'border-green-500/30 bg-green-500/10'
                  : 'border-gray-500/30 bg-gray-500/10'
              }`}
            >
              <output.icon className={`w-4 h-4 ${
                output.enabled ? 'text-green-400' : 'text-gray-400'
              }`} />
              <span className={`text-sm ${
                output.enabled ? 'text-green-400' : 'text-gray-400'
              }`}>
                {output.label}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Generate Button */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={handleGenerate}
        disabled={!prompt.trim()}
        className="w-full flex items-center justify-center space-x-3 p-4 bg-gradient-to-r from-primary-600 to-secondary-600 text-white font-medium rounded-lg hover:from-primary-700 hover:to-secondary-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Sparkles className="w-5 h-5" />
        <span>Generate Multi-Modal Experience</span>
        <Wand2 className="w-5 h-5" />
      </motion.button>

      {/* Additional Options */}
      <div className="flex items-center justify-between text-sm text-gray-400">
        <div className="flex items-center space-x-4">
          <label className="flex items-center space-x-2">
            <input type="checkbox" className="rounded" defaultChecked />
            <span>High Quality</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="checkbox" className="rounded" />
            <span>Auto-save</span>
          </label>
        </div>
        
        <button className="flex items-center space-x-1 hover:text-white transition-colors">
          <RefreshCw className="w-4 h-4" />
          <span>Random Prompt</span>
        </button>
      </div>
    </div>
  );
};

export default TextToAllPanel;
