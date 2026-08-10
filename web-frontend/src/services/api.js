import axios from 'axios';

// Always append /api to the base URL
const PRODUCTION_API_URL = 'https://fossee-project-api.vercel.app';
const BASE_URL = import.meta.env.PROD ? PRODUCTION_API_URL : (import.meta.env.VITE_API_URL || 'http://localhost:8000');
const API_BASE_URL = `${BASE_URL}/api`;

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token storage key (must match api/client.js)
const TOKEN_KEY = 'fossee_auth_token';

// Add auth token and CSRF token to requests
api.interceptors.request.use((config) => {
  // Add auth token if available
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }

  // Add CSRF token for POST/PUT/DELETE requests
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/login/', { username, password }),

  logout: () =>
    api.post('/auth/logout/'),

  getUser: () =>
    api.get('/auth/user/'),
};

// Dataset API
export const datasetAPI = {
  list: () =>
    api.get('/datasets/'),

  get: (id) =>
    api.get(`/datasets/${id}/`),

  upload: (file, name) => {
    const formData = new FormData();
    formData.append('file', file);
    if (name) formData.append('filename', name);

    return api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  delete: (id) =>
    api.delete(`/datasets/${id}/`),

  getReportUrl: (id) =>
    `${API_BASE_URL}/report/${id}/`,
};

export default api;
