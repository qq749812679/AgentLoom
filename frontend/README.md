# 🎨 Multi-Modal AI Frontend

A modern React frontend for the Multi-Modal AI Orchestrator platform, showcasing real-time AI agent visualization and interactive multi-modal content creation.

## ✨ Features

### 🎯 **Core Interface**
- **Real-time Agent Monitoring**: Live status updates and progress visualization
- **Interactive Creation Studio**: Multi-modal content generation with intuitive controls
- **Smart Device Management**: Visual control panel for connected IoT devices
- **Community Hub**: Share and discover AI-generated content

### 🎨 **Design & UX**
- **Modern Dark Theme**: Sleek, professional interface optimized for content creation
- **Responsive Design**: Seamless experience across desktop, tablet, and mobile
- **Smooth Animations**: Framer Motion powered transitions and micro-interactions
- **Glass Morphism**: Contemporary UI with backdrop blur effects

### 🤖 **AI Integration**
- **Live Agent Status**: Real-time visualization of AI agent workflows
- **Progress Tracking**: Visual progress bars and status indicators
- **Interactive Controls**: Direct manipulation of AI generation parameters
- **Result Preview**: Immediate preview of generated content

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm/yarn
- Backend API running (see main project README)

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Open http://localhost:3000
```

### Docker Setup
```bash
# Build frontend container
docker build -t multimodal-frontend .

# Run with docker-compose (from project root)
docker-compose up frontend
```

### One-Command Setup (Recommended)
- Windows (PowerShell):
  1) cd multiscen && powershell -ExecutionPolicy Bypass -File setup.ps1
  2) streamlit run app.py
  3) cd frontend && npm install && npm start
- macOS/Linux:
  1) cd multiscen && bash setup.sh
  2) streamlit run app.py
  3) cd frontend && npm install && npm start

## 🏗️ Architecture

### Component Structure
```
src/
├── components/           # Reusable UI components
│   ├── Layout/          # Navigation and layout
│   ├── Agents/          # Agent visualization
│   ├── Studio/          # Creation interfaces
│   └── Dashboard/       # Dashboard widgets
├── pages/               # Main application pages
├── store/               # Zustand state management
├── hooks/               # Custom React hooks
├── services/            # API and WebSocket services
└── utils/               # Helper functions
```

### State Management
- **Zustand**: Lightweight state management for UI and data
- **Real-time Updates**: WebSocket integration for live agent status
- **Persistent Storage**: User preferences and session data

### Styling System
- **Tailwind CSS**: Utility-first styling framework
- **Custom Design System**: Consistent colors, spacing, and typography
- **Responsive Breakpoints**: Mobile-first responsive design
- **Dark Theme**: Optimized for content creation workflows

## 🎛️ Key Components

### 🏠 **Dashboard (HomePage)**
- System overview and quick actions
- Agent status grid with real-time updates
- Performance metrics and usage statistics
- Quick access to frequently used features

### 🎨 **Creative Studio (StudioPage)**
- **Text-to-All**: Generate images, music, lighting, and video from text
- **Image-to-Music**: Create soundtracks from uploaded images
- **Music-to-Lights**: Design lighting choreography from audio
- **Video Creation**: Compose synchronized audio-visual content

### 🤖 **Agents Page**
- Live agent network visualization
- Performance metrics and success rates
- Individual agent configuration and monitoring
- Task distribution and workload analysis

### 💡 **Devices Page**
- Connected device management
- Real-time device status and control
- Lighting visualization and color selection
- Multi-room coordination interface

### 🤝 **Community Page**
- Browse featured community creations
- Share your own AI-generated content
- Like, comment, and download community projects
- Trending tags and popular creators

## 🎭 **UI/UX Highlights**

### Visual Design
- **Gradient Accents**: Beautiful color gradients for visual hierarchy
- **Glass Effects**: Translucent panels with backdrop blur
- **Micro-animations**: Smooth hover effects and state transitions
- **Status Indicators**: Clear visual feedback for system states

### Interaction Patterns
- **Progressive Disclosure**: Advanced settings hidden by default
- **Contextual Actions**: Relevant controls appear based on current state
- **Keyboard Shortcuts**: Power user shortcuts for common actions
- **Drag & Drop**: Intuitive file upload and content manipulation

### Responsive Behavior
- **Mobile Navigation**: Collapsible sidebar for mobile devices
- **Touch Gestures**: Swipe and tap interactions on touch devices
- **Adaptive Layouts**: Flexible grids that adapt to screen size
- **Performance Optimization**: Lazy loading and code splitting

## 🔧 Development

### Available Scripts
```bash
npm start          # Development server
npm build          # Production build
npm test           # Run test suite
npm run lint       # Code linting
npm run format     # Code formatting
```

### Environment Variables
```bash
REACT_APP_API_URL=http://localhost:8000    # Backend API URL
REACT_APP_WS_URL=ws://localhost:8000/ws    # WebSocket URL
REACT_APP_VERSION=1.0.0                    # App version
```

### Development Tools
- **TypeScript**: Type safety and better developer experience
- **ESLint + Prettier**: Code quality and formatting
- **React DevTools**: Component debugging and profiling
- **Tailwind CSS IntelliSense**: Enhanced CSS development

## 📱 **Responsive Design**

### Breakpoints
- **sm**: 640px+ (Mobile landscape)
- **md**: 768px+ (Tablet)
- **lg**: 1024px+ (Desktop)
- **xl**: 1280px+ (Large desktop)

### Mobile Optimizations
- Collapsible sidebar navigation
- Touch-friendly button sizes
- Optimized image loading
- Gesture-based interactions

## 🔮 **Future Enhancements**

### Planned Features
- **3D Visualizations**: Three.js powered agent network graphs
- **Voice Interface**: Speech-to-text content creation
- **AR Preview**: Augmented reality lighting preview
- **Collaborative Editing**: Real-time multi-user editing

### Performance Improvements
- **Code Splitting**: Reduce initial bundle size
- **Service Worker**: Offline functionality
- **WebGL Acceleration**: GPU-powered visualizations
- **Edge Caching**: Faster content delivery

## 🤝 **Contributing**

See the main project [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Frontend-specific Guidelines
- Follow React best practices and hooks patterns
- Use TypeScript for all new components
- Maintain responsive design principles
- Write meaningful component documentation

---

**Built with ❤️ using React, TypeScript, and Tailwind CSS**
