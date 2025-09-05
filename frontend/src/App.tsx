import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout/Layout';
import HomePage from './pages/HomePage';
import StudioPage from './pages/StudioPage';
import AgentsPage from './pages/AgentsPage';
import DevicesPage from './pages/DevicesPage';
import CommunityPage from './pages/CommunityPage';
import { useAppStore } from './store/appStore';

function App() {
  const { theme } = useAppStore();

  return (
    <div className={`app ${theme === 'dark' ? 'dark' : ''}`}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/studio" element={<StudioPage />} />
            <Route path="/agents" element={<AgentsPage />} />
            <Route path="/devices" element={<DevicesPage />} />
            <Route path="/community" element={<CommunityPage />} />
          </Routes>
        </Layout>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'rgba(30, 41, 59, 0.95)',
              color: '#fff',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
            },
          }}
        />
      </Router>
    </div>
  );
}

export default App;
