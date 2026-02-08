/**
 * Upload Page - CSV file upload interface
 * Route: /
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CSVUploadZone from '../components/CSVUploadZone';

export default function UploadPage() {
  const navigate = useNavigate();
  const [uploadResult, setUploadResult] = useState(null);

  const handleUploadSuccess = (data) => {
    setUploadResult(data);
    // Navigate to dashboard after successful upload
    setTimeout(() => {
      navigate('/dashboard', { state: { datasetId: data.id, summary: data } });
    }, 1500);
  };

  const handleUploadError = (error) => {
    console.error('Upload error:', error);
  };

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="font-serif text-3xl font-semibold text-text-primary mb-3">
          Upload Equipment Data
        </h1>
        <p className="text-text-secondary">
          Upload your CSV file containing chemical equipment parameters for analysis and visualization.
        </p>
      </div>

      {/* Upload Zone */}
      <CSVUploadZone 
        onUploadSuccess={handleUploadSuccess}
        onUploadError={handleUploadError}
      />

      {/* Expected Format */}
      <div className="lab-panel mt-8">
        <h3 className="font-semibold text-text-primary mb-4">Expected CSV Format</h3>
        <p className="text-text-secondary text-sm mb-4">
          Your CSV file should contain the following columns:
        </p>
        <div className="overflow-x-auto">
          <table className="data-table text-sm">
            <thead>
              <tr>
                <th>Column Name</th>
                <th>Type</th>
                <th>Description</th>
                <th>Example</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code className="text-primary-700">Equipment Name</code></td>
                <td><span className="badge-info">String</span></td>
                <td>Unique identifier for the equipment</td>
                <td className="font-mono">Pump-101</td>
              </tr>
              <tr>
                <td><code className="text-primary-700">Type</code></td>
                <td><span className="badge-info">String</span></td>
                <td>Equipment category</td>
                <td className="font-mono">Pump</td>
              </tr>
              <tr>
                <td><code className="text-primary-700">Flowrate</code></td>
                <td><span className="badge-success">Number</span></td>
                <td>Flow rate measurement (L/min)</td>
                <td className="font-mono">125.50</td>
              </tr>
              <tr>
                <td><code className="text-primary-700">Pressure</code></td>
                <td><span className="badge-success">Number</span></td>
                <td>Pressure reading (bar)</td>
                <td className="font-mono">3.25</td>
              </tr>
              <tr>
                <td><code className="text-primary-700">Temperature</code></td>
                <td><span className="badge-success">Number</span></td>
                <td>Temperature reading (°C)</td>
                <td className="font-mono">75.8</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <div className="lab-panel text-center">
          <div className="w-12 h-12 mx-auto bg-primary-700/10 text-primary-700 rounded-lg flex items-center justify-center mb-4">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h4 className="font-semibold text-text-primary mb-2">Statistical Analysis</h4>
          <p className="text-text-secondary text-sm">
            Get mean, min, max, and standard deviation for all parameters
          </p>
        </div>

        <div className="lab-panel text-center">
          <div className="w-12 h-12 mx-auto bg-warning/10 text-warning rounded-lg flex items-center justify-center mb-4">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h4 className="font-semibold text-text-primary mb-2">Outlier Detection</h4>
          <p className="text-text-secondary text-sm">
            IQR-based anomaly detection highlights unusual readings
          </p>
        </div>

        <div className="lab-panel text-center">
          <div className="w-12 h-12 mx-auto bg-success/10 text-success rounded-lg flex items-center justify-center mb-4">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h4 className="font-semibold text-text-primary mb-2">Health Scoring</h4>
          <p className="text-text-secondary text-sm">
            0-100 health scores for equipment monitoring
          </p>
        </div>
      </div>
    </div>
  );
}
