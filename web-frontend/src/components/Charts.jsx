/**
 * Chart.js Components
 * Chemical Equipment Parameter Visualizer
 * FOSSEE Scientific Analytics UI
 * 
 * Components:
 * - TypeDistributionBar: Bar chart for equipment type distribution
 * - ParameterLineChart: Line chart for Flow/Pressure/Temperature trends
 * - SummaryCards: Key metrics display cards
 */
import { useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';

// FOSSEE Color Palette
const COLORS = {
  primary900: '#0F2A44',
  primary700: '#1B7F79',
  primary600: '#3A4E9F',
  flowrate: '#1B7F79',
  pressure: '#3A4E9F',
  temperature: '#C53030',
  success: '#27AB6E',
  warning: '#D97706',
  error: '#C53030',
  bgMain: '#F7F9FC',
  border: '#D9E2EC',
  textPrimary: '#102A43',
  textSecondary: '#486581',
  textMuted: '#829AB1',
  distribution: ['#1B7F79', '#3A4E9F', '#D97706', '#C53030', '#27AB6E', '#7C3AED', '#0891B2'],
};

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Generate plain English insight for a value
 */
function generateInsight(value, parameter, context = {}) {
  const { mean, min, max, total } = context;

  if (parameter === 'count' || parameter === 'type') {
    const percentage = total ? ((value / total) * 100).toFixed(1) : 0;
    if (percentage > 30) return `This is a major category, representing ${percentage}% of all equipment`;
    if (percentage > 15) return `A significant portion at ${percentage}% of the total`;
    return `Makes up ${percentage}% of the equipment inventory`;
  }

  if (parameter === 'flowrate') {
    if (mean && value > mean * 1.2) return `High flow rate - ${((value / mean - 1) * 100).toFixed(0)}% above average`;
    if (mean && value < mean * 0.8) return `Low flow rate - ${((1 - value / mean) * 100).toFixed(0)}% below average`;
    return `Normal flow rate within expected range`;
  }

  if (parameter === 'pressure') {
    if (mean && value > mean * 1.15) return `Elevated pressure - monitor for potential issues`;
    if (mean && value < mean * 0.85) return `Low pressure - may indicate leaks or blockages`;
    return `Pressure within normal operating range`;
  }

  if (parameter === 'temperature') {
    if (value > 100) return `High temperature - ensure cooling systems are active`;
    if (value > 80) return `Warm - approaching upper threshold`;
    if (value < 20) return `Cold - verify if this is expected for operation`;
    return `Temperature within safe operating range`;
  }

  return `Value: ${typeof value === 'number' ? value.toFixed(2) : value}`;
}

/**
 * Format number with appropriate precision
 */
function formatValue(value, unit = '') {
  if (typeof value !== 'number') return value;
  const formatted = value >= 1000 ? value.toLocaleString() : value.toFixed(2);
  return unit ? `${formatted} ${unit}` : formatted;
}

/**
 * Get unit for parameter
 */
function getUnit(parameter) {
  const units = {
    flowrate: 'L/min',
    pressure: 'bar',
    temperature: '°C',
  };
  return units[parameter] || '';
}

// ============================================================================
// TYPE DISTRIBUTION BAR CHART
// ============================================================================

/**
 * Bar chart showing equipment type distribution
 */
export function TypeDistributionBar({ statistics, title = 'Equipment Type Distribution' }) {
  const { chartData, total } = useMemo(() => {
    if (!statistics?.type_distribution) return { chartData: null, total: 0 };

    const entries = Object.entries(statistics.type_distribution)
      .sort((a, b) => b[1] - a[1]); // Sort by count descending

    const labels = entries.map(([type]) => type);
    const data = entries.map(([, count]) => count);
    const total = data.reduce((sum, val) => sum + val, 0);

    return {
      chartData: {
        labels,
        datasets: [{
          label: 'Equipment Count',
          data,
          backgroundColor: COLORS.distribution.slice(0, data.length),
          borderRadius: 6,
          borderSkipped: false,
          maxBarThickness: 60,
        }],
      },
      total,
    };
  }, [statistics]);

  const options = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: COLORS.primary900,
        titleFont: { family: 'Inter', size: 13, weight: '600' },
        bodyFont: { family: 'JetBrains Mono', size: 12 },
        padding: 12,
        cornerRadius: 8,
        displayColors: true,
        callbacks: {
          title: (items) => `${items[0].label} Equipment`,
          label: (context) => {
            const count = context.raw;
            const percentage = ((count / total) * 100).toFixed(1);
            return `  ${count} units (${percentage}%)`;
          },
          afterLabel: (context) => {
            const insight = generateInsight(context.raw, 'type', { total });
            return `  💡 ${insight}`;
          },
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: { color: COLORS.border, drawBorder: false },
        ticks: {
          font: { family: 'JetBrains Mono', size: 11 },
          color: COLORS.textMuted,
        },
      },
      y: {
        grid: { display: false },
        ticks: {
          font: { family: 'Inter', size: 12, weight: '500' },
          color: COLORS.textPrimary,
        },
      },
    },
  }), [total]);

  if (!chartData) {
    return (
      <div className="lab-panel flex items-center justify-center h-64">
        <p className="text-text-muted">No type distribution data available</p>
      </div>
    );
  }

  return (
    <div className="lab-panel">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold" style={{ color: COLORS.textPrimary }}>{title}</h3>
        <span
          className="text-sm font-mono px-2 py-1 rounded"
          style={{ backgroundColor: COLORS.bgMain, color: COLORS.textMuted }}
        >
          {total} total
        </span>
      </div>
      <div style={{ height: `${Math.max(200, chartData.labels.length * 45)}px` }}>
        <Bar data={chartData} options={options} />
      </div>
    </div>
  );
}

