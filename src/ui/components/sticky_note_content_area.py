"""
Content area component for sticky notes.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTextEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class StickyNoteContentArea(QWidget):
    """Content area component for sticky notes with line numbers."""
    
    content_changed = pyqtSignal(str)
    
    def __init__(self):
        """Initialize content area."""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setObjectName("sticky-note-content")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Line numbers
        self.line_numbers = QTextEdit()
        self.line_numbers.setReadOnly(True)
        self.line_numbers.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.line_numbers.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.line_numbers.setFixedWidth(40)
        self.line_numbers.setObjectName("sticky-note-line-numbers")
        
        # Text editor
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        layout.addWidget(self.line_numbers)
        layout.addWidget(self.text_edit)
        
        self.setLayout(layout)
    
    def on_text_changed(self):
        """Handle text changes."""
        content = self.text_edit.toPlainText()
        self.content_changed.emit(content)
    
    def set_content(self, content: str):
        """Set content in the text editor."""
        self.text_edit.blockSignals(True)
        self.text_edit.setPlainText(content)
        self.text_edit.blockSignals(False)
        self.update_line_numbers(content)
    
    def get_content(self) -> str:
        """Get content from the text editor."""
        return self.text_edit.toPlainText()
    
    def update_line_numbers(self, content: str):
        """Update line numbers display."""
        lines = content.split('\n')
        line_count = len(lines)
        
        line_numbers_text = '\n'.join(str(i + 1) for i in range(line_count))
        
        self.line_numbers.blockSignals(True)
        self.line_numbers.setPlainText(line_numbers_text)
        self.line_numbers.blockSignals(False)
    
    def sync_scroll_positions(self):
        """Sync scroll positions between text editor and line numbers."""
        v_scroll = self.text_edit.verticalScrollBar()
        self.line_numbers.verticalScrollBar().setValue(v_scroll.value())
    
    def set_font_size(self, font_size: int):
        """Set font size for both text editor and line numbers."""
        font = QFont()
        font.setPointSize(font_size)
        self.text_edit.setFont(font)
        self.line_numbers.setFont(font)
    
    def focus_editor(self):
        """Focus the text editor."""
        self.text_edit.setFocus()
