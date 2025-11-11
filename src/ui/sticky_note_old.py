"""
Individual sticky note window component.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QComboBox,
    QPushButton, QColorDialog, QMessageBox, QFrame, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QSize
from PyQt6.QtGui import QFont, QColor, QMouseEvent, QTextCursor
from src.core.note import Note
from src.core.data_manager import DataManager
from src.utils.constants import (
    COPY_BUTTON_TEXT, COLOR_BUTTON_TEXT, CLOSE_BUTTON_TEXT,
    FONT_SIZES, DEFAULT_FONT_SIZE, COLOR_PALETTE,
    STICKY_NOTE_MIN_SIZE, STICKY_NOTE_MAX_SIZE
)
from src.utils.helpers import count_lines_and_chars


class StickyNoteWindow(QWidget):
    """Individual sticky note window with frameless design."""
    
    note_closed = pyqtSignal(str)  # note_id
    note_content_changed = pyqtSignal(str, str)  # note_id, content
    
    def __init__(self, note: Note, data_manager: DataManager):
        """Initialize sticky note window."""
        super().__init__()
        self.note = note
        self.data_manager = data_manager
        self.dragging = False
        self.drag_position = QPoint()
        self.resizing = False
        self.resize_position = QPoint()
        
        self.init_ui()
        self.setup_window_properties()
        self.update_content_display()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title bar (draggable area)
        self.title_bar = self.create_title_bar()
        layout.addWidget(self.title_bar)
        
        # Content area
        self.content_area = self.create_content_area()
        layout.addWidget(self.content_area)
        
        # Info bar
        self.info_bar = self.create_info_bar()
        layout.addWidget(self.info_bar)
        
        self.setLayout(layout)
        
        # Set initial appearance
        self.update_appearance(self.note.color, self.note.font_size)
    
    def create_title_bar(self) -> QWidget:
        """Create the draggable title bar."""
        title_bar = QWidget()
        title_bar.setFixedHeight(30)
        title_bar.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border-bottom: 1px solid #ccc;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)
        
        # Title label
        self.title_label = QLabel(self.get_window_title())
        self.title_label.setStyleSheet("font-weight: bold;")
        
        # Control buttons
        self.copy_button = QPushButton(COPY_BUTTON_TEXT)
        self.copy_button.setFixedSize(25, 25)
        self.copy_button.setToolTip("Copy note content")
        self.copy_button.clicked.connect(self.copy_content)
        
        self.color_button = QPushButton(COLOR_BUTTON_TEXT)
        self.color_button.setFixedSize(25, 25)
        self.color_button.setToolTip("Change note color")
        self.color_button.clicked.connect(self.change_color)
        
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems([str(size) for size in FONT_SIZES])
        self.font_size_combo.setCurrentText(str(self.note.font_size))
        self.font_size_combo.currentTextChanged.connect(self.on_font_size_changed)
        self.font_size_combo.setFixedWidth(40)
        self.font_size_combo.setToolTip("Font size")
        
        self.close_button = QPushButton(CLOSE_BUTTON_TEXT)
        self.close_button.setFixedSize(25, 25)
        self.close_button.setToolTip("Close note")
        self.close_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.copy_button)
        layout.addWidget(self.color_button)
        layout.addWidget(self.font_size_combo)
        layout.addWidget(self.close_button)
        
        title_bar.setLayout(layout)
        return title_bar
    
    def create_content_area(self) -> QWidget:
        """Create the content area with line numbers."""
        content_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Line numbers
        self.line_numbers = QTextEdit()
        self.line_numbers.setReadOnly(True)
        self.line_numbers.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.line_numbers.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.line_numbers.setFixedWidth(40)
        self.line_numbers.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8;
                border: none;
                border-right: 1px solid #ddd;
                color: #666;
                font-family: monospace;
            }
        """)
        
        # Text editor
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        layout.addWidget(self.line_numbers)
        layout.addWidget(self.text_edit)
        
        content_widget.setLayout(layout)
        return content_widget
    
    def create_info_bar(self) -> QWidget:
        """Create the info bar with statistics."""
        info_bar = QWidget()
        info_bar.setFixedHeight(20)
        info_bar.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border-top: 1px solid #ccc;
                font-size: 10px;
                color: #666;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        
        self.info_label = QLabel("Characters: 0 | Lines: 0")
        
        layout.addWidget(self.info_label)
        info_bar.setLayout(layout)
        return info_bar
    
    def setup_window_properties(self):
        """Set up window properties for frameless design."""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        # Set initial position and size
        self.move(self.note.x, self.note.y)
        self.resize(self.note.w, self.note.h)
        
        # Set minimum and maximum size
        self.setMinimumSize(*STICKY_NOTE_MIN_SIZE)
        self.setMaximumSize(*STICKY_NOTE_MAX_SIZE)
    
    def get_window_title(self) -> str:
        """Get window title with note preview."""
        preview = self.note.get_preview(20)
        return f"{self.note.id}: {preview}"
    
    def update_content_display(self):
        """Update the content display with current note content."""
        # Block signals to prevent recursive updates
        self.text_edit.blockSignals(True)
        self.text_edit.setPlainText(self.note.content)
        self.text_edit.blockSignals(False)
        
        self.update_line_numbers()
        self.update_info()
        self.update_title()
    
    def update_line_numbers(self):
        """Update line numbers display."""
        content = self.note.content
        lines = content.split('\n')
        line_count = len(lines)
        
        line_numbers_text = '\n'.join(str(i + 1) for i in range(line_count))
        
        self.line_numbers.blockSignals(True)
        self.line_numbers.setPlainText(line_numbers_text)
        self.line_numbers.blockSignals(False)
        
        # Sync scroll positions
        v_scroll = self.text_edit.verticalScrollBar()
        self.line_numbers.verticalScrollBar().setValue(v_scroll.value())
    
    def update_info(self):
        """Update character and line count."""
        line_count, char_count = count_lines_and_chars(self.note.content)
        self.info_label.setText(f"Characters: {char_count} | Lines: {line_count}")
    
    def update_title(self):
        """Update window title."""
        self.title_label.setText(self.get_window_title())
    
    def on_text_changed(self):
        """Handle text changes."""
        content = self.text_edit.toPlainText()
        self.note.update_content(content)
        
        self.update_line_numbers()
        self.update_info()
        self.update_title()
        
        # Save to data manager
        self.data_manager.update_note_content(self.note.id, content)
        
        # Emit signal for dashboard synchronization
        self.note_content_changed.emit(self.note.id, content)
    
    def on_font_size_changed(self, size_str: str):
        """Handle font size changes."""
        try:
            font_size = int(size_str)
            self.note.update_appearance(font_size=font_size)
            self.update_appearance(self.note.color, font_size)
            
            # Save to data manager
            self.data_manager.update_note_appearance(
                self.note.id, 
                font_size=font_size
            )
        except ValueError:
            pass
    
    def update_appearance(self, color: str, font_size: int):
        """Update note appearance."""
        # Set background color
        self.setStyleSheet(f"background-color: {color};")
        
        # Set font size
        font = QFont()
        font.setPointSize(font_size)
        self.text_edit.setFont(font)
        self.line_numbers.setFont(font)
    
    def update_content(self, content: str):
        """Update content from external source."""
        self.note.update_content(content)
        self.update_content_display()
    
    def copy_content(self):
        """Copy note content to clipboard."""
        if self.note.content:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.note.content)
            
            # Show brief confirmation
            original_text = self.copy_button.text()
            self.copy_button.setText("✓")
            QApplication.processEvents()
            
            # Reset after delay
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(1000, lambda: self.copy_button.setText(COPY_BUTTON_TEXT))
    
    def change_color(self):
        """Change note background color."""
        color_dialog = QColorDialog()
        color_dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, False)
        color_dialog.setCurrentColor(QColor(self.note.color))
        
        # Add custom color palette
        for color in COLOR_PALETTE:
            color_dialog.setCustomColor(COLOR_PALETTE.index(color), QColor(color))
        
        if color_dialog.exec() == QColorDialog.DialogCode.Accepted:
            new_color = color_dialog.selectedColor().name()
            self.note.update_appearance(color=new_color)
            self.update_appearance(new_color, self.note.font_size)
            
            # Save to data manager
            self.data_manager.update_note_appearance(
                self.note.id, 
                color=new_color
            )
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for dragging and resizing."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if click is in resize area (bottom-right corner)
            if (event.pos().x() > self.width() - 10 and 
                event.pos().y() > self.height() - 10):
                self.resizing = True
                self.resize_position = event.globalPosition().toPoint()
            else:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for dragging and resizing."""
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
        elif self.resizing:
            delta = event.globalPosition().toPoint() - self.resize_position
            new_size = QSize(self.width() + delta.x(), self.height() + delta.y())
            
            # Apply constraints
            new_size = new_size.boundedTo(self.maximumSize())
            new_size = new_size.expandedTo(self.minimumSize())
            
            self.resize(new_size)
            self.resize_position = event.globalPosition().toPoint()
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release."""
        self.dragging = False
        self.resizing = False
        
        # Save position and size
        if event.button() == Qt.MouseButton.LeftButton:
            self.data_manager.update_note_position(self.note.id, self.x(), self.y())
            self.data_manager.update_note_size(self.note.id, self.width(), self.height())
        
        super().mouseReleaseEvent(event)
    
    def closeEvent(self, event):
        """Handle window closure."""
        self.note_closed.emit(self.note.id)
        super().closeEvent(event)
