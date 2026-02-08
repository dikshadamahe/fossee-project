"""
HistoryPanel - Dataset History Sidebar for PyQt5
Chemical Equipment Parameter Visualizer
FOSSEE Scientific Analytics UI

Features:
- List of uploaded datasets
- Selection with preview
- Delete functionality
"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime
import os

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
}


class HistoryItem(QWidget):
    """Individual history item widget"""
    
    def __init__(self, filename: str, record_count: int, date: datetime, 
                 equipment_types: list = None, parent=None):
        super().__init__(parent)
        
        self.filename = filename
        self.record_count = record_count
        self.date = date
        self.equipment_types = equipment_types or []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Filename row
        name_row = QHBoxLayout()
        
        icon_label = QLabel("📄")
        icon_label.setStyleSheet("font-size: 20px; background: transparent;")
        name_row.addWidget(icon_label)
        
        name_label = QLabel(self.filename)
        name_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {COLORS['text-primary']};
            background: transparent;
        """)
        name_label.setWordWrap(True)
        name_row.addWidget(name_label, stretch=1)
        
        layout.addLayout(name_row)
        
        # Stats row
        stats_text = f"{self.record_count} records"
        if self.equipment_types:
            stats_text += f" · {len(self.equipment_types)} types"
        
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS['text-secondary']};
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            background: transparent;
            margin-left: 28px;
        """)
        layout.addWidget(stats_label)
        
        # Date row
        date_str = self.date.strftime("%b %d, %Y at %H:%M")
        date_label = QLabel(date_str)
        date_label.setStyleSheet(f"""
            font-size: 11px;
            color: {COLORS['text-muted']};
            background: transparent;
            margin-left: 28px;
        """)
        layout.addWidget(date_label)
        
        # Type badges (if any)
        if self.equipment_types:
            types_row = QHBoxLayout()
            types_row.setSpacing(4)
            types_row.setContentsMargins(28, 4, 0, 0)
            
            for eq_type in self.equipment_types[:3]:  # Show max 3
                badge = QLabel(eq_type)
                badge.setStyleSheet(f"""
                    background-color: rgba(27, 127, 121, 0.15);
                    color: {COLORS['primary-700']};
                    font-size: 10px;
                    font-weight: 600;
                    padding: 2px 6px;
                    border-radius: 4px;
                """)
                types_row.addWidget(badge)
            
            if len(self.equipment_types) > 3:
                more = QLabel(f"+{len(self.equipment_types) - 3}")
                more.setStyleSheet(f"""
                    color: {COLORS['text-muted']};
                    font-size: 10px;
                    background: transparent;
                """)
                types_row.addWidget(more)
            
            types_row.addStretch()
            layout.addLayout(types_row)


class HistoryPanel(QFrame):
    """
    Dataset history panel with list and actions
    
    Signals:
        dataset_selected(dict): Emitted when a dataset is selected
        dataset_deleted(str): Emitted when a dataset is deleted
    """
    
    dataset_selected = pyqtSignal(dict)
    dataset_deleted = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HistoryPanel")
        self.setMinimumWidth(320)
        
        self._datasets = []  # List of dataset dicts
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setStyleSheet(f"""
            background-color: {COLORS['primary-900']};
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            padding: 16px;
        """)
        header_layout = QHBoxLayout(header)
        
        title = QLabel("📁 Upload History")
        title.setStyleSheet(f"""
            color: white;
            font-size: 16px;
            font-weight: 600;
            background: transparent;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.count_label = QLabel("0 datasets")
        self.count_label.setStyleSheet(f"""
            color: {COLORS['primary-700']};
            font-size: 12px;
            background: rgba(255,255,255,0.1);
            padding: 4px 8px;
            border-radius: 4px;
        """)
        header_layout.addWidget(self.count_label)
        
        layout.addWidget(header)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['surface']};
                border: none;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }}
            QListWidget::item {{
                border-bottom: 1px solid {COLORS['border']};
                padding: 0;
            }}
            QListWidget::item:selected {{
                background-color: rgba(27, 127, 121, 0.1);
                border-left: 3px solid {COLORS['primary-700']};
            }}
            QListWidget::item:hover:!selected {{
                background-color: {COLORS['bg-main']};
            }}
        """)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget)
        
        # Footer with actions
        footer = QFrame()
        footer.setStyleSheet(f"""
            background-color: {COLORS['bg-main']};
            border-top: 1px solid {COLORS['border']};
            padding: 12px;
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setSpacing(8)
        
        self.delete_button = QPushButton("🗑 Delete")
        self.delete_button.setObjectName("DangerButton")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self._delete_selected)
        footer_layout.addWidget(self.delete_button)
        
        footer_layout.addStretch()
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.setObjectName("SecondaryButton")
        self.clear_button.clicked.connect(self._clear_all)
        footer_layout.addWidget(self.clear_button)
        
        layout.addWidget(footer)
    
    def add_dataset(self, filename: str, df, date: datetime = None):
        """Add a dataset to the history"""
        if date is None:
            date = datetime.now()
        
        equipment_types = []
        if 'Type' in df.columns:
            equipment_types = df['Type'].dropna().unique().tolist()
        
        dataset = {
            'id': len(self._datasets),
            'filename': filename,
            'record_count': len(df),
            'date': date,
            'equipment_types': equipment_types,
            'dataframe': df,
        }
        
        self._datasets.insert(0, dataset)  # Add to beginning
        self._refresh_list()
    
    def _refresh_list(self):
        """Refresh the list display"""
        self.list_widget.clear()
        
        for dataset in self._datasets:
            item_widget = HistoryItem(
                filename=dataset['filename'],
                record_count=dataset['record_count'],
                date=dataset['date'],
                equipment_types=dataset['equipment_types']
            )
            
            item = QListWidgetItem()
            item.setData(Qt.UserRole, dataset['id'])
            item.setSizeHint(item_widget.sizeHint())
            
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)
        
        self.count_label.setText(f"{len(self._datasets)} dataset{'s' if len(self._datasets) != 1 else ''}")
        self.delete_button.setEnabled(False)
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle item selection"""
        dataset_id = item.data(Qt.UserRole)
        dataset = next((d for d in self._datasets if d['id'] == dataset_id), None)
        
        if dataset:
            self.delete_button.setEnabled(True)
            self.dataset_selected.emit(dataset)
    
    def _delete_selected(self):
        """Delete selected dataset"""
        current = self.list_widget.currentItem()
        if not current:
            return
        
        dataset_id = current.data(Qt.UserRole)
        dataset = next((d for d in self._datasets if d['id'] == dataset_id), None)
        
        if dataset:
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Delete '{dataset['filename']}' from history?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self._datasets = [d for d in self._datasets if d['id'] != dataset_id]
                self._refresh_list()
                self.dataset_deleted.emit(dataset['filename'])
    
    def _clear_all(self):
        """Clear all datasets"""
        if not self._datasets:
            return
        
        reply = QMessageBox.question(
            self,
            "Clear History",
            f"Delete all {len(self._datasets)} datasets from history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self._datasets = []
            self._refresh_list()
    
    def get_selected_dataset(self) -> dict:
        """Get currently selected dataset"""
        current = self.list_widget.currentItem()
        if current:
            dataset_id = current.data(Qt.UserRole)
            return next((d for d in self._datasets if d['id'] == dataset_id), None)
        return None
    
    def get_all_datasets(self) -> list:
        """Get all datasets"""
        return self._datasets.copy()
