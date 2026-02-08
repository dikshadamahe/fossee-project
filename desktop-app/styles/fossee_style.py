"""
FOSSEE Scientific Analytics - QSS Stylesheet
Chemical Equipment Parameter Visualizer
PyQt5 Desktop Application

Design System v1.0 - Exact hex values from design.md
"""

# =============================================================================
# COLOR TOKENS (exact hex from design.md)
# =============================================================================

COLORS = {
    # Primary Colors
    'primary-900': '#0F2A44',  # Headers, nav background
    'primary-700': '#1B7F79',  # Primary actions, links
    'primary-600': '#3A4E9F',  # Analytics highlight
    'success': '#2EA043',       # Valid CSV, positive
    'warning': '#D97706',       # Data issues
    'error': '#C53030',         # Validation error
    
    # Neutrals
    'bg-main': '#F7F9FC',       # App background
    'surface': '#FFFFFF',       # Cards
    'border': '#E2E8F0',        # Dividers
    'text-primary': '#102A43',  # Body
    'text-secondary': '#486581', # Subtext
    'text-muted': '#829AB1',    # Labels
    
    # Chart Palette
    'flowrate': '#1B7F79',
    'pressure': '#3A4E9F',
    'temperature': '#C53030',
}

# =============================================================================
# FONT SETTINGS
# =============================================================================

FONTS = {
    'primary': 'Segoe UI, Noto Sans, sans-serif',
    'mono': 'JetBrains Mono, Consolas, monospace',
    'heading': 'Segoe UI, Noto Sans, sans-serif',
}

# =============================================================================
# MAIN QSS STYLESHEET
# =============================================================================

