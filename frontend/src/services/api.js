import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

console.log('📡 API Base URL:', API_BASE_URL)

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }

    // Log API errors for debugging
    if (error.message === 'Network Error' || !error.response) {
      console.error('❌ Backend connection failed:', error.message)
    }

    return Promise.reject(error)
  }
)

// API endpoints
export const api = {
  // Dashboard
  getDashboardStats: () => apiClient.get('/dashboard/stats'),
  getDashboardLive: () => apiClient.get('/dashboard/live'),

  // Analytics endpoints
  getAnalyticsSummary: () => apiClient.get('/analytics/summary'),
  getAnalyticsDaily: () => apiClient.get('/analytics/daily'),
  getUtilizationTrend: () => apiClient.get('/dashboard/utilization-trend'),

  // Forecast endpoints
  getForecast: (days = 7) => apiClient.get(`/forecast/run?days=${days}`),
  getForecastAccuracy: () => apiClient.get('/forecast/accuracy'),


  // Chargers
  getChargers: () => apiClient.get('/chargers'),
  getChargerById: (id) => apiClient.get(`/chargers/${id}`),
  getChargerStatus: () => apiClient.get('/chargers/status'),

  // Map / Stations
  getStations: (params) => apiClient.get('/map/stations', { params }),

  // Analytics
  getUtilizationData: (params) => apiClient.get('/analytics/utilization', { params }),
  getTrafficData: (params) => apiClient.get('/analytics/traffic', { params }),
  getHeatmapData: (params) => apiClient.get('/analytics/heatmap', { params }),
  getOccupancyStats: () => apiClient.get('/analytics/occupancy'),

  // Predictions
  getDemandForecast: (params) => apiClient.get('/predictions/demand', { params }),
  getPeakPredictions: () => apiClient.get('/predictions/peaks'),
  getSeasonalAnalysis: () => apiClient.get('/predictions/seasonal'),

  // Recommendations
  // Recommendations
  getRecommendations: () => apiClient.get('/recommendations'),
  getRecommendationById: (id) => apiClient.get(`/recommendations/${id}`),
  implementRecommendation: (id) => apiClient.post(`/recommendations/${id}/implement`),

  // Video Upload
  uploadVideo: (formData) => apiClient.post('/video/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),

  // Cameras
  getCameraFeeds: () => apiClient.get('/cameras'),
  getCameraById: (id) => apiClient.get(`/cameras/${id}`),

  // Real-time metrics
  getCurrentMetrics: () => apiClient.get('/metrics/current'),
  getAlerts: () => apiClient.get('/alerts'),
}

export default apiClient
