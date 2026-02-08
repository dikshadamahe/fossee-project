"""
CSV Upload Widget for PyQt5
FOSSEE Scientific Analytics UI
"""

import os
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QFileDialog, QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent


REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']


class CSVUploadWidget(QWidget):
    """CSV upload zone with drag-and-drop support"""
    
    upload_started = pyqtSignal()
    upload_success = pyqtSignal(dict)
    upload_error = pyqtSignal(str)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        
        self.setAcceptDrops(True)
        self.setMinimumHeight(220)
        
        self._setup_ui()
        self._set_state('empty')
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        
        # Main container frame
        self.container = QFrame()
        self.container.setObjectName("uploadZone")
        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setSpacing(8)
        
        # Icon placeholder
        self.icon_label = QLabel("📄")
        self.icon_label.setAlignment(Qt.AlignCenter)
        icon_font = self.icon_label.font()
        icon_font.setPointSize(32)
        self.icon_label.setFont(icon_font)
        container_layout.addWidget(self.icon_label)
        
        # Title
        self.title_label = QLabel("Drop your CSV file here")
        self.title_label.setObjectName("sectionHeader")
        self.title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("or click to browse")
        self.subtitle_label.setObjectName("secondary")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.subtitle_label)
        
        # Required columns info
        columns_text = ", ".join(REQUIRED_COLUMNS)
        self.columns_label = QLabel(f"Required columns: {columns_text}")
        self.columns_label.setObjectName("muted")
        self.columns_label.setAlignment(Qt.AlignCenter)
        self.columns_label.setWordWrap(True)
        container_layout.addWidget(self.columns_label)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.hide()
        container_layout.addWidget(self.progress_bar)
        
        # Browse button
        self.browse_button = QPushButton("Browse Files")
        self.browse_button.setObjectName("secondary")
        self.browse_button.clicked.connect(self._browse_file)
        container_layout.addWidget(self.browse_button, alignment=Qt.AlignCenter)
        
        layout.addWidget(self.container)
        
        # Apply base style
        self._apply_style()
    
    def _apply_style(self, state='empty'):
        """Apply style based on state"""
        border_color = '#E2E8F0'
        bg_color = 'transparent'
        
        if state == 'drag-over':
            border_color = '#1B7F79'
            bg_color = 'rgba(27, 127, 121, 0.05)'
        elif state == 'valid':
            border_color = '#2EA043'
            bg_color = 'rgba(46, 160, 67, 0.05)'
        elif state == 'invalid':
            border_color = '#C53030'
            bg_color = 'rgba(197, 48, 48, 0.05)'
        elif state == 'processing':
            border_color = '#D97706'
            bg_color = 'rgba(217, 119, 6, 0.05)'
        
        self.container.setStyleSheet(f"""
            QFrame#uploadZone {{
                background-color: {bg_color};
                border: 2px dashed {border_color};
                border-radius: 10px;
                padding: 32px;
            }}
        """)
    
    def _set_state(self, state, message=None):
        """Update the UI state"""
        self._apply_style(state)
        
        if state == 'empty':
            self.icon_label.setText("📄")
            self.title_label.setText("Drop your CSV file here")
            self.subtitle_label.setText("or click to browse")
            self.columns_label.show()
            self.progress_bar.hide()
            self.browse_button.show()
        
        elif state == 'drag-over':
            self.icon_label.setText("📥")
            self.title_label.setText("Drop to upload")
            self.subtitle_label.setText("")
        
        elif state == 'processing':
            self.icon_label.setText("⏳")
            self.title_label.setText(message or "Processing...")
            self.subtitle_label.setText("")
            self.columns_label.hide()
            self.progress_bar.show()
            self.browse_button.hide()
        
        elif state == 'valid':
            self.icon_label.setText("✅")
            self.title_label.setText("Upload Complete")
            self.subtitle_label.setText(message or "")
            self.columns_label.hide()
            self.progress_bar.hide()
            self.browse_button.show()
            self.browse_button.setText("Upload Another")
        
        elif state == 'invalid':
            self.icon_label.setText("❌")
            self.title_label.setText("Validation Error")
            self.subtitle_label.setText(message or "")
            self.columns_label.show()
            self.progress_bar.hide()
            self.browse_button.show()
            self.browse_button.setText("Try Again")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith('.csv'):
                event.acceptProposedAction()
                self._set_state('drag-over')
    
    def dragLeaveEvent(self, event):
        self._set_state('empty')
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.endswith('.csv'):
                self._upload_file(file_path)
    
    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )
        if file_path:
            self._upload_file(file_path)
    
    def _validate_csv(self, file_path):
        """Validate CSV structure locally"""
        try:
            df = pd.read_csv(file_path, nrows=5)
            columns = [c.strip().lower() for c in df.columns]
            required_lower = [c.lower() for c in REQUIRED_COLUMNS]
            
            missing = []
            for req in required_lower:
                found = False
                for col in columns:
                    if col == req or col.replace('_', ' ') == req or col.replace(' ', '_') == req:
                        found = True
                        break
                if not found:
                    missing.append(REQUIRED_COLUMNS[required_lower.index(req)])
            
            if missing:
                return False, f"Missing columns: {', '.join(missing)}"
            
            return True, None
        except Exception as e:
            return False, str(e)
    
    def _upload_file(self, file_path):
        """Upload file to API"""
        self.upload_started.emit()
        
        # Validate locally first
        self._set_state('processing', 'Validating CSV...')
        self.progress_bar.setValue(20)
        
        valid, error = self._validate_csv(file_path)
        
        if not valid:
            self._set_state('invalid', error)
            self.upload_error.emit(error)
            return
        
        # Upload to server
        self._set_state('processing', 'Uploading to server...')
        self.progress_bar.setValue(50)
        
        try:
            result = self.api_client.upload_dataset(file_path)
            
            if result.get('success'):
                dataset = result.get('dataset', {})
                row_count = dataset.get('row_count', 0)
                self._set_state('valid', f"Successfully loaded {row_count} records")
                self.progress_bar.setValue(100)
                self.upload_success.emit(dataset)
            else:
                error = result.get('error', 'Upload failed')
                self._set_state('invalid', error)
                self.upload_error.emit(error)
        except Exception as e:
            error = f"Connection error: {str(e)}"
            self._set_state('invalid', error)
            self.upload_error.emit(error)
