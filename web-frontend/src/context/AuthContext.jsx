/**
 * Authentication Context for React
 * Chemical Equipment Parameter Visualizer
 * FOSSEE Scientific Analytics
 * 
 * Provides authentication state and methods throughout the app
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authApi } from '../api/client';

// Types
const AuthContext = createContext(null);

// Token storage keys
const TOKEN_KEY = 'fossee_auth_token';
const USER_KEY = 'fossee_auth_user';

/**
 * Auth Provider Component
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check for stored auth on mount
  useEffect(() => {
    const storedToken = localStorage.getItem(TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);
    
    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } catch (e) {
        // Clear invalid data
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
      }
    }
    setLoading(false);
  }, []);

  // Login
  const login = useCallback(async (username, password) => {
    setError(null);
    setLoading(true);
    
    try {
      const response = await authApi.login(username, password);
      
      // Store in state
      setToken(response.token);
      setUser(response.user);
      
      // Persist to localStorage
      localStorage.setItem(TOKEN_KEY, response.token);
      localStorage.setItem(USER_KEY, JSON.stringify(response.user));
      
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.error || 'Login failed';
      setError(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  }, []);

  // Register
  const register = useCallback(async (username, email, password, passwordConfirm) => {
    setError(null);
    setLoading(true);
    
    try {
      const response = await authApi.register(username, email, password, passwordConfirm);
      
      // Store in state
      setToken(response.token);
      setUser(response.user);
      
      // Persist to localStorage
      localStorage.setItem(TOKEN_KEY, response.token);
      localStorage.setItem(USER_KEY, JSON.stringify(response.user));
      
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.error || 'Registration failed';
      const details = err.response?.data?.details || {};
      setError(message);
      return { success: false, error: message, details };
    } finally {
      setLoading(false);
    }
  }, []);

  // Logout
  const logout = useCallback(async () => {
    try {
      if (token) {
        await authApi.logout();
      }
    } catch (err) {
      // Ignore logout errors
    } finally {
      // Clear state and storage
      setToken(null);
      setUser(null);
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    }
  }, [token]);

  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const value = {
    user,
    token,
    loading,
    error,
    isAuthenticated: !!token,
    login,
    register,
    logout,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to use auth context
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
