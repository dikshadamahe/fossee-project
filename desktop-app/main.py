"""
FOSSEE Scientific Analytics - PyQt5 Desktop Application
Chemical Equipment Parameter Visualizer

Main Application Entry Point
- Identical layout to web frontend
- Calls same Django REST APIs
- Matplotlib charts with FOSSEE color palette
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame, QStatusBar,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from styles.fossee_style import get_stylesheet, COLORS
from api_client import get_client, APIClient
from pages import UploadPage, DashboardPage, HistoryPage
from pages.auth_page import LoginPage, RegisterPage


class NavButton(QPushButton):
    """Navigation button styled like web frontend nav links"""
    
    def __init__(self, icon: str, text: str, parent=None):
        # Handle empty icon
        if icon:
            super().__init__(f"{icon}  {text}", parent)
        else:
            super().__init__(text, parent)
        self._active = False
        self._update_style()
    
    def set_active(self, active: bool):
        self._active = active
        self._update_style()
    
    def _update_style(self):
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary-700']};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 16px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: #156B66;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: rgba(255, 255, 255, 0.8);
                    border: none;
                    border-radius: 8px;
                    padding: 10px 16px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                }}
            """)


class Header(QFrame):
    """Application header matching web frontend"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary-900']};
                padding: 0;
            }}
        """)
        self.setFixedHeight(70)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(16)
        
        # Logo
        logo = QLabel("CEV")
        logo.setStyleSheet(f"""
            background-color: {COLORS['primary-700']};
            border-radius: 8px;
            padding: 8px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        """)
        logo.setFixedSize(40, 40)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)
        
        # Title
        title_container = QVBoxLayout()
        title_container.setSpacing(0)
        
        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: 600;
            background: transparent;
        """)
        title_container.addWidget(title)
        
        subtitle = QLabel("FOSSEE Scientific Analytics")
        subtitle.setStyleSheet(f"""
            color: {COLORS['primary-700']};
            font-size: 12px;
            background: transparent;
        """)
        title_container.addWidget(subtitle)
        
        layout.addLayout(title_container)
        layout.addStretch()
        
        # Navigation buttons
        self.nav_buttons = {}
        
        self.upload_btn = NavButton("", "Upload")
        self.nav_buttons['upload'] = self.upload_btn
        layout.addWidget(self.upload_btn)
        
        self.dashboard_btn = NavButton("", "Dashboard")
        self.nav_buttons['dashboard'] = self.dashboard_btn
        layout.addWidget(self.dashboard_btn)
        
        self.history_btn = NavButton("", "History")
        self.nav_buttons['history'] = self.history_btn
        layout.addWidget(self.history_btn)
        
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); width: 1px;")
        line.setFixedHeight(30)
        layout.addWidget(line)
        
        # Auth Buttons
        self.login_btn = NavButton("", "Login")
        self.nav_buttons['login'] = self.login_btn
        layout.addWidget(self.login_btn)
        
        self.logout_btn = NavButton("", "Logout")
        self.logout_btn.hide()
        layout.addWidget(self.logout_btn)
    
    def set_active_page(self, page: str):
        """Update active nav button"""
        for name, btn in self.nav_buttons.items():
            btn.set_active(name == page)
            
    def set_authenticated(self, is_auth: bool):
        """Toggle auth buttons"""
        self.login_btn.setVisible(not is_auth)
        self.logout_btn.setVisible(is_auth)


class MainWindow(QMainWindow):
    """Main application window - identical layout to web frontend"""
    
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        
        self.setWindowTitle("Chemical Equipment Visualizer - FOSSEE")
        self.setMinimumSize(1280, 800)
        
        self._current_dataset_id = None
        self._user = None
        
        self._setup_statusbar()
        self._setup_ui()
        self._connect_signals()
        
        # Check API connection
        if not self.api_client.check_connection():
            QMessageBox.warning(
                self,
                "Connection Warning",
                "Cannot connect to Django backend at localhost:8000.\n"
                "Please ensure the server is running:\n\n"
                "  cd backend && python manage.py runserver"
            )
    
    def _setup_ui(self):
        """Create main UI layout - matches web frontend"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header (like web frontend's <header>)
        self.header = Header()
        layout.addWidget(self.header)
        
        # Page stack (like web frontend's <Outlet />)
        self.page_stack = QStackedWidget()
        self.page_stack.setStyleSheet(f"background-color: {COLORS['bg-main']};")
        
        # Create pages
        self.upload_page = UploadPage(self.api_client)
        self.dashboard_page = DashboardPage(self.api_client)
        self.history_page = HistoryPage(self.api_client)
        self.login_page = LoginPage(self.api_client)
        self.register_page = RegisterPage(self.api_client)
        
        self.page_stack.addWidget(self.upload_page)      # index 0
        self.page_stack.addWidget(self.dashboard_page)   # index 1
        self.page_stack.addWidget(self.history_page)     # index 2
        self.page_stack.addWidget(self.login_page)       # index 3
        self.page_stack.addWidget(self.register_page)    # index 4
        
        layout.addWidget(self.page_stack, stretch=1)
        
        # Start on upload page
        self._navigate('upload')
    
    def _setup_statusbar(self):
        """Create status bar"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready - Connect to Django backend at localhost:8000")
    
    def _connect_signals(self):
        """Connect all signals"""
        # Header navigation
        self.header.upload_btn.clicked.connect(lambda: self._navigate('upload'))
        self.header.dashboard_btn.clicked.connect(lambda: self._navigate('dashboard'))
        self.header.history_btn.clicked.connect(lambda: self._navigate('history'))
        self.header.login_btn.clicked.connect(lambda: self._navigate('login'))
        self.header.logout_btn.clicked.connect(self._handle_logout)
        
        # Upload page signals
        self.upload_page.upload_complete.connect(self._on_upload_complete)
        
        # History page signals
        self.history_page.view_dataset.connect(self._view_dataset)
        self.history_page.download_report.connect(self._download_report)
        
        # Dashboard signals
        self.dashboard_page.download_report.connect(self._download_report)
        
        # Auth signals
        self.login_page.login_success.connect(self._handle_login_success)
        self.login_page.switch_to_register.connect(lambda: self._navigate('register'))
        
        self.register_page.register_success.connect(lambda: self._navigate('login'))
        self.register_page.switch_to_login.connect(lambda: self._navigate('login'))
    
    def _navigate(self, page: str):
        """Navigate to a page"""
        page_map = {
            'upload': 0,
            'dashboard': 1,
            'history': 2,
            'login': 3,
            'register': 4
        }
        
        if page in page_map:
            self.page_stack.setCurrentIndex(page_map[page])
            self.header.set_active_page(page)
            
            title = page.title()
            if self._user:
                self.statusbar.showMessage(f"Page: {title} | User: {self._user.get('username')}")
            else:
                self.statusbar.showMessage(f"Page: {title}")
    
    def _on_upload_complete(self, dataset_id: int, summary: dict):
        """Handle successful upload"""
        self._current_dataset_id = dataset_id
        self.dashboard_page.load_from_summary(dataset_id, summary)
        self._navigate('dashboard')
        self.statusbar.showMessage(f"Uploaded dataset #{dataset_id} - {summary.get('total_count', 0)} records")
    
    def _view_dataset(self, dataset_id: int):
        """View a dataset from history"""
        self._current_dataset_id = dataset_id
        self.dashboard_page.load_dataset(dataset_id)
        self._navigate('dashboard')
        self.statusbar.showMessage(f"Viewing dataset #{dataset_id}")
    
    def _download_report(self, dataset_id: int):
        """Download PDF report for dataset"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            f"equipment_report_{dataset_id}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if filepath:
            self.statusbar.showMessage("Generating report...")
            result = self.api_client.download_report(dataset_id, filepath)
            
            if result.success:
                self.statusbar.showMessage(f"Report saved: {filepath}")
                QMessageBox.information(self, "Success", f"Report saved to:\n{filepath}")
            else:
                self.statusbar.showMessage("Report generation failed")
                QMessageBox.warning(self, "Error", f"Failed to generate report:\n{result.error}")

    def _handle_login_success(self, user_data):
        """Handle successful login"""
        self._user = user_data
        self.header.set_authenticated(True)
        self.statusbar.showMessage(f"Logged in as {user_data.get('username')}")
        
        # Update history page auth state - this will show user's datasets
        self.history_page.set_authenticated(True)
        
        self._navigate('upload')

    def _handle_logout(self):
        """Handle logout"""
        self.api_client.logout()
        self._user = None
        self.header.set_authenticated(False)
        self.statusbar.showMessage("Logged out")
        
        # Update history page auth state - this will hide datasets
        self.history_page.set_authenticated(False)
        
        self._navigate('login')


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("FOSSEE")
    
    # Set font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Apply FOSSEE stylesheet
    app.setStyleSheet(get_stylesheet())
    
    # Create API client
    api_client = get_client("http://localhost:8000")
    
    # Create and show main window
    window = MainWindow(api_client)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
