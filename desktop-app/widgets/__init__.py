"""
FOSSEE Scientific Analytics - PyQt5 Desktop Application
Chemical Equipment Parameter Visualizer

Widgets Package
"""

from .upload_widget import UploadWidget
from .table_widget import TableWidget
from .chart_widget import ChartWidget, SummaryCardsWidget
from .history_panel import HistoryPanel

__all__ = [
    'UploadWidget',
    'TableWidget', 
    'ChartWidget',
    'SummaryCardsWidget',
    'HistoryPanel',
]
