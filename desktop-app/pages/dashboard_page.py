"""
Dashboard Page - Analytics Visualization
Chemical Equipment Parameter Visualizer - PyQt5 Desktop
FOSSEE Scientific Analytics

Clean layout with summary cards, pie chart, and parameter line chart
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QPushButton, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# FOSSEE Colors
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
    'flowrate': '#1B7F79',
    'pressure': '#3A4E9F',
    'temperature': '#C53030',
    'distribution': ['#1B7F79', '#3A4E9F', '#D97706', '#C53030', '#27AB6E', '#7C3AED'],
}

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial'],
    'font.size': 10,
    'axes.facecolor': COLORS['surface'],
    'figure.facecolor': COLORS['surface'],
})


class SummaryCard(QFrame):
    """Summary card with icon - FIXED LAYOUT"""
    
    def __init__(self, icon: str, title: str, value: str, unit: str = "", 
                 color: str = None, parent=None):
        super().__init__(parent)
        
        accent = color or COLORS['primary-700']
        
        self.setStyleSheet(f"""
            SummaryCard {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        self.setMinimumWidth(160)
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(10)
        
        # Icon in colored box
        icon_lbl = QLabel(icon)
        icon_lbl.setFixedSize(36, 36)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            background-color: {accent}25;
            color: {accent};
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
        """)
        main_layout.addWidget(icon_lbl)
        
        # Title label
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"""
            color: {COLORS['text-muted']};
            font-size: 11px;
            font-weight: 500;
        """)
        main_layout.addWidget(title_lbl)
        
        # Value with unit
        value_text = f"{value} <span style='font-size:11px; color:{COLORS['text-muted']};'>{unit}</span>"
        value_lbl = QLabel(value_text)
        value_lbl.setStyleSheet(f"""
            color: {COLORS['text-primary']};
            font-size: 20px;
            font-weight: bold;
        """)
        main_layout.addWidget(value_lbl)


class TypeDistributionChart(QFrame):
    """Pie chart for equipment type distribution"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            TypeDistributionChart {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        header = QLabel("Equipment Type Distribution")
        header.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {COLORS['text-primary']};")
        layout.addWidget(header)
        
        self.fig = Figure(figsize=(4, 3), dpi=100, facecolor=COLORS['surface'])
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        layout.addWidget(self.canvas)
    
    def set_data(self, type_distribution: dict):
        self.ax.clear()
        
        if not type_distribution:
            self.ax.text(0.5, 0.5, 'No data', ha='center', va='center', color=COLORS['text-muted'])
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        sorted_items = sorted(type_distribution.items(), key=lambda x: x[1], reverse=True)
        labels = [item[0] for item in sorted_items]
        sizes = [item[1] for item in sorted_items]
        total = sum(sizes)
        
        colors = [COLORS['distribution'][i % len(COLORS['distribution'])] for i in range(len(labels))]
        
        wedges, _, autotexts = self.ax.pie(
            sizes, labels=None, colors=colors,
            autopct=lambda pct: f'{pct:.0f}%' if pct > 8 else '',
            startangle=90, pctdistance=0.7,
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=1.5)
        )
        
        for at in autotexts:
            at.set_color('white')
            at.set_fontsize(8)
            at.set_fontweight('bold')
        
        self.ax.text(0, 0, f'{total}', ha='center', va='center', fontsize=16, fontweight='bold', color=COLORS['text-primary'])
        
        self.ax.legend(wedges, [f'{l} ({s})' for l, s in zip(labels, sizes)],
                      loc='center left', bbox_to_anchor=(0.95, 0.5), fontsize=8, frameon=False)
        
        self.ax.axis('equal')
        self.fig.tight_layout()
        self.canvas.draw()


class ParameterChart(QFrame):
    """Line chart with dropdown selector"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._df = None
        
        self.setStyleSheet(f"""
            ParameterChart {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        # Header row
        header_row = QHBoxLayout()
        
        header = QLabel("Parameter Trends")
        header.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {COLORS['text-primary']};")
        header_row.addWidget(header)
        header_row.addStretch()
        
        # Dropdown with PNG arrow image
        import os
        arrow_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'dropdown_arrow.png').replace('\\', '/')
        
        self.selector = QComboBox()
        self.selector.addItems(["All Parameters", "Flow Rate", "Pressure", "Temperature"])
        self.selector.setStyleSheet(f"""
            QComboBox {{
                background: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px 12px;
                padding-right: 30px;
                min-width: 140px;
                font-size: 13px;
                color: {COLORS['text-primary']};
            }}
            QComboBox:hover {{ border-color: {COLORS['primary-700']}; }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 24px;
                border: none;
            }}
            QComboBox::down-arrow {{
                image: url({arrow_path});
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                background: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 4px;
                selection-background-color: {COLORS['primary-700']};
                selection-color: white;
            }}
            QComboBox QAbstractItemView::item {{
                padding: 8px 12px;
                color: {COLORS['text-primary']};
            }}
            QComboBox QAbstractItemView::item:hover {{
                background: {COLORS['bg-main']};
            }}
        """)
        self.selector.currentTextChanged.connect(self._refresh)
        header_row.addWidget(self.selector)
        
        layout.addLayout(header_row)
        
        self.fig = Figure(figsize=(7, 4), dpi=100, facecolor=COLORS['surface'])
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        layout.addWidget(self.canvas)
    
    def set_data(self, df: pd.DataFrame):
        self._df = df
        self._refresh()
    
    def _refresh(self):
        self.ax.clear()
        
        if self._df is None or self._df.empty:
            self.ax.text(0.5, 0.5, 'No data', ha='center', va='center', color=COLORS['text-muted'])
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        df = self._df.head(12).copy()
        x = range(len(df))
        
        x_labels = []
        for idx, row in df.iterrows():
            name = str(row.get('Equipment Name', row.get('equipment_name', f'{idx}')))
            x_labels.append(name[:6])
        
        params = {
            'Flow Rate': (['Flowrate', 'flowrate'], COLORS['flowrate']),
            'Pressure': (['Pressure', 'pressure'], COLORS['pressure']),
            'Temperature': (['Temperature', 'temperature'], COLORS['temperature']),
        }
        
        selected = self.selector.currentText()
        
        if selected == "All Parameters":
            for name, (cols, color) in params.items():
                col = next((c for c in cols if c in df.columns), None)
                if col:
                    y = df[col].fillna(0).values
                    self.ax.plot(x, y, color=color, linewidth=2, marker='o', markersize=4, label=name)
        else:
            cols, color = params.get(selected, ([], COLORS['primary-700']))
            col = next((c for c in cols if c in df.columns), None)
            if col:
                y = df[col].fillna(0).values
                self.ax.bar(x, y, color=color, width=0.6, edgecolor='white')
                mean = np.nanmean(y)
                self.ax.axhline(mean, color=color, linestyle='--', alpha=0.7, label=f'Avg: {mean:.1f}')
        
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
        self.ax.grid(True, axis='y', alpha=0.3, color=COLORS['border'])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        # Legend outside the plot at top right
        self.ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9, frameon=False)
        
        self.fig.tight_layout(rect=[0, 0, 0.85, 1])
        self.canvas.draw()


