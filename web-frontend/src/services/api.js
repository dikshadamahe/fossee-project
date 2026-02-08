import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add CSRF token to requests
api.interceptors.request.use((config) => {
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
