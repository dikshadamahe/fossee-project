from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

# FOSSEE Colors
COLORS = {
    'primary-700': '#1B7F79',
    'primary-900': '#0F2A44',
    'bg-main': '#F7F9FC',
    'surface': '#FFFFFF',
    'border': '#E2E8F0',
    'text-primary': '#102A43',
    'text-secondary': '#486581',
}


class AuthPage(QWidget):
    """Base class for Auth pages - CLEAN DESIGN"""
    
    def __init__(self, api_client, title):
        super().__init__()
        self.api_client = api_client
        
        # Set background
        self.setStyleSheet(f"background-color: {COLORS['bg-main']};")
        
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        
        # Card container
        self.card = QFrame()
        self.card.setFixedWidth(380)
        self.card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                border-top: 4px solid {COLORS['primary-700']};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setSpacing(6)
        self.card_layout.setContentsMargins(32, 28, 32, 28)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS['primary-900']};
            padding-bottom: 16px;
            background: transparent;
            border: none;
        """)
        self.card_layout.addWidget(self.title_label)
        
        self.layout.addWidget(self.card)
    
    def _add_field(self, label_text: str, placeholder: str, is_password: bool = False) -> QLineEdit:
        """Add a labeled input field"""
        label = QLabel(label_text)
        label.setStyleSheet(f"""
            color: {COLORS['text-primary']};
            font-size: 13px;
            font-weight: 500;
            padding-top: 8px;
            background: transparent;
            border: none;
        """)
        self.card_layout.addWidget(label)
        
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
        input_field.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['bg-main']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 12px 14px;
                font-size: 14px;
                color: {COLORS['text-primary']};
            }}
            QLineEdit:focus {{
                border-color: {COLORS['primary-700']};
            }}
        """)
        self.card_layout.addWidget(input_field)
        return input_field
    
    def _add_primary_button(self, text: str) -> QPushButton:
        """Add primary action button"""
        self.card_layout.addSpacing(12)
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary-700']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 20px;
                font-size: 15px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #156B66;
            }}
            QPushButton:pressed {{
                background-color: #0F4F4C;
            }}
        """)
        self.card_layout.addWidget(btn)
        return btn
    
    def _add_link_button(self, text: str) -> QPushButton:
        """Add secondary link button"""
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['primary-700']};
                border: 1px solid {COLORS['primary-700']};
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #1B7F7910;
            }}
        """)
        self.card_layout.addWidget(btn)
        return btn


class LoginPage(AuthPage):
    login_success = pyqtSignal(dict)
    switch_to_register = pyqtSignal()

    def __init__(self, api_client):
        super().__init__(api_client, "Login")
        
        self.username_input = self._add_field("Username", "Enter your username")
        self.password_input = self._add_field("Password", "Enter your password", is_password=True)
        
        self.login_btn = self._add_primary_button("Login")
        self.login_btn.clicked.connect(self.handle_login)
        
        self.register_link = self._add_link_button("Don't have an account? Register")
        self.register_link.clicked.connect(self.switch_to_register.emit)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
            
        result = self.api_client.login(username, password)
        if result.success:
            self.login_success.emit(result.data)
        else:
            QMessageBox.warning(self, "Login Failed", result.error or "Invalid credentials")


class RegisterPage(AuthPage):
    register_success = pyqtSignal()
    switch_to_login = pyqtSignal()

    def __init__(self, api_client):
        super().__init__(api_client, "Register")
        
        self.username_input = self._add_field("Username", "Choose a username")
        self.email_input = self._add_field("Email", "Enter your email")
        self.password_input = self._add_field("Password", "Create a password", is_password=True)
        self.confirm_input = self._add_field("Confirm Password", "Confirm password", is_password=True)
        
        self.register_btn = self._add_primary_button("Register")
        self.register_btn.clicked.connect(self.handle_register)
        
        self.login_link = self._add_link_button("Already have an account? Login")
        self.login_link.clicked.connect(self.switch_to_login.emit)

    def handle_register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not all([username, email, password, confirm]):
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
            
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
            
        result = self.api_client.register(username, email, password, confirm)
        if result.success:
            QMessageBox.information(self, "Success", "Registration successful! Please login.")
            self.register_success.emit()
        else:
            QMessageBox.warning(self, "Registration Failed", result.error or "Registration failed")
