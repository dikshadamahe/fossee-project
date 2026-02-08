/**
 * Dashboard Page - Data visualization and analytics
 * Route: /dashboard
 */
import { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { datasetAPI } from '../services/api';
import SummaryCards from '../components/SummaryCards';
import DataTable from '../components/DataTable';
import { ParameterBarChart, TypeDistributionChart, MultiParameterChart } from '../components/Charts';

export default function DashboardPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [records, setRecords] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  // Get dataset ID from location state or URL params
  const datasetId = location.state?.datasetId;

  useEffect(() => {
    if (!datasetId) {
      // Try to load the most recent dataset
      loadLatestDataset();
    } else {
      loadDataset(datasetId);
    }
  }, [datasetId]);

  const loadLatestDataset = async () => {
    try {
      setLoading(true);
      const response = await datasetAPI.list();
      // Backend returns paginated response: {count, next, previous, results}
      const datasets = response.data.results || response.data;

      if (datasets && datasets.length > 0) {
        // Load the most recent one
        await loadDataset(datasets[0].id);
      } else {
        setError('no-data');
      }
    } catch (err) {
      // If 401 (not logged in), just show no-data prompt instead of error
      if (err.response?.status === 401) {
        setError('no-data');
      } else {
        setError('Failed to load datasets');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadDataset = async (id) => {
    try {
      setLoading(true);
      const response = await datasetAPI.get(id);
      setDataset(response.data);
      setRecords(response.data.records || []);
      // Backend returns summary_json, not statistics
      setStatistics(response.data.summary_json || null);
      setError(null);
    } catch (err) {
      setError('Failed to load dataset');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!dataset?.id) return;

    try {
      window.open(datasetAPI.getReportUrl(dataset.id), '_blank');
    } catch (err) {
      console.error('Failed to download report:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-700/20 border-t-primary-700 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-text-secondary">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error === 'no-data') {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center lab-panel max-w-md">
          <div className="w-16 h-16 mx-auto bg-primary-700/10 text-primary-700 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h2 className="font-serif text-xl font-semibold text-text-primary mb-2">No Data Available</h2>
          <p className="text-text-secondary mb-6">
            Upload a CSV file to see your equipment analytics dashboard.
          </p>
          <Link to="/" className="btn-primary">
            Upload Data
          </Link>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center lab-panel max-w-md">
          <div className="w-16 h-16 mx-auto bg-error/10 text-error rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="font-serif text-xl font-semibold text-text-primary mb-2">Error Loading Data</h2>
          <p className="text-text-secondary mb-6">{error}</p>
          <button onClick={() => window.location.reload()} className="btn-secondary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'charts', label: 'Charts' },
    { id: 'table', label: 'Data Table' },
  ];

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-serif text-2xl font-semibold text-text-primary">
            Analytics Dashboard
          </h1>
          {dataset && (
            <p className="text-text-secondary mt-1">
              {dataset.filename} • {records.length} records
            </p>
          )}
        </div>
        <div className="flex items-center gap-3">
          <Link to="/history" className="btn-secondary">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            History
          </Link>
          <button onClick={handleDownloadReport} className="btn-primary">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download Report
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 mb-6 border-b border-border pb-4">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === tab.id
              ? 'bg-primary-700 text-white'
              : 'text-text-secondary hover:bg-bg-main'
              }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-8">
          {/* Summary Cards */}
          <SummaryCards summary={statistics} />

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <TypeDistributionChart statistics={statistics} />
            <MultiParameterChart records={records.slice(0, 10)} />
          </div>
        </div>
      )}

      {activeTab === 'charts' && (
        <div className="space-y-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="lab-panel p-6">
              <h3 className="font-semibold text-text-primary mb-4">Flow Rate by Equipment</h3>
              <ParameterBarChart records={records.slice(0, 15)} parameter="flowrate" />
            </div>
            <div className="lab-panel p-6">
              <h3 className="font-semibold text-text-primary mb-4">Pressure by Equipment</h3>
              <ParameterBarChart records={records.slice(0, 15)} parameter="pressure" />
            </div>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="lab-panel p-6">
              <h3 className="font-semibold text-text-primary mb-4">Temperature by Equipment</h3>
              <ParameterBarChart records={records.slice(0, 15)} parameter="temperature" />
            </div>
            <TypeDistributionChart statistics={statistics} />
          </div>
        </div>
      )}

      {activeTab === 'table' && (
        <DataTable records={records} pageSize={20} />
      )}
    </div>
  );
}
