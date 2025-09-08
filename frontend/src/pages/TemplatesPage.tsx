import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, PartyPopper, HeartPulse, Clapperboard, BookOpen } from 'lucide-react';
import { useAppStore } from '../store/appStore';

interface TemplateItem {
  title: string;
  description: string;
  icon: React.ElementType;
  gradient: string;
  action: () => void;
}

const TemplatesPage: React.FC = () => {
  const { setCurrentPage } = useAppStore();

  useEffect(() => {
    setCurrentPage('templates');
  }, [setCurrentPage]);

  const templates: TemplateItem[] = [
    {
      title: '情境导演 Director',
      description: '统一时间轴：音乐节拍驱动灯光与转场，跨模态风格一致',
      icon: Clapperboard,
      gradient: 'from-blue-500 to-purple-500',
      action: () => (window.location.href = '/studio?mode=text-to-all&template=director')
    },
    {
      title: '亲子即兴剧场 Kids Theater',
      description: '一句话生成分镜/配音/配乐，家长可热更新剧情',
      icon: BookOpen,
      gradient: 'from-green-500 to-teal-500',
      action: () => (window.location.href = '/studio?mode=text-to-all&template=kids-theater')
    },
    {
      title: '身心调谐 Wellness',
      description: '心率/呼吸驱动 BPM 与灯光呼吸曲线，放松与专注双模式',
      icon: HeartPulse,
      gradient: 'from-emerald-500 to-cyan-500',
      action: () => (window.location.href = '/studio?mode=text-to-all&template=wellness')
    },
    {
      title: '派对 DJ/VJ',
      description: '投票触发高潮与切歌，VJ 视觉与 Hue/WLED 追光同步',
      icon: PartyPopper,
      gradient: 'from-yellow-500 to-orange-500',
      action: () => (window.location.href = '/studio?mode=video&template=party')
    },
    {
      title: '家居情境食谱 Home Recipes',
      description: '自然语言 → 可复用 Recipe，下发到 Home Assistant/MQTT',
      icon: Sparkles,
      gradient: 'from-pink-500 to-red-500',
      action: () => (window.location.href = '/studio?mode=text-to-all&template=recipe')
    }
  ];

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">模板库 Templates</h1>
          <p className="text-gray-400 text-sm">五大场景开箱即用，支持参数快照与复用</p>
        </div>
        <button
          onClick={() => window.dispatchEvent(new CustomEvent('open-whats-new'))}
          className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/15 text-sm"
        >
          查看 What's New
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map((t, i) => (
          <motion.button
            key={i}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={t.action}
            className={`w-full text-left p-6 rounded-2xl bg-gradient-to-br ${t.gradient} bg-opacity-20 border border-white/10 shadow-lg`}
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center">
                <t.icon className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-semibold">{t.title}</h3>
            </div>
            <p className="text-sm text-gray-100/90">{t.description}</p>
          </motion.button>
        ))}
      </div>
    </div>
  );
};

export default TemplatesPage; 