"""
Helper functions for the application.
"""
import os
import json
import time
from typing import Dict, Any, Optional
from .constants import NOTES_DIR, TEMPLATES_DIR


def generate_note_id() -> str:
    """Generate a unique note ID based on timestamp."""
    return f"note_{int(time.time() * 1000)}"


def get_note_file_path(note_id: str) -> str:
    """Get the file path for a note."""
    return os.path.join(NOTES_DIR, f"{note_id}.json")


def get_template_file_path(template_id: str) -> str:
    """Get the file path for a template."""
    return os.path.join(TEMPLATES_DIR, f"{template_id}.json")


def ensure_directories_exist() -> None:
    """Ensure that data directories exist."""
    os.makedirs(NOTES_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)


def save_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")
        return False


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load data from a JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
    return None


def delete_file(file_path: str) -> bool:
    """Delete a file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
    return False


def get_preview_text(text: str, max_length: int = 50) -> str:
    """Get a preview of text with ellipsis if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def get_current_timestamp() -> str:
    """Get current timestamp as string."""
    return time.strftime("%Y-%m-%d %H:%M:%S")


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be safe for file system."""
    # Remove or replace problematic characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def count_lines_and_chars(text: str) -> tuple[int, int]:
    """Count lines and characters in text."""
    lines = text.split('\n')
    char_count = len(text)
    line_count = len(lines)
    return line_count, char_count
