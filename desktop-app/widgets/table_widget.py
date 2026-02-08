"""
TableWidget - Data Table for PyQt5
Chemical Equipment Parameter Visualizer
FOSSEE Scientific Analytics UI

Features:
- Sticky header
- Mono numbers
- Type badges
- Sort + filter
- Pagination
"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QPushButton, QLineEdit, QComboBox, QSpinBox,
    QWidget, QAbstractItemView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import pandas as pd

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

# Type badge colors
TYPE_COLORS = {
    'Pump': '#1B7F79',
    'Valve': '#3A4E9F',
    'Heat Exchanger': '#D97706',
    'Reactor': '#C53030',
    'Compressor': '#2EA043',
    'Tank': '#7C3AED',
    'Filter': '#0891B2',
}


class TableWidget(QFrame):
    """
    Data table with sorting, filtering, and pagination
    
    Signals:
        row_selected(int): Emitted when a row is selected
        row_double_clicked(int): Emitted when a row is double-clicked
    """
    
    row_selected = pyqtSignal(int)
    row_double_clicked = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LabPanel")
        
        self._df = None
        self._filtered_df = None
        self._current_page = 1
        self._page_size = 20
        self._sort_column = None
        self._sort_ascending = True
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header with title and controls
        header = QHBoxLayout()
        
        self.title_label = QLabel("Equipment Data")
        self.title_label.setObjectName("HeadingH3")
        header.addWidget(self.title_label)
        
        header.addStretch()
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search equipment...")
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(self._apply_filter)
        header.addWidget(self.search_input)
        
        # Type filter
        self.type_filter = QComboBox()
        self.type_filter.addItem("All Types")
        self.type_filter.setFixedWidth(150)
        self.type_filter.currentTextChanged.connect(self._apply_filter)
        header.addWidget(self.type_filter)
        
        layout.addLayout(header)
        
        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self._handle_sort)
        self.table.cellClicked.connect(lambda row, col: self.row_selected.emit(row))
        self.table.cellDoubleClicked.connect(lambda row, col: self.row_double_clicked.emit(row))
        
        # Set fonts
        mono_font = QFont("JetBrains Mono", 12)
        self.table.setFont(mono_font)
        
        layout.addWidget(self.table)
        
        # Pagination footer
        footer = QHBoxLayout()
        
        self.info_label = QLabel("Showing 0 of 0 records")
        self.info_label.setObjectName("TextMuted")
        footer.addWidget(self.info_label)
        
        footer.addStretch()
        
        # Page size
        footer.addWidget(QLabel("Rows per page:"))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["10", "20", "50", "100"])
        self.page_size_combo.setCurrentText("20")
        self.page_size_combo.currentTextChanged.connect(self._change_page_size)
        self.page_size_combo.setFixedWidth(70)
        footer.addWidget(self.page_size_combo)
        
        # Navigation buttons
        self.prev_button = QPushButton("← Previous")
        self.prev_button.setObjectName("SecondaryButton")
        self.prev_button.clicked.connect(self._prev_page)
        footer.addWidget(self.prev_button)
        
        self.page_label = QLabel("Page 1 of 1")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setFixedWidth(100)
        footer.addWidget(self.page_label)
        
        self.next_button = QPushButton("Next →")
        self.next_button.setObjectName("SecondaryButton")
        self.next_button.clicked.connect(self._next_page)
        footer.addWidget(self.next_button)
        
        layout.addLayout(footer)
    
    def set_data(self, df: pd.DataFrame, title: str = None):
        """Load data into the table"""
        self._df = df.copy()
        self._filtered_df = self._df.copy()
        self._current_page = 1
        
        if title:
            self.title_label.setText(title)
        
        # Populate type filter
        self.type_filter.blockSignals(True)
        self.type_filter.clear()
        self.type_filter.addItem("All Types")
        if 'Type' in df.columns:
            types = sorted(df['Type'].dropna().unique())
            self.type_filter.addItems(types)
        self.type_filter.blockSignals(False)
        
        # Set up columns
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.tolist())
        
        self._refresh_table()
    
    def _apply_filter(self):
        """Apply search and type filters"""
        if self._df is None:
            return
        
        self._filtered_df = self._df.copy()
        
        # Search filter
        search_text = self.search_input.text().lower()
        if search_text:
            mask = self._filtered_df.astype(str).apply(
                lambda row: row.str.lower().str.contains(search_text).any(), 
                axis=1
            )
            self._filtered_df = self._filtered_df[mask]
        
        # Type filter
        type_filter = self.type_filter.currentText()
        if type_filter != "All Types" and 'Type' in self._filtered_df.columns:
            self._filtered_df = self._filtered_df[self._filtered_df['Type'] == type_filter]
        
        self._current_page = 1
        self._refresh_table()
    
    def _handle_sort(self, column: int):
        """Handle column header click for sorting"""
        if self._filtered_df is None:
            return
        
        col_name = self._filtered_df.columns[column]
        
        if self._sort_column == col_name:
            self._sort_ascending = not self._sort_ascending
        else:
            self._sort_column = col_name
            self._sort_ascending = True
        
        self._filtered_df = self._filtered_df.sort_values(
            by=col_name, 
            ascending=self._sort_ascending,
            na_position='last'
        )
        
        self._refresh_table()
    
    def _refresh_table(self):
        """Refresh table display with current page"""
        if self._filtered_df is None:
            return
        
        total_rows = len(self._filtered_df)
        total_pages = max(1, (total_rows + self._page_size - 1) // self._page_size)
        
        start_idx = (self._current_page - 1) * self._page_size
        end_idx = min(start_idx + self._page_size, total_rows)
        
        page_df = self._filtered_df.iloc[start_idx:end_idx]
        
        self.table.setRowCount(len(page_df))
        
        for row_idx, (_, row) in enumerate(page_df.iterrows()):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem()
                
                col_name = self._filtered_df.columns[col_idx]
                
                # Format based on column type
                if col_name == 'Type':
                    item.setText(str(value))
                    color = TYPE_COLORS.get(str(value), COLORS['primary-600'])
                    item.setForeground(QColor(color))
                    item.setFont(QFont("Segoe UI", 12, QFont.Bold))
                elif col_name in ['Flowrate', 'Pressure', 'Temperature']:
                    try:
                        item.setText(f"{float(value):.2f}")
                    except (ValueError, TypeError):
                        item.setText(str(value))
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item.setText(str(value) if pd.notna(value) else "—")
                
                self.table.setItem(row_idx, col_idx, item)
        
        # Update info labels
        self.info_label.setText(
            f"Showing {start_idx + 1}-{end_idx} of {total_rows} records"
        )
        self.page_label.setText(f"Page {self._current_page} of {total_pages}")
        
        # Update button states
        self.prev_button.setEnabled(self._current_page > 1)
        self.next_button.setEnabled(self._current_page < total_pages)
    
    def _change_page_size(self, size_str: str):
        """Change the number of rows per page"""
        self._page_size = int(size_str)
        self._current_page = 1
        self._refresh_table()
    
    def _prev_page(self):
        """Go to previous page"""
        if self._current_page > 1:
            self._current_page -= 1
            self._refresh_table()
    
    def _next_page(self):
        """Go to next page"""
        total_rows = len(self._filtered_df) if self._filtered_df is not None else 0
        total_pages = max(1, (total_rows + self._page_size - 1) // self._page_size)
        if self._current_page < total_pages:
            self._current_page += 1
            self._refresh_table()
    
    def get_selected_row(self) -> int:
        """Get currently selected row index"""
        selected = self.table.currentRow()
        return selected if selected >= 0 else None
    
    def get_selected_data(self) -> pd.Series:
        """Get data for currently selected row"""
        row = self.get_selected_row()
        if row is not None and self._filtered_df is not None:
            start_idx = (self._current_page - 1) * self._page_size
            actual_idx = start_idx + row
            if actual_idx < len(self._filtered_df):
                return self._filtered_df.iloc[actual_idx]
        return None
    
    def export_to_csv(self, filepath: str):
        """Export current filtered data to CSV"""
        if self._filtered_df is not None:
            self._filtered_df.to_csv(filepath, index=False)
