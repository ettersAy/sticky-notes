"""
Title bar component for sticky notes.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit
from PyQt6.QtCore import pyqtSignal
from src.utils.constants import COPY_BUTTON_TEXT, COLOR_BUTTON_TEXT, CLOSE_BUTTON_TEXT, FONT_SIZES


class StickyNoteTitleBar(QWidget):
    """Title bar component for sticky notes with controls."""
    
    copy_requested = pyqtSignal()
    color_change_requested = pyqtSignal()
    font_size_changed = pyqtSignal(int)
    close_requested = pyqtSignal()
    title_changed = pyqtSignal(str)  # title
    
    def __init__(self, note_id: str, title: str, font_size: int):
        """Initialize title bar."""
        super().__init__()
        self.note_id = note_id
        self.title = title
        self.font_size = font_size
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setFixedHeight(30)
        self.setObjectName("sticky-note-title-bar")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)
        
        # Title input field
        self.title_input = QLineEdit(self.title)
        self.title_input.setPlaceholderText("Note title...")
        self.title_input.textChanged.connect(self.on_title_changed)
        self.title_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 5px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        
        # Control buttons
        self.copy_button = QPushButton(COPY_BUTTON_TEXT)
        self.copy_button.setFixedSize(25, 25)
        self.copy_button.setToolTip("Copy note content")
        self.copy_button.setObjectName("sticky-note-control-button")
        self.copy_button.clicked.connect(self.copy_requested.emit)
        
        self.color_button = QPushButton(COLOR_BUTTON_TEXT)
        self.color_button.setFixedSize(25, 25)
        self.color_button.setToolTip("Change note color")
        self.color_button.setObjectName("sticky-note-control-button")
        self.color_button.clicked.connect(self.color_change_requested.emit)
        
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems([str(size) for size in FONT_SIZES])
        self.font_size_combo.setCurrentText(str(self.font_size))
        self.font_size_combo.currentTextChanged.connect(self.on_font_size_changed)
        self.font_size_combo.setFixedWidth(40)
        self.font_size_combo.setToolTip("Font size")
        
        self.close_button = QPushButton(CLOSE_BUTTON_TEXT)
        self.close_button.setFixedSize(25, 25)
        self.close_button.setToolTip("Close note")
        self.close_button.setObjectName("sticky-note-control-button")
        self.close_button.clicked.connect(self.close_requested.emit)
        
        layout.addWidget(self.title_input)
        layout.addStretch()
        layout.addWidget(self.copy_button)
        layout.addWidget(self.color_button)
        layout.addWidget(self.font_size_combo)
        layout.addWidget(self.close_button)
        
        self.setLayout(layout)
    
    def get_window_title(self) -> str:
        """Get window title with note title."""
        return self.title
    
    def on_title_changed(self, title: str):
        """Handle title changes."""
        self.title = title
        self.title_changed.emit(title)
    
    def on_font_size_changed(self, size_str: str):
        """Handle font size changes."""
        try:
            font_size = int(size_str)
            self.font_size_changed.emit(font_size)
        except ValueError:
            pass
    
    def update_title(self, title: str):
        """Update window title."""
        self.title = title
        self.title_input.blockSignals(True)
        self.title_input.setText(title)
        self.title_input.blockSignals(False)
    
    def update_copy_button_text(self, text: str):
        """Update copy button text (for confirmation)."""
        self.copy_button.setText(text)
