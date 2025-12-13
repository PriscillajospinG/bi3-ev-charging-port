import { create } from 'zustand'

const useAppStore = create((set, get) => ({
  // Real-time data
  currentMetrics: null,
  chargers: [],
  cameras: [],
  alerts: [],
  
  // Dashboard data
  trafficStats: null,
  utilizationData: [],
  occupancyData: [],
  
  // Predictions
  demandForecast: null,
  predictions: [],
  
  // Recommendations
  recommendations: [],
  
  // WebSocket connection status
  isConnected: false,
  
  // Loading states
  isLoading: false,
  error: null,

  // Actions
  setCurrentMetrics: (metrics) => set({ currentMetrics: metrics }),
  
  setChargers: (chargers) => set({ chargers }),
  
  updateCharger: (chargerId, updates) => set((state) => ({
    chargers: state.chargers.map(charger =>
      charger.id === chargerId ? { ...charger, ...updates } : charger
    ),
  })),
  
  setCameras: (cameras) => set({ cameras }),
  
  addAlert: (alert) => set((state) => ({
    alerts: [alert, ...state.alerts].slice(0, 50), // Keep last 50 alerts
  })),
  
  clearAlerts: () => set({ alerts: [] }),
  
  setTrafficStats: (stats) => set({ trafficStats: stats }),
  
  setUtilizationData: (data) => set({ utilizationData: data }),
  
  setOccupancyData: (data) => set({ occupancyData: data }),
  
  setDemandForecast: (forecast) => set({ demandForecast: forecast }),
  
  setPredictions: (predictions) => set({ predictions }),
  
  setRecommendations: (recommendations) => set({ recommendations }),
  
  setConnectionStatus: (isConnected) => set({ isConnected }),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  setError: (error) => set({ error }),
}))

export default useAppStore
