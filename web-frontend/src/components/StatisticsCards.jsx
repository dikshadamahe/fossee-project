import React from 'react';

export default function StatisticsCards({ statistics }) {
  if (!statistics) {
    return null;
  }

  const formatValue = (value) => {
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    return value;
  };

  const stats = [
    {
      label: 'Average Flowrate',
      value: statistics.flowrate?.mean,
      details: `Range: ${formatValue(statistics.flowrate?.min)} - ${formatValue(statistics.flowrate?.max)}`,
      colorClass: 'flowrate',
    },
    {
      label: 'Average Pressure',
      value: statistics.pressure?.mean,
      details: `Range: ${formatValue(statistics.pressure?.min)} - ${formatValue(statistics.pressure?.max)}`,
      colorClass: 'pressure',
    },
    {
      label: 'Average Temperature',
      value: statistics.temperature?.mean,
      details: `Range: ${formatValue(statistics.temperature?.min)} - ${formatValue(statistics.temperature?.max)}`,
      colorClass: 'temperature',
    },
  ];

  return (
    <div className="stats-grid">
      {stats.map((stat) => (
        <div key={stat.label} className={`stat-card ${stat.colorClass}`}>
          <div className="stat-label">{stat.label}</div>
          <div className="stat-value">{formatValue(stat.value)}</div>
          <div className="stat-details">{stat.details}</div>
        </div>
      ))}
    </div>
  );
}
