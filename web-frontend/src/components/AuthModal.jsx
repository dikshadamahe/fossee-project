/**
 * Authentication Modal Component
 * Chemical Equipment Parameter Visualizer
 * FOSSEE Scientific Analytics
 * 
 * Login/Register modal with tabbed interface
 */

import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function AuthModal({ isOpen, onClose }) {
    const [activeTab, setActiveTab] = useState('login');
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        passwordConfirm: '',
    });
    const [fieldErrors, setFieldErrors] = useState({});

    const { login, register, loading, error, clearError } = useAuth();

    if (!isOpen) return null;

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        // Clear field error when user types
        if (fieldErrors[name]) {
            setFieldErrors(prev => ({ ...prev, [name]: null }));
        }
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        clearError();
        setFieldErrors({});

        const result = await login(formData.username, formData.password);
        if (result.success) {
            onClose();
            setFormData({ username: '', email: '', password: '', passwordConfirm: '' });
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        clearError();
        setFieldErrors({});

        // Client-side validation
        if (formData.password !== formData.passwordConfirm) {
            setFieldErrors({ passwordConfirm: 'Passwords do not match' });
            return;
        }

        const result = await register(
            formData.username,
            formData.email,
            formData.password,
            formData.passwordConfirm
        );

        if (result.success) {
            onClose();
            setFormData({ username: '', email: '', password: '', passwordConfirm: '' });
        } else if (result.details) {
            setFieldErrors(result.details);
        }
    };

    const handleTabChange = (tab) => {
        setActiveTab(tab);
        clearError();
        setFieldErrors({});
    };

    return (
        <div className="auth-modal-overlay" onClick={onClose}>
            <div className="auth-modal" onClick={e => e.stopPropagation()}>
                {/* Header */}
                <div className="auth-modal-header">
                    <h2>Welcome to FOSSEE Analytics</h2>
                    <button className="auth-modal-close" onClick={onClose}>×</button>
                </div>

                {/* Tabs */}
                <div className="auth-tabs">
                    <button
                        className={`auth-tab ${activeTab === 'login' ? 'active' : ''}`}
                        onClick={() => handleTabChange('login')}
                    >
                        Login
                    </button>
                    <button
                        className={`auth-tab ${activeTab === 'register' ? 'active' : ''}`}
                        onClick={() => handleTabChange('register')}
                    >
                        Register
                    </button>
                </div>

                {/* Error Display */}
                {error && (
                    <div className="auth-error">
                        {error}
                    </div>
                )}

                {/* Login Form */}
                {activeTab === 'login' && (
                    <form onSubmit={handleLogin} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="login-username">Username or Email</label>
                            <input
                                id="login-username"
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                placeholder="Enter your username or email"
                                required
                                disabled={loading}
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="login-password">Password</label>
                            <input
                                id="login-password"
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Enter your password"
                                required
                                disabled={loading}
                            />
                        </div>

                        <button type="submit" className="auth-submit" disabled={loading}>
                            {loading ? 'Logging in...' : 'Login'}
                        </button>
                    </form>
                )}

                {/* Register Form */}
                {activeTab === 'register' && (
                    <form onSubmit={handleRegister} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="register-username">Username</label>
                            <input
                                id="register-username"
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                placeholder="Choose a username"
                                required
                                disabled={loading}
                            />
                            {fieldErrors.username && (
                                <span className="field-error">{fieldErrors.username}</span>
                            )}
                        </div>

                        <div className="form-group">
                            <label htmlFor="register-email">Email</label>
                            <input
                                id="register-email"
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="Enter your email"
                                required
                                disabled={loading}
                            />
                            {fieldErrors.email && (
                                <span className="field-error">{fieldErrors.email}</span>
                            )}
                        </div>

                        <div className="form-group">
                            <label htmlFor="register-password">Password</label>
                            <input
                                id="register-password"
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Create a password (min 8 characters)"
                                required
                                minLength={8}
                                disabled={loading}
                            />
                            {fieldErrors.password && (
                                <span className="field-error">
                                    {Array.isArray(fieldErrors.password)
                                        ? fieldErrors.password.join(', ')
                                        : fieldErrors.password}
                                </span>
                            )}
                        </div>

                        <div className="form-group">
                            <label htmlFor="register-password-confirm">Confirm Password</label>
                            <input
                                id="register-password-confirm"
                                type="password"
                                name="passwordConfirm"
                                value={formData.passwordConfirm}
                                onChange={handleChange}
                                placeholder="Confirm your password"
                                required
                                disabled={loading}
                            />
                            {fieldErrors.passwordConfirm && (
                                <span className="field-error">{fieldErrors.passwordConfirm}</span>
                            )}
                        </div>

                        <button type="submit" className="auth-submit" disabled={loading}>
                            {loading ? 'Creating account...' : 'Create Account'}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
}
