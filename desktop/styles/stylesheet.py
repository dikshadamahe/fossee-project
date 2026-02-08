"""
FOSSEE Scientific Analytics UI - QSS Stylesheet
Chemical Equipment Parameter Visualizer - Desktop
Matching the design system tokens exactly
"""

STYLESHEET = """
/* Main Window */
QMainWindow {
    background-color: #F7F9FC;
}

QWidget {
    font-family: "Segoe UI", "Noto Sans", sans-serif;
    font-size: 15px;
    color: #102A43;
}

/* Headers */
QLabel#header {
    font-size: 28px;
    font-weight: 600;
    color: #0F2A44;
}

QLabel#subheader {
    font-size: 22px;
    font-weight: 600;
    color: #0F2A44;
}

QLabel#sectionHeader {
    font-size: 18px;
    font-weight: 600;
    color: #0F2A44;
}

/* Lab Panel (Card) */
QFrame#labPanel {
    background-color: #FFFFFF;
    border-radius: 10px;
    border-top: 3px solid #1B7F79;
}

QFrame#labPanelHeader {
    background-color: transparent;
    border-bottom: 1px solid #E2E8F0;
    padding: 16px 20px;
}

QFrame#labPanelBody {
    background-color: transparent;
    padding: 20px;
}

/* Buttons */
QPushButton {
    background-color: #1B7F79;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #166965;
}

QPushButton:pressed {
    background-color: #145856;
}

QPushButton:disabled {
    background-color: #B0B0B0;
}

QPushButton#secondary {
    background-color: transparent;
    color: #1B7F79;
    border: 1px solid #1B7F79;
}

QPushButton#secondary:hover {
    background-color: rgba(27, 127, 121, 0.1);
}

QPushButton#danger {
    background-color: #C53030;
}

QPushButton#danger:hover {
    background-color: #a82828;
}

/* Input Fields */
QLineEdit, QTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    selection-background-color: #1B7F79;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #1B7F79;
}

/* Tables */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    gridline-color: #E2E8F0;
    font-family: "JetBrains Mono", "Consolas", monospace;
    font-size: 13px;
}

QTableWidget::item {
    padding: 8px 16px;
    border-bottom: 1px solid #E2E8F0;
}

QTableWidget::item:selected {
    background-color: rgba(27, 127, 121, 0.1);
    color: #102A43;
}

QTableWidget::item:alternate {
    background-color: #F7F9FC;
}

QHeaderView::section {
    background-color: #0F2A44;
    color: white;
    font-weight: 600;
    font-size: 13px;
    padding: 12px 16px;
    border: none;
}

QHeaderView::section:first {
    border-top-left-radius: 8px;
}

QHeaderView::section:last {
    border-top-right-radius: 8px;
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: #F7F9FC;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #E2E8F0;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #829AB1;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #F7F9FC;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #E2E8F0;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #829AB1;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* Status Labels */
QLabel#success {
    color: #2EA043;
    font-weight: 500;
}

QLabel#warning {
    color: #D97706;
    font-weight: 500;
}

QLabel#error {
    color: #C53030;
    font-weight: 500;
}

QLabel#muted {
    color: #829AB1;
    font-size: 13px;
}

QLabel#secondary {
    color: #486581;
}

/* Monospace Text */
QLabel#mono {
    font-family: "JetBrains Mono", "Consolas", monospace;
    font-size: 13px;
    font-weight: 500;
}

/* List Widget */
QListWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    outline: none;
}

QListWidget::item {
    padding: 12px 16px;
    border-bottom: 1px solid #E2E8F0;
}

QListWidget::item:selected {
    background-color: rgba(27, 127, 121, 0.1);
    border-left: 3px solid #1B7F79;
}

QListWidget::item:hover {
    background-color: rgba(27, 127, 121, 0.05);
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    background-color: #FFFFFF;
    top: -1px;
}

QTabBar::tab {
    background-color: transparent;
    color: #486581;
    padding: 12px 24px;
    font-weight: 500;
    border: none;
    border-bottom: 2px solid transparent;
}

QTabBar::tab:selected {
    color: #1B7F79;
    border-bottom: 2px solid #1B7F79;
}

QTabBar::tab:hover {
    color: #1B7F79;
}

/* Progress Bar */
QProgressBar {
    background-color: #E2E8F0;
    border-radius: 2px;
    height: 4px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #1B7F79;
    border-radius: 2px;
}

/* Tool Tip */
QToolTip {
    background-color: #102A43;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
}

/* Group Box */
QGroupBox {
    font-weight: 600;
    font-size: 14px;
    color: #0F2A44;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    margin-top: 16px;
    padding-top: 16px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 0 8px;
    background-color: #FFFFFF;
}

/* Message Box */
QMessageBox {
    background-color: #FFFFFF;
}

QMessageBox QLabel {
    color: #102A43;
}
"""
