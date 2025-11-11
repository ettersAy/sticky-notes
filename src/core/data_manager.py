"""
Data manager for handling note and template persistence.
"""
import os
from typing import Dict, List, Optional
from .note import Note
from .template import Template
from ..utils.helpers import (
    ensure_directories_exist, save_json_file, load_json_file, 
    delete_file, get_note_file_path, get_template_file_path
)


class DataManager:
    """Manages data persistence for notes and templates."""
    
    def __init__(self):
        """Initialize data manager."""
        ensure_directories_exist()
        self.notes: Dict[str, Note] = {}
        self._load_notes()
    
    def _load_notes(self) -> None:
        """Load all notes from the data directory."""
        notes_dir = "data/notes"
        if not os.path.exists(notes_dir):
            return
        
        for filename in os.listdir(notes_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(notes_dir, filename)
                data = load_json_file(file_path)
                if data:
                    try:
                        note = Note.from_dict(data)
                        self.notes[note.id] = note
                    except Exception as e:
                        print(f"Error loading note from {file_path}: {e}")
    
    def save_note(self, note: Note) -> bool:
        """Save a note to disk."""
        file_path = get_note_file_path(note.id)
        success = save_json_file(file_path, note.to_dict())
        if success:
            self.notes[note.id] = note
        return success
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note from disk and memory."""
        file_path = get_note_file_path(note_id)
        success = delete_file(file_path)
        if success and note_id in self.notes:
            del self.notes[note_id]
        return success
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID."""
        return self.notes.get(note_id)
    
    def get_all_notes(self) -> List[Note]:
        """Get all notes sorted by update time (newest first)."""
        notes = list(self.notes.values())
        notes.sort(key=lambda note: note.updated_at, reverse=True)
        return notes
    
    def search_notes(self, query: str) -> List[Note]:
        """Search notes by content."""
        if not query.strip():
            return self.get_all_notes()
        
        query_lower = query.lower()
        results = []
        
        for note in self.notes.values():
            if (query_lower in note.content.lower() or 
                query_lower in note.title.lower()):
                results.append(note)
        
        # Sort by relevance (simple implementation)
        results.sort(key=lambda note: (
            note.content.lower().count(query_lower) + 
            note.title.lower().count(query_lower)
        ), reverse=True)
        
        return results
    
    def create_new_note(self, content: str = "", color: str = None, 
                       font_size: int = None) -> Note:
        """Create a new note."""
        note = Note(content=content)
        if color:
            note.color = color
        if font_size:
            note.font_size = font_size
        
        self.save_note(note)
        return note
    
    def update_note_content(self, note_id: str, content: str) -> bool:
        """Update note content."""
        note = self.get_note(note_id)
        if note:
            note.update_content(content)
            return self.save_note(note)
        return False
    
    def update_note_title(self, note_id: str, title: str) -> bool:
        """Update note title."""
        note = self.get_note(note_id)
        if note:
            note.update_title(title)
            return self.save_note(note)
        return False
    
    def update_note_position(self, note_id: str, x: int, y: int) -> bool:
        """Update note position."""
        note = self.get_note(note_id)
        if note:
            note.update_position(x, y)
            return self.save_note(note)
        return False
    
    def update_note_size(self, note_id: str, w: int, h: int) -> bool:
        """Update note size."""
        note = self.get_note(note_id)
        if note:
            note.update_size(w, h)
            return self.save_note(note)
        return False
    
    def update_note_appearance(self, note_id: str, color: str = None, 
                              font_size: int = None) -> bool:
        """Update note appearance."""
        note = self.get_note(note_id)
        if note:
            note.update_appearance(color, font_size)
            return self.save_note(note)
        return False
    
    def get_note_count(self) -> int:
        """Get total number of notes."""
        return len(self.notes)
    
    def export_notes(self, file_path: str) -> bool:
        """Export all notes to a single JSON file."""
        notes_data = {
            "notes": [note.to_dict() for note in self.notes.values()],
            "export_timestamp": "TODO",  # Add timestamp
            "total_notes": len(self.notes)
        }
        return save_json_file(file_path, notes_data)
    
    def import_notes(self, file_path: str) -> bool:
        """Import notes from a JSON file."""
        data = load_json_file(file_path)
        if not data or "notes" not in data:
            return False
        
        imported_count = 0
        for note_data in data["notes"]:
            try:
                note = Note.from_dict(note_data)
                if self.save_note(note):
                    imported_count += 1
            except Exception as e:
                print(f"Error importing note: {e}")
        
        return imported_count > 0
