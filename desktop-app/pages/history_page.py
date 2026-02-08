"""
History Page - Dataset History List
Chemical Equipment Parameter Visualizer - PyQt5 Desktop
FOSSEE Scientific Analytics

Matches web frontend: /src/pages/HistoryPage.jsx
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QListWidget, QListWidgetItem, QPushButton, QMessageBox,
    QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from datetime import datetime

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


class DatasetCard(QFrame):
    """Individual dataset card in history list"""
    
    view_clicked = pyqtSignal(int)
    delete_clicked = pyqtSignal(int)
    download_clicked = pyqtSignal(int)
    
    def __init__(self, dataset: dict, parent=None):
        super().__init__(parent)
        self.dataset = dataset
        self.dataset_id = dataset.get('id')
        self.setObjectName("LabPanel")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Header row
        header = QHBoxLayout()
        
        icon = QLabel("📄")
        icon.setStyleSheet("font-size: 24px; background: transparent;")
        header.addWidget(icon)
        
        name = QLabel(self.dataset.get('filename', 'Unknown'))
        name.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {COLORS['text-primary']};
            background: transparent;
        """)
        header.addWidget(name, stretch=1)
        
        # Record count badge
        count = self.dataset.get('record_count', 0)
        badge = QLabel(f"{count} records")
        badge.setStyleSheet(f"""
            background-color: rgba(27, 127, 121, 0.15);
            color: {COLORS['primary-700']};
            font-size: 12px;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 4px;
        """)
        header.addWidget(badge)
        
        layout.addLayout(header)
        
        # Date
        uploaded_at = self.dataset.get('uploaded_at', '')
        if uploaded_at:
            try:
                dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                date_str = dt.strftime("%B %d, %Y at %H:%M")
            except:
                date_str = uploaded_at
        else:
            date_str = "Unknown date"
        
        date_lbl = QLabel(f"Uploaded: {date_str}")
        date_lbl.setStyleSheet(f"""
            color: {COLORS['text-muted']};
            font-size: 12px;
            background: transparent;
        """)
        layout.addWidget(date_lbl)
        
        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        
        view_btn = QPushButton("📊 View")
        view_btn.clicked.connect(lambda: self.view_clicked.emit(self.dataset_id))
        btn_row.addWidget(view_btn)
        
        download_btn = QPushButton("📥 Report")
        download_btn.setObjectName("SecondaryButton")
        download_btn.clicked.connect(lambda: self.download_clicked.emit(self.dataset_id))
        btn_row.addWidget(download_btn)
        
        btn_row.addStretch()
        
        delete_btn = QPushButton("🗑")
        delete_btn.setObjectName("DangerButton")
        delete_btn.setFixedWidth(40)
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.dataset_id))
        btn_row.addWidget(delete_btn)
        
        layout.addLayout(btn_row)


class FetchWorker(QThread):
    """Background thread for fetching datasets"""
    finished = pyqtSignal(bool, list)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
    
    def run(self):
        result = self.api_client.get_datasets()
        if result.success:
            self.finished.emit(True, result.data or [])
        else:
            self.finished.emit(False, [])


class HistoryPage(QWidget):
    """
    History Page - List of uploaded datasets
    
    Signals:
        view_dataset(int): Emitted when user clicks view on a dataset
        download_report(int): Emitted when user clicks download report
    """
    
    view_dataset = pyqtSignal(int)
    download_report = pyqtSignal(int)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self._worker = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_row = QHBoxLayout()
        
        title = QLabel("Upload History")
        title.setObjectName("HeadingH1")
        header_row.addWidget(title)
        
        header_row.addStretch()
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        header_row.addWidget(self.refresh_btn)
        
        layout.addLayout(header_row)
        
        # Description
        desc = QLabel("View and manage your previously uploaded datasets.")
        desc.setObjectName("TextSecondary")
        layout.addWidget(desc)
        
        # Scroll area for cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(16)
        self.cards_layout.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(self.cards_container)
        layout.addWidget(scroll, stretch=1)
        
        # Empty state
        self.empty_label = QLabel("📁 No datasets uploaded yet")
        self.empty_label.setStyleSheet(f"""
            color: {COLORS['text-muted']};
            font-size: 16px;
            padding: 40px;
        """)
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setVisible(False)
        layout.addWidget(self.empty_label)
    
    def showEvent(self, event):
        """Refresh when page becomes visible"""
        super().showEvent(event)
        self.refresh()
    
    def refresh(self):
        """Fetch datasets from API"""
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Loading...")
        
        self._worker = FetchWorker(self.api_client)
        self._worker.finished.connect(self._on_fetch_complete)
        self._worker.start()
    
    def _on_fetch_complete(self, success: bool, datasets: list):
        """Handle fetch completion"""
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("🔄 Refresh")
        
        # Clear existing cards
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not success or not datasets:
            self.empty_label.setVisible(True)
            return
        
        self.empty_label.setVisible(False)
        
        for dataset in datasets:
            card = DatasetCard(dataset)
            card.view_clicked.connect(self.view_dataset.emit)
            card.delete_clicked.connect(self._delete_dataset)
            card.download_clicked.connect(self.download_report.emit)
            self.cards_layout.addWidget(card)
        
        self.cards_layout.addStretch()
    
    def _delete_dataset(self, dataset_id: int):
        """Delete a dataset"""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this dataset?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = self.api_client.delete_dataset(dataset_id)
            if result.success:
                self.refresh()
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete: {result.error}")
