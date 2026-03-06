import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (email, password) => api.post('/users/login', { email, password }),
  register: (userData) => api.post('/users/register', userData),
  getCurrentUser: () => api.get('/users/me'),
}

// Breach API
export const breachAPI = {
  getAll: (skip = 0, limit = 100) => api.get('/breaches', { params: { skip, limit } }),
  getById: (id) => api.get(`/breaches/${id}`),
  search: (query) => api.get('/breaches/search', { params: { query } }),
  sync: () => api.post('/breaches/sync'),
}

// Email Check API
export const emailCheckAPI = {
  checkEmail: (email) => api.post('/users/check-email', { email }),
  getUserBreaches: () => api.get('/users/breaches'),
  checkPassword: (password) => api.post('/users/check-password', { password }),
}

// Password Analysis API
export const passwordAnalysisAPI = {
  analyzePassword: (data) => api.post('/ml-analysis/analyze-password', data),
  analyzeCredential: (credentialId, password) =>
    api.post(`/ml-analysis/analyze-credential/${credentialId}`, { password }),
  detectWeakPasswords: (data) => api.post('/ml-analysis/detect-weak-passwords', data),
}

// Reporting API
export const reportingAPI = {
  getTrends: (days = 30) => api.get('/reports/trends', { params: { days } }),
  getStatistics: () => api.get('/reports/statistics'),
}

// Recommendations API
export const recommendationsAPI = {
  getRecommendations: () => api.get('/analysis/recommendations'),
}

// Notifications API
export const notificationsAPI = {
  getAll: () => api.get('/notifications'),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
  delete: (id) => api.delete(`/notifications/${id}`),
}

// Data Collection API
export const dataCollectionAPI = {
  syncHIBP: () => api.post('/data-collection/sync/hibp'),
  scrape: (sources, parseCredentials = true) =>
    api.post('/data-collection/scrape', { sources, parse_credentials: parseCredentials }),
  collectAll: (sources) => api.post('/data-collection/collect/all', { sources }),
}

export default api
