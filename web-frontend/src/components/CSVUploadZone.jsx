/**
 * CSVUploadZone Component
 * Enhanced CSV upload with column preview, mapping detection, and progress
 * FOSSEE Scientific Analytics UI
 * 
 * States: empty, drag, validating, error, success
 */
import { useState, useCallback, useMemo } from 'react';
import { datasetAPI } from '../services/api';

// FOSSEE Color Palette
const COLORS = {
  primary900: '#0F2A44',
  primary700: '#1B7F79',
  primary600: '#3A4E9F',
  success: '#27AB6E',
  warning: '#D97706',
  error: '#C53030',
  bgMain: '#F7F9FC',
  border: '#D9E2EC',
  textPrimary: '#102A43',
  textSecondary: '#486581',
  textMuted: '#829AB1',
};

// Required columns for equipment data
const REQUIRED_COLUMNS = [
  { key: 'equipment_name', label: 'Equipment Name', aliases: ['equipment name', 'name', 'equipment_name', 'equipmentname'] },
  { key: 'type', label: 'Type', aliases: ['type', 'equipment_type', 'equipment type', 'equipmenttype'] },
  { key: 'flowrate', label: 'Flowrate', aliases: ['flowrate', 'flow_rate', 'flow rate', 'flow'] },
  { key: 'pressure', label: 'Pressure', aliases: ['pressure', 'press', 'psi', 'bar'] },
  { key: 'temperature', label: 'Temperature', aliases: ['temperature', 'temp', 'celsius', 'fahrenheit'] },
];

