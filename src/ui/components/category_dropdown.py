"""
Category dropdown menu component for the dashboard.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMenu, QHBoxLayout, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from src.core.template import TemplateManager
from src.utils.constants import TEMPLATES, SEARCH_PLACEHOLDER


class CategoryDropdown(QWidget):
    """Dropdown menu for note categories/templates."""
    
    template_selected = pyqtSignal(str)  # template_id
    search_changed = pyqtSignal(str)  # search_query
    
    def __init__(self, parent=None):
        """Initialize category dropdown."""
        super().__init__(parent)
        self.template_manager = TemplateManager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Search field
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText(SEARCH_PLACEHOLDER)
        self.search_field.textChanged.connect(self.on_search_text_changed)
        layout.addWidget(self.search_field)
        
        # New note button
        self.new_note_button = QPushButton("➕")
        self.new_note_button.setFixedSize(30, 30)
        self.new_note_button.setToolTip("Create new note")
        layout.addWidget(self.new_note_button)
        
        # Dropdown button
        self.dropdown_button = QPushButton("▼")
        self.dropdown_button.setFixedSize(30, 30)
        self.dropdown_button.setToolTip("Show categories")
        self.dropdown_button.clicked.connect(self.show_dropdown_menu)
        layout.addWidget(self.dropdown_button)
        
        self.setLayout(layout)
    
    def show_dropdown_menu(self):
        """Show the dropdown menu with categories."""
        menu = QMenu(self)
        
        # Add template actions with emoji icons
        templates = self.template_manager.get_all_templates()
        
        # Map template IDs to emoji icons
        emoji_map = {
            "todo": "📝",
            "meeting": "📅", 
            "code": "💻",
            "shopping": "🛒",
            "ideas": "💡"
        }
        
        for template_id, template in templates.items():
            emoji = emoji_map.get(template_id, "📄")
            action = QAction(f"{emoji} {template.name}", self)
            action.triggered.connect(
                lambda checked, tid=template_id: self.on_template_selected(tid)
            )
            menu.addAction(action)
        
        # Show menu below the dropdown button
        menu.exec(self.dropdown_button.mapToGlobal(
            self.dropdown_button.rect().bottomLeft()
        ))
    
    def on_template_selected(self, template_id: str):
        """Handle template selection from dropdown."""
        self.template_selected.emit(template_id)
    
    def on_search_text_changed(self, text):
        """Handle search text changes."""
        self.search_changed.emit(text.strip())
    
    def get_search_query(self) -> str:
        """Get current search query."""
        return self.search_field.text().strip()
    
    def set_search_query(self, query: str):
        """Set search query."""
        self.search_field.setText(query)
    
    def clear_search(self):
        """Clear search field."""
        self.search_field.clear()
    
    def connect_new_note_signal(self, callback):
        """Connect the new note button to a callback."""
        self.new_note_button.clicked.connect(callback)
