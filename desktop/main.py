"""
FOSSEE Scientific Analytics - Desktop Application
Chemical Equipment Parameter Visualizer
PyQt5 + Matplotlib
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QFrame, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QTabWidget, QMessageBox, QFileDialog, QStatusBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

# Add components to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from styles.stylesheet import STYLESHEET
from components.api_client import APIClient
from components.login_dialog import LoginDialog
from components.csv_upload import CSVUploadWidget
from components.data_table import DataTableWidget
from components.charts import MultiParameterChart, TypeDistributionChart, StatisticsPanel


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.api_client = APIClient()
        self.current_user = None
        self.datasets = []
        self.active_dataset = None
        
        self._setup_window()
        self._setup_ui()
        self._setup_status_bar()
        
        # Show login dialog
        self._show_login()
    
    def _setup_window(self):
        """Configure main window"""
        self.setWindowTitle("FOSSEE Scientific Analytics - Chemical Equipment Visualizer")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Apply stylesheet
        self.setStyleSheet(STYLESHEET)
    
    def _setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setContentsMargins(24, 24, 24, 24)
        
        # Left panel
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 900])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
    
    def _create_header(self):
        """Create the header bar"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #0F2A44;
                padding: 16px 24px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QHBoxLayout(header)
        
        # Title
        title = QLabel("FOSSEE Scientific Analytics")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.DemiBold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # User info
        self.user_label = QLabel()
        self.user_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(self.user_label)
        
        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self._on_logout)
        layout.addWidget(self.logout_button)
        
        return header
    
    def _create_left_panel(self):
        """Create the left panel with upload and dataset list"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 12, 0)
        layout.setSpacing(24)
        
        # Upload section
        upload_frame = self._create_lab_panel("Upload CSV")
        upload_layout = upload_frame.layout()
        
        self.upload_widget = CSVUploadWidget(self.api_client)
        self.upload_widget.upload_success.connect(self._on_upload_success)
        self.upload_widget.upload_error.connect(self._on_upload_error)
        upload_layout.addWidget(self.upload_widget)
        
        layout.addWidget(upload_frame)
        
        # Dataset list section
        datasets_frame = self._create_lab_panel("Recent Datasets", "Last 5")
        datasets_layout = datasets_frame.layout()
        
        self.dataset_list = QListWidget()
        self.dataset_list.itemClicked.connect(self._on_dataset_selected)
        datasets_layout.addWidget(self.dataset_list)
        
        layout.addWidget(datasets_frame)
        
        return panel
    
    def _create_right_panel(self):
        """Create the right panel with data visualization"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 0, 0, 0)
        layout.setSpacing(24)
        
        # Dataset info header
        info_frame = self._create_lab_panel("Dataset")
        info_layout = info_frame.layout()
        
        info_content = QHBoxLayout()
        
        self.dataset_name_label = QLabel("No dataset selected")
        self.dataset_name_label.setObjectName("sectionHeader")
        info_content.addWidget(self.dataset_name_label)
        
        self.dataset_count_label = QLabel()
        self.dataset_count_label.setObjectName("muted")
        info_content.addWidget(self.dataset_count_label)
        
        info_content.addStretch()
        
        self.download_report_button = QPushButton("Download PDF Report")
        self.download_report_button.setObjectName("secondary")
        self.download_report_button.clicked.connect(self._download_report)
        self.download_report_button.setEnabled(False)
        info_content.addWidget(self.download_report_button)
        
        self.delete_dataset_button = QPushButton("Delete")
        self.delete_dataset_button.setObjectName("danger")
        self.delete_dataset_button.clicked.connect(self._delete_dataset)
        self.delete_dataset_button.setEnabled(False)
        info_content.addWidget(self.delete_dataset_button)
        
        info_layout.addLayout(info_content)
        
        # Statistics panel
        self.statistics_panel = StatisticsPanel()
        info_layout.addWidget(self.statistics_panel)
        
        layout.addWidget(info_frame)
        
        # Tabs for charts and table
        viz_frame = self._create_lab_panel("Visualization")
        viz_layout = viz_frame.layout()
        
        self.tabs = QTabWidget()
        
        # Charts tab
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)
        charts_layout.setSpacing(24)
        
        self.multi_chart = MultiParameterChart()
        charts_layout.addWidget(self.multi_chart)
        
        self.type_chart = TypeDistributionChart()
        charts_layout.addWidget(self.type_chart)
        
        self.tabs.addTab(charts_widget, "Charts")
        
        # Table tab
        self.data_table = DataTableWidget()
        self.tabs.addTab(self.data_table, "Data Table")
        
        viz_layout.addWidget(self.tabs)
        layout.addWidget(viz_frame, 1)
        
        return panel
    
    def _create_lab_panel(self, title, subtitle=None):
        """Create a lab panel (card) with header"""
        frame = QFrame()
        frame.setObjectName("labPanel")
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setObjectName("labPanelHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)
        
        title_label = QLabel(title)
        title_label.setObjectName("sectionHeader")
        header_layout.addWidget(title_label)
        
        if subtitle:
            header_layout.addStretch()
            subtitle_label = QLabel(subtitle)
            subtitle_label.setObjectName("muted")
            header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header)
        
        # Body (the caller will add content here)
        body = QFrame()
        body.setObjectName("labPanelBody")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(body)
        
        # Store body layout reference
        frame.body_layout = body_layout
        frame.layout = lambda: body_layout
        
        return frame
    
    def _setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _show_login(self):
        """Show login dialog"""
        dialog = LoginDialog(self.api_client, self)
        dialog.login_success.connect(self._on_login_success)
        
        if dialog.exec_() != LoginDialog.Accepted:
            # User closed dialog without logging in
            QApplication.quit()
    
    def _on_login_success(self, user):
        """Handle successful login"""
        self.current_user = user
        self.user_label.setText(f"Logged in as {user.get('username', 'User')}")
        self._load_datasets()
        self.status_bar.showMessage("Login successful")
    
    def _on_logout(self):
        """Handle logout"""
        self.api_client.logout()
        self.current_user = None
        self.datasets = []
        self.active_dataset = None
        self._clear_display()
        self._show_login()
    
    def _load_datasets(self):
        """Load datasets from API"""
        try:
            self.datasets = self.api_client.get_datasets()
            self._refresh_dataset_list()
        except Exception as e:
            self.status_bar.showMessage(f"Failed to load datasets: {str(e)}")
    
    def _refresh_dataset_list(self):
        """Refresh the dataset list widget"""
        self.dataset_list.clear()
        
        for dataset in self.datasets:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, dataset['id'])
            
            name = dataset.get('name', 'Unnamed')
            count = dataset.get('row_count', 0)
            date = dataset.get('uploaded_at', '')[:10]
            
            item.setText(f"{name}\n{count} records · {date}")
            item.setSizeHint(QSize(0, 60))
            
            self.dataset_list.addItem(item)
    
    def _on_dataset_selected(self, item):
        """Handle dataset selection"""
        dataset_id = item.data(Qt.UserRole)
        
        try:
            dataset = self.api_client.get_dataset(dataset_id)
            if dataset:
                self.active_dataset = dataset
                self._display_dataset(dataset)
                self.status_bar.showMessage(f"Loaded dataset: {dataset.get('name', '')}")
        except Exception as e:
            self.status_bar.showMessage(f"Failed to load dataset: {str(e)}")
    
    def _display_dataset(self, dataset):
        """Display dataset in the visualization panel"""
        # Update info
        self.dataset_name_label.setText(dataset.get('name', 'Dataset'))
        self.dataset_count_label.setText(f"{dataset.get('row_count', 0)} records")
        
        # Enable buttons
        self.download_report_button.setEnabled(True)
        self.delete_dataset_button.setEnabled(True)
        
        # Update statistics
        statistics = dataset.get('statistics', {})
        self.statistics_panel.set_data(statistics)
        
        # Update charts
        records = dataset.get('records', [])
        self.multi_chart.set_data(records)
        self.type_chart.set_data(statistics)
        
        # Update table
        self.data_table.set_records(records)
    
    def _clear_display(self):
        """Clear all displayed data"""
        self.dataset_name_label.setText("No dataset selected")
        self.dataset_count_label.setText("")
        self.download_report_button.setEnabled(False)
        self.delete_dataset_button.setEnabled(False)
        self.statistics_panel.set_data(None)
        self.multi_chart.set_data([])
        self.type_chart.set_data(None)
        self.data_table.set_records([])
        self.dataset_list.clear()
    
    def _on_upload_success(self, dataset):
        """Handle successful upload"""
        self.status_bar.showMessage(f"Uploaded: {dataset.get('name', '')} ({dataset.get('row_count', 0)} records)")
        self._load_datasets()
        self.active_dataset = dataset
        self._display_dataset(dataset)
    
    def _on_upload_error(self, error):
        """Handle upload error"""
        self.status_bar.showMessage(f"Upload failed: {error}")
        QMessageBox.warning(self, "Upload Error", error)
    
    def _download_report(self):
        """Download PDF report for active dataset"""
        if not self.active_dataset:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"{self.active_dataset.get('name', 'report')}_report.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                success = self.api_client.download_report(self.active_dataset['id'], file_path)
                if success:
                    self.status_bar.showMessage(f"Report saved: {file_path}")
                    QMessageBox.information(self, "Success", f"Report saved to:\n{file_path}")
                else:
                    self.status_bar.showMessage("Failed to download report")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to download report: {str(e)}")
    
    def _delete_dataset(self):
        """Delete the active dataset"""
        if not self.active_dataset:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{self.active_dataset.get('name', 'this dataset')}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.api_client.delete_dataset(self.active_dataset['id'])
                if success:
                    self.status_bar.showMessage("Dataset deleted")
                    self.active_dataset = None
                    self._clear_display()
                    self._load_datasets()
                else:
                    self.status_bar.showMessage("Failed to delete dataset")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete dataset: {str(e)}")


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("FOSSEE Scientific Analytics")
    app.setOrganizationName("FOSSEE IIT Bombay")
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
