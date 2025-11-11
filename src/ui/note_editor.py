"""
Note editor component for viewing and editing note content.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout, 
    QPushButton, QColorDialog, QMessageBox, QApplication, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QTextCursor, QFont, QColor
from src.core.note import Note
from src.utils.constants import (
    COPY_BUTTON_TEXT, COLOR_BUTTON_TEXT, FONT_SIZES, DEFAULT_FONT_SIZE,
    COLOR_PALETTE
)
from src.utils.helpers import count_lines_and_chars


class NoteEditor(QWidget):
    """Note editor for viewing and editing note content."""
    
    content_changed = pyqtSignal(str, str)  # note_id, content
    appearance_changed = pyqtSignal(str, str, int)  # note_id, color, font_size
    title_changed = pyqtSignal(str, str)  # note_id, title
    
    def __init__(self, parent=None):
        """Initialize note editor."""
        super().__init__(parent)
        self.current_note = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Title and controls row
        title_controls_layout = QHBoxLayout()
        
        # Title input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Note title...")
        self.title_input.textChanged.connect(self.on_title_changed)
        
        # Font size decrease button
        self.font_decrease_button = QPushButton("🅰️⬇")
        self.font_decrease_button.setToolTip("Decrease font size")
        self.font_decrease_button.clicked.connect(self.decrease_font_size)
        self.font_decrease_button.setFixedSize(30, 30)
        
        # Font size increase button
        self.font_increase_button = QPushButton("🅰️⬆")
        self.font_increase_button.setToolTip("Increase font size")
        self.font_increase_button.clicked.connect(self.increase_font_size)
        self.font_increase_button.setFixedSize(30, 30)
        
        # Color button
        self.color_button = QPushButton(COLOR_BUTTON_TEXT)
        self.color_button.setToolTip("Change note color")
        self.color_button.clicked.connect(self.change_color)
        self.color_button.setFixedSize(30, 30)
        
        # Copy button
        self.copy_button = QPushButton(COPY_BUTTON_TEXT)
        self.copy_button.setToolTip("Copy note content")
        self.copy_button.clicked.connect(self.copy_content)
        self.copy_button.setFixedSize(30, 30)
        
        title_controls_layout.addWidget(self.title_input)
        title_controls_layout.addWidget(self.font_decrease_button)
        title_controls_layout.addWidget(self.font_increase_button)
        title_controls_layout.addWidget(self.color_button)
        title_controls_layout.addWidget(self.copy_button)
        
        # Text editor
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.text_edit.setPlaceholderText("Start typing your note...")
        
        # Info bar
        self.info_label = QLabel("Characters: 0 | Lines: 0")
        self.info_label.setStyleSheet("color: gray; font-size: 10px;")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(title_controls_layout)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
        
        # Set initial state
        self.set_note(None)
    
    def set_note(self, note: Note):
        """Set the current note to edit."""
        self.current_note = note
        
        if note:
            # Block signals to prevent recursive updates
            self.title_input.blockSignals(True)
            self.title_input.setText(note.title)
            self.title_input.blockSignals(False)
            
            self.text_edit.blockSignals(True)
            self.text_edit.setPlainText(note.content)
            self.text_edit.blockSignals(False)
            
            # Update text edit font
            font = QFont()
            font.setPointSize(note.font_size)
            self.text_edit.setFont(font)
            
            self.update_info()
            self.setEnabled(True)
        else:
            self.title_input.clear()
            self.text_edit.clear()
            self.info_label.setText("Characters: 0 | Lines: 0")
            self.setEnabled(False)
    
    def on_title_changed(self, title: str):
        """Handle title changes."""
        if not self.current_note:
            return
        
        self.current_note.update_title(title)
        
        # Emit signal for data persistence
        self.title_changed.emit(self.current_note.id, title)
    
    def on_text_changed(self):
        """Handle text changes."""
        if not self.current_note:
            return
        
        content = self.text_edit.toPlainText()
        self.current_note.update_content(content)
        self.update_info()
        
        # Emit signal for data persistence
        self.content_changed.emit(self.current_note.id, content)
    
    def decrease_font_size(self):
        """Decrease font size."""
        if not self.current_note:
            return
        
        current_size = self.current_note.font_size
        # Find next smaller font size
        smaller_sizes = [size for size in FONT_SIZES if size < current_size]
        if smaller_sizes:
            new_size = max(smaller_sizes)
            self.current_note.update_appearance(font_size=new_size)
            
            # Update text edit font
            font = QFont()
            font.setPointSize(new_size)
            self.text_edit.setFont(font)
            
            # Emit signal
            self.appearance_changed.emit(
                self.current_note.id, 
                self.current_note.color, 
                new_size
            )
    
    def increase_font_size(self):
        """Increase font size."""
        if not self.current_note:
            return
        
        current_size = self.current_note.font_size
        # Find next larger font size
        larger_sizes = [size for size in FONT_SIZES if size > current_size]
        if larger_sizes:
            new_size = min(larger_sizes)
            self.current_note.update_appearance(font_size=new_size)
            
            # Update text edit font
            font = QFont()
            font.setPointSize(new_size)
            self.text_edit.setFont(font)
            
            # Emit signal
            self.appearance_changed.emit(
                self.current_note.id, 
                self.current_note.color, 
                new_size
            )
    
    def copy_content(self):
        """Copy note content to clipboard."""
        if self.current_note and self.current_note.content:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_note.content)
            
            # Show tooltip confirmation
            self.copy_button.setToolTip("✓ Copied!")
            QTimer.singleShot(5000, lambda: self.copy_button.setToolTip("Copy note content"))
    
    def change_color(self):
        """Change note background color."""
        if not self.current_note:
            return
        
        # Create color dialog
        color_dialog = QColorDialog()
        color_dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, False)
        color_dialog.setCurrentColor(QColor(self.current_note.color))
        
        # Add custom color palette
        for color in COLOR_PALETTE:
            color_dialog.setCustomColor(COLOR_PALETTE.index(color), QColor(color))
        
        if color_dialog.exec() == QColorDialog.DialogCode.Accepted:
            new_color = color_dialog.selectedColor().name()
            self.current_note.update_appearance(color=new_color)
            
            # Emit signal
            self.appearance_changed.emit(
                self.current_note.id, 
                new_color, 
                self.current_note.font_size
            )
    
    def update_info(self):
        """Update character and line count."""
        if not self.current_note:
            return
        
        content = self.current_note.content
        line_count, char_count = count_lines_and_chars(content)
        self.info_label.setText(f"Characters: {char_count} | Lines: {line_count}")
    
    def get_content(self) -> str:
        """Get current editor content."""
        return self.text_edit.toPlainText()
    
    def set_content(self, content: str):
        """Set editor content."""
        self.text_edit.setPlainText(content)
    
    def clear(self):
        """Clear the editor."""
        self.text_edit.clear()
        self.set_note(None)
    
    def set_font_size(self, size: int):
        """Set font size."""
        if size in FONT_SIZES:
            # Update text edit font
            font = QFont()
            font.setPointSize(size)
            self.text_edit.setFont(font)
    
    def set_background_color(self, color: str):
        """Set background color (for preview purposes)."""
        self.text_edit.setStyleSheet(f"background-color: {color};")
    
    def focus_editor(self):
        """Focus the text editor."""
        self.text_edit.setFocus()
