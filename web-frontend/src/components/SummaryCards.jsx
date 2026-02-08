/**
 * Summary Cards Component
 * Display key metrics in card format
 */

export function SummaryCard({ title, value, unit, icon, trend, color = 'primary' }) {
  const colorClasses = {
    primary: 'text-primary-700 bg-primary-700/10',
    success: 'text-success bg-success/10',
    warning: 'text-warning bg-warning/10',
    error: 'text-error bg-error/10',
  };

  return (
    <div className="summary-card">
      <div className="flex items-start justify-between">
        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${colorClasses[color]}`}>
          {icon}
        </div>
        {trend !== undefined && (
          <span className={`text-sm font-medium ${trend >= 0 ? 'text-success' : 'text-error'}`}>
            {trend >= 0 ? '↑' : '↓'} {Math.abs(trend).toFixed(1)}%
          </span>
        )}
      </div>
      <div className="mt-4">
        <p className="text-text-secondary text-sm">{title}</p>
        <p className="text-2xl font-semibold text-text-primary mt-1 font-mono">
          {typeof value === 'number' ? value.toLocaleString() : value}
          {unit && <span className="text-sm text-text-muted ml-1">{unit}</span>}
        </p>
      </div>
    </div>
  );
}

export function HealthScoreCard({ score, label }) {
  const getScoreColor = (score) => {
    if (score >= 80) return { bg: 'bg-success', text: 'text-success', label: 'Excellent' };
    if (score >= 60) return { bg: 'bg-primary-700', text: 'text-primary-700', label: 'Good' };
    if (score >= 40) return { bg: 'bg-warning', text: 'text-warning', label: 'Fair' };
    return { bg: 'bg-error', text: 'text-error', label: 'Poor' };
  };

  const scoreInfo = getScoreColor(score);

  return (
    <div className="summary-card">
      <div className="flex items-center justify-between mb-4">
        <p className="text-text-secondary text-sm">{label}</p>
        <span className={`badge-${score >= 60 ? 'success' : score >= 40 ? 'warning' : 'error'}`}>
          {scoreInfo.label}
        </span>
      </div>
      <div className="flex items-end gap-3">
        <span className={`text-4xl font-bold font-mono ${scoreInfo.text}`}>
          {score}
        </span>
        <span className="text-text-muted text-sm mb-1">/ 100</span>
      </div>
      <div className="mt-4 h-2 bg-bg-main rounded-full overflow-hidden">
        <div 
          className={`h-full ${scoreInfo.bg} transition-all duration-500`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

export function StatCard({ title, stats }) {
  return (
    <div className="summary-card">
      <h4 className="text-text-primary font-semibold mb-4">{title}</h4>
      <div className="space-y-3">
        {stats.map((stat, index) => (
          <div key={index} className="flex items-center justify-between">
            <span className="text-text-secondary text-sm">{stat.label}</span>
            <span className="font-mono text-text-primary">
              {typeof stat.value === 'number' ? stat.value.toFixed(2) : stat.value}
              {stat.unit && <span className="text-text-muted text-xs ml-1">{stat.unit}</span>}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function SummaryCards({ summary }) {
  if (!summary) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <SummaryCard
        title="Total Records"
        value={summary.total_records || 0}
        color="primary"
        icon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        }
      />
      <SummaryCard
        title="Equipment Types"
        value={summary.type_distribution ? Object.keys(summary.type_distribution).length : 0}
        color="success"
        icon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        }
      />
      <SummaryCard
        title="Outliers Detected"
        value={summary.outlier_count || 0}
        color={summary.outlier_count > 0 ? 'warning' : 'success'}
        icon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        }
      />
      {summary.health_scores && (
        <HealthScoreCard 
          score={summary.health_scores.overall || 0} 
          label="Overall Health Score"
        />
      )}
    </div>
  );
}