// ============================================================================
// PARAMETER LINE CHART
// ============================================================================

/**
 * Line chart for Flow Rate, Pressure, Temperature trends
 */
export function ParameterLineChart({ records, title = 'Parameter Trends', showLegend = true }) {
  const { chartData, stats } = useMemo(() => {
    if (!records || records.length === 0) return { chartData: null, stats: {} };

    // Calculate statistics for insights
    const calcStats = (values) => {
      const valid = values.filter(v => v != null && !isNaN(v));
      if (valid.length === 0) return { mean: 0, min: 0, max: 0 };
      return {
        mean: valid.reduce((a, b) => a + b, 0) / valid.length,
        min: Math.min(...valid),
        max: Math.max(...valid),
      };
    };

    const flowrates = records.map(r => r.flowrate);
    const pressures = records.map(r => r.pressure);
    const temperatures = records.map(r => r.temperature);

    const stats = {
      flowrate: calcStats(flowrates),
      pressure: calcStats(pressures),
      temperature: calcStats(temperatures),
    };

    const labels = records.map((r, i) => r.equipment_name?.substring(0, 10) || `#${i + 1}`);

    return {
      chartData: {
        labels,
        datasets: [
          {
            label: 'Flow Rate (L/min)',
            data: flowrates,
            borderColor: COLORS.flowrate,
            backgroundColor: `${COLORS.flowrate}20`,
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: COLORS.flowrate,
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
          },
          {
            label: 'Pressure (bar)',
            data: pressures,
            borderColor: COLORS.pressure,
            backgroundColor: `${COLORS.pressure}20`,
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: COLORS.pressure,
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
          },
          {
            label: 'Temperature (°C)',
            data: temperatures,
            borderColor: COLORS.temperature,
            backgroundColor: `${COLORS.temperature}20`,
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: COLORS.temperature,
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
          },
        ],
      },
      stats,
    };
  }, [records]);

  const options = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        display: showLegend,
        position: 'top',
        labels: {
          font: { family: 'Inter', size: 12 },
          color: COLORS.textSecondary,
          padding: 16,
          usePointStyle: true,
          pointStyle: 'circle',
        },
      },
      tooltip: {
        backgroundColor: COLORS.primary900,
        titleFont: { family: 'Inter', size: 13, weight: '600' },
        bodyFont: { family: 'JetBrains Mono', size: 12 },
        padding: 14,
        cornerRadius: 8,
        displayColors: true,
        callbacks: {
          title: (items) => `📍 ${items[0].label}`,
          label: (context) => {
            const value = context.raw;
            const datasetLabel = context.dataset.label;
            return `  ${datasetLabel}: ${formatValue(value)}`;
          },
          afterBody: (items) => {
            const insights = [];
            items.forEach(item => {
              let param = '';
              if (item.dataset.label.includes('Flow')) param = 'flowrate';
              else if (item.dataset.label.includes('Pressure')) param = 'pressure';
              else if (item.dataset.label.includes('Temperature')) param = 'temperature';

              if (param && stats[param]) {
                const insight = generateInsight(item.raw, param, stats[param]);
                insights.push(`  💡 ${insight}`);
              }
            });
            return insights.length > 0 ? ['', '─── Insights ───', ...insights] : [];
          },
        },
      },
    },
    scales: {
      x: {
        grid: { color: COLORS.border, drawBorder: false },
        ticks: {
          font: { family: 'Inter', size: 11 },
          color: COLORS.textMuted,
          maxRotation: 45,
        },
      },
      y: {
        beginAtZero: true,
        grid: { color: COLORS.border, drawBorder: false },
        ticks: {
          font: { family: 'JetBrains Mono', size: 11 },
          color: COLORS.textMuted,
        },
      },
    },
  }), [showLegend, stats]);

  if (!chartData) {
    return (
      <div className="lab-panel flex items-center justify-center h-64">
        <p className="text-text-muted">No parameter data available</p>
      </div>
    );
  }

  return (
    <div className="lab-panel p-6">
      <h3 className="font-semibold mb-4" style={{ color: COLORS.textPrimary }}>{title}</h3>
      <div style={{ height: '320px' }}>
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
}

