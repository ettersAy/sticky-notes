"""
Main dashboard window for the Sticky Notes application.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
    QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent
from src.core.data_manager import DataManager
from src.core.template import TemplateManager
from src.utils.constants import APP_TITLE, DASHBOARD_WINDOW_SIZE
from src.ui.components.note_list import NoteList
from src.ui.components.category_dropdown import CategoryDropdown
from src.ui.note_editor import NoteEditor
from src.ui.sticky_note import StickyNoteWindow


class DashboardWindow(QMainWindow):
    """Main dashboard window for managing sticky notes."""
    
    def __init__(self):
        """Initialize dashboard window."""
        super().__init__()
        self.data_manager = DataManager()
        self.template_manager = TemplateManager()
        self.open_note_windows = {}  # note_id -> StickyNoteWindow
        self.current_note_id = None
        
        self.init_ui()
        self.connect_signals()
        self.refresh_notes()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, *DASHBOARD_WINDOW_SIZE)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel
        left_panel = self.create_left_panel()
        
        # Right panel
        right_panel = self.create_right_panel()
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (30% left, 70% right)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
    
    def create_left_panel(self) -> QWidget:
        """Create the left panel with category dropdown and note list."""
        left_panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Category dropdown with search and new note button
        self.category_dropdown = CategoryDropdown()
        layout.addWidget(self.category_dropdown)
        
        # Note list
        self.note_list = NoteList()
        layout.addWidget(self.note_list)
        
        left_panel.setLayout(layout)
        return left_panel
    
    def create_right_panel(self) -> QWidget:
        """Create the right panel with note editor."""
        right_panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Note editor
        self.note_editor = NoteEditor()
        layout.addWidget(self.note_editor)
        
        right_panel.setLayout(layout)
        return right_panel
    
    def connect_signals(self):
        """Connect all signals and slots."""
        # Note list signals
        self.note_list.note_selected.connect(self.on_note_selected)
        self.note_list.note_double_clicked.connect(self.open_note_window)
        self.note_list.delete_note_requested.connect(self.delete_note)
        self.note_list.copy_note_requested.connect(self.on_copy_note_requested)
        self.note_list.color_change_requested.connect(self.on_color_change_requested)
        self.note_list.font_size_increase_requested.connect(self.on_font_size_increase_requested)
        self.note_list.font_size_decrease_requested.connect(self.on_font_size_decrease_requested)
        
        # Category dropdown signals
        self.category_dropdown.template_selected.connect(self.create_note_from_template)
        self.category_dropdown.search_changed.connect(self.on_search_changed)
        self.category_dropdown.connect_new_note_signal(self.create_new_note)
        
        # Note editor signals
        self.note_editor.content_changed.connect(self.on_note_content_changed)
        self.note_editor.appearance_changed.connect(self.on_note_appearance_changed)
        self.note_editor.title_changed.connect(self.on_note_title_changed)
    
    def refresh_notes(self):
        """Refresh the note list with current data."""
        notes = self.data_manager.get_all_notes()
        self.note_list.update_notes(notes)
        
        # Handle real-time search
        query = self.category_dropdown.get_search_query()
        if query:
            search_results = self.data_manager.search_notes(query)
            self.note_list.update_notes(search_results)
    
    def on_note_selected(self, note_id: str):
        """Handle note selection from list or search."""
        note = self.data_manager.get_note(note_id)
        if note:
            self.current_note_id = note_id
            self.note_editor.set_note(note)
            self.note_list.select_note(note_id)
    
    def create_new_note(self):
        """Create a new blank note."""
        note = self.data_manager.create_new_note()
        self.refresh_notes()
        self.on_note_selected(note.id)
        self.note_editor.focus_editor()
    
    def create_note_from_template(self, template_id: str):
        """Create a new note from a template."""
        note = self.template_manager.create_note_from_template(template_id)
        self.data_manager.save_note(note)
        self.refresh_notes()
        self.on_note_selected(note.id)
        self.note_editor.focus_editor()
    
    def delete_note(self, note_id: str):
        """Delete the selected note."""
        if not note_id:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this note?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Close associated note window if open
            if note_id in self.open_note_windows:
                self.open_note_windows[note_id].close()
                del self.open_note_windows[note_id]
            
            # Delete from data manager
            self.data_manager.delete_note(note_id)
            
            # Clear editor if deleted note was current
            if self.current_note_id == note_id:
                self.current_note_id = None
                self.note_editor.set_note(None)
            
            self.refresh_notes()
    
    def open_note_window(self, note_id: str):
        """Open a note in a separate sticky note window."""
        note = self.data_manager.get_note(note_id)
        if not note:
            return
        
        # Create new window or focus existing one
        if note_id in self.open_note_windows:
            self.open_note_windows[note_id].raise_()
            self.open_note_windows[note_id].activateWindow()
        else:
            note_window = StickyNoteWindow(note, self.data_manager)
            note_window.note_closed.connect(
                lambda nid: self.on_note_window_closed(nid)
            )
            note_window.note_content_changed.connect(
                lambda nid, content: self.on_external_note_changed(nid, content)
            )
            note_window.show()
            self.open_note_windows[note_id] = note_window
    
    def on_note_window_closed(self, note_id: str):
        """Handle note window closure."""
        if note_id in self.open_note_windows:
            del self.open_note_windows[note_id]
    
    def on_external_note_changed(self, note_id: str, content: str):
        """Handle note changes from external windows."""
        # Update data manager
        self.data_manager.update_note_content(note_id, content)
        
        # Refresh UI if this note is currently selected
        if self.current_note_id == note_id:
            note = self.data_manager.get_note(note_id)
            if note:
                self.note_editor.set_note(note)
        
        self.refresh_notes()
    
    def on_note_content_changed(self, note_id: str, content: str):
        """Handle note content changes from editor."""
        self.data_manager.update_note_content(note_id, content)
        self.refresh_notes()
        
        # Update open note windows
        if note_id in self.open_note_windows:
            self.open_note_windows[note_id].update_content(content)
    
    def on_note_title_changed(self, note_id: str, title: str):
        """Handle note title changes."""
        self.data_manager.update_note_title(note_id, title)
        self.refresh_notes()
        
        # Update open note windows
        if note_id in self.open_note_windows:
            self.open_note_windows[note_id].update_title(title)
    
    def on_note_appearance_changed(self, note_id: str, color: str, font_size: int):
        """Handle note appearance changes."""
        self.data_manager.update_note_appearance(note_id, color, font_size)
        
        # Update open note windows
        if note_id in self.open_note_windows:
            self.open_note_windows[note_id].update_appearance(color, font_size)
    
    def on_copy_note_requested(self, note_id: str):
        """Handle copy note request from context menu."""
        note = self.data_manager.get_note(note_id)
        if note and note.content:
            clipboard = QApplication.clipboard()
            clipboard.setText(note.content)
    
    def on_color_change_requested(self, note_id: str):
        """Handle color change request from context menu."""
        note = self.data_manager.get_note(note_id)
        if not note:
            return
        
        # Create color dialog
        from PyQt6.QtWidgets import QColorDialog
        from PyQt6.QtGui import QColor
        from src.utils.constants import COLOR_PALETTE
        
        color_dialog = QColorDialog()
        color_dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, False)
        color_dialog.setCurrentColor(QColor(note.color))
        
        # Add custom color palette
        for color in COLOR_PALETTE:
            color_dialog.setCustomColor(COLOR_PALETTE.index(color), QColor(color))
        
        if color_dialog.exec() == QColorDialog.DialogCode.Accepted:
            new_color = color_dialog.selectedColor().name()
            self.data_manager.update_note_appearance(note_id, color=new_color)
            self.refresh_notes()
            
            # Update open note windows
            if note_id in self.open_note_windows:
                self.open_note_windows[note_id].update_appearance(new_color, note.font_size)
    
    def on_font_size_increase_requested(self, note_id: str):
        """Handle font size increase request from context menu."""
        note = self.data_manager.get_note(note_id)
        if not note:
            return
        
        from src.utils.constants import FONT_SIZES
        
        current_size = note.font_size
        # Find next larger font size
        larger_sizes = [size for size in FONT_SIZES if size > current_size]
        if larger_sizes:
            new_size = min(larger_sizes)
            self.data_manager.update_note_appearance(note_id, font_size=new_size)
            self.refresh_notes()
            
            # Update open note windows
            if note_id in self.open_note_windows:
                self.open_note_windows[note_id].update_appearance(note.color, new_size)
    
    def on_font_size_decrease_requested(self, note_id: str):
        """Handle font size decrease request from context menu."""
        note = self.data_manager.get_note(note_id)
        if not note:
            return
        
        from src.utils.constants import FONT_SIZES
        
        current_size = note.font_size
        # Find next smaller font size
        smaller_sizes = [size for size in FONT_SIZES if size < current_size]
        if smaller_sizes:
            new_size = max(smaller_sizes)
            self.data_manager.update_note_appearance(note_id, font_size=new_size)
            self.refresh_notes()
            
            # Update open note windows
            if note_id in self.open_note_windows:
                self.open_note_windows[note_id].update_appearance(note.color, new_size)
    
    def on_search_changed(self, query: str):
        """Handle real-time search changes."""
        if query:
            search_results = self.data_manager.search_notes(query)
            self.note_list.update_notes(search_results)
        else:
            # Show all notes when search is cleared
            self.refresh_notes()
    
    def closeEvent(self, event: QCloseEvent):
        """Handle application closure."""
        # Close all open note windows
        for note_window in self.open_note_windows.values():
            note_window.close()
        
        event.accept()
