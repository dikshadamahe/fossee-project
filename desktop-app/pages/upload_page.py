"""
Upload Page - CSV Upload Interface
Chemical Equipment Parameter Visualizer - PyQt5 Desktop
FOSSEE Scientific Analytics

Matches web frontend: /src/pages/UploadPage.jsx
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QProgressBar, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
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


class UploadWorker(QThread):
    """Background thread for API upload"""
    finished = pyqtSignal(bool, dict)
    progress = pyqtSignal(int)
    
    def __init__(self, api_client, filepath):
        super().__init__()
        self.api_client = api_client
        self.filepath = filepath
    
    def run(self):
        self.progress.emit(30)
        result = self.api_client.upload(self.filepath)
        self.progress.emit(100)
        self.finished.emit(result.success, result.data if result.success else {'error': result.error})


class UploadZone(QFrame):
    """Drag-and-drop upload zone widget"""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("UploadZone")
        self.setAcceptDrops(True)
        self.setMinimumHeight(280)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Icon (using Unicode symbol instead of emoji)
        self.icon_label = QLabel("\u2191")  # Up arrow
        self.icon_label.setStyleSheet(f"""
            font-size: 48px;
            background: transparent;
            color: {COLORS['primary-700']};
            font-weight: bold;
        """)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # Title
        self.title = QLabel("Drop your CSV file here")
        self.title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 600;
            color: {COLORS['text-primary']};
            background: transparent;
        """)
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        # Subtitle
        self.subtitle = QLabel("or click to browse")
        self.subtitle.setStyleSheet(f"""
            font-size: 14px;
            color: {COLORS['text-secondary']};
            background: transparent;
        """)
        self.subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle)
        
        # Required columns hint
        hint = QLabel("Required columns: Equipment Name · Type · Flowrate · Pressure · Temperature")
        hint.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS['text-muted']};
            background: transparent;
            margin-top: 16px;
        """)
        hint.setAlignment(Qt.AlignCenter)
        hint.setWordWrap(True)
        layout.addWidget(hint)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.toLocalFile().endswith('.csv'):
                event.acceptProposedAction()
                self.setStyleSheet(f"""
                    QFrame#UploadZone {{
                        background-color: rgba(27, 127, 121, 0.05);
                        border: 2px solid {COLORS['primary-700']};
                        border-radius: 10px;
                    }}
                """)
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet("")
    
    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet("")
        urls = event.mimeData().urls()
        if urls:
            filepath = urls[0].toLocalFile()
            if filepath.endswith('.csv'):
                self.file_dropped.emit(filepath)
    
    def mousePressEvent(self, event):
        self.parent()._browse_file()


class UploadPage(QWidget):
    """
    Upload Page - CSV file upload interface
    
    Signals:
        upload_complete(int, dict): Emitted when upload succeeds (dataset_id, summary)
    """
    
    upload_complete = pyqtSignal(int, dict)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self._worker = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Page header
        header = QLabel("Upload Dataset")
        header.setObjectName("HeadingH1")
        layout.addWidget(header)
        
        desc = QLabel("Upload a CSV file containing chemical equipment parameters for analysis.")
        desc.setObjectName("TextSecondary")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Upload zone
        self.upload_zone = UploadZone(self)
        self.upload_zone.file_dropped.connect(self._process_file)
        layout.addWidget(self.upload_zone)
        
        # Progress section (hidden initially)
        self.progress_frame = QFrame()
        self.progress_frame.setVisible(False)
        progress_layout = QVBoxLayout(self.progress_frame)
        
        self.progress_label = QLabel("Uploading...")
        self.progress_label.setStyleSheet(f"color: {COLORS['text-secondary']};")
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(self.progress_frame)
        
        # Result section (hidden initially)
        self.result_frame = QFrame()
        self.result_frame.setObjectName("LabPanel")
        self.result_frame.setVisible(False)
        result_layout = QVBoxLayout(self.result_frame)
        
        self.result_icon = QLabel("\u2713")  # Checkmark
        self.result_icon.setStyleSheet(f"""
            font-size: 48px;
            background: transparent;
            color: {COLORS['success']};
            font-weight: bold;
        """)
        self.result_icon.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(self.result_icon)
        
        self.result_title = QLabel("Upload Successful!")
        self.result_title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 600;
            color: {COLORS['success']};
            background: transparent;
        """)
        self.result_title.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(self.result_title)
        
        self.result_details = QLabel("")
        self.result_details.setStyleSheet(f"color: {COLORS['text-secondary']}; background: transparent;")
        self.result_details.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(self.result_details)
        
        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignCenter)
        btn_row.setSpacing(12)
        
        self.view_btn = QPushButton("View Dashboard")
        self.view_btn.clicked.connect(lambda: self._navigate('dashboard'))
        btn_row.addWidget(self.view_btn)
        
        self.another_btn = QPushButton("Upload Another")
        self.another_btn.setObjectName("SecondaryButton")
        self.another_btn.clicked.connect(self._reset)
        btn_row.addWidget(self.another_btn)
        
        result_layout.addLayout(btn_row)
        layout.addWidget(self.result_frame)
        
        layout.addStretch()
    
    def _browse_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if filepath:
            self._process_file(filepath)
    
    def _process_file(self, filepath: str):
        """Upload file to Django API"""
        self.upload_zone.setVisible(False)
        self.progress_frame.setVisible(True)
        self.progress_bar.setValue(10)
        self.progress_label.setText(f"Uploading {os.path.basename(filepath)}...")
        
        # Start background upload
        self._worker = UploadWorker(self.api_client, filepath)
        self._worker.progress.connect(self.progress_bar.setValue)
        self._worker.finished.connect(self._on_upload_complete)
        self._worker.start()
    
    def _on_upload_complete(self, success: bool, data: dict):
        """Handle upload completion - auto-navigate to dashboard on success"""
        self.progress_frame.setVisible(False)
        
        if success:
            summary = data.get('summary', {})
            dataset_id = data.get('dataset_id')
            
            if dataset_id:
                # Store data and immediately navigate to dashboard (like web app)
                self._last_dataset_id = dataset_id
                self._last_summary = summary
                # Auto-navigate to dashboard
                self.upload_complete.emit(dataset_id, summary)
                # Reset for next upload
                self._reset()
        else:
            # Show error state
            self.result_frame.setVisible(True)
            self.result_icon.setText("\u2717")  # X mark
            self.result_icon.setStyleSheet(f"""
                font-size: 48px;
                background: transparent;
                color: {COLORS['error']};
                font-weight: bold;
            """)
            self.result_title.setText("Upload Failed")
            self.result_title.setStyleSheet(f"""
                font-size: 20px;
                font-weight: 600;
                color: {COLORS['error']};
                background: transparent;
            """)
            self.result_details.setText(data.get('error', 'Unknown error'))
            self.view_btn.setVisible(False)
    
    def _navigate(self, page: str):
        """Emit navigation signal"""
        if hasattr(self, '_last_dataset_id'):
            self.upload_complete.emit(self._last_dataset_id, self._last_summary)
    
    def _reset(self):
        """Reset to initial state"""
        self.upload_zone.setVisible(True)
        self.progress_frame.setVisible(False)
        self.result_frame.setVisible(False)
        self.view_btn.setVisible(True)
        self.progress_bar.setValue(0)
