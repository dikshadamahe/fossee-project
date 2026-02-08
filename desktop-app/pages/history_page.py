"""
History Page - Dataset History List
Chemical Equipment Parameter Visualizer - PyQt5 Desktop
FOSSEE Scientific Analytics

Only shows datasets for AUTHENTICATED users.
Backend filters by user, but we also check client-side token.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from datetime import datetime, timezone, timedelta

# Indian Standard Time offset (GMT+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

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


def format_timestamp_ist(uploaded_at: str) -> str:
    """Format timestamp to IST (GMT+5:30)"""
    if not uploaded_at:
        return "Unknown date"
    
    try:
        if uploaded_at.endswith('Z'):
            dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
        elif '+' in uploaded_at or uploaded_at.count('-') > 2:
            dt = datetime.fromisoformat(uploaded_at)
        else:
            dt = datetime.fromisoformat(uploaded_at)
            dt = dt.replace(tzinfo=timezone.utc)
        
        dt_ist = dt.astimezone(IST)
        return dt_ist.strftime("%d %b %Y, %I:%M %p IST")
    except Exception:
        return uploaded_at


class DatasetCard(QFrame):
    """Individual dataset card in history list"""
    
    view_clicked = pyqtSignal(int)
    delete_clicked = pyqtSignal(int)
    download_clicked = pyqtSignal(int)
    
    def __init__(self, dataset: dict, parent=None):
        super().__init__(parent)
        self.dataset = dataset
        self.dataset_id = dataset.get('id')
        self.setObjectName("DatasetCard")
        self.setStyleSheet(f"""
            QFrame#DatasetCard {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
            QFrame#DatasetCard:hover {{
                border-color: {COLORS['primary-700']};
            }}
        """)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Header row
        header = QHBoxLayout()
        
        # Filename
        name = QLabel(self.dataset.get('filename', 'Unknown'))
        name.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 600;
            color: {COLORS['text-primary']};
            background: transparent;
        """)
        header.addWidget(name, stretch=1)
        
        # Record count badge
        count = self.dataset.get('record_count', 0)
        badge = QLabel(f"{count} records")
        badge.setStyleSheet(f"""
            background-color: {COLORS['success']}20;
            color: {COLORS['success']};
            font-size: 12px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 12px;
        """)
        header.addWidget(badge)
        
        layout.addLayout(header)
        
        # Date in IST
        uploaded_at = self.dataset.get('uploaded_at', '')
        date_str = format_timestamp_ist(uploaded_at)
        
        date_lbl = QLabel(f"Uploaded: {date_str}")
        date_lbl.setStyleSheet(f"""
            color: {COLORS['text-muted']};
            font-size: 12px;
            background: transparent;
        """)
        layout.addWidget(date_lbl)
        
        # Action buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        # View button
        view_btn = QPushButton("View")
        view_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary-700']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #156B66;
            }}
        """)
        view_btn.clicked.connect(lambda: self.view_clicked.emit(self.dataset_id))
        btn_row.addWidget(view_btn)
        
        # Download button
        download_btn = QPushButton("Report")
        download_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['primary-700']};
                border: 1px solid {COLORS['primary-700']};
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary-700']}10;
            }}
        """)
        download_btn.clicked.connect(lambda: self.download_clicked.emit(self.dataset_id))
        btn_row.addWidget(download_btn)
        
        btn_row.addStretch()
        
        # Delete button
        delete_btn = QPushButton("X")
        delete_btn.setFixedWidth(36)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['error']};
                border: 1px solid {COLORS['error']};
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['error']}10;
            }}
        """)
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.dataset_id))
        btn_row.addWidget(delete_btn)
        
        layout.addLayout(btn_row)


class FetchWorker(QThread):
    """Background thread for fetching datasets"""
    finished = pyqtSignal(bool, list, str)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
    
    def run(self):
        result = self.api_client.get_datasets()
        if result.success:
            data = result.data or []
            if isinstance(data, dict) and 'results' in data:
                data = data['results']
            elif isinstance(data, dict):
                data = []
            self.finished.emit(True, data, "")
        else:
            self.finished.emit(False, [], result.error or "Failed to fetch datasets")


class HistoryPage(QWidget):
    """
    History Page - List of uploaded datasets
    
    ONLY shows data when user is authenticated (has token).
    Shows login prompt when not authenticated.
    """
    
    view_dataset = pyqtSignal(int)
    download_report = pyqtSignal(int)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self._worker = None
        self._is_authenticated = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_row = QHBoxLayout()
        
        title = QLabel("Upload History")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 600;
            color: {COLORS['text-primary']};
        """)
        header_row.addWidget(title)
        
        header_row.addStretch()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary-700']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #156B66;
            }}
            QPushButton:disabled {{
                background-color: {COLORS['border']};
            }}
        """)
        self.refresh_btn.clicked.connect(self.refresh)
        header_row.addWidget(self.refresh_btn)
        
        layout.addLayout(header_row)
        
        # Description
        desc = QLabel("View and manage your previously uploaded datasets.")
        desc.setStyleSheet(f"""
            color: {COLORS['text-secondary']};
            font-size: 14px;
        """)
        layout.addWidget(desc)
        
        # Scroll area for cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(16)
        self.cards_layout.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(self.cards_container)
        layout.addWidget(scroll, stretch=1)
        
        # Empty state
        self.empty_label = QFrame()
        self.empty_label.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 2px dashed {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        empty_layout = QVBoxLayout(self.empty_label)
        empty_layout.setAlignment(Qt.AlignCenter)
        
        empty_text = QLabel("No datasets uploaded yet")
        empty_text.setStyleSheet(f"""
            color: {COLORS['text-muted']};
            font-size: 16px;
            padding: 40px;
        """)
        empty_text.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_text)
        
        self.empty_label.setVisible(False)
        layout.addWidget(self.empty_label)
        
        # Login required state
        self.login_required = QFrame()
        self.login_required.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['warning']}15;
                border: 1px solid {COLORS['warning']};
                border-radius: 12px;
            }}
        """)
        login_layout = QVBoxLayout(self.login_required)
        login_layout.setAlignment(Qt.AlignCenter)
        
        login_text = QLabel("Please log in to view your upload history")
        login_text.setStyleSheet(f"""
            color: {COLORS['warning']};
            font-size: 16px;
            font-weight: 500;
            padding: 30px;
        """)
        login_text.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(login_text)
        
        login_hint = QLabel("Your datasets are synced with your account")
        login_hint.setStyleSheet(f"""
            color: {COLORS['text-muted']};
            font-size: 13px;
            padding-bottom: 20px;
        """)
        login_hint.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(login_hint)
        
        self.login_required.setVisible(True)  # Show by default
        layout.addWidget(self.login_required)
    
    def set_authenticated(self, is_authenticated: bool):
        """Called when auth state changes"""
        self._is_authenticated = is_authenticated
        if is_authenticated:
            self.login_required.setVisible(False)
            self.refresh()
        else:
            # Clear data and show login prompt
            self._clear_cards()
            self.empty_label.setVisible(False)
            self.login_required.setVisible(True)
    
    def showEvent(self, event):
        """Refresh when page becomes visible (only if authenticated)"""
        super().showEvent(event)
        if self._is_authenticated:
            self.refresh()
    
    def refresh(self):
        """Fetch datasets from API (only if authenticated)"""
        if not self._is_authenticated:
            self.login_required.setVisible(True)
            return
        
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Loading...")
        self.login_required.setVisible(False)
        self.empty_label.setVisible(False)
        
        self._worker = FetchWorker(self.api_client)
        self._worker.finished.connect(self._on_fetch_complete)
        self._worker.start()
    
    def _clear_cards(self):
        """Clear all dataset cards"""
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def _on_fetch_complete(self, success: bool, datasets: list, error: str):
        """Handle fetch completion"""
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("Refresh")
        
        self._clear_cards()
        
        if not success:
            self.empty_label.setVisible(True)
            return
        
        if not datasets:
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