STYLESHEET = """
/* ==========================================================================
   FOSSEE Scientific Analytics - PyQt5 Stylesheet
   Design System v1.0
   ========================================================================== */

/* --------------------------------------------------------------------------
   GLOBAL RESET & BASE
   -------------------------------------------------------------------------- */

* {
    font-family: "Segoe UI", "Noto Sans", sans-serif;
    font-size: 15px;
    color: #102A43;
}

QMainWindow, QWidget {
    background-color: #F7F9FC;
}

/* --------------------------------------------------------------------------
   LAB PANELS (Cards)
   -------------------------------------------------------------------------- */

QFrame#LabPanel, QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    border-top: 3px solid #1B7F79;
    padding: 16px;
}

QGroupBox {
    font-size: 16px;
    font-weight: 600;
    color: #102A43;
    margin-top: 12px;
    padding-top: 20px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    background-color: #FFFFFF;
    color: #102A43;
}

/* --------------------------------------------------------------------------
   BUTTONS
   -------------------------------------------------------------------------- */

/* Primary Button */
QPushButton {
    background-color: #1B7F79;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 600;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #156B66;
}

QPushButton:pressed {
    background-color: #0F5550;
}

QPushButton:disabled {
    background-color: #829AB1;
    color: #E2E8F0;
}

QPushButton:focus {
    outline: none;
    border: none;
}

*:focus {
    outline: none;
}

/* Secondary Button */
QPushButton#SecondaryButton {
    background-color: transparent;
    color: #1B7F79;
    border: 2px solid #1B7F79;
}

QPushButton#SecondaryButton:hover {
    background-color: rgba(27, 127, 121, 0.1);
}

/* Danger Button */
QPushButton#DangerButton {
    background-color: #C53030;
    color: #FFFFFF;
}

QPushButton#DangerButton:hover {
    background-color: #A02828;
}

/* Icon Button */
QPushButton#IconButton {
    background-color: transparent;
    border: none;
    padding: 8px;
    min-height: 32px;
    min-width: 32px;
    border-radius: 8px;
}

QPushButton#IconButton:hover {
    background-color: #E2E8F0;
}

/* --------------------------------------------------------------------------
   LABELS
   -------------------------------------------------------------------------- */

QLabel {
    color: #102A43;
    background-color: transparent;
}

QLabel#HeadingH1 {
    font-size: 28px;
    font-weight: 600;
    color: #102A43;
}

QLabel#HeadingH2 {
    font-size: 22px;
    font-weight: 600;
    color: #102A43;
}

QLabel#HeadingH3 {
    font-size: 18px;
    font-weight: 600;
    color: #102A43;
}

QLabel#TextSecondary {
    color: #486581;
    font-size: 14px;
}

QLabel#TextMuted {
    color: #829AB1;
    font-size: 13px;
}

QLabel#MonoLabel {
    font-family: "JetBrains Mono", "Consolas", monospace;
    font-size: 13px;
}

/* --------------------------------------------------------------------------
   INPUTS
   -------------------------------------------------------------------------- */

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 15px;
    color: #102A43;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #1B7F79;
    outline: none;
}

QLineEdit:disabled {
    background-color: #F7F9FC;
    color: #829AB1;
}

/* --------------------------------------------------------------------------
   COMBO BOX
   -------------------------------------------------------------------------- */

QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 10px 12px;
    min-height: 40px;
    color: #102A43;
}

QComboBox:hover {
    border-color: #1B7F79;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #486581;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    selection-background-color: rgba(27, 127, 121, 0.15);
    selection-color: #102A43;
    padding: 4px;
}

/* --------------------------------------------------------------------------
   TABLES
   -------------------------------------------------------------------------- */

QTableWidget, QTableView {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    gridline-color: #E2E8F0;
    font-family: "JetBrains Mono", "Consolas", monospace;
    font-size: 13px;
}

QTableWidget::item, QTableView::item {
    padding: 8px 12px;
    border-bottom: 1px solid #E2E8F0;
}

QTableWidget::item:selected, QTableView::item:selected {
    background-color: rgba(27, 127, 121, 0.15);
    color: #102A43;
}

QHeaderView::section {
    background-color: #0F2A44;
    color: #FFFFFF;
    font-family: "Segoe UI", "Noto Sans", sans-serif;
    font-size: 13px;
    font-weight: 600;
    padding: 10px 12px;
    border: none;
    border-right: 1px solid #1B7F79;
}

QHeaderView::section:first {
    border-top-left-radius: 10px;
}

QHeaderView::section:last {
    border-top-right-radius: 10px;
    border-right: none;
}

/* --------------------------------------------------------------------------
   SCROLL BARS
   -------------------------------------------------------------------------- */

QScrollBar:vertical {
    background-color: #F7F9FC;
    width: 12px;
    border-radius: 6px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background-color: #829AB1;
    border-radius: 4px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background-color: #486581;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #F7F9FC;
    height: 12px;
    border-radius: 6px;
    margin: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #829AB1;
    border-radius: 4px;
    min-width: 40px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #486581;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* --------------------------------------------------------------------------
   PROGRESS BAR
   -------------------------------------------------------------------------- */

QProgressBar {
    background-color: #E2E8F0;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #1B7F79;
    border-radius: 4px;
}

/* --------------------------------------------------------------------------
   TAB WIDGET
   -------------------------------------------------------------------------- */

QTabWidget::pane {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    border-top-left-radius: 0;
    padding: 16px;
}

QTabBar::tab {
    background-color: #F7F9FC;
    color: #486581;
    border: 1px solid #E2E8F0;
    border-bottom: none;
    padding: 10px 20px;
    font-weight: 500;
    margin-right: 2px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #1B7F79;
    font-weight: 600;
    border-bottom: 2px solid #1B7F79;
}

QTabBar::tab:hover:!selected {
    background-color: #E2E8F0;
}

/* --------------------------------------------------------------------------
   SPLITTER
   -------------------------------------------------------------------------- */

QSplitter::handle {
    background-color: #E2E8F0;
    width: 2px;
    height: 2px;
}

QSplitter::handle:hover {
    background-color: #1B7F79;
}

/* --------------------------------------------------------------------------
   LIST WIDGET
   -------------------------------------------------------------------------- */

QListWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 4px;
}

QListWidget::item {
    padding: 12px 16px;
    border-radius: 8px;
    margin: 2px;
}

QListWidget::item:selected {
    background-color: rgba(27, 127, 121, 0.15);
    color: #102A43;
}

QListWidget::item:hover:!selected {
    background-color: #F7F9FC;
}

/* --------------------------------------------------------------------------
   MENU BAR
   -------------------------------------------------------------------------- */

QMenuBar {
    background-color: #0F2A44;
    color: #FFFFFF;
    padding: 4px 8px;
}

QMenuBar::item {
    padding: 8px 16px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #1B7F79;
}

QMenu {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    padding: 10px 24px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: rgba(27, 127, 121, 0.15);
}

/* --------------------------------------------------------------------------
   STATUS BAR
   -------------------------------------------------------------------------- */

QStatusBar {
    background-color: #0F2A44;
    color: #FFFFFF;
    font-size: 13px;
}

QStatusBar::item {
    border: none;
}

/* --------------------------------------------------------------------------
   MESSAGE BOX
   -------------------------------------------------------------------------- */

QMessageBox {
    background-color: #FFFFFF;
}

QMessageBox QLabel {
    color: #102A43;
    font-size: 14px;
    min-width: 200px;
}

QMessageBox QPushButton {
    background-color: #1B7F79;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 24px;
    font-size: 13px;
    font-weight: 600;
    min-height: 32px;
    min-width: 80px;
}

QMessageBox QPushButton:hover {
    background-color: #156B66;
}

QDialogButtonBox QPushButton {
    background-color: #1B7F79;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 24px;
    font-size: 13px;
    font-weight: 600;
    min-height: 32px;
    min-width: 80px;
}

QDialogButtonBox QPushButton:hover {
    background-color: #156B66;
}

QDialog QPushButton {
    background-color: #1B7F79;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 24px;
    font-size: 13px;
    font-weight: 600;
    min-height: 32px;
    min-width: 80px;
}

QDialog QPushButton:hover {
    background-color: #156B66;
}

/* --------------------------------------------------------------------------
   TOOLTIPS
   -------------------------------------------------------------------------- */

QToolTip {
    background-color: #0F2A44;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
}

/* --------------------------------------------------------------------------
   UPLOAD ZONE (Custom Widget)
   -------------------------------------------------------------------------- */

QFrame#UploadZone {
    background-color: #FFFFFF;
    border: 2px dashed #E2E8F0;
    border-radius: 10px;
    min-height: 220px;
}

QFrame#UploadZone[state="drag"] {
    border-color: #1B7F79;
    border-style: solid;
    background-color: rgba(27, 127, 121, 0.05);
}

QFrame#UploadZone[state="valid"] {
    border-color: #2EA043;
    background-color: rgba(46, 160, 67, 0.05);
}

QFrame#UploadZone[state="invalid"] {
    border-color: #C53030;
    background-color: rgba(197, 48, 48, 0.05);
}

QFrame#UploadZone[state="processing"] {
    border-color: #3A4E9F;
    background-color: rgba(58, 78, 159, 0.05);
}

/* --------------------------------------------------------------------------
   BADGES
   -------------------------------------------------------------------------- */

QLabel#BadgeSuccess {
    background-color: rgba(46, 160, 67, 0.15);
    color: #2EA043;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 600;
}

QLabel#BadgeWarning {
    background-color: rgba(217, 119, 6, 0.15);
    color: #D97706;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 600;
}

QLabel#BadgeError {
    background-color: rgba(197, 48, 48, 0.15);
    color: #C53030;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 600;
}

QLabel#BadgeInfo {
    background-color: rgba(58, 78, 159, 0.15);
    color: #3A4E9F;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 600;
}

/* --------------------------------------------------------------------------
   SUMMARY CARDS
   -------------------------------------------------------------------------- */

QFrame#SummaryCard {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 20px;
    min-width: 180px;
}

QLabel#SummaryCardTitle {
    color: #486581;
    font-size: 13px;
    font-weight: 400;
}

QLabel#SummaryCardValue {
    color: #102A43;
    font-family: "JetBrains Mono", "Consolas", monospace;
    font-size: 28px;
    font-weight: 600;
}

QLabel#SummaryCardUnit {
    color: #829AB1;
    font-size: 14px;
}

/* --------------------------------------------------------------------------
   CHART CONTAINER
   -------------------------------------------------------------------------- */

QFrame#ChartContainer {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    border-top: 3px solid #1B7F79;
    padding: 16px;
}

/* --------------------------------------------------------------------------
   HISTORY PANEL
   -------------------------------------------------------------------------- */

QFrame#HistoryPanel {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    min-width: 320px;
}

QFrame#HistoryItem {
    background-color: transparent;
    border-bottom: 1px solid #E2E8F0;
    padding: 12px 16px;
}

QFrame#HistoryItem:hover {
    background-color: #F7F9FC;
}

QFrame#HistoryItem[selected="true"] {
    background-color: rgba(27, 127, 121, 0.1);
    border-left: 3px solid #1B7F79;
}
"""

def get_stylesheet():
    """Return the complete QSS stylesheet"""
    return STYLESHEET

def get_colors():
    """Return the color dictionary"""
    return COLORS.copy()

def get_fonts():
    """Return the font dictionary"""
    return FONTS.copy()
