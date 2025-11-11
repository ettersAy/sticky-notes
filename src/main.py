"""
Main entry point for the Sticky Notes application.
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add the parent directory to Python path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.dashboard import DashboardWindow
from src.utils.style_manager import StyleManager


def main():
    """Main application entry point."""
    # Create application instance
    app = QApplication(sys.argv)
    app.setApplicationName("Sticky Notes")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    dashboard = DashboardWindow()
    dashboard.show()
    
    # Set up application-wide styles
    setup_application_styles(app)
    
    # Start the event loop
    sys.exit(app.exec())


def setup_application_styles(app: QApplication):
    """Set up application-wide styles and settings."""
    # Initialize style manager and apply global styles
    style_manager = StyleManager()
    style_manager.apply_global_styles(app)
    
    # Set application-wide font
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)


if __name__ == "__main__":
    main()
