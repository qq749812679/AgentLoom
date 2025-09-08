import React, { useEffect, useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import { useAppStore } from '../../store/appStore';
import WhatsNewModal from './WhatsNewModal';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { sidebarOpen } = useAppStore();
  const [showWhatsNew, setShowWhatsNew] = useState(false);

  useEffect(() => {
    const handler = () => setShowWhatsNew(true);
    window.addEventListener('open-whats-new', handler as EventListener);
    return () => window.removeEventListener('open-whats-new', handler as EventListener);
  }, []);

  return (
    <div className="min-h-screen bg-dark-900 text-white">
      {/* Background Pattern */}
      <div className="fixed inset-0 bg-gradient-to-br from-primary-900/20 via-dark-900 to-secondary-900/20">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5"></div>
      </div>
      
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <div className={`transition-all duration-300 ${
        sidebarOpen ? 'ml-64' : 'ml-16'
      }`}>
        {/* Header */}
        <Header />
        
        {/* Page Content */}
        <main className="relative min-h-screen pt-20 p-6">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>

      {/* Modals */}
      <WhatsNewModal open={showWhatsNew} onClose={() => setShowWhatsNew(false)} />
    </div>
  );
};

export default Layout;
