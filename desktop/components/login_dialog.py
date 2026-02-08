"""
Login Dialog for PyQt5 Desktop Application
FOSSEE Scientific Analytics UI
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from .api_client import APIClient


class LoginDialog(QDialog):
    """Login dialog for authentication"""
    
    login_success = pyqtSignal(dict)
    
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        
        self.setWindowTitle("FOSSEE Analytics - Login")
        self.setFixedSize(400, 350)
        self.setModal(True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header = QLabel("FOSSEE Analytics")
        header.setObjectName("header")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setWeight(QFont.DemiBold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        subtitle = QLabel("Chemical Equipment Parameter Visualizer")
        subtitle.setObjectName("secondary")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(24)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setObjectName("error")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        # Username
        username_label = QLabel("Username")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.returnPressed.connect(self._focus_password)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self._on_login)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(16)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self._on_login)
        layout.addWidget(self.login_button)
        
        layout.addStretch()
        
        # Footer
        footer = QLabel("Use the admin credentials created during setup")
        footer.setObjectName("muted")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
    
    def _focus_password(self):
        self.password_input.setFocus()
    
    def _on_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self._show_error("Please enter username and password")
            return
        
        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")
        
        try:
            result = self.api_client.login(username, password)
            
            if result.get('success'):
                self.login_success.emit(result.get('user', {}))
                self.accept()
            else:
                self._show_error(result.get('error', 'Login failed'))
        except Exception as e:
            self._show_error(f"Connection error: {str(e)}")
        finally:
            self.login_button.setEnabled(True)
            self.login_button.setText("Sign In")
    
    def _show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
