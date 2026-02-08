"""
ChartWidget - Matplotlib Chart Container for PyQt5
Chemical Equipment Parameter Visualizer
FOSSEE Scientific Analytics UI

Charts:
- Bar: Type distribution
- Line: Flow/Pressure/Temperature trends
"""

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    
    # Chart palette
    'flowrate': '#1B7F79',
    'pressure': '#3A4E9F',
    'temperature': '#C53030',
    'distribution': ['#1B7F79', '#3A4E9F', '#2EA043', '#D97706', '#C53030', '#7C3AED', '#0891B2'],
}

# Configure matplotlib style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Noto Sans', 'DejaVu Sans'],
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'axes.labelcolor': COLORS['text-primary'],
    'axes.edgecolor': COLORS['border'],
    'axes.facecolor': COLORS['surface'],
    'axes.grid': True,
    'grid.color': COLORS['border'],
    'grid.alpha': 0.6,
    'xtick.color': COLORS['text-muted'],
    'ytick.color': COLORS['text-muted'],
    'figure.facecolor': COLORS['surface'],
    'legend.frameon': True,
    'legend.facecolor': COLORS['surface'],
    'legend.edgecolor': COLORS['border'],
})


class MplCanvas(FigureCanvas):
    """Matplotlib canvas widget"""
    
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=COLORS['surface'])
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)


