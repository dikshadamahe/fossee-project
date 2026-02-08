"""
Data Table Widget for PyQt5
FOSSEE Scientific Analytics UI
Uses JetBrains Mono for numeric data as per design system
"""

from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DataTableWidget(QWidget):
    """Data table with pagination and sorting"""
    
    PAGE_SIZE = 20
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.records = []
        self.current_page = 0
        self.sort_column = None
        self.sort_order = Qt.AscendingOrder
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(False)  # We handle sorting manually
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        
        # Set column headers
        columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # Configure header
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, len(columns)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # Pagination
        pagination_layout = QHBoxLayout()
        pagination_layout.setSpacing(8)
        
        self.btn_first = QPushButton("First")
        self.btn_first.setObjectName("secondary")
        self.btn_first.clicked.connect(self._go_first)
        
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.setObjectName("secondary")
        self.btn_prev.clicked.connect(self._go_prev)
        
        self.page_label = QLabel()
        self.page_label.setObjectName("muted")
        self.page_label.setAlignment(Qt.AlignCenter)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.setObjectName("secondary")
        self.btn_next.clicked.connect(self._go_next)
        
        self.btn_last = QPushButton("Last")
        self.btn_last.setObjectName("secondary")
        self.btn_last.clicked.connect(self._go_last)
        
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.btn_first)
        pagination_layout.addWidget(self.btn_prev)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.btn_next)
        pagination_layout.addWidget(self.btn_last)
        pagination_layout.addStretch()
        
        layout.addLayout(pagination_layout)
    
    def set_records(self, records):
        """Set the records to display"""
        self.records = records or []
        self.current_page = 0
        self._refresh_table()
    
    def _get_sorted_records(self):
        """Get records sorted by current sort column"""
        if not self.records:
            return []
        
        if self.sort_column is None:
            return self.records
        
        # Map column index to record key
        keys = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']
        key = keys[self.sort_column]
        
        reverse = self.sort_order == Qt.DescendingOrder
        return sorted(self.records, key=lambda r: r.get(key, ''), reverse=reverse)
    
    def _refresh_table(self):
        """Refresh the table display"""
        sorted_records = self._get_sorted_records()
        total_pages = max(1, (len(sorted_records) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        
        # Clamp current page
        self.current_page = max(0, min(self.current_page, total_pages - 1))
        
        # Get page records
        start = self.current_page * self.PAGE_SIZE
        end = start + self.PAGE_SIZE
        page_records = sorted_records[start:end]
        
        # Populate table
        self.table.setRowCount(len(page_records))
        
        # Mono font for numbers
        mono_font = QFont("JetBrains Mono", 11)
        mono_font.setStyleHint(QFont.Monospace)
        
        for row, record in enumerate(page_records):
            # Equipment Name
            item = QTableWidgetItem(record.get('equipment_name', ''))
            self.table.setItem(row, 0, item)
            
            # Type
            item = QTableWidgetItem(record.get('equipment_type', ''))
            self.table.setItem(row, 1, item)
            
            # Flowrate (mono font, right aligned)
            value = record.get('flowrate', 0)
            item = QTableWidgetItem(f"{value:.2f}")
            item.setFont(mono_font)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, item)
            
            # Pressure (mono font, right aligned)
            value = record.get('pressure', 0)
            item = QTableWidgetItem(f"{value:.2f}")
            item.setFont(mono_font)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 3, item)
            
            # Temperature (mono font, right aligned)
            value = record.get('temperature', 0)
            item = QTableWidgetItem(f"{value:.2f}")
            item.setFont(mono_font)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 4, item)
        
        # Update pagination
        self.page_label.setText(f"Page {self.current_page + 1} of {total_pages}")
        self.btn_first.setEnabled(self.current_page > 0)
        self.btn_prev.setEnabled(self.current_page > 0)
        self.btn_next.setEnabled(self.current_page < total_pages - 1)
        self.btn_last.setEnabled(self.current_page < total_pages - 1)
    
    def _on_header_clicked(self, column):
        """Handle header click for sorting"""
        if self.sort_column == column:
            # Toggle sort order
            if self.sort_order == Qt.AscendingOrder:
                self.sort_order = Qt.DescendingOrder
            else:
                self.sort_order = Qt.AscendingOrder
        else:
            self.sort_column = column
            self.sort_order = Qt.AscendingOrder
        
        self._refresh_table()
    
    def _go_first(self):
        self.current_page = 0
        self._refresh_table()
    
    def _go_prev(self):
        self.current_page = max(0, self.current_page - 1)
        self._refresh_table()
    
    def _go_next(self):
        total_pages = max(1, (len(self.records) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        self.current_page = min(total_pages - 1, self.current_page + 1)
        self._refresh_table()
    
    def _go_last(self):
        total_pages = max(1, (len(self.records) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        self.current_page = total_pages - 1
        self._refresh_table()
