/**
 * App Component - Main application with routing
 * Chemical Equipment Parameter Visualizer
 * FOSSEE Scientific Analytics UI
 */
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import UploadPage from './pages/UploadPage';
import DashboardPage from './pages/DashboardPage';
import HistoryPage from './pages/HistoryPage';
import ReportPage from './pages/ReportPage';

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* Home - Upload page */}
          <Route index element={<UploadPage />} />

          {/* Dashboard - Analytics visualization */}
          <Route path="dashboard" element={<DashboardPage />} />

          {/* History - List of uploaded datasets */}
          <Route path="history" element={<HistoryPage />} />

          {/* Report - PDF preview and download */}
          <Route path="report" element={<ReportPage />} />
          <Route path="report/:id" element={<ReportPage />} />

          {/* Catch-all redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}
