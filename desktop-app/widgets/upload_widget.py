"""
UploadWidget - CSV Upload Zone for PyQt5
Chemical Equipment Parameter Visualizer
FOSSEE Scientific Analytics UI

States: empty, drag, valid, invalid, processing
"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QFileDialog, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QFont
import pandas as pd
import os

# FOSSEE Colors
COLORS = {
    'primary-700': '#1B7F79',
    'primary-600': '#3A4E9F',
    'success': '#2EA043',
    'warning': '#D97706',
    'error': '#C53030',
    'text-primary': '#102A43',
    'text-secondary': '#486581',
    'text-muted': '#829AB1',
}

REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
COLUMN_ALIASES = {
    'equipment name': 'Equipment Name',
    'equipment_name': 'Equipment Name',
    'name': 'Equipment Name',
    'type': 'Type',
    'equipment_type': 'Type',
    'flowrate': 'Flowrate',
    'flow_rate': 'Flowrate',
    'flow': 'Flowrate',
    'pressure': 'Pressure',
    'press': 'Pressure',
    'temperature': 'Temperature',
    'temp': 'Temperature',
}


class UploadWidget(QFrame):
    """
    CSV Upload Zone with drag-and-drop support
    
    Signals:
        file_uploaded(str, pd.DataFrame): Emitted when file is successfully loaded
        upload_error(str): Emitted when upload fails
    """
    
    file_uploaded = pyqtSignal(str, object)  # filename, dataframe
    upload_error = pyqtSignal(str)  # error message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("UploadZone")
        self.setAcceptDrops(True)
        self.setMinimumHeight(220)
        
        self._state = "empty"  # empty, drag, valid, invalid, processing
        self._filename = ""
        self._df = None
        self._column_mapping = {}
        
        self._setup_ui()
        self._update_state("empty")
    
    def _setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet(f"font-size: 48px; color: {COLORS['primary-700']};")
        layout.addWidget(self.icon_label)
        
        # Title
        self.title_label = QLabel("Drop your CSV file here")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"""
            font-size: 18px; 
            font-weight: 600; 
            color: {COLORS['text-primary']};
        """)
        layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("or click to browse")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet(f"font-size: 14px; color: {COLORS['text-secondary']};")
        layout.addWidget(self.subtitle_label)
        
        # Required columns info
        cols_text = " · ".join(REQUIRED_COLUMNS)
        self.columns_label = QLabel(f"Required: {cols_text}")
        self.columns_label.setAlignment(Qt.AlignCenter)
        self.columns_label.setWordWrap(True)
        self.columns_label.setStyleSheet(f"""
            font-size: 12px; 
            color: {COLORS['text-muted']}; 
            margin-top: 8px;
        """)
        layout.addWidget(self.columns_label)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(8)
        layout.addWidget(self.progress_bar)
        
        # Status message
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)
        
        # Column mapping preview (hidden by default)
        self.mapping_frame = QFrame()
        self.mapping_layout = QVBoxLayout(self.mapping_frame)
        self.mapping_layout.setSpacing(4)
        self.mapping_frame.setVisible(False)
        layout.addWidget(self.mapping_frame)
        
        # Buttons container
        self.buttons_frame = QFrame()
        self.buttons_layout = QHBoxLayout(self.buttons_frame)
        self.buttons_layout.setSpacing(12)
        
        self.browse_button = QPushButton("Browse Files")
        self.browse_button.clicked.connect(self._browse_file)
        self.buttons_layout.addWidget(self.browse_button)
        
        self.retry_button = QPushButton("Try Again")
        self.retry_button.setObjectName("SecondaryButton")
        self.retry_button.clicked.connect(self._reset)
        self.retry_button.setVisible(False)
        self.buttons_layout.addWidget(self.retry_button)
        
        layout.addWidget(self.buttons_frame)
    
    def _update_state(self, state: str):
        """Update the visual state of the widget"""
        self._state = state
        self.setProperty("state", state)
        self.style().unpolish(self)
        self.style().polish(self)
        
        if state == "empty":
            self.icon_label.setText("📁")
            self.title_label.setText("Drop your CSV file here")
            self.subtitle_label.setText("or click to browse")
            self.subtitle_label.setVisible(True)
            self.columns_label.setVisible(True)
            self.progress_bar.setVisible(False)
            self.status_label.setVisible(False)
            self.mapping_frame.setVisible(False)
            self.browse_button.setVisible(True)
            self.retry_button.setVisible(False)
            
        elif state == "drag":
            self.icon_label.setText("📥")
            self.title_label.setText("Release to upload")
            self.subtitle_label.setVisible(False)
            self.columns_label.setVisible(False)
            
        elif state == "processing":
            self.icon_label.setText("⏳")
            self.title_label.setText(f"Processing {self._filename}...")
            self.subtitle_label.setVisible(False)
            self.columns_label.setVisible(False)
            self.progress_bar.setVisible(True)
            self.browse_button.setVisible(False)
            
        elif state == "valid":
            self.icon_label.setText("✅")
            self.title_label.setText("Upload Successful!")
            self.title_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {COLORS['success']};")
            self.subtitle_label.setText(f"{self._filename} • {len(self._df)} records")
            self.subtitle_label.setVisible(True)
            self.columns_label.setVisible(False)
            self.progress_bar.setVisible(False)
            self.status_label.setVisible(False)
            self.mapping_frame.setVisible(True)
            self.browse_button.setText("Upload Another")
            self.browse_button.setVisible(True)
            self._show_column_mapping()
            
        elif state == "invalid":
            self.icon_label.setText("❌")
            self.title_label.setText("Validation Error")
            self.title_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {COLORS['error']};")
            self.subtitle_label.setVisible(False)
            self.columns_label.setVisible(False)
            self.progress_bar.setVisible(False)
            self.status_label.setVisible(True)
            self.browse_button.setVisible(False)
            self.retry_button.setVisible(True)
    
    def _show_column_mapping(self):
        """Display column mapping results"""
        # Clear existing
        while self.mapping_layout.count():
            child = self.mapping_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        header = QLabel("Column Mapping:")
        header.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {COLORS['text-secondary']};")
        self.mapping_layout.addWidget(header)
        
        for req_col, mapped_col in self._column_mapping.items():
            row = QHBoxLayout()
            
            source = QLabel(mapped_col if mapped_col else "—")
            source.setStyleSheet(f"""
                font-family: 'JetBrains Mono', 'Consolas', monospace;
                font-size: 12px;
                color: {COLORS['text-muted']};
            """)
            row.addWidget(source)
            
            arrow = QLabel("→")
            arrow.setStyleSheet(f"color: {COLORS['primary-700']};")
            row.addWidget(arrow)
            
            target = QLabel(req_col)
            color = COLORS['success'] if mapped_col else COLORS['error']
            target.setStyleSheet(f"""
                font-family: 'JetBrains Mono', 'Consolas', monospace;
                font-size: 12px;
                font-weight: 600;
                color: {color};
            """)
            row.addWidget(target)
            
            row.addStretch()
            
            container = QFrame()
            container.setLayout(row)
            self.mapping_layout.addWidget(container)
    
    def _browse_file(self):
        """Open file dialog to select CSV"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if filepath:
            self._process_file(filepath)
    
    def _process_file(self, filepath: str):
        """Process the uploaded CSV file"""
        self._filename = os.path.basename(filepath)
        self._update_state("processing")
        self.progress_bar.setValue(20)
        
        try:
            # Read CSV
            self.progress_bar.setValue(40)
            df = pd.read_csv(filepath)
            
            self.progress_bar.setValue(60)
            
            # Normalize column names
            df.columns = [col.strip() for col in df.columns]
            
            # Detect column mappings
            self._column_mapping = {}
            missing = []
            
            for req_col in REQUIRED_COLUMNS:
                matched = None
                for col in df.columns:
                    normalized = col.lower().strip()
                    if normalized in COLUMN_ALIASES:
                        if COLUMN_ALIASES[normalized] == req_col:
                            matched = col
                            break
                    elif normalized == req_col.lower():
                        matched = col
                        break
                
                self._column_mapping[req_col] = matched
                if not matched:
                    missing.append(req_col)
            
            self.progress_bar.setValue(80)
            
            if missing:
                self._update_state("invalid")
                self.status_label.setText(f"Missing columns: {', '.join(missing)}")
                self.status_label.setStyleSheet(f"font-size: 14px; color: {COLORS['error']};")
                self.upload_error.emit(f"Missing required columns: {', '.join(missing)}")
                return
            
            # Rename columns to standard names
            rename_map = {v: k for k, v in self._column_mapping.items() if v}
            df = df.rename(columns=rename_map)
            
            self.progress_bar.setValue(100)
            self._df = df
            self._update_state("valid")
            self.file_uploaded.emit(self._filename, self._df)
            
        except Exception as e:
            self._update_state("invalid")
            self.status_label.setText(str(e))
            self.status_label.setStyleSheet(f"font-size: 14px; color: {COLORS['error']};")
            self.upload_error.emit(str(e))
    
    def _reset(self):
        """Reset to initial state"""
        self._filename = ""
        self._df = None
        self._column_mapping = {}
        self.progress_bar.setValue(0)
        self.title_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {COLORS['text-primary']};")
        self._update_state("empty")
    
    # Drag and drop handlers
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.toLocalFile().endswith('.csv'):
                event.acceptProposedAction()
                self._update_state("drag")
    
    def dragLeaveEvent(self, event):
        if self._state == "drag":
            self._update_state("empty")
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            filepath = urls[0].toLocalFile()
            if filepath.endswith('.csv'):
                self._process_file(filepath)
            else:
                self._update_state("invalid")
                self.status_label.setText("Please upload a CSV file")
                self.status_label.setStyleSheet(f"font-size: 14px; color: {COLORS['error']};")
                self.status_label.setVisible(True)
                self.retry_button.setVisible(True)
    
    def mousePressEvent(self, event):
        if self._state in ("empty", "valid"):
            self._browse_file()
    
    def get_dataframe(self):
        """Return the loaded DataFrame"""
        return self._df
    
    def get_filename(self):
        """Return the loaded filename"""
        return self._filename
