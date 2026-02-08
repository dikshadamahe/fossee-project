/**
 * History Page - List of all uploaded datasets
 * Route: /history
 * Requires authentication - shows login prompt for guests
 */
import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { apiClient, Endpoints } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function HistoryPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(true);
  const [datasets, setDatasets] = useState([]);
  const [error, setError] = useState(null);
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  useEffect(() => {
    // Only load datasets if user is authenticated
    if (!isAuthenticated) {
      setError('login-required');
      setLoading(false);
      return;
    }
    loadDatasets();
  }, [isAuthenticated]);

  const loadDatasets = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getDatasets();
      // Backend returns paginated response: {count, results}
      const data = response.results || response || [];
      setDatasets(data);
      setError(null);
    } catch (err) {
      setError('Failed to load datasets');
    } finally {
      setLoading(false);
    }
  };

  const handleView = (dataset) => {
    navigate('/dashboard', { state: { datasetId: dataset.id } });
  };

  const handleDownload = (dataset) => {
    const reportUrl = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api${Endpoints.report(dataset.id)}`;
    window.open(reportUrl, '_blank');
  };

  const handleDelete = async (dataset) => {
    try {
      await apiClient.deleteDataset(dataset.id);
      setDatasets(prev => prev.filter(d => d.id !== dataset.id));
      setDeleteConfirm(null);
    } catch (err) {
      console.error('Failed to delete dataset:', err);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-700/20 border-t-primary-700 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-text-secondary">Loading history...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-serif text-2xl font-semibold text-text-primary">
            Upload History
          </h1>
          <p className="text-text-secondary mt-1">
            View and manage your previously uploaded datasets
          </p>
        </div>
        <Link to="/" className="btn-primary">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Upload New
        </Link>
      </div>

      {/* Login Required Message */}
      {error === 'login-required' && (
        <div className="lab-panel text-center py-16">
          <div className="w-16 h-16 mx-auto bg-warning/10 text-warning rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 className="font-serif text-xl font-semibold text-text-primary mb-2">Login Required</h2>
          <p className="text-text-secondary mb-6">
            Please log in to view your upload history. Your datasets are synced across web and desktop.
          </p>
          <p className="text-text-muted text-sm">
            Use the Login button in the top right corner to access your account.
          </p>
        </div>
      )}

      {error && error !== 'login-required' && (
        <div className="p-4 bg-error/10 border border-error/20 rounded-lg text-error mb-6">
          {error}
        </div>
      )}

      {error !== 'login-required' && datasets.length === 0 && !error && (
        <div className="lab-panel text-center py-16">
          <div className="w-16 h-16 mx-auto bg-primary-700/10 text-primary-700 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="font-serif text-xl font-semibold text-text-primary mb-2">No Upload History</h2>
          <p className="text-text-secondary mb-6">
            You haven't uploaded any datasets yet.
          </p>
          <Link to="/" className="btn-primary">
            Upload Your First Dataset
          </Link>
        </div>
      )}

      {error !== 'login-required' && datasets.length > 0 && (
        <div className="lab-panel p-0 overflow-hidden">
          <table className="data-table">
            <thead>
              <tr>
                <th>Filename</th>
                <th>Records</th>
                <th>Equipment Types</th>
                <th>Uploaded</th>
                <th className="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {datasets.map((dataset) => (
                <tr key={dataset.id}>
                  <td>
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-primary-700/10 text-primary-700 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <div>
                        <p className="font-medium text-text-primary">{dataset.filename}</p>
                        <p className="text-sm text-text-muted">ID: {dataset.id}</p>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className="font-mono">{dataset.record_count || '—'}</span>
                  </td>
                  <td>
                    <div className="flex flex-wrap gap-1">
                      {dataset.equipment_types?.slice(0, 3).map((type, i) => (
                        <span key={i} className="badge-info text-xs">{type}</span>
                      ))}
                      {dataset.equipment_types?.length > 3 && (
                        <span className="text-text-muted text-xs">+{dataset.equipment_types.length - 3}</span>
                      )}
                    </div>
                  </td>
                  <td>
                    <span className="text-text-secondary">{formatDate(dataset.uploaded_at)}</span>
                  </td>
                  <td>
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => handleView(dataset)}
                        className="p-2 hover:bg-bg-main rounded-lg text-primary-700"
                        title="View Dashboard"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </button>
                      <button
                        onClick={() => handleDownload(dataset)}
                        className="p-2 hover:bg-bg-main rounded-lg text-success"
                        title="Download Report"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </button>
                      <button
                        onClick={() => setDeleteConfirm(dataset)}
                        className="p-2 hover:bg-error/10 rounded-lg text-error"
                        title="Delete"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-elevated p-6 max-w-md mx-4">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-12 h-12 bg-error/10 text-error rounded-full flex items-center justify-center">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-text-primary">Delete Dataset?</h3>
                <p className="text-text-secondary text-sm">
                  This will permanently delete "{deleteConfirm.filename}"
                </p>
              </div>
            </div>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setDeleteConfirm(null)}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button
                onClick={() => handleDelete(deleteConfirm)}
                className="px-4 py-2 bg-error text-white rounded-lg hover:bg-error/90 font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