// ============================================================================
// SUMMARY CARDS
// ============================================================================

/**
 * Individual Summary Card
 */
function SummaryCard({ title, value, unit, icon, color, insight, trend }) {
  const trendColor = trend > 0 ? COLORS.success : trend < 0 ? COLORS.error : COLORS.textMuted;
  const trendIcon = trend > 0 ? '↑' : trend < 0 ? '↓' : '→';

  return (
    <div
      className="rounded-xl p-5 border transition-shadow hover:shadow-lg"
      style={{
        backgroundColor: 'white',
        borderColor: COLORS.border,
      }}
    >
      <div className="flex items-start justify-between mb-3">
        <div
          className="w-10 h-10 rounded-lg flex items-center justify-center"
          style={{ backgroundColor: `${color}15` }}
        >
          <span style={{ color }}>{icon}</span>
        </div>
        {trend !== undefined && (
          <span
            className="text-sm font-medium flex items-center gap-1"
            style={{ color: trendColor }}
          >
            {trendIcon} {Math.abs(trend).toFixed(1)}%
          </span>
        )}
      </div>

      <p className="text-sm mb-1" style={{ color: COLORS.textSecondary }}>{title}</p>

      <div className="flex items-baseline gap-1">
        <span
          className="text-2xl font-bold font-mono"
          style={{ color: COLORS.textPrimary }}
        >
          {typeof value === 'number' ? formatValue(value) : value}
        </span>
        {unit && (
          <span className="text-sm" style={{ color: COLORS.textMuted }}>{unit}</span>
        )}
      </div>

      {insight && (
        <p
          className="text-xs mt-2 pt-2 border-t"
          style={{ color: COLORS.textMuted, borderColor: COLORS.border }}
        >
          💡 {insight}
        </p>
      )}
    </div>
  );
}

/**
 * Summary Cards Grid
 */
