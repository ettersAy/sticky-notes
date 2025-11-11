"""
Note list component for the dashboard.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, 
    QHBoxLayout, QPushButton, QLineEdit, QMenu, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QAction
from src.core.note import Note
from src.utils.constants import (
    NEW_NOTE_BUTTON_TEXT, DELETE_BUTTON_TEXT, NOTE_LIST_ITEM_HEIGHT,
    COPY_BUTTON_TEXT, COLOR_BUTTON_TEXT, FONT_SIZES
)


class NoteList(QWidget):
    """Note list component displaying all notes."""
    
    note_selected = pyqtSignal(str)  # note_id
    note_double_clicked = pyqtSignal(str)  # note_id
    new_note_requested = pyqtSignal()
    delete_note_requested = pyqtSignal(str)  # note_id
    copy_note_requested = pyqtSignal(str)  # note_id
    color_change_requested = pyqtSignal(str)  # note_id
    font_size_increase_requested = pyqtSignal(str)  # note_id
    font_size_decrease_requested = pyqtSignal(str)  # note_id
    
    def __init__(self, parent=None):
        """Initialize note list."""
        super().__init__(parent)
        self.current_notes = []
        self.selected_note_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Header with delete button only (new note button moved to category dropdown)
        header_layout = QHBoxLayout()
        # Notes list
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.on_note_selected)
        self.notes_list.itemDoubleClicked.connect(self.on_note_double_clicked)
        self.notes_list.setAlternatingRowColors(True)
        
        # No notes label
        self.no_notes_label = QLabel("No notes yet. Create your first note!")
        self.no_notes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_notes_label.setStyleSheet("color: gray; padding: 20px;")
        self.no_notes_label.setVisible(False)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.notes_list)
        layout.addWidget(self.no_notes_label)
        
        self.setLayout(layout)
    
    def update_notes(self, notes: list[Note]):
        """Update the note list with new notes."""
        self.current_notes = notes
        self.notes_list.clear()
        
        if not notes:
            self.no_notes_label.setVisible(True)
            self.notes_list.setVisible(False)
            self.delete_button.setEnabled(False)
            return
        
        self.no_notes_label.setVisible(False)
        self.notes_list.setVisible(True)
        
        for note in notes:
            item = QListWidgetItem()
            
            # Create custom widget for note item - single line with title and menu button
            widget = QWidget()
            widget_layout = QHBoxLayout()
            widget_layout.setContentsMargins(8, 5, 8, 5)
            widget_layout.setSpacing(5)
            
            # Color indicator
            color_indicator = QLabel("•")
            color_indicator.setStyleSheet(f"color: {note.color}; font-size: 16px;")
            color_indicator.setFixedWidth(15)
            
            # Title label
            title_label = QLabel(note.title)
            title_font = QFont()
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setStyleSheet("padding: 2px;")
            
            # Menu button
            menu_button = QPushButton("☰")
            menu_button.setFixedSize(20, 20)
            menu_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    color: #ccc;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: #f0f0f0;
                    border-radius: 3px;
                }
            """)
            menu_button.setToolTip("Note actions")
            menu_button.clicked.connect(lambda checked, nid=note.id: self.show_note_menu(nid))
            
            widget_layout.addWidget(color_indicator)
            widget_layout.addWidget(title_label)
            widget_layout.addStretch()
            widget_layout.addWidget(menu_button)
            
            widget.setLayout(widget_layout)
            widget.setStyleSheet("""
                QWidget {
                    border-bottom: 1px solid #eee;
                    padding: 2px;
                }
                QWidget:hover {
                    background-color: #f5f5f5;
                }
            """)
            
            item.setSizeHint(widget.sizeHint())
            item.setData(Qt.ItemDataRole.UserRole, note.id)
            self.notes_list.addItem(item)
            self.notes_list.setItemWidget(item, widget)
    
    def on_note_selected(self, item):
        """Handle note selection."""
        note_id = item.data(Qt.ItemDataRole.UserRole)
        self.selected_note_id = note_id
        self.note_selected.emit(note_id)
    
    def on_note_double_clicked(self, item):
        """Handle note double click."""
        note_id = item.data(Qt.ItemDataRole.UserRole)
        self.note_double_clicked.emit(note_id)
    
    def on_delete_clicked(self):
        """Handle delete button click."""
        if self.selected_note_id:
            self.delete_note_requested.emit(self.selected_note_id)
    
    def clear_selection(self):
        """Clear current selection."""
        self.notes_list.clearSelection()
        self.selected_note_id = None
    
    def select_note(self, note_id: str):
        """Select a specific note in the list."""
        for i in range(self.notes_list.count()):
            item = self.notes_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == note_id:
                self.notes_list.setCurrentItem(item)
                self.selected_note_id = note_id
                break
    
    def get_selected_note_id(self) -> str:
        """Get currently selected note ID."""
        return self.selected_note_id
    
    def get_note_count(self) -> int:
        """Get number of notes in the list."""
        return len(self.current_notes)
    
    def show_note_menu(self, note_id: str):
        """Show context menu for note actions."""
        menu = QMenu(self)
        
        # Copy action
        copy_action = QAction("📋 Copy", self)
        copy_action.triggered.connect(lambda: self.on_copy_requested(note_id))
        menu.addAction(copy_action)
        
        # Color change action
        color_action = QAction("🎨 Color", self)
        color_action.triggered.connect(lambda: self.on_color_change_requested(note_id))
        menu.addAction(color_action)
        
        # Font size increase action
        font_increase_action = QAction("🅰️⬆ Increase Font", self)
        font_increase_action.triggered.connect(lambda: self.on_font_size_increase_requested(note_id))
        menu.addAction(font_increase_action)
        
        # Font size decrease action
        font_decrease_action = QAction("🅰️⬇ Decrease Font", self)
        font_decrease_action.triggered.connect(lambda: self.on_font_size_decrease_requested(note_id))
        menu.addAction(font_decrease_action)
        
        # Delete action
        delete_action = QAction("🗑️ Delete", self)
        delete_action.triggered.connect(lambda: self.on_delete_requested(note_id))
        menu.addAction(delete_action)
        
        # Show menu at cursor position
        menu.exec(self.cursor().pos())
    
    def on_copy_requested(self, note_id: str):
        """Handle copy request."""
        self.copy_note_requested.emit(note_id)
    
    def on_color_change_requested(self, note_id: str):
        """Handle color change request."""
        self.color_change_requested.emit(note_id)
    
    def on_font_size_increase_requested(self, note_id: str):
        """Handle font size increase request."""
        self.font_size_increase_requested.emit(note_id)
    
    def on_font_size_decrease_requested(self, note_id: str):
        """Handle font size decrease request."""
        self.font_size_decrease_requested.emit(note_id)
    
    def on_delete_requested(self, note_id: str):
        """Handle delete request."""
        self.delete_note_requested.emit(note_id)