class DashboardPage(QWidget):
    """Dashboard with summary cards and charts"""
    
    download_report = pyqtSignal(int)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self._dataset_id = None
        self._df = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header
        header_row = QHBoxLayout()
        header = QLabel("Analytics Dashboard")
        header.setStyleSheet(f"font-size: 22px; font-weight: 600; color: {COLORS['text-primary']};")
        header_row.addWidget(header)
        header_row.addStretch()
        
        self.download_btn = QPushButton("Download Report")
        self.download_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary-700']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background: #156B66; }}
            QPushButton:disabled {{ background: {COLORS['border']}; }}
        """)
        self.download_btn.clicked.connect(lambda: self.download_report.emit(self._dataset_id) if self._dataset_id else None)
        self.download_btn.setEnabled(False)
        header_row.addWidget(self.download_btn)
        layout.addLayout(header_row)
        
        # Content container
        self.content = QWidget()
        content_layout = QVBoxLayout(self.content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Cards row - using simple HBox
        self.cards_row = QHBoxLayout()
        self.cards_row.setSpacing(16)
        content_layout.addLayout(self.cards_row)
        
        # Charts row
        charts_row = QHBoxLayout()
        charts_row.setSpacing(20)
        
        self.type_chart = TypeDistributionChart()
        self.type_chart.setMinimumHeight(280)
        charts_row.addWidget(self.type_chart, 1)
        
        self.param_chart = ParameterChart()
        self.param_chart.setMinimumHeight(280)
        charts_row.addWidget(self.param_chart, 1)
        
        content_layout.addLayout(charts_row)
        content_layout.addStretch()
        
        self.content.setVisible(False)
        layout.addWidget(self.content)
        
        # Placeholder
        self.placeholder = QLabel("Upload a dataset to see analytics")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet(f"""
            color: {COLORS['text-muted']};
            font-size: 16px;
            padding: 80px;
            background: {COLORS['surface']};
            border: 2px dashed {COLORS['border']};
            border-radius: 12px;
        """)
        layout.addWidget(self.placeholder)
    
    def load_dataset(self, dataset_id: int):
        self._dataset_id = dataset_id
        self.download_btn.setEnabled(True)
        
        result = self.api_client.get_summary(dataset_id)
        if not result.success:
            return
        
        self._df = self.api_client.dataset_to_dataframe(dataset_id)
        self._update_cards(result.data)
        self._update_charts(result.data)
        
        self.placeholder.setVisible(False)
        self.content.setVisible(True)
    
    def load_from_summary(self, dataset_id: int, summary: dict):
        self._dataset_id = dataset_id
        self.download_btn.setEnabled(True)
        
        self._df = self.api_client.dataset_to_dataframe(dataset_id)
        self._update_cards(summary)
        self._update_charts(summary)
        
        self.placeholder.setVisible(False)
        self.content.setVisible(True)
    
    def _update_cards(self, summary: dict):
        # Clear existing cards
        while self.cards_row.count():
            child = self.cards_row.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        total = summary.get('total_count', summary.get('total_records', 0))
        types = summary.get('type_distribution', {})
        avg_flow = summary.get('avg_flowrate', 0)
        avg_press = summary.get('avg_pressure', 0)
        
        # Create cards with simple icons
        cards_data = [
            ("≡", "Total Records", str(total), "records", COLORS['primary-700']),
            ("◇", "Equipment Types", str(len(types)), "types", COLORS['success']),
            ("●", "Avg Flow Rate", f"{avg_flow:.1f}", "L/min", COLORS['flowrate']),
            ("◆", "Avg Pressure", f"{avg_press:.1f}", "bar", COLORS['pressure']),
        ]
        
        for icon, title, value, unit, color in cards_data:
            card = SummaryCard(icon, title, value, unit, color)
            self.cards_row.addWidget(card)
    
    def _update_charts(self, summary: dict):
        self.type_chart.set_data(summary.get('type_distribution', {}))
        if self._df is not None:
            self.param_chart.set_data(self._df)
