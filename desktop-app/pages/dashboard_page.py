"""
Dashboard Page - Analytics Visualization
Chemical Equipment Parameter Visualizer - PyQt5 Desktop
FOSSEE Scientific Analytics

Matches web frontend: /src/pages/DashboardPage.jsx
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QComboBox, QScrollArea, QSplitter
)
from PyQt5.QtCore import Qt, pyqtSignal
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# FOSSEE Colors (exact hex from design.md)
COLORS = {
    'primary-900': '#0F2A44',
    'primary-700': '#1B7F79',
    'primary-600': '#3A4E9F',
    'success': '#2EA043',
    'warning': '#D97706',
    'error': '#C53030',
    'bg-main': '#F7F9FC',
    'surface': '#FFFFFF',
    'border': '#E2E8F0',
    'text-primary': '#102A43',
    'text-secondary': '#486581',
    'text-muted': '#829AB1',
    # Chart palette (same as web frontend)
    'flowrate': '#1B7F79',
    'pressure': '#3A4E9F',
    'temperature': '#C53030',
    'distribution': ['#1B7F79', '#3A4E9F', '#2EA043', '#D97706', '#C53030', '#7C3AED', '#0891B2'],
}

# Configure matplotlib
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Noto Sans', 'DejaVu Sans'],
    'font.size': 10,
    'axes.facecolor': COLORS['surface'],
    'axes.edgecolor': COLORS['border'],
    'axes.grid': True,
    'grid.color': COLORS['border'],
    'grid.alpha': 0.5,
    'figure.facecolor': COLORS['surface'],
})


class SummaryCard(QFrame):
    """Individual summary statistic card"""
    
    def __init__(self, icon: str, title: str, value: str, unit: str = "", 
                 color: str = None, insight: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("SummaryCard")
        
        accent = color or COLORS['primary-700']
        self.setStyleSheet(f"""
            QFrame#SummaryCard {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
                border-left: 4px solid {accent};
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Icon
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 24px; background: transparent;")
        layout.addWidget(icon_lbl)
        
        # Title
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"""
            color: {COLORS['text-secondary']};
            font-size: 13px;
            background: transparent;
        """)
        layout.addWidget(title_lbl)
        
        # Value + Unit
        value_row = QHBoxLayout()
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"""
            color: {COLORS['text-primary']};
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            font-size: 28px;
            font-weight: 600;
            background: transparent;
        """)
        value_row.addWidget(value_lbl)
        
        if unit:
            unit_lbl = QLabel(unit)
            unit_lbl.setStyleSheet(f"""
                color: {COLORS['text-muted']};
                font-size: 14px;
                background: transparent;
                margin-left: 4px;
            """)
            value_row.addWidget(unit_lbl)
        
        value_row.addStretch()
        layout.addLayout(value_row)
        
        # Insight (plain English)
        if insight:
            insight_lbl = QLabel(insight)
            insight_lbl.setStyleSheet(f"""
                color: {accent};
                font-size: 11px;
                background: transparent;
            """)
            insight_lbl.setWordWrap(True)
            layout.addWidget(insight_lbl)


