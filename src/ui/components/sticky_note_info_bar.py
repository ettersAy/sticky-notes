"""
Info bar component for sticky notes.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from src.utils.helpers import count_lines_and_chars


class StickyNoteInfoBar(QWidget):
    """Info bar component for sticky notes with statistics."""
    
    def __init__(self):
        """Initialize info bar."""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setFixedHeight(20)
        self.setObjectName("sticky-note-info-bar")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        
        self.info_label = QLabel("Characters: 0 | Lines: 0")
        
        layout.addWidget(self.info_label)
        self.setLayout(layout)
    
    def update_info(self, content: str):
        """Update character and line count."""
        line_count, char_count = count_lines_and_chars(content)
        self.info_label.setText(f"Characters: {char_count} | Lines: {line_count}")
