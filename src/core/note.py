"""
Note data model representing a sticky note.
"""
import time
from typing import Dict, Any
from ..utils.helpers import generate_note_id, get_current_timestamp
from ..utils.constants import DEFAULT_NOTE_COLOR, DEFAULT_FONT_SIZE


class Note:
    """Represents a sticky note with all its properties."""
    
    def __init__(self, note_id: str = None, title: str = "", content: str = "", 
                 color: str = DEFAULT_NOTE_COLOR, font_size: int = DEFAULT_FONT_SIZE,
                 x: int = 100, y: int = 100, w: int = 300, h: int = 350):
        """Initialize a note with given properties."""
        self.id = note_id or generate_note_id()
        self.title = self._validate_title(title)
        self.content = content
        self.color = color
        self.font_size = font_size
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.created_at = get_current_timestamp()
        self.updated_at = get_current_timestamp()
    
    def update_content(self, content: str) -> None:
        """Update note content and timestamp."""
        self.content = content
        self.updated_at = get_current_timestamp()
        self._update_title_from_content()
    
    def update_title(self, title: str) -> None:
        """Update note title and timestamp."""
        self.title = self._validate_title(title)
        self.updated_at = get_current_timestamp()
    
    def update_position(self, x: int, y: int) -> None:
        """Update note position."""
        self.x = x
        self.y = y
        self.updated_at = get_current_timestamp()
    
    def update_size(self, w: int, h: int) -> None:
        """Update note size."""
        self.w = w
        self.h = h
        self.updated_at = get_current_timestamp()
    
    def update_appearance(self, color: str = None, font_size: int = None) -> None:
        """Update note appearance."""
        if color:
            self.color = color
        if font_size:
            self.font_size = font_size
        self.updated_at = get_current_timestamp()
    
    def _validate_title(self, title: str) -> str:
        """Validate and truncate title to maximum 150 characters."""
        if not title:
            return "Untitled Note"
        
        # Truncate to maximum 150 characters
        if len(title) > 150:
            return title[:147] + "..."
        
        return title
    
    def _update_title_from_content(self) -> None:
        """Update title based on content (first line or preview)."""
        if not self.content.strip():
            self.title = "Untitled Note"
            return
        
        lines = self.content.strip().split('\n')
        first_line = lines[0].strip()
        
        if first_line:
            # Use first line as title, truncate if too long
            if len(first_line) > 30:
                self.title = first_line[:27] + "..."
            else:
                self.title = first_line
        else:
            self.title = "Untitled Note"
        
        # Ensure title respects maximum length
        self.title = self._validate_title(self.title)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert note to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "color": self.color,
            "font_size": self.font_size,
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Note':
        """Create note from dictionary data."""
        note = cls(
            note_id=data.get("id"),
            title=data.get("title", ""),
            content=data.get("content", ""),
            color=data.get("color", DEFAULT_NOTE_COLOR),
            font_size=data.get("font_size", DEFAULT_FONT_SIZE),
            x=data.get("x", 100),
            y=data.get("y", 100),
            w=data.get("w", 300),
            h=data.get("h", 350)
        )
        
        # Preserve timestamps if available
        if "created_at" in data:
            note.created_at = data["created_at"]
        if "updated_at" in data:
            note.updated_at = data["updated_at"]
        
        return note
    
    def get_preview(self, max_length: int = 50) -> str:
        """Get a preview of the note content."""
        from ..utils.helpers import get_preview_text
        return get_preview_text(self.content, max_length)
    
    def __str__(self) -> str:
        """String representation of the note."""
        return f"Note({self.id}: {self.title})"
    
    def __repr__(self) -> str:
        """Detailed representation of the note."""
        return f"Note(id={self.id}, title='{self.title}', content_length={len(self.content)})"