class TypeDistributionChart(QFrame):
    """Horizontal bar chart for equipment type distribution"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ChartContainer")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Header
        header = QLabel("Equipment Type Distribution")
        header.setObjectName("HeadingH3")
        layout.addWidget(header)
        
        # Canvas
        self.fig = Figure(figsize=(6, 4), dpi=100, facecolor=COLORS['surface'])
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        layout.addWidget(self.canvas)
    
    def set_data(self, type_distribution: dict):
        """Update chart with type distribution data"""
        self.ax.clear()
        
        if not type_distribution:
            self.ax.text(0.5, 0.5, 'No data', ha='center', va='center',
                        fontsize=12, color=COLORS['text-muted'])
            self.canvas.draw()
            return
        
        # Sort by count
        sorted_items = sorted(type_distribution.items(), key=lambda x: x[1])
        types = [item[0] for item in sorted_items]
        counts = [item[1] for item in sorted_items]
        total = sum(counts)
        
        colors = [COLORS['distribution'][i % len(COLORS['distribution'])] 
                  for i in range(len(types))]
        
        bars = self.ax.barh(types, counts, color=colors, height=0.6, 
                           edgecolor='white', linewidth=1)
        
        # Add labels with percentages
        for bar, count in zip(bars, counts):
            pct = (count / total) * 100
            self.ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{count} ({pct:.1f}%)', ha='left', va='center',
                        fontsize=9, color=COLORS['text-secondary'],
                        fontfamily='JetBrains Mono')
        
        self.ax.set_xlabel('Count')
        self.ax.set_xlim(0, max(counts) * 1.3)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        self.fig.tight_layout()
        self.canvas.draw()


class ParameterLineChart(QFrame):
    """Multi-line chart for Flow/Pressure/Temperature trends"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ChartContainer")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Header with parameter selector
        header_row = QHBoxLayout()
        
        header = QLabel("Parameter Trends")
        header.setObjectName("HeadingH3")
        header_row.addWidget(header)
        
        header_row.addStretch()
        
        self.param_selector = QComboBox()
        self.param_selector.addItems([
            "All Parameters",
            "Flowrate",
            "Pressure", 
            "Temperature"
        ])
        self.param_selector.currentTextChanged.connect(self._on_param_changed)
        self.param_selector.setFixedWidth(150)
        header_row.addWidget(self.param_selector)
        
        layout.addLayout(header_row)
        
        # Canvas
        self.fig = Figure(figsize=(8, 4), dpi=100, facecolor=COLORS['surface'])
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        layout.addWidget(self.canvas)
        
        self._df = None
    
    def set_data(self, df: pd.DataFrame):
        """Store data and refresh chart"""
        self._df = df
        self._refresh_chart()
    
    def _on_param_changed(self, param: str):
        """Handle parameter selection change"""
        self._refresh_chart()
    
    def _refresh_chart(self):
        """Redraw the chart"""
        self.ax.clear()
        
        if self._df is None or self._df.empty:
            self.ax.text(0.5, 0.5, 'No data', ha='center', va='center',
                        fontsize=12, color=COLORS['text-muted'])
            self.canvas.draw()
            return
        
        param = self.param_selector.currentText()
        x = range(len(self._df))
        
        param_config = {
            'Flowrate': {'color': COLORS['flowrate'], 'unit': 'L/min'},
            'Pressure': {'color': COLORS['pressure'], 'unit': 'bar'},
            'Temperature': {'color': COLORS['temperature'], 'unit': '°C'},
        }
        
        if param == "All Parameters":
            for p, config in param_config.items():
                if p in self._df.columns:
                    y = self._df[p].values
                    self.ax.plot(x, y, color=config['color'], linewidth=2,
                               marker='o', markersize=3, label=f"{p} ({config['unit']})")
        else:
            if param in self._df.columns:
                config = param_config.get(param, {'color': COLORS['primary-700'], 'unit': ''})
                y = self._df[param].values
                self.ax.plot(x, y, color=config['color'], linewidth=2,
                           marker='o', markersize=4, label=param)
                self.ax.fill_between(x, y, alpha=0.15, color=config['color'])
                
                # Add mean line
                mean_val = np.nanmean(y)
                self.ax.axhline(y=mean_val, color=config['color'], linestyle='--', 
                               alpha=0.7, linewidth=1.5)
                self.ax.text(len(x), mean_val, f'  Avg: {mean_val:.2f}',
                           va='center', fontsize=9, color=config['color'])
        
        self.ax.set_ylabel('Value')
        self.ax.legend(loc='upper right')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        self.fig.tight_layout()
        self.canvas.draw()


