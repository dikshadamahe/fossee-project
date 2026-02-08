/**
 * Report Page - PDF report preview and download
 * Route: /report/:id
 */
import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { datasetAPI } from '../services/api';
import SummaryCards from '../components/SummaryCards';
import { TypeDistributionChart } from '../components/Charts';
import DataTable from '../components/DataTable';

export default function ReportPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [dataset, setDataset] = useState(null);
  const [error, setError] = useState(null);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    if (id) {
      loadDataset(id);
    } else {
      loadLatestDataset();
    }
  }, [id]);

  const loadLatestDataset = async () => {
    try {
      setLoading(true);
      const response = await datasetAPI.list();
      if (response.data && response.data.length > 0) {
        navigate(`/report/${response.data[0].id}`, { replace: true });
      } else {
        setError('no-data');
      }
    } catch (err) {
      setError('Failed to load datasets');
    } finally {
      setLoading(false);
    }
  };

  const loadDataset = async (datasetId) => {
    try {
      setLoading(true);
      const response = await datasetAPI.get(datasetId);
      setDataset(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load dataset');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!dataset?.id) return;
    
    setDownloading(true);
    try {
      window.open(datasetAPI.getReportUrl(dataset.id), '_blank');
    } catch (err) {
      console.error('Failed to download report:', err);
    } finally {
      setTimeout(() => setDownloading(false), 1000);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-700/20 border-t-primary-700 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-text-secondary">Loading report...</p>
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
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h2 className="font-serif text-xl font-semibold text-text-primary mb-2">No Data Available</h2>
          <p className="text-text-secondary mb-6">
            Upload a CSV file to generate a report.
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
          <h2 className="font-serif text-xl font-semibold text-text-primary mb-2">Error Loading Report</h2>
          <p className="text-text-secondary mb-6">{error}</p>
          <Link to="/history" className="btn-secondary">
            View History
          </Link>
        </div>
      </div>
    );
  }

  const records = dataset?.records || [];
  const statistics = dataset?.statistics || {};

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-serif text-2xl font-semibold text-text-primary">
            Equipment Analysis Report
          </h1>
          <p className="text-text-secondary mt-1">
            {dataset?.filename} • Generated {new Date().toLocaleDateString()}
          </p>
        </div>
        <button 
          onClick={handleDownload}
          disabled={downloading}
          className="btn-primary disabled:opacity-60"
        >
          {downloading ? (
            <>
              <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download PDF
            </>
          )}
        </button>
      </div>

      {/* Report Preview */}
      <div className="space-y-8">
        {/* Summary Section */}
        <section>
          <h2 className="font-serif text-lg font-semibold text-text-primary mb-4 pb-2 border-b border-border">
            Executive Summary
          </h2>
          <SummaryCards summary={statistics} />
        </section>

        {/* Type Distribution */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h2 className="font-serif text-lg font-semibold text-text-primary mb-4 pb-2 border-b border-border">
              Equipment Distribution
            </h2>
            <TypeDistributionChart statistics={statistics} />
          </div>
          
          {/* Parameter Statistics */}
          <div>
            <h2 className="font-serif text-lg font-semibold text-text-primary mb-4 pb-2 border-b border-border">
              Parameter Statistics
            </h2>
            <div className="lab-panel">
              <table className="data-table text-sm">
                <thead>
                  <tr>
                    <th>Parameter</th>
                    <th>Mean</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>Std Dev</th>
                  </tr>
                </thead>
                <tbody>
                  {statistics.parameter_stats && Object.entries(statistics.parameter_stats).map(([param, stats]) => (
                    <tr key={param}>
                      <td className="font-medium">{param.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</td>
                      <td className="font-mono">{stats.mean?.toFixed(2) || '—'}</td>
                      <td className="font-mono">{stats.min?.toFixed(2) || '—'}</td>
                      <td className="font-mono">{stats.max?.toFixed(2) || '—'}</td>
                      <td className="font-mono">{stats.std?.toFixed(2) || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Data Preview */}
        <section>
          <h2 className="font-serif text-lg font-semibold text-text-primary mb-4 pb-2 border-b border-border">
            Data Preview (First 20 Records)
          </h2>
          <DataTable records={records.slice(0, 20)} pageSize={20} />
        </section>

        {/* Outliers Section */}
        {statistics.outliers && Object.keys(statistics.outliers).some(k => statistics.outliers[k]?.length > 0) && (
          <section>
            <h2 className="font-serif text-lg font-semibold text-text-primary mb-4 pb-2 border-b border-border">
              Outlier Analysis
            </h2>
            <div className="lab-panel">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(statistics.outliers).map(([param, indices]) => (
                  <div key={param} className="p-4 bg-bg-main rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-text-primary">
                        {param.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                      </span>
                      <span className={`badge-${indices.length > 0 ? 'warning' : 'success'}`}>
                        {indices.length} outliers
                      </span>
                    </div>
                    {indices.length > 0 && (
                      <p className="text-sm text-text-muted">
                        Records: {indices.slice(0, 5).join(', ')}
                        {indices.length > 5 && ` +${indices.length - 5} more`}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        {/* Footer */}
        <div className="text-center py-8 border-t border-border">
          <p className="text-text-muted text-sm">
            Generated by Chemical Equipment Parameter Visualizer • FOSSEE Project • IIT Bombay
          </p>
        </div>
      </div>
    </div>
  );
}
