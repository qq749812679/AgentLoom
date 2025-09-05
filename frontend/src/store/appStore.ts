import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface Agent {
  id: string;
  name: string;
  type: 'image' | 'music' | 'lighting' | 'video' | 'orchestrator' | 'safety' | 'memory';
  status: 'idle' | 'working' | 'completed' | 'error';
  progress: number;
  lastActive: Date;
  capabilities: string[];
  metrics: {
    tasksCompleted: number;
    avgResponseTime: number;
    successRate: number;
  };
}

export interface GenerationJob {
  id: string;
  type: 'text-to-all' | 'image-to-music' | 'music-to-lights' | 'collaboration';
  prompt: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress: number;
  startTime: Date;
  results?: {
    image?: string;
    music?: string;
    lighting?: any;
    video?: string;
  };
  agents: string[];
}

export interface Device {
  id: string;
  name: string;
  type: 'hue' | 'wled' | 'generic';
  status: 'online' | 'offline' | 'connecting';
  ip?: string;
  capabilities: string[];
  currentState?: any;
}

export interface AppState {
  // UI State
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  currentPage: string;
  
  // Agents
  agents: Agent[];
  
  // Jobs
  jobs: GenerationJob[];
  currentJob?: GenerationJob;
  
  // Devices
  devices: Device[];
  
  // Real-time data
  isConnected: boolean;
  connectionStatus: 'connected' | 'connecting' | 'disconnected';
  
  // User preferences
  userPreferences: {
    defaultQuality: 'fast' | 'balanced' | 'quality';
    autoSave: boolean;
    notifications: boolean;
  };
}

export interface AppActions {
  // UI Actions
  setTheme: (theme: 'light' | 'dark') => void;
  toggleSidebar: () => void;
  setCurrentPage: (page: string) => void;
  
  // Agent Actions
  updateAgent: (id: string, updates: Partial<Agent>) => void;
  resetAgents: () => void;
  
  // Job Actions
  addJob: (job: Omit<GenerationJob, 'id' | 'startTime'>) => void;
  updateJob: (id: string, updates: Partial<GenerationJob>) => void;
  setCurrentJob: (job: GenerationJob | undefined) => void;
  
  // Device Actions
  updateDevice: (id: string, updates: Partial<Device>) => void;
  addDevice: (device: Omit<Device, 'id'>) => void;
  
  // Connection Actions
  setConnectionStatus: (status: 'connected' | 'connecting' | 'disconnected') => void;
  
  // Preferences
  updatePreferences: (preferences: Partial<AppState['userPreferences']>) => void;
}

// Initial agents data
const initialAgents: Agent[] = [
  {
    id: 'orchestrator',
    name: 'Orchestrator',
    type: 'orchestrator',
    status: 'idle',
    progress: 0,
    lastActive: new Date(),
    capabilities: ['workflow-planning', 'agent-coordination', 'task-distribution'],
    metrics: { tasksCompleted: 156, avgResponseTime: 1.2, successRate: 98.5 }
  },
  {
    id: 'vision-agent',
    name: 'Vision Agent',
    type: 'image',
    status: 'idle',
    progress: 0,
    lastActive: new Date(),
    capabilities: ['text-to-image', 'image-analysis', 'style-transfer'],
    metrics: { tasksCompleted: 89, avgResponseTime: 5.8, successRate: 95.2 }
  },
  {
    id: 'audio-agent',
    name: 'Audio Agent',
    type: 'music',
    status: 'idle',
    progress: 0,
    lastActive: new Date(),
    capabilities: ['music-generation', 'audio-analysis', 'sound-synthesis'],
    metrics: { tasksCompleted: 67, avgResponseTime: 12.4, successRate: 92.8 }
  },
  {
    id: 'lighting-agent',
    name: 'Lighting Agent',
    type: 'lighting',
    status: 'idle',
    progress: 0,
    lastActive: new Date(),
    capabilities: ['lighting-design', 'color-mapping', 'device-control'],
    metrics: { tasksCompleted: 134, avgResponseTime: 0.8, successRate: 99.1 }
  },
  {
    id: 'video-agent',
    name: 'Video Agent',
    type: 'video',
    status: 'idle',
    progress: 0,
    lastActive: new Date(),
    capabilities: ['video-composition', 'effects-processing', 'timeline-editing'],
    metrics: { tasksCompleted: 23, avgResponseTime: 18.7, successRate: 88.4 }
  },
  {
    id: 'safety-agent',
    name: 'Safety Agent',
    type: 'safety',
    status: 'idle',
    progress: 0,
    lastActive: new Date(),
    capabilities: ['content-filtering', 'safety-monitoring', 'compliance-check'],
    metrics: { tasksCompleted: 298, avgResponseTime: 0.3, successRate: 99.9 }
  }
];

// Initial devices data
const initialDevices: Device[] = [
  {
    id: 'hue-bridge',
    name: 'Philips Hue Bridge',
    type: 'hue',
    status: 'online',
    ip: '192.168.1.100',
    capabilities: ['rgb-control', 'brightness', 'scenes'],
    currentState: { brightness: 80, color: '#4F46E5' }
  },
  {
    id: 'wled-strip',
    name: 'WLED Light Strip',
    type: 'wled',
    status: 'online',
    ip: '192.168.1.101',
    capabilities: ['rgb-control', 'effects', 'segments'],
    currentState: { brightness: 100, effect: 'Rainbow' }
  }
];

export const useAppStore = create<AppState & AppActions>()(
  devtools(
    (set, get) => ({
      // Initial State
      theme: 'dark',
      sidebarOpen: true,
      currentPage: 'home',
      agents: initialAgents,
      jobs: [],
      currentJob: undefined,
      devices: initialDevices,
      isConnected: true,
      connectionStatus: 'connected',
      userPreferences: {
        defaultQuality: 'balanced',
        autoSave: true,
        notifications: true,
      },

      // UI Actions
      setTheme: (theme) => set({ theme }),
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setCurrentPage: (currentPage) => set({ currentPage }),

      // Agent Actions
      updateAgent: (id, updates) =>
        set((state) => ({
          agents: state.agents.map((agent) =>
            agent.id === id ? { ...agent, ...updates, lastActive: new Date() } : agent
          ),
        })),

      resetAgents: () =>
        set((state) => ({
          agents: state.agents.map((agent) => ({
            ...agent,
            status: 'idle' as const,
            progress: 0,
          })),
        })),

      // Job Actions
      addJob: (jobData) =>
        set((state) => ({
          jobs: [
            ...state.jobs,
            {
              ...jobData,
              id: `job-${Date.now()}`,
              startTime: new Date(),
            },
          ],
        })),

      updateJob: (id, updates) =>
        set((state) => ({
          jobs: state.jobs.map((job) =>
            job.id === id ? { ...job, ...updates } : job
          ),
        })),

      setCurrentJob: (currentJob) => set({ currentJob }),

      // Device Actions
      updateDevice: (id, updates) =>
        set((state) => ({
          devices: state.devices.map((device) =>
            device.id === id ? { ...device, ...updates } : device
          ),
        })),

      addDevice: (deviceData) =>
        set((state) => ({
          devices: [
            ...state.devices,
            {
              ...deviceData,
              id: `device-${Date.now()}`,
            },
          ],
        })),

      // Connection Actions
      setConnectionStatus: (connectionStatus) =>
        set({ connectionStatus, isConnected: connectionStatus === 'connected' }),

      // Preferences
      updatePreferences: (preferences) =>
        set((state) => ({
          userPreferences: { ...state.userPreferences, ...preferences },
        })),
    }),
    {
      name: 'multi-modal-ai-store',
    }
  )
);
