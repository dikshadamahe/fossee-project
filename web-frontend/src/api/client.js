/**
 * API Client - Axios Implementation
 * Chemical Equipment Parameter Visualizer
 * FOSSEE Scientific Analytics
 * 
 * Centralized API client matching desktop-app/api_client.py
 */

import axios from 'axios';

// =============================================================================
// CONFIGURATION
// =============================================================================

const CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  API_PREFIX: '/api',
  TIMEOUT: 30000, // milliseconds
};

// Token storage key
const TOKEN_KEY = 'fossee_auth_token';

// Create axios instance
const api = axios.create({
  baseURL: `${CONFIG.BASE_URL}${CONFIG.API_PREFIX}`,
  timeout: CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// =============================================================================
// REQUEST INTERCEPTOR - Add auth token
// =============================================================================

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// =============================================================================
// RESPONSE INTERCEPTOR - Handle 401 errors
// =============================================================================

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, clear it
      // Note: Don't clear on login/register endpoints
      const url = error.config.url || '';
      if (!url.includes('/auth/')) {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem('fossee_auth_user');
      }
    }
    return Promise.reject(error);
  }
);

// =============================================================================
// ENDPOINTS (Centralized - matches Python api_client.py)
// =============================================================================

export const Endpoints = {
  // Auth endpoints
  AUTH_REGISTER: '/auth/register/',
  AUTH_LOGIN: '/auth/login/',
  AUTH_LOGOUT: '/auth/logout/',
  AUTH_USER: '/auth/user/',

  // POST - Upload CSV file
  UPLOAD: '/upload/',

  // GET - List all datasets (history)
  DATASETS: '/datasets/',

  // GET - Dataset summary statistics
  summary: (id) => `/summary/${id}/`,

  // GET/DELETE - Single dataset with records
  dataset: (id) => `/datasets/${id}/`,

  // GET - Download PDF report
  report: (id) => `/report/${id}/`,
};

// =============================================================================
// AUTH API METHODS
// =============================================================================

export const authApi = {
  /**
   * POST /api/auth/register/
   * Register new user
   */
  register: async (username, email, password, passwordConfirm) => {
    const response = await api.post(Endpoints.AUTH_REGISTER, {
      username,
      email,
      password,
      password_confirm: passwordConfirm,
    });
    return response.data;
  },

  /**
   * POST /api/auth/login/
   * Login user
   */
  login: async (username, password) => {
    const response = await api.post(Endpoints.AUTH_LOGIN, {
      username,
      password,
    });
    return response.data;
  },

  /**
   * POST /api/auth/logout/
   * Logout user
   */
  logout: async () => {
    await api.post(Endpoints.AUTH_LOGOUT);
  },

  /**
   * GET /api/auth/user/
   * Get current user profile
   */
  getUser: async () => {
    const response = await api.get(Endpoints.AUTH_USER);
    return response.data;
  },
};

// =============================================================================
// DATA API METHODS
// =============================================================================

export const apiClient = {
  /**
   * POST /api/upload/
   * Upload CSV file to backend
   * @param {File} file - CSV file object
   * @param {string|null} filename - Optional custom filename
   * @returns {Promise<UploadResponse>}
   */
  upload: async (file, filename = null) => {
    const formData = new FormData();
    formData.append('file', file);
    if (filename) {
      formData.append('filename', filename);
    }

    const response = await api.post(Endpoints.UPLOAD, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  /**
   * GET /api/summary/<id>/
   * Get dataset summary statistics
   * @param {number} datasetId
   * @returns {Promise<SummaryResponse>}
   */
  getSummary: async (datasetId) => {
    const response = await api.get(Endpoints.summary(datasetId));
    return response.data;
  },

  /**
   * GET /api/datasets/
   * List all datasets (history)
   * @returns {Promise<DatasetListItem[]>}
   */
  getDatasets: async () => {
    const response = await api.get(Endpoints.DATASETS);
    return response.data;
  },

  /**
   * GET /api/datasets/<id>/
   * Get single dataset with all records
   * @param {number} datasetId
   * @returns {Promise<DatasetDetail>}
   */
  getDataset: async (datasetId) => {
    const response = await api.get(Endpoints.dataset(datasetId));
    return response.data;
  },

  /**
   * DELETE /api/datasets/<id>/
   * Delete a dataset
   * @param {number} datasetId
   * @returns {Promise<void>}
   */
  deleteDataset: async (datasetId) => {
    await api.delete(Endpoints.dataset(datasetId));
  },

  /**
   * GET /api/report/<id>/
   * Download PDF report as blob
   * @param {number} datasetId
   * @returns {Promise<Blob>}
   */
  downloadReport: async (datasetId) => {
    const response = await api.get(Endpoints.report(datasetId), {
      responseType: 'blob',
    });
    return response.data;
  },

  /**
   * Check if backend is reachable
   * @returns {Promise<boolean>}
   */
  checkConnection: async () => {
    try {
      await api.get(Endpoints.DATASETS, { timeout: 5000 });
      return true;
    } catch {
      return false;
    }
  },
};

// =============================================================================
// RESPONSE TYPES (JSDoc for IDE support)
// =============================================================================

/**
 * @typedef {Object} UploadResponse
 * @property {boolean} success
 * @property {number} dataset_id
 * @property {string} message
 * @property {SummaryResponse} summary
 */

/**
 * @typedef {Object} SummaryResponse
 * @property {number} total_count
 * @property {number} avg_flowrate
 * @property {number} avg_pressure
 * @property {number} avg_temperature
 * @property {Object.<string, number>} type_distribution - e.g. {"Pump": 5, "Valve": 3}
 */

/**
 * @typedef {Object} DatasetListItem
 * @property {number} id
 * @property {string} filename
 * @property {number} record_count
 * @property {string} uploaded_at - ISO datetime string
 */

/**
 * @typedef {Object} EquipmentRecord
 * @property {number} id
 * @property {string} equipment_name
 * @property {string} equipment_type
 * @property {number} flowrate
 * @property {number} pressure
 * @property {number} temperature
 */

/**
 * @typedef {Object} DatasetDetail
 * @property {number} id
 * @property {string} filename
 * @property {string} uploaded_at
 * @property {EquipmentRecord[]} records
 */

/**
 * @typedef {Object} ErrorResponse
 * @property {string} error
 * @property {string[]} details
 */

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Download blob as file
 * @param {Blob} blob
 * @param {string} filename
 */
export const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

/**
 * Download PDF report and trigger file save
 * @param {number} datasetId
 * @param {string} filename
 */
export const saveReport = async (datasetId, filename = 'report.pdf') => {
  const blob = await apiClient.downloadReport(datasetId);
  downloadBlob(blob, filename);
};

export default apiClient;