export function SummaryCardsGrid({ statistics, records }) {
  const cardData = useMemo(() => {
    if (!statistics && !records) return [];

    const cards = [];

    // Total Records
    const totalRecords = records?.length || statistics?.total_records || 0;
    cards.push({
      title: 'Total Equipment',
      value: totalRecords,
      unit: 'units',
      icon: '📊',
      color: COLORS.primary700,
      insight: totalRecords > 100
        ? 'Large dataset - analysis may reveal significant patterns'
        : totalRecords > 20
          ? 'Good sample size for reliable statistics'
          : 'Consider adding more data for better insights',
    });

    // Equipment Types
    const typeCount = statistics?.type_distribution
      ? Object.keys(statistics.type_distribution).length
      : 0;
    cards.push({
      title: 'Equipment Types',
      value: typeCount,
      unit: 'types',
      icon: '🏭',
      color: COLORS.primary600,
      insight: typeCount > 5
        ? 'Diverse equipment portfolio detected'
        : typeCount > 2
          ? 'Moderate variety in equipment types'
          : 'Limited equipment types in this dataset',
    });

    // Parameter Statistics
    if (statistics?.parameter_stats) {
      const params = statistics.parameter_stats;

      if (params.flowrate) {
        cards.push({
          title: 'Avg Flow Rate',
          value: params.flowrate.mean,
          unit: 'L/min',
          icon: '💧',
          color: COLORS.flowrate,
          insight: generateInsight(params.flowrate.mean, 'flowrate', params.flowrate),
        });
      }

      if (params.pressure) {
        cards.push({
          title: 'Avg Pressure',
          value: params.pressure.mean,
          unit: 'bar',
          icon: '⚡',
          color: COLORS.pressure,
          insight: generateInsight(params.pressure.mean, 'pressure', params.pressure),
        });
      }

      if (params.temperature) {
        cards.push({
          title: 'Avg Temperature',
          value: params.temperature.mean,
          unit: '°C',
          icon: '🌡️',
          color: COLORS.temperature,
          insight: generateInsight(params.temperature.mean, 'temperature', params.temperature),
        });
      }
    }

    // Outliers
    if (statistics?.outliers) {
      const outlierCount = Object.values(statistics.outliers)
        .reduce((sum, arr) => sum + (arr?.length || 0), 0);
      cards.push({
        title: 'Outliers Detected',
        value: outlierCount,
        unit: 'records',
        icon: '⚠️',
        color: outlierCount > 0 ? COLORS.warning : COLORS.success,
        insight: outlierCount > 5
          ? 'Multiple anomalies detected - review recommended'
          : outlierCount > 0
            ? 'A few unusual readings found - may need investigation'
            : 'All readings within normal ranges',
      });
    }

    // Health Score
    if (statistics?.health_scores?.overall !== undefined) {
      const score = statistics.health_scores.overall;
      cards.push({
        title: 'Overall Health',
        value: score,
        unit: '/ 100',
        icon: '❤️',
        color: score >= 80 ? COLORS.success : score >= 60 ? COLORS.warning : COLORS.error,
        insight: score >= 80
          ? 'Excellent - equipment operating optimally'
          : score >= 60
            ? 'Good - minor attention may be needed'
            : 'Needs attention - review equipment status',
      });
    }

    return cards;
  }, [statistics, records]);

  if (cardData.length === 0) {
    return (
      <div className="lab-panel text-center py-8">
        <p style={{ color: COLORS.textMuted }}>No summary data available</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {cardData.map((card, index) => (
        <SummaryCard key={index} {...card} />
      ))}
    </div>
  );
}

// ============================================================================
// LEGACY EXPORTS (for backward compatibility)
// ============================================================================

export function ParameterBarChart({ records, parameter }) {
  const chartData = useMemo(() => {
    if (!records || records.length === 0) return null;

    const labels = records.map(r => r.equipment_name?.substring(0, 15) || 'Unknown');
    const data = records.map(r => r[parameter]);
    const mean = data.reduce((a, b) => a + b, 0) / data.length;

    const colorMap = {
      flowrate: COLORS.flowrate,
      pressure: COLORS.pressure,
      temperature: COLORS.temperature,
    };

    return {
      labels,
      datasets: [{
        label: parameter.charAt(0).toUpperCase() + parameter.slice(1),
        data,
        backgroundColor: colorMap[parameter] || COLORS.primary700,
        borderRadius: 4,
        maxBarThickness: 50,
      }],
      stats: { mean, min: Math.min(...data), max: Math.max(...data) },
    };
  }, [records, parameter]);

  const options = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: COLORS.primary900,
        titleFont: { family: 'Inter', size: 13, weight: '600' },
        bodyFont: { family: 'JetBrains Mono', size: 12 },
        padding: 12,
        cornerRadius: 8,
        callbacks: {
          label: (context) => `  ${formatValue(context.raw, getUnit(parameter))}`,
          afterLabel: (context) => {
            const insight = generateInsight(context.raw, parameter, chartData?.stats || {});
            return `  💡 ${insight}`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: {
          font: { family: 'Inter', size: 11 },
          color: COLORS.textMuted,
          maxRotation: 45,
        },
      },
      y: {
        beginAtZero: true,
        grid: { color: COLORS.border },
        ticks: {
          font: { family: 'JetBrains Mono', size: 11 },
          color: COLORS.textMuted,
        },
      },
    },
  }), [parameter, chartData]);

  if (!chartData) {
    return <div className="flex items-center justify-center h-48 text-text-muted">No data available</div>;
  }

  return (
    <div style={{ height: '280px' }}>
      <Bar data={chartData} options={options} />
    </div>
  );
}

export function TypeDistributionChart({ statistics }) {
  const { chartData, total } = useMemo(() => {
    if (!statistics?.type_distribution) return { chartData: null, total: 0 };

    const labels = Object.keys(statistics.type_distribution);
    const data = Object.values(statistics.type_distribution);
    const total = data.reduce((sum, val) => sum + val, 0);

    return {
      chartData: {
        labels,
        datasets: [{
          data,
          backgroundColor: COLORS.distribution.slice(0, data.length),
          borderColor: '#FFFFFF',
          borderWidth: 3,
          hoverOffset: 8,
        }],
      },
      total,
    };
  }, [statistics]);

  const options = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          font: { family: 'Inter', size: 12 },
          color: COLORS.textSecondary,
          padding: 12,
          usePointStyle: true,
        },
      },
      tooltip: {
        backgroundColor: COLORS.primary900,
        titleFont: { family: 'Inter', size: 13, weight: '600' },
        bodyFont: { family: 'JetBrains Mono', size: 12 },
        padding: 12,
        cornerRadius: 8,
        callbacks: {
          label: (context) => {
            const count = context.raw;
            const percentage = ((count / total) * 100).toFixed(1);
            return `  ${count} units (${percentage}%)`;
          },
          afterLabel: (context) => {
            const insight = generateInsight(context.raw, 'type', { total });
            return `  💡 ${insight}`;
          },
        },
      },
    },
  }), [total]);

  if (!chartData) {
    return <div className="flex items-center justify-center h-48 text-text-muted">No data available</div>;
  }

  return (
    <div className="lab-panel p-6" style={{ height: '320px' }}>
      <Doughnut data={chartData} options={options} />
    </div>
  );
}

export function MultiParameterChart({ records }) {
  return <ParameterLineChart records={records} title="Multi-Parameter Overview" />;
}