// Icons
const UploadIcon = ({ className = "w-12 h-12" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
  </svg>
);

const CheckCircleIcon = ({ className = "w-12 h-12" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ExclamationIcon = ({ className = "w-12 h-12" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
  </svg>
);

const DocumentIcon = ({ className = "w-5 h-5" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
  </svg>
);

const CheckIcon = ({ className = "w-4 h-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
  </svg>
);

const XIcon = ({ className = "w-4 h-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
  </svg>
);

const ArrowRightIcon = ({ className = "w-4 h-4" }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
  </svg>
);

/**
 * Progress Bar Component
 */
function ProgressBar({ progress, status, message }) {
  const getProgressColor = () => {
    if (status === 'error') return COLORS.error;
    if (status === 'success') return COLORS.success;
    return COLORS.primary700;
  };

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium" style={{ color: COLORS.textSecondary }}>
          {message}
        </span>
        <span className="text-sm font-mono" style={{ color: COLORS.primary700 }}>
          {progress}%
        </span>
      </div>
      <div 
        className="h-2 rounded-full overflow-hidden"
        style={{ backgroundColor: COLORS.bgMain }}
      >
        <div 
          className="h-full rounded-full transition-all duration-500 ease-out"
          style={{ 
            width: `${progress}%`,
            backgroundColor: getProgressColor(),
          }}
        />
      </div>
    </div>
  );
}

/**
 * Column Preview Component
 */
function ColumnPreview({ columns, previewData }) {
  if (!columns || columns.length === 0) return null;

  return (
    <div className="mt-4 overflow-hidden rounded-lg border" style={{ borderColor: COLORS.border }}>
      <div 
        className="px-4 py-2 text-sm font-medium"
        style={{ backgroundColor: COLORS.bgMain, color: COLORS.textSecondary }}
      >
        Column Preview ({columns.length} columns detected)
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr style={{ backgroundColor: COLORS.primary900 }}>
              {columns.map((col, i) => (
                <th 
                  key={i} 
                  className="px-3 py-2 text-left font-mono text-xs whitespace-nowrap"
                  style={{ color: 'white' }}
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {previewData.slice(0, 3).map((row, rowIdx) => (
              <tr 
                key={rowIdx} 
                className="border-t"
                style={{ borderColor: COLORS.border }}
              >
                {columns.map((col, colIdx) => (
                  <td 
                    key={colIdx} 
                    className="px-3 py-2 font-mono text-xs whitespace-nowrap"
                    style={{ color: COLORS.textPrimary }}
                  >
                    {row[colIdx] || '—'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {previewData.length > 3 && (
        <div 
          className="px-4 py-2 text-xs text-center"
          style={{ backgroundColor: COLORS.bgMain, color: COLORS.textMuted }}
        >
          + {previewData.length - 3} more rows
        </div>
      )}
    </div>
  );
}

/**
 * Mapping Detective Component - Shows column mapping status
 */
function MappingDetective({ detectedMappings, columns }) {
  if (!columns || columns.length === 0) return null;

  return (
    <div className="mt-4">
      <div 
        className="text-sm font-medium mb-3 flex items-center gap-2"
        style={{ color: COLORS.textSecondary }}
      >
        <DocumentIcon />
        Column Mapping Detection
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
        {REQUIRED_COLUMNS.map((reqCol) => {
          const mapping = detectedMappings.find(m => m.required === reqCol.key);
          const isMatched = mapping?.matched;
          
          return (
            <div 
              key={reqCol.key}
              className="flex items-center gap-2 px-3 py-2 rounded-lg border"
              style={{ 
                borderColor: isMatched ? COLORS.success : COLORS.error,
                backgroundColor: isMatched ? `${COLORS.success}10` : `${COLORS.error}10`,
              }}
            >
              <div 
                className="flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center"
                style={{ 
                  backgroundColor: isMatched ? COLORS.success : COLORS.error,
                  color: 'white',
                }}
              >
                {isMatched ? <CheckIcon className="w-3 h-3" /> : <XIcon className="w-3 h-3" />}
              </div>
              <div className="flex-1 min-w-0">
                <div 
                  className="text-xs font-medium truncate"
                  style={{ color: COLORS.textPrimary }}
                >
                  {reqCol.label}
                </div>
                {isMatched && (
                  <div className="flex items-center gap-1 text-xs" style={{ color: COLORS.textMuted }}>
                    <span className="truncate">{mapping.source}</span>
                    <ArrowRightIcon className="w-3 h-3 flex-shrink-0" />
                    <span className="truncate font-mono" style={{ color: COLORS.primary700 }}>
                      {reqCol.key}
                    </span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/**
 * Main CSVUploadZone Component
 */
export default function CSVUploadZone({ onUploadSuccess, onUploadError }) {
  // State: 'empty' | 'drag' | 'validating' | 'error' | 'success'
  const [status, setStatus] = useState('empty');
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [errorDetails, setErrorDetails] = useState([]);
  const [fileName, setFileName] = useState('');
  const [fileSize, setFileSize] = useState(0);
  const [columns, setColumns] = useState([]);
  const [previewData, setPreviewData] = useState([]);
  const [detectedMappings, setDetectedMappings] = useState([]);
  const [uploadResult, setUploadResult] = useState(null);

  /**
   * Detect column mappings
   */
  const detectMappings = useCallback((headers) => {
    const mappings = [];
    const normalizedHeaders = headers.map(h => h.toLowerCase().trim());
    
    REQUIRED_COLUMNS.forEach(reqCol => {
      let matchedHeader = null;
      let matchedIndex = -1;
      
      // Check each alias
      for (const alias of reqCol.aliases) {
        const idx = normalizedHeaders.findIndex(h => 
          h === alias || 
          h.replace(/[_\s-]/g, '') === alias.replace(/[_\s-]/g, '')
        );
        if (idx !== -1) {
          matchedHeader = headers[idx];
          matchedIndex = idx;
          break;
        }
      }
      
      mappings.push({
        required: reqCol.key,
        label: reqCol.label,
        matched: matchedHeader !== null,
        source: matchedHeader,
        sourceIndex: matchedIndex,
      });
    });
    
    return mappings;
  }, []);

  /**
   * Parse CSV content
   */
  const parseCSV = useCallback((text) => {
    const lines = text.split('\n').filter(line => line.trim());
    if (lines.length === 0) return { headers: [], rows: [] };
    
    const parseRow = (row) => {
      const result = [];
      let current = '';
      let inQuotes = false;
      
      for (let i = 0; i < row.length; i++) {
        const char = row[i];
        if (char === '"') {
          inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
          result.push(current.trim());
          current = '';
        } else {
          current += char;
        }
      }
      result.push(current.trim());
      return result;
    };
    
    const headers = parseRow(lines[0]);
    const rows = lines.slice(1).map(parseRow);
    
    return { headers, rows };
  }, []);

  /**
   * Validate file
   */
  const validateFile = useCallback(async (file) => {
    setStatus('validating');
    setProgress(10);
    setProgressMessage('Reading file...');
    setFileName(file.name);
    setFileSize(file.size);
    
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onprogress = (e) => {
        if (e.lengthComputable) {
          const readProgress = Math.round((e.loaded / e.total) * 30);
          setProgress(10 + readProgress);
        }
      };
      
      reader.onload = (e) => {
        try {
          setProgress(45);
          setProgressMessage('Parsing CSV structure...');
          
          const { headers, rows } = parseCSV(e.target.result);
          
          if (headers.length === 0) {
            reject({ message: 'CSV file is empty', details: [] });
            return;
          }
          
          if (rows.length === 0) {
            reject({ message: 'CSV file has no data rows', details: [] });
            return;
          }
          
          setColumns(headers);
          setPreviewData(rows.slice(0, 5));
          
          setProgress(60);
          setProgressMessage('Detecting column mappings...');
          
          const mappings = detectMappings(headers);
          setDetectedMappings(mappings);
          
          // Check for missing required columns
          const missing = mappings.filter(m => !m.matched);
          
          if (missing.length > 0) {
            reject({ 
              message: `Missing ${missing.length} required column(s)`,
              details: missing.map(m => `"${m.label}" not found`),
            });
            return;
          }
          
          setProgress(80);
          setProgressMessage('Validation complete');
          
          resolve({ 
            headers, 
            rows, 
            mappings,
            rowCount: rows.length,
          });
        } catch (err) {
          reject({ message: 'Failed to parse CSV file', details: [err.message] });
        }
      };
      
      reader.onerror = () => {
        reject({ message: 'Failed to read file', details: [] });
      };
      
      reader.readAsText(file);
    });
  }, [parseCSV, detectMappings]);

  /**
   * Upload file to server
   */
  const uploadFile = useCallback(async (file) => {
    try {
      // Validate first
      const validation = await validateFile(file);
      
      setProgress(85);
      setProgressMessage('Uploading to server...');
      
      // Upload to server
      const response = await datasetAPI.upload(file);
      
      setProgress(100);
      setProgressMessage('Upload complete!');
      setStatus('success');
      setUploadResult({
        ...response.data,
        rowCount: validation.rowCount,
      });
      
      if (onUploadSuccess) {
        onUploadSuccess(response.data);
      }
    } catch (error) {
      setStatus('error');
      setProgress(0);
      
      if (error.response?.data) {
        setErrorMessage(error.response.data.error || 'Upload failed');
        setErrorDetails(error.response.data.details || []);
      } else if (error.message) {
        setErrorMessage(error.message);
        setErrorDetails(error.details || []);
      } else {
        setErrorMessage('An unexpected error occurred');
        setErrorDetails([]);
      }
      
      if (onUploadError) {
        onUploadError(error);
      }
    }
  }, [validateFile, onUploadSuccess, onUploadError]);

  /**
   * Handle file drop
   */
  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setStatus('empty');
    
    const file = e.dataTransfer?.files?.[0];
    if (file && file.name.endsWith('.csv')) {
      uploadFile(file);
    } else {
      setStatus('error');
      setErrorMessage('Invalid file type');
      setErrorDetails(['Please upload a CSV file (.csv)']);
    }
  }, [uploadFile]);

  /**
   * Handle file input change
   */
  const handleFileChange = useCallback((e) => {
    const file = e.target.files?.[0];
    if (file) {
      uploadFile(file);
    }
  }, [uploadFile]);

  /**
   * Handle drag events
   */
  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (status !== 'validating') {
      setStatus('drag');
    }
  }, [status]);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (status === 'drag') {
      setStatus('empty');
    }
  }, [status]);

  /**
   * Reset to initial state
   */
  const handleReset = useCallback(() => {
    setStatus('empty');
    setProgress(0);
    setProgressMessage('');
    setErrorMessage('');
    setErrorDetails([]);
    setFileName('');
    setFileSize(0);
    setColumns([]);
    setPreviewData([]);
    setDetectedMappings([]);
    setUploadResult(null);
  }, []);

  /**
   * Format file size
   */
  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  /**
   * Get zone styles based on status
   */
  const getZoneStyles = useMemo(() => {
    const base = {
      borderWidth: '2px',
      borderStyle: 'dashed',
      borderRadius: '12px',
      transition: 'all 0.2s ease',
    };
    
    switch (status) {
      case 'drag':
        return {
          ...base,
          borderColor: COLORS.primary700,
          backgroundColor: `${COLORS.primary700}08`,
          borderStyle: 'solid',
        };
      case 'validating':
        return {
          ...base,
          borderColor: COLORS.primary600,
          backgroundColor: `${COLORS.primary600}05`,
        };
      case 'error':
        return {
          ...base,
          borderColor: COLORS.error,
          backgroundColor: `${COLORS.error}05`,
        };
      case 'success':
        return {
          ...base,
          borderColor: COLORS.success,
          backgroundColor: `${COLORS.success}05`,
          borderStyle: 'solid',
        };
      default:
        return {
          ...base,
          borderColor: COLORS.border,
          backgroundColor: 'white',
        };
    }
  }, [status]);

  return (
    <div className="w-full">
      {/* Drop Zone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => status !== 'validating' && document.getElementById('csv-file-input')?.click()}
        className="relative cursor-pointer"
        style={getZoneStyles}
      >
        <input
          id="csv-file-input"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="hidden"
          disabled={status === 'validating'}
        />

        <div className="p-8 text-center">
          {/* Empty State */}
          {status === 'empty' && (
            <div className="flex flex-col items-center gap-4">
              <div 
                className="w-16 h-16 rounded-full flex items-center justify-center"
                style={{ backgroundColor: `${COLORS.primary700}10` }}
              >
                <UploadIcon className="w-8 h-8" style={{ color: COLORS.primary700 }} />
              </div>
              <div>
                <p className="text-lg font-medium" style={{ color: COLORS.textPrimary }}>
                  Drop your CSV file here
                </p>
                <p className="mt-1" style={{ color: COLORS.textSecondary }}>
                  or <span style={{ color: COLORS.primary700 }} className="font-medium">browse</span> to select
                </p>
              </div>
              <div className="flex flex-wrap justify-center gap-2 mt-2">
                {REQUIRED_COLUMNS.map(col => (
                  <span 
                    key={col.key}
                    className="px-2 py-1 rounded text-xs font-mono"
                    style={{ backgroundColor: COLORS.bgMain, color: COLORS.textMuted }}
                  >
                    {col.label}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Drag State */}
          {status === 'drag' && (
            <div className="flex flex-col items-center gap-4">
              <div 
                className="w-16 h-16 rounded-full flex items-center justify-center animate-pulse"
                style={{ backgroundColor: COLORS.primary700 }}
              >
                <UploadIcon className="w-8 h-8 text-white" />
              </div>
              <p className="text-lg font-medium" style={{ color: COLORS.primary700 }}>
                Release to upload
              </p>
            </div>
          )}

          {/* Validating State */}
          {status === 'validating' && (
            <div className="space-y-6">
              <div className="flex items-center gap-4">
                <div 
                  className="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
                  style={{ backgroundColor: `${COLORS.primary600}10` }}
                >
                  <DocumentIcon className="w-6 h-6" style={{ color: COLORS.primary600 }} />
                </div>
                <div className="text-left flex-1">
                  <p className="font-medium truncate" style={{ color: COLORS.textPrimary }}>
                    {fileName}
                  </p>
                  <p className="text-sm" style={{ color: COLORS.textMuted }}>
                    {formatSize(fileSize)}
                  </p>
                </div>
              </div>
              <ProgressBar progress={progress} status="validating" message={progressMessage} />
            </div>
          )}

          {/* Error State */}
          {status === 'error' && (
            <div className="flex flex-col items-center gap-4">
              <div 
                className="w-16 h-16 rounded-full flex items-center justify-center"
                style={{ backgroundColor: `${COLORS.error}10` }}
              >
                <ExclamationIcon className="w-8 h-8" style={{ color: COLORS.error }} />
              </div>
              <div>
                <p className="text-lg font-medium" style={{ color: COLORS.error }}>
                  {errorMessage}
                </p>
                {errorDetails.length > 0 && (
                  <ul className="mt-2 space-y-1">
                    {errorDetails.map((detail, i) => (
                      <li key={i} className="text-sm" style={{ color: COLORS.textMuted }}>
                        • {detail}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); handleReset(); }}
                className="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                style={{ 
                  backgroundColor: `${COLORS.error}10`,
                  color: COLORS.error,
                }}
              >
                Try Again
              </button>
            </div>
          )}

          {/* Success State */}
          {status === 'success' && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div 
                  className="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0"
                  style={{ backgroundColor: `${COLORS.success}10` }}
                >
                  <CheckCircleIcon className="w-8 h-8" style={{ color: COLORS.success }} />
                </div>
                <div className="text-left flex-1">
                  <p className="font-medium" style={{ color: COLORS.success }}>
                    Upload Successful!
                  </p>
                  <p className="text-sm" style={{ color: COLORS.textMuted }}>
                    {uploadResult?.rowCount || 0} records loaded from {fileName}
                  </p>
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); handleReset(); }}
                  className="px-3 py-1.5 rounded text-sm font-medium"
                  style={{ 
                    backgroundColor: COLORS.bgMain,
                    color: COLORS.textSecondary,
                  }}
                >
                  Upload Another
                </button>
              </div>
              <ProgressBar progress={100} status="success" message="Complete" />
            </div>
          )}
        </div>
      </div>

      {/* Column Preview - shown during validation and success */}
      {(status === 'validating' || status === 'success' || status === 'error') && columns.length > 0 && (
        <ColumnPreview columns={columns} previewData={previewData} />
      )}

      {/* Mapping Detective - shown during validation and success */}
      {(status === 'validating' || status === 'success' || status === 'error') && detectedMappings.length > 0 && (
        <MappingDetective detectedMappings={detectedMappings} columns={columns} />
      )}
    </div>
  );
}
