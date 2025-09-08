import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles, Lightbulb, Music, Image as ImageIcon, Video } from 'lucide-react';

interface WhatsNewModalProps {
  open: boolean;
  onClose: () => void;
}

const FeatureItem: React.FC<{ icon: React.ReactNode; title: string; desc: string; }> = ({ icon, title, desc }) => (
  <div className="flex items-start space-x-3 p-3 rounded-lg hover:bg-white/5 transition-colors">
    <div className="mt-1">{icon}</div>
    <div>
      <p className="font-medium">{title}</p>
      <p className="text-sm text-gray-400">{desc}</p>
    </div>
  </div>
);

const WhatsNewModal: React.FC<WhatsNewModalProps> = ({ open, onClose }) => {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          onClick={onClose}
        >
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 20, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 200, damping: 22 }}
            className="w-full max-w-2xl bg-dark-800 border border-white/10 rounded-2xl p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold">What’s New</h3>
                  <p className="text-sm text-gray-400">Unified timeline • True device control • Scene templates</p>
                </div>
              </div>
              <button onClick={onClose} className="p-2 rounded-lg hover:bg-white/10">
                <X className="w-5 h-5 text-gray-300" />
              </button>
            </div>

            <div className="space-y-3">
              <FeatureItem icon={<ImageIcon className="w-5 h-5 text-blue-400" />} title="Text → Image → Music → Lights → Video" desc="统一时间轴同步，跨模态风格一致，实时生成与合成。" />
              <FeatureItem icon={<Lightbulb className="w-5 h-5 text-yellow-400" />} title="真设备控制 (Hue/WLED & GPIO/USB)" desc="一键发现与健康检查，边缘设备低延迟渲染，离线回放。" />
              <FeatureItem icon={<Music className="w-5 h-5 text-green-400" />} title="节拍/情绪驱动" desc="音乐节拍驱动灯光编排与视频转场，情绪曲线贯穿全流程。" />
              <FeatureItem icon={<Video className="w-5 h-5 text-pink-400" />} title="五大模板场景" desc="情境导演、亲子剧场、身心调谐、派对 DJ/VJ、家居情境食谱。" />
            </div>

            <div className="mt-6 flex items-center justify-end space-x-3">
              <a href="/templates" className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/15 transition-colors text-sm">查看模板库</a>
              <button onClick={onClose} className="px-4 py-2 rounded-lg bg-primary-600 hover:bg-primary-500 transition-colors text-sm">开始体验</button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default WhatsNewModal; 