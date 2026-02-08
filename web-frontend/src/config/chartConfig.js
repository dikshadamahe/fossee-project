/**
 * Chart.js Configuration
 * FOSSEE Scientific Analytics UI - design.md Chart Palette
 * 
 * Rules from design.md Section 7:
 * - No 3D
 * - No gradients
 * - Tooltips plain English
 * - Legend bottom
 * - Max 5 colors per chart
 */

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
} from 'chart.js'

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
)

// =================================================================
// FOSSEE Color Palette (design.md Section 2)
// =================================================================

export const chartColors = {
  // Parameter colors
  flowrate: '#1B7F79',
  pressure: '#3A4E9F',
  temperature: '#C53030',
  
  // Distribution set (max 5 colors)
  distribution: [
    '#1B7F79', // primary-700
    '#3A4E9F', // primary-600
    '#2EA043', // success
    '#D97706', // warning
    '#C53030', // error (5th color if needed)
  ],
  
  // Semantic colors
  success: '#2EA043',
  warning: '#D97706',
  error: '#C53030',
  
  // Neutral
  grid: '#E2E8F0',
  text: '#102A43',
  textSecondary: '#486581',
  textMuted: '#829AB1',
  background: '#FFFFFF',
}

export const chartFonts = {
  family: "'Inter', 'Segoe UI', 'Noto Sans', sans-serif",
  monoFamily: "'JetBrains Mono', 'Consolas', monospace",
}

// =================================================================
// Chart.js Global Defaults (design.md Section 7)
// =================================================================

ChartJS.defaults.font.family = chartFonts.family
ChartJS.defaults.font.size = 12
ChartJS.defaults.color = chartColors.textSecondary
ChartJS.defaults.plugins.legend.position = 'bottom'
ChartJS.defaults.plugins.legend.labels.usePointStyle = true
ChartJS.defaults.plugins.legend.labels.padding = 16

// Tooltip styling
ChartJS.defaults.plugins.tooltip.backgroundColor = chartColors.text
ChartJS.defaults.plugins.tooltip.titleFont = { weight: '600' }
ChartJS.defaults.plugins.tooltip.bodyFont = { family: chartFonts.monoFamily }
ChartJS.defaults.plugins.tooltip.padding = 12
ChartJS.defaults.plugins.tooltip.cornerRadius = 8
ChartJS.defaults.plugins.tooltip.displayColors = true

// =================================================================
// Default Chart Options
// =================================================================

export const defaultChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        font: {
          family: chartFonts.family,
          size: 12,
        },
        color: chartColors.textSecondary,
        padding: 16,
        usePointStyle: true,
      },
    },
    tooltip: {
      backgroundColor: chartColors.text,
      titleFont: {
        family: chartFonts.family,
        size: 13,
        weight: '600',
      },
      bodyFont: {
        family: chartFonts.monoFamily,
        size: 12,
      },
      padding: 12,
      cornerRadius: 8,
      displayColors: true,
      callbacks: {
        label: (context) => {
          const label = context.dataset.label || ''
          const value = context.parsed.y !== undefined ? context.parsed.y : context.parsed
          return `${label}: ${typeof value === 'number' ? value.toFixed(2) : value}`
        },
      },
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
      ticks: {
        font: {
          family: chartFonts.family,
          size: 11,
        },
        color: chartColors.textMuted,
      },
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(16, 42, 67, 0.1)', // Grid alpha 0.1 from design.md
      },
      ticks: {
        font: {
          family: chartFonts.monoFamily,
          size: 11,
        },
        color: chartColors.textSecondary,
      },
    },
  },
}

// Bar chart specific options
export const barChartOptions = {
  ...defaultChartOptions,
}

// Line chart options
export const lineChartOptions = {
  ...defaultChartOptions,
  elements: {
    line: {
      tension: 0.3,
      borderWidth: 2,
    },
    point: {
      radius: 3,
      hoverRadius: 5,
    },
  },
}

// Pie/Doughnut chart options
export const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        font: {
          family: chartFonts.family,
          size: 12,
        },
        color: chartColors.textSecondary,
        padding: 16,
        usePointStyle: true,
      },
    },
    tooltip: {
      backgroundColor: chartColors.text,
      bodyFont: {
        family: chartFonts.monoFamily,
        size: 12,
      },
      padding: 12,
      cornerRadius: 8,
      callbacks: {
        label: (context) => {
          const label = context.label || ''
          const value = context.parsed
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          return `${label}: ${value} (${percentage}%)`
        },
      },
    },
  },
}

// =================================================================
// Dataset Generators
// =================================================================

export function createFlowrateDataset(data, label = 'Flowrate') {
  return {
    label,
    data,
    backgroundColor: chartColors.flowrate,
    borderColor: chartColors.flowrate,
    borderWidth: 0,
  }
}

export function createPressureDataset(data, label = 'Pressure') {
  return {
    label,
    data,
    backgroundColor: chartColors.pressure,
    borderColor: chartColors.pressure,
    borderWidth: 0,
  }
}

export function createTemperatureDataset(data, label = 'Temperature') {
  return {
    label,
    data,
    backgroundColor: chartColors.temperature,
    borderColor: chartColors.temperature,
    borderWidth: 0,
  }
}

export function createDistributionDataset(data) {
  return {
    data,
    backgroundColor: chartColors.distribution.slice(0, data.length),
    borderColor: chartColors.background,
    borderWidth: 2,
  }
}

export default ChartJS