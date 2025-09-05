import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, Heart, Share2, Download, Eye } from 'lucide-react';
import { useAppStore } from '../store/appStore';

const CommunityPage: React.FC = () => {
  const { setCurrentPage } = useAppStore();

  useEffect(() => {
    setCurrentPage('community');
  }, [setCurrentPage]);

  const mockProjects = [
    {
      id: '1',
      title: 'Cozy Winter Cabin',
      creator: 'Alice Creator',
      likes: 234,
      views: 1200,
      downloads: 89,
      thumbnail: '/api/placeholder/300/200',
      tags: ['winter', 'cozy', 'ambient']
    },
    {
      id: '2',
      title: 'Cyberpunk City Nights',
      creator: 'Bob Designer',
      likes: 567,
      views: 3400,
      downloads: 145,
      thumbnail: '/api/placeholder/300/200',
      tags: ['cyberpunk', 'neon', 'futuristic']
    },
    // Add more mock projects...
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold gradient-text">Community</h1>
          <p className="text-gray-400 mt-2">
            Discover and share amazing multi-modal creations
          </p>
        </div>
        
        <button className="button-primary">
          <Share2 className="w-4 h-4 mr-2" />
          Share Creation
        </button>
      </motion.div>

      {/* Featured Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockProjects.map((project, index) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card hover:bg-white/10 transition-all cursor-pointer group"
          >
            <div className="aspect-video bg-gradient-to-br from-primary-600/20 to-secondary-600/20 rounded-lg mb-4 flex items-center justify-center">
              <span className="text-gray-400">Preview Image</span>
            </div>
            
            <h3 className="font-semibold text-white mb-2 group-hover:text-primary-400 transition-colors">
              {project.title}
            </h3>
            
            <p className="text-sm text-gray-400 mb-3">by {project.creator}</p>
            
            <div className="flex items-center justify-between text-sm text-gray-400 mb-3">
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-1">
                  <Heart className="w-4 h-4" />
                  <span>{project.likes}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Eye className="w-4 h-4" />
                  <span>{project.views}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Download className="w-4 h-4" />
                  <span>{project.downloads}</span>
                </div>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-1">
              {project.tags.map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-1 text-xs bg-white/10 rounded text-gray-300"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default CommunityPage;
