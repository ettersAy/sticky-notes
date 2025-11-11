"""
Refactored individual sticky note window component.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QColorDialog, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QSize, QTimer
from PyQt6.QtGui import QMouseEvent, QColor
from src.core.note import Note
from src.core.data_manager import DataManager
from src.utils.constants import (
    COPY_BUTTON_TEXT, COLOR_PALETTE,
    STICKY_NOTE_MIN_SIZE, STICKY_NOTE_MAX_SIZE
)
from src.ui.components.sticky_note_title_bar import StickyNoteTitleBar
from src.ui.components.sticky_note_content_area import StickyNoteContentArea
from src.ui.components.sticky_note_info_bar import StickyNoteInfoBar


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
        
        # Title bar
        self.title_bar = StickyNoteTitleBar(
            self.note.id,
            self.note.title,
            self.note.font_size
        )
        self.title_bar.copy_requested.connect(self.copy_content)
        self.title_bar.color_change_requested.connect(self.change_color)
        self.title_bar.font_size_changed.connect(self.on_font_size_changed)
        self.title_bar.close_requested.connect(self.close)
        self.title_bar.title_changed.connect(self.on_title_changed)
        layout.addWidget(self.title_bar)
        
        # Content area
        self.content_area = StickyNoteContentArea()
        self.content_area.content_changed.connect(self.on_text_changed)
        layout.addWidget(self.content_area)
        
        # Info bar
        self.info_bar = StickyNoteInfoBar()
        layout.addWidget(self.info_bar)
        
        self.setLayout(layout)
        
        # Set initial appearance
        self.update_appearance(self.note.color, self.note.font_size)
    
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
    
    def update_content_display(self):
        """Update the content display with current note content."""
        self.content_area.set_content(self.note.content)
        self.info_bar.update_info(self.note.content)
        self.title_bar.update_title(self.note.title)
    
    def on_title_changed(self, title: str):
        """Handle title changes."""
        self.note.update_title(title)
        
        # Save to data manager
        self.data_manager.update_note_title(self.note.id, title)
    
    def on_text_changed(self, content: str):
        """Handle text changes."""
        self.note.update_content(content)
        
        # Update UI components
        self.info_bar.update_info(content)
        self.title_bar.update_title(self.note.title)
        
        # Save to data manager
        self.data_manager.update_note_content(self.note.id, content)
        
        # Emit signal for dashboard synchronization
        self.note_content_changed.emit(self.note.id, content)
    
    def on_font_size_changed(self, font_size: int):
        """Handle font size changes."""
        self.note.update_appearance(font_size=font_size)
        self.update_appearance(self.note.color, font_size)
        
        # Save to data manager
        self.data_manager.update_note_appearance(self.note.id, font_size=font_size)
    
    def update_appearance(self, color: str, font_size: int):
        """Update note appearance."""
        # Set background color
        self.setStyleSheet(f"background-color: {color};")
        
        # Set font size
        self.content_area.set_font_size(font_size)
    
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
            self.title_bar.update_copy_button_text("✓")
            QApplication.processEvents()
            
            # Reset after delay
            QTimer.singleShot(1000, lambda: self.title_bar.update_copy_button_text(COPY_BUTTON_TEXT))
    
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
            self.data_manager.update_note_appearance(self.note.id, color=new_color)
    
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