class ChartWidget(QFrame):
    """
    Chart container with matplotlib backend
    
    Supports:
    - Bar charts (type distribution)
    - Line charts (parameter trends)
    - Combined multi-parameter charts
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ChartContainer")
        
        self._df = None
        self._chart_type = "bar"
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header = QHBoxLayout()
        
        self.title_label = QLabel("Chart")
        self.title_label.setObjectName("HeadingH3")
        header.addWidget(self.title_label)
        
        header.addStretch()
        
        # Chart type selector
        self.chart_selector = QComboBox()
        self.chart_selector.addItems([
            "Type Distribution (Bar)",
            "Parameter Trends (Line)",
            "All Parameters (Multi-Line)",
        ])
        self.chart_selector.currentIndexChanged.connect(self._on_chart_type_changed)
        self.chart_selector.setFixedWidth(200)
        header.addWidget(self.chart_selector)
        
        # Export button
        self.export_button = QPushButton("📷 Export")
        self.export_button.setObjectName("SecondaryButton")
        self.export_button.clicked.connect(self._export_chart)
        header.addWidget(self.export_button)
        
        layout.addLayout(header)
        
        # Canvas
        self.canvas = MplCanvas(self, width=10, height=6, dpi=100)
        layout.addWidget(self.canvas)
        
        # Optional toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet(f"background-color: {COLORS['bg-main']}; border-radius: 8px;")
        layout.addWidget(self.toolbar)
    
    def set_data(self, df: pd.DataFrame, title: str = None):
        """Set data and refresh chart"""
        self._df = df.copy()
        if title:
            self.title_label.setText(title)
        self._refresh_chart()
    
    def _on_chart_type_changed(self, index: int):
        """Handle chart type selection change"""
        self._refresh_chart()
    
    def _refresh_chart(self):
        """Redraw the chart based on current selection"""
        if self._df is None:
            return
        
        self.canvas.axes.clear()
        
        chart_type = self.chart_selector.currentIndex()
        
        if chart_type == 0:
            self._draw_type_distribution()
        elif chart_type == 1:
            self._draw_parameter_trends()
        elif chart_type == 2:
            self._draw_multi_parameter()
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()
    
    def _draw_type_distribution(self):
        """Draw horizontal bar chart for equipment type distribution"""
        ax = self.canvas.axes
        
        if 'Type' not in self._df.columns:
            ax.text(0.5, 0.5, 'No "Type" column found', 
                   ha='center', va='center', fontsize=14, color=COLORS['text-muted'])
            return
        
        type_counts = self._df['Type'].value_counts().sort_values(ascending=True)
        
        colors = [COLORS['distribution'][i % len(COLORS['distribution'])] 
                  for i in range(len(type_counts))]
        
        bars = ax.barh(type_counts.index, type_counts.values, color=colors, 
                       height=0.6, edgecolor='white', linewidth=1)
        
        # Add value labels
        for bar, value in zip(bars, type_counts.values):
            width = bar.get_width()
            percentage = (value / len(self._df)) * 100
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{value} ({percentage:.1f}%)',
                   ha='left', va='center', fontsize=10, 
                   color=COLORS['text-secondary'],
                   fontfamily='JetBrains Mono')
        
        ax.set_xlabel('Count', fontweight='500')
        ax.set_title('Equipment Type Distribution', pad=15, fontweight='600', 
                    color=COLORS['text-primary'])
        ax.set_xlim(0, max(type_counts.values) * 1.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    def _draw_parameter_trends(self):
        """Draw line chart for single parameter trend"""
        ax = self.canvas.axes
        
        # Default to flowrate
        param = 'Flowrate'
        if param not in self._df.columns:
            for alt in ['Pressure', 'Temperature']:
                if alt in self._df.columns:
                    param = alt
                    break
        
        if param not in self._df.columns:
            ax.text(0.5, 0.5, 'No parameter columns found',
                   ha='center', va='center', fontsize=14, color=COLORS['text-muted'])
            return
        
        x = range(len(self._df))
        y = self._df[param].values
        
        param_colors = {
            'Flowrate': COLORS['flowrate'],
            'Pressure': COLORS['pressure'],
            'Temperature': COLORS['temperature'],
        }
        color = param_colors.get(param, COLORS['primary-700'])
        
        ax.plot(x, y, color=color, linewidth=2, marker='o', 
                markersize=4, markerfacecolor=color, markeredgecolor='white',
                markeredgewidth=1.5, label=param)
        ax.fill_between(x, y, alpha=0.15, color=color)
        
        # Add mean line
        mean_val = np.nanmean(y)
        ax.axhline(y=mean_val, color=color, linestyle='--', alpha=0.7, linewidth=1.5)
        ax.text(len(x), mean_val, f'  Mean: {mean_val:.2f}', 
               va='center', fontsize=10, color=color,
               fontfamily='JetBrains Mono')
        
        # Labels
        if 'Equipment Name' in self._df.columns:
            labels = [name[:10] for name in self._df['Equipment Name']]
            ax.set_xticks(x[::max(1, len(x)//10)])
            ax.set_xticklabels(labels[::max(1, len(x)//10)], rotation=45, ha='right')
        
        units = {'Flowrate': 'L/min', 'Pressure': 'bar', 'Temperature': '°C'}
        ax.set_ylabel(f'{param} ({units.get(param, "")})', fontweight='500')
        ax.set_title(f'{param} Trend Analysis', pad=15, fontweight='600',
                    color=COLORS['text-primary'])
        ax.legend(loc='upper right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    def _draw_multi_parameter(self):
        """Draw multi-line chart for all parameters"""
        ax = self.canvas.axes
        
        params = []
        param_config = {
            'Flowrate': {'color': COLORS['flowrate'], 'unit': 'L/min'},
            'Pressure': {'color': COLORS['pressure'], 'unit': 'bar'},
            'Temperature': {'color': COLORS['temperature'], 'unit': '°C'},
        }
        
        for param in param_config:
            if param in self._df.columns:
                params.append(param)
        
        if not params:
            ax.text(0.5, 0.5, 'No parameter columns found',
                   ha='center', va='center', fontsize=14, color=COLORS['text-muted'])
            return
        
        x = range(len(self._df))
        
        for param in params:
            y = self._df[param].values
            config = param_config[param]
            
            ax.plot(x, y, color=config['color'], linewidth=2, marker='o',
                   markersize=3, markerfacecolor=config['color'], 
                   markeredgecolor='white', markeredgewidth=1,
                   label=f"{param} ({config['unit']})")
        
        if 'Equipment Name' in self._df.columns:
            labels = [name[:8] for name in self._df['Equipment Name']]
            step = max(1, len(x) // 10)
            ax.set_xticks(x[::step])
            ax.set_xticklabels(labels[::step], rotation=45, ha='right')
        
        ax.set_ylabel('Value', fontweight='500')
        ax.set_title('Multi-Parameter Overview', pad=15, fontweight='600',
                    color=COLORS['text-primary'])
        ax.legend(loc='upper right', framealpha=0.95)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    def _export_chart(self):
        """Export chart as PNG"""
        from PyQt5.QtWidgets import QFileDialog
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export Chart",
            "chart.png",
            "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg)"
        )
        
        if filepath:
            self.canvas.fig.savefig(filepath, dpi=150, bbox_inches='tight',
                                   facecolor=COLORS['surface'], edgecolor='none')
    
    def set_chart_type(self, chart_type: str):
        """Set chart type programmatically"""
        type_map = {
            'bar': 0,
            'line': 1,
            'multi': 2,
        }
        if chart_type in type_map:
            self.chart_selector.setCurrentIndex(type_map[chart_type])


class SummaryCardsWidget(QFrame):
    """Summary statistics cards"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LabPanel")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        self.title_label = QLabel("Summary Statistics")
        self.title_label.setObjectName("HeadingH3")
        layout.addWidget(self.title_label)
        
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(16)
        layout.addLayout(self.cards_layout)
    
    def set_data(self, df: pd.DataFrame):
        """Calculate and display summary statistics"""
        # Clear existing cards
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Total records card
        self._add_card("📊", "Total Records", str(len(df)), "", COLORS['primary-700'])
        
        # Equipment types
        if 'Type' in df.columns:
            type_count = df['Type'].nunique()
            self._add_card("🏭", "Equipment Types", str(type_count), "", COLORS['primary-600'])
        
        # Parameter averages
        param_icons = {'Flowrate': '💧', 'Pressure': '⚡', 'Temperature': '🌡️'}
        param_units = {'Flowrate': 'L/min', 'Pressure': 'bar', 'Temperature': '°C'}
        param_colors = {
            'Flowrate': COLORS['flowrate'],
            'Pressure': COLORS['pressure'],
            'Temperature': COLORS['temperature'],
        }
        
        for param in ['Flowrate', 'Pressure', 'Temperature']:
            if param in df.columns:
                mean_val = df[param].mean()
                self._add_card(
                    param_icons[param],
                    f"Avg {param}",
                    f"{mean_val:.2f}",
                    param_units[param],
                    param_colors[param]
                )
    
    def _add_card(self, icon: str, title: str, value: str, unit: str, color: str):
        """Add a summary card"""
        card = QFrame()
        card.setObjectName("SummaryCard")
        card.setStyleSheet(f"""
            QFrame#SummaryCard {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
                border-left: 4px solid {color};
                padding: 16px;
                min-width: 150px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 24px; background: transparent;")
        card_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {COLORS['text-secondary']};
            font-size: 13px;
            background: transparent;
        """)
        card_layout.addWidget(title_label)
        
        # Value row
        value_row = QHBoxLayout()
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {COLORS['text-primary']};
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            font-size: 24px;
            font-weight: 600;
            background: transparent;
        """)
        value_row.addWidget(value_label)
        
        if unit:
            unit_label = QLabel(unit)
            unit_label.setStyleSheet(f"""
                color: {COLORS['text-muted']};
                font-size: 14px;
                background: transparent;
            """)
            value_row.addWidget(unit_label)
        
        value_row.addStretch()
        card_layout.addLayout(value_row)
        
        self.cards_layout.addWidget(card)
