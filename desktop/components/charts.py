"""
Chart Widget using Matplotlib embedded in PyQt5
FOSSEE Scientific Analytics UI
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .chart_config import (
    configure_matplotlib, 
    CHART_COLORS, 
    COLORS,
    create_bar_chart,
    create_multi_bar_chart,
    create_pie_chart
)


class ChartWidget(QWidget):
    """Base chart widget with Matplotlib canvas"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        configure_matplotlib()
        
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.figure.set_facecolor(COLORS['surface'])
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
    
    def clear(self):
        """Clear the figure"""
        self.figure.clear()
        self.canvas.draw()


class ParameterBarChart(ChartWidget):
    """Bar chart for a single parameter"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_data(self, records, parameter='flowrate'):
        """Set data and redraw chart"""
        self.figure.clear()
        
        if not records:
            self.canvas.draw()
            return
        
        ax = self.figure.add_subplot(111)
        
        labels = [r.get('equipment_name', '')[:12] for r in records]
        data = [r.get(parameter, 0) for r in records]
        
        create_bar_chart(ax, labels, data, parameter, parameter.capitalize())
        
        self.figure.tight_layout()
        self.canvas.draw()


class MultiParameterChart(ChartWidget):
    """Grouped bar chart for all parameters"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure.set_size_inches(10, 5)
    
    def set_data(self, records):
        """Set data and redraw chart"""
        self.figure.clear()
        
        if not records:
            self.canvas.draw()
            return
        
        ax = self.figure.add_subplot(111)
        
        labels = [r.get('equipment_name', '')[:12] for r in records[:15]]  # Limit for readability
        
        datasets = {
            'flowrate': [r.get('flowrate', 0) for r in records[:15]],
            'pressure': [r.get('pressure', 0) for r in records[:15]],
            'temperature': [r.get('temperature', 0) for r in records[:15]],
        }
        
        create_multi_bar_chart(ax, labels, datasets, 'Parameter Comparison')
        
        self.figure.tight_layout()
        self.canvas.draw()


class TypeDistributionChart(ChartWidget):
    """Pie chart for equipment type distribution"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure.set_size_inches(6, 5)
    
    def set_data(self, statistics):
        """Set data from statistics and redraw chart"""
        self.figure.clear()
        
        if not statistics or 'type_distribution' not in statistics:
            self.canvas.draw()
            return
        
        ax = self.figure.add_subplot(111)
        
        distribution = statistics['type_distribution']
        labels = list(distribution.keys())
        data = list(distribution.values())
        
        create_pie_chart(ax, labels, data, 'Equipment Type Distribution')
        
        self.figure.tight_layout()
        self.canvas.draw()


class StatisticsPanel(QWidget):
    """Panel showing statistics summary"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        configure_matplotlib()
        
        self.figure = Figure(figsize=(10, 3), dpi=100)
        self.figure.set_facecolor(COLORS['surface'])
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
    
    def set_data(self, statistics):
        """Set statistics data and redraw"""
        self.figure.clear()
        
        if not statistics:
            self.canvas.draw()
            return
        
        # Create 3 subplots for each parameter
        params = ['flowrate', 'pressure', 'temperature']
        colors = [CHART_COLORS['flowrate'], CHART_COLORS['pressure'], CHART_COLORS['temperature']]
        
        for i, (param, color) in enumerate(zip(params, colors)):
            ax = self.figure.add_subplot(1, 3, i + 1)
            
            stats = statistics.get(param, {})
            
            # Create a simple visualization
            categories = ['Min', 'Mean', 'Max']
            values = [
                stats.get('min', 0),
                stats.get('mean', 0),
                stats.get('max', 0),
            ]
            
            bars = ax.bar(categories, values, color=color, width=0.6)
            ax.set_title(param.capitalize(), fontweight='600', color=COLORS['text_primary'])
            
            # Add value labels on bars
            for bar, val in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f'{val:.1f}',
                    ha='center',
                    va='bottom',
                    fontsize=9,
                    fontfamily='monospace'
                )
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        self.figure.tight_layout()
        self.canvas.draw()
