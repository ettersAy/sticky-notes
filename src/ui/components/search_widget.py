"""
Search widget component for the dashboard.
"""
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QListWidget, 
    QListWidgetItem, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from src.core.note import Note
from src.utils.constants import SEARCH_PLACEHOLDER, SEARCH_BUTTON_TEXT, MAX_SEARCH_RESULTS


class SearchWidget(QWidget):
    """Search widget with search field and results list."""
    
    note_selected = pyqtSignal(str)  # note_id
    search_toggled = pyqtSignal(bool)  # is_visible
    
    def __init__(self, parent=None):
        """Initialize search widget."""
        super().__init__(parent)
        self.is_visible = False
        self.current_results = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Search field and toggle button
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText(SEARCH_PLACEHOLDER)
        self.search_field.textChanged.connect(self.on_search_text_changed)
        self.search_field.setVisible(False)
        
        self.toggle_button = QPushButton(SEARCH_BUTTON_TEXT)
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.clicked.connect(self.toggle_search)
        
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.toggle_button)
        
        # Results list
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_result_selected)
        self.results_list.setVisible(False)
        
        # No results label
        self.no_results_label = QLabel("No matching notes found")
        self.no_results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_results_label.setVisible(False)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.results_list)
        layout.addWidget(self.no_results_label)
        
        self.setLayout(layout)
    
    def toggle_search(self):
        """Toggle search field visibility."""
        self.is_visible = not self.is_visible
        self.search_field.setVisible(self.is_visible)
        self.results_list.setVisible(self.is_visible and bool(self.current_results))
        self.no_results_label.setVisible(self.is_visible and not self.current_results)
        
        if self.is_visible:
            self.search_field.setFocus()
        else:
            self.search_field.clear()
            self.clear_results()
        
        self.search_toggled.emit(self.is_visible)
    
    def on_search_text_changed(self, text):
        """Handle search text changes."""
        if not text.strip():
            self.clear_results()
            return
        
        # Emit signal to parent to perform search
        # Parent will call update_results with the results
        pass
    
    def update_results(self, notes: list[Note]):
        """Update search results display."""
        self.current_results = notes
        self.results_list.clear()
        
        if not notes:
            self.no_results_label.setVisible(True)
            self.results_list.setVisible(False)
            return
        
        self.no_results_label.setVisible(False)
        self.results_list.setVisible(True)
        
        for note in notes[:MAX_SEARCH_RESULTS]:
            item = QListWidgetItem()
            
            # Create custom widget for note preview
            widget = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(5, 2, 5, 2)
            
            title_label = QLabel(note.title)
            title_font = QFont()
            title_font.setBold(True)
            title_label.setFont(title_font)
            
            preview_label = QLabel(note.get_preview())
            preview_label.setStyleSheet("color: gray;")
            
            layout.addWidget(title_label)
            layout.addWidget(preview_label)
            widget.setLayout(layout)
            
            item.setSizeHint(widget.sizeHint())
            item.setData(Qt.ItemDataRole.UserRole, note.id)
            self.results_list.addItem(item)
            self.results_list.setItemWidget(item, widget)
    
    def clear_results(self):
        """Clear search results."""
        self.current_results = []
        self.results_list.clear()
        self.results_list.setVisible(False)
        self.no_results_label.setVisible(False)
    
    def on_result_selected(self, item):
        """Handle result selection."""
        note_id = item.data(Qt.ItemDataRole.UserRole)
        self.note_selected.emit(note_id)
        self.toggle_search()  # Hide search after selection
    
    def get_search_query(self) -> str:
        """Get current search query."""
        return self.search_field.text().strip()
    
    def set_search_query(self, query: str):
        """Set search query."""
        self.search_field.setText(query)
    
    def show_search(self):
        """Show search field."""
        if not self.is_visible:
            self.toggle_search()
    
    def hide_search(self):
        """Hide search field."""
        if self.is_visible:
            self.toggle_search()
