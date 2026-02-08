import React, { useState } from 'react';

export default function DataTable({ records, pageSize = 20 }) {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');

  if (!records || records.length === 0) {
    return (
      <div className="empty-state">
        <h3>No data to display</h3>
        <p>Upload a CSV file to see the data table</p>
      </div>
    );
  }

  // Sorting
  const sortedRecords = [...records].sort((a, b) => {
    if (!sortField) return 0;
    
    const aVal = a[sortField];
    const bVal = b[sortField];
    
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
    }
    
    return sortDirection === 'asc' 
      ? String(aVal).localeCompare(String(bVal))
      : String(bVal).localeCompare(String(aVal));
  });

  // Pagination
  const totalPages = Math.ceil(sortedRecords.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const paginatedRecords = sortedRecords.slice(startIndex, startIndex + pageSize);

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const SortIndicator = ({ field }) => {
    if (sortField !== field) return null;
    return <span style={{ marginLeft: '4px' }}>{sortDirection === 'asc' ? '↑' : '↓'}</span>;
  };

  return (
    <div>
      <div className="data-table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('equipment_name')} style={{ cursor: 'pointer' }}>
                Equipment Name <SortIndicator field="equipment_name" />
              </th>
              <th onClick={() => handleSort('equipment_type')} style={{ cursor: 'pointer' }}>
                Type <SortIndicator field="equipment_type" />
              </th>
              <th onClick={() => handleSort('flowrate')} style={{ cursor: 'pointer' }}>
                Flowrate <SortIndicator field="flowrate" />
              </th>
              <th onClick={() => handleSort('pressure')} style={{ cursor: 'pointer' }}>
                Pressure <SortIndicator field="pressure" />
              </th>
              <th onClick={() => handleSort('temperature')} style={{ cursor: 'pointer' }}>
                Temperature <SortIndicator field="temperature" />
              </th>
            </tr>
          </thead>
          <tbody>
            {paginatedRecords.map((record) => (
              <tr key={record.id}>
                <td>{record.equipment_name}</td>
                <td>
                  <span className="type-badge">{record.equipment_type}</span>
                </td>
                <td className="numeric">{record.flowrate.toFixed(2)}</td>
                <td className="numeric">{record.pressure.toFixed(2)}</td>
                <td className="numeric">{record.temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            className="pagination-btn"
            onClick={() => setCurrentPage(1)}
            disabled={currentPage === 1}
          >
            First
          </button>
          <button
            className="pagination-btn"
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span className="pagination-info">
            Page {currentPage} of {totalPages}
          </span>
          <button
            className="pagination-btn"
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
          <button
            className="pagination-btn"
            onClick={() => setCurrentPage(totalPages)}
            disabled={currentPage === totalPages}
          >
            Last
          </button>
        </div>
      )}
    </div>
  );
}
