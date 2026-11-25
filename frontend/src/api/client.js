import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Quick predict endpoint (no auth). Resolve from VITE_PREDICT_URL or derive from VITE_API_URL
const PREDICT_BASE = import.meta.env.VITE_PREDICT_URL || (import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace(/\/api$/, '') + '/predict' : 'http://localhost:5000/predict');

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Global response handler: if token is invalid or we get unprocessable entity
// due to auth/token issues, clear local auth and redirect to login so user
// can re-authenticate and obtain a fresh token.
client.interceptors.response.use(
  (response) => response,
  (error) => {
    try {
      const status = error.response && error.response.status;
      if (status === 401 || status === 422) {
        console.warn('Auth error (status', status, ') — dispatching sessionExpired');
        try {
          // notify UI to show modal
          window.dispatchEvent(new Event('sessionExpired'));
        } catch (e) {
          // fallback: clear and redirect
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          if (typeof window !== 'undefined') window.location.href = '/login';
        }
      }
    } catch (e) {
      // swallow
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (userData) => client.post('/auth/register', userData),
  login: (credentials) => client.post('/auth/login', credentials),
  getCurrentUser: () => client.get('/auth/me')
};

export const predictionAPI = {
  predict: (data) => client.post('/predictions/predict', data)
};

export const quickPredict = (data) => axios.post(PREDICT_BASE, data, { headers: {'Content-Type': 'application/json'} });

export const workerAPI = {
  getProfile: () => client.get('/worker/profile'),
  getMetrics: (limit = 20) => client.get(`/worker/metrics?limit=${limit}`),
  getAlerts: (limit = 10) => client.get(`/worker/alerts?limit=${limit}`),
  markAlertRead: (alertId) => client.put(`/worker/alerts/${alertId}/read`)
};

export const supervisorAPI = {
  getAllWorkers: () => client.get('/supervisor/workers'),
  getDashboardStats: () => client.get('/supervisor/dashboard/stats'),
  getWorkerHistory: (workerId, limit = 100) => 
    client.get(`/supervisor/worker/${workerId}/history?limit=${limit}`),
  getZonesOverview: () => client.get('/supervisor/zones'),
  markAlertRead: (alertId) => client.put(`/supervisor/alerts/${alertId}/read`)
};

export default client;
