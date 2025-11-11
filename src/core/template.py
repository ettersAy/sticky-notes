"""
Template data model for predefined note templates.
"""
from typing import Dict, Any
from ..utils.constants import TEMPLATES, DEFAULT_NOTE_COLOR


class Template:
    """Represents a predefined note template."""
    
    def __init__(self, template_id: str, name: str, content: str, color: str = DEFAULT_NOTE_COLOR):
        """Initialize a template with given properties."""
        self.id = template_id
        self.name = name
        self.content = content
        self.color = color
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "color": self.color
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Template':
        """Create template from dictionary data."""
        return cls(
            template_id=data.get("id"),
            name=data.get("name", ""),
            content=data.get("content", ""),
            color=data.get("color", DEFAULT_NOTE_COLOR)
        )
    
    @classmethod
    def get_default_templates(cls) -> Dict[str, 'Template']:
        """Get all default templates."""
        templates = {}
        for template_id, template_data in TEMPLATES.items():
            templates[template_id] = cls(
                template_id=template_id,
                name=template_data["name"],
                content=template_data["content"],
                color=template_data["color"]
            )
        return templates
    
    def __str__(self) -> str:
        """String representation of the template."""
        return f"Template({self.id}: {self.name})"
    
    def __repr__(self) -> str:
        """Detailed representation of the template."""
        return f"Template(id={self.id}, name='{self.name}', content_length={len(self.content)})"


class TemplateManager:
    """Manages template operations."""
    
    def __init__(self):
        """Initialize template manager."""
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self) -> None:
        """Load default templates."""
        self.templates = Template.get_default_templates()
    
    def get_template(self, template_id: str) -> Template:
        """Get a template by ID."""
        return self.templates.get(template_id)
    
    def get_all_templates(self) -> Dict[str, Template]:
        """Get all available templates."""
        return self.templates.copy()
    
    def get_template_names(self) -> list[str]:
        """Get list of template names."""
        return [template.name for template in self.templates.values()]
    
    def create_note_from_template(self, template_id: str) -> 'Note':
        """Create a new note from a template."""
        from .note import Note
        
        template = self.get_template(template_id)
        if not template:
            # Fallback to empty note if template not found
            return Note()
        
        note = Note(
            content=template.content,
            color=template.color
        )
        return note