class DashboardPage(QWidget):
    """
    Dashboard Page - Analytics visualization
    
    Layout matches web frontend with:
    - Summary cards grid
    - Type distribution bar chart
    - Parameter line charts
    """
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self._dataset_id = None
        self._df = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Page header
        header = QLabel("Analytics Dashboard")
        header.setObjectName("HeadingH1")
        layout.addWidget(header)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        
        # Summary cards grid
        self.cards_grid = QGridLayout()
        self.cards_grid.setSpacing(16)
        content_layout.addLayout(self.cards_grid)
        
        # Charts row
        charts_splitter = QSplitter(Qt.Horizontal)
        
        self.type_chart = TypeDistributionChart()
        charts_splitter.addWidget(self.type_chart)
        
        self.param_chart = ParameterLineChart()
        charts_splitter.addWidget(self.param_chart)
        
        charts_splitter.setSizes([400, 600])
        content_layout.addWidget(charts_splitter)
        
        # Placeholder when no data
        self.placeholder = QLabel("📊 Upload a dataset to see analytics")
        self.placeholder.setStyleSheet(f"""
            color: {COLORS['text-muted']};
            font-size: 18px;
            padding: 60px;
        """)
        self.placeholder.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.placeholder)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Initially hide charts
        self.type_chart.setVisible(False)
        self.param_chart.setVisible(False)
    
    def load_dataset(self, dataset_id: int):
        """Load and display dataset analytics"""
        self._dataset_id = dataset_id
        
        # Get summary from API
        summary_result = self.api_client.get_summary(dataset_id)
        if not summary_result.success:
            return
        
        summary = summary_result.data
        
        # Get full dataset for charts
        self._df = self.api_client.dataset_to_dataframe(dataset_id)
        
        self._update_cards(summary)
        self._update_charts(summary)
        
        self.placeholder.setVisible(False)
        self.type_chart.setVisible(True)
        self.param_chart.setVisible(True)
    
    def load_from_summary(self, dataset_id: int, summary: dict):
        """Load from pre-fetched summary data"""
        self._dataset_id = dataset_id
        
        # Get full dataset for charts
        self._df = self.api_client.dataset_to_dataframe(dataset_id)
        
        self._update_cards(summary)
        self._update_charts(summary)
        
        self.placeholder.setVisible(False)
        self.type_chart.setVisible(True)
        self.param_chart.setVisible(True)
    
    def _update_cards(self, summary: dict):
        """Update summary cards"""
        # Clear existing cards
        while self.cards_grid.count():
            child = self.cards_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        total = summary.get('total_count', 0)
        avg_flow = summary.get('avg_flowrate', 0)
        avg_press = summary.get('avg_pressure', 0)
        avg_temp = summary.get('avg_temperature', 0)
        types = summary.get('type_distribution', {})
        
        # Generate insights
        flow_insight = "Normal operating range" if 10 < avg_flow < 100 else "Check flow parameters"
        press_insight = "Pressure within limits" if 0.5 < avg_press < 10 else "Review pressure settings"
        temp_insight = "Temperature stable" if 15 < avg_temp < 80 else "Monitor temperature"
        
        cards = [
            SummaryCard("📊", "Total Records", str(total), "", COLORS['primary-700'],
                       f"{len(types)} equipment types"),
            SummaryCard("💧", "Avg Flowrate", f"{avg_flow:.2f}", "L/min", 
                       COLORS['flowrate'], flow_insight),
            SummaryCard("⚡", "Avg Pressure", f"{avg_press:.2f}", "bar",
                       COLORS['pressure'], press_insight),
            SummaryCard("🌡️", "Avg Temperature", f"{avg_temp:.2f}", "°C",
                       COLORS['temperature'], temp_insight),
        ]
        
        for i, card in enumerate(cards):
            self.cards_grid.addWidget(card, 0, i)
    
    def _update_charts(self, summary: dict):
        """Update charts"""
        type_dist = summary.get('type_distribution', {})
        self.type_chart.set_data(type_dist)
        
        if self._df is not None:
            self.param_chart.set_data(self._df)
