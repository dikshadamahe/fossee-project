"""
Custom styled message dialogs to replace QMessageBox.
QMessageBox uses native Windows rendering which ignores Qt stylesheets.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


COLORS = {
    'primary-700': '#1B7F79',
    'primary-900': '#0F2A44',
    'bg-main': '#F7F9FC',
    'surface': '#FFFFFF',
    'border': '#E2E8F0',
    'text-primary': '#102A43',
    'text-secondary': '#486581',
    'warning': '#D97706',
    'error': '#C53030',
    'success': '#2EA043',
}


class StyledMessageDialog(QDialog):
    """Clean, modern message dialog matching FOSSEE design system."""

    YES = 1
    NO = 0

    def __init__(self, parent, title, message, icon_type="info", buttons=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(380)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self._result_value = self.NO

        # Remove default window background, use card style
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['surface']};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Top accent bar
        accent = QFrame()
        accent.setFixedHeight(4)
        icon_colors = {
            "warning": COLORS['warning'],
            "error": COLORS['error'],
            "info": COLORS['primary-700'],
            "success": COLORS['success'],
            "question": COLORS['primary-700'],
        }
        accent_color = icon_colors.get(icon_type, COLORS['primary-700'])
        accent.setStyleSheet(f"background-color: {accent_color}; border: none;")
        layout.addWidget(accent)

        # Content area
        content = QVBoxLayout()
        content.setSpacing(16)
        content.setContentsMargins(28, 24, 28, 24)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {COLORS['primary-900']};
            font-size: 17px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)
        content.addWidget(title_label)

        # Message
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet(f"""
            color: {COLORS['text-secondary']};
            font-size: 14px;
            line-height: 1.5;
            background: transparent;
            border: none;
        """)
        content.addWidget(msg_label)

        content.addSpacing(8)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        if buttons == "yes_no":
            no_btn = QPushButton("Cancel")
            no_btn.setCursor(Qt.PointingHandCursor)
            no_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['text-secondary']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 8px;
                    padding: 9px 22px;
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['bg-main']};
                    color: {COLORS['text-primary']};
                }}
            """)
            no_btn.clicked.connect(lambda: self._close_with(self.NO))
            btn_layout.addWidget(no_btn)

            yes_btn = QPushButton("Confirm")
            yes_btn.setCursor(Qt.PointingHandCursor)
            yes_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary-700']};
                    color: #FFFFFF;
                    border: none;
                    border-radius: 8px;
                    padding: 9px 22px;
                    font-size: 13px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: #156B66;
                }}
            """)
            yes_btn.clicked.connect(lambda: self._close_with(self.YES))
            btn_layout.addWidget(yes_btn)
        else:
            ok_btn = QPushButton("OK")
            ok_btn.setCursor(Qt.PointingHandCursor)
            ok_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary-700']};
                    color: #FFFFFF;
                    border: none;
                    border-radius: 8px;
                    padding: 9px 28px;
                    font-size: 13px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: #156B66;
                }}
            """)
            ok_btn.clicked.connect(self.accept)
            btn_layout.addWidget(ok_btn)

        content.addLayout(btn_layout)
        layout.addLayout(content)

    def _close_with(self, value):
        self._result_value = value
        self.accept()

    @property
    def result_value(self):
        return self._result_value


def show_warning(parent, title, message):
    dlg = StyledMessageDialog(parent, title, message, icon_type="warning")
    dlg.exec_()


def show_info(parent, title, message):
    dlg = StyledMessageDialog(parent, title, message, icon_type="success")
    dlg.exec_()


def show_error(parent, title, message):
    dlg = StyledMessageDialog(parent, title, message, icon_type="error")
    dlg.exec_()


def ask_yes_no(parent, title, message) -> bool:
    dlg = StyledMessageDialog(parent, title, message, icon_type="question", buttons="yes_no")
    dlg.exec_()
    return dlg.result_value == StyledMessageDialog.YES
