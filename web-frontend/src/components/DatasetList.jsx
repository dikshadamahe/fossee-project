import React from 'react';

export default function DatasetList({ datasets, activeId, onSelect, onDelete }) {
  if (!datasets || datasets.length === 0) {
    return (
      <div className="empty-state" style={{ padding: 'var(--space-6)' }}>
        <p className="text-muted">No datasets uploaded yet</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="dataset-list">
      {datasets.map((dataset) => (
        <div
          key={dataset.id}
          className={`dataset-item ${activeId === dataset.id ? 'active' : ''}`}
          onClick={() => onSelect(dataset.id)}
        >
          <div className="dataset-info">
            <h4>{dataset.name}</h4>
            <p className="dataset-meta">
              <span className="mono">{dataset.row_count}</span> records · {formatDate(dataset.uploaded_at)}
            </p>
          </div>
          <div className="lab-panel-actions">
            <button
              className="btn btn-sm btn-danger"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(dataset.id);
              }}
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
