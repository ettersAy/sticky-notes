#!/usr/bin/env python3
"""
Script to update existing notes with titles based on their content.
This script will generate titles for all existing notes that don't have titles.
"""
import os
import json
from pathlib import Path


def get_note_file_path(note_id: str) -> str:
    """Get the file path for a note."""
    return f"data/notes/{note_id}.json"


def load_json_file(file_path: str):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def save_json_file(file_path: str, data: dict) -> bool:
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False


def _validate_title(title: str) -> str:
    """Validate and truncate title to maximum 150 characters."""
    if not title:
        return "Untitled Note"
    
    # Truncate to maximum 150 characters
    if len(title) > 150:
        return title[:147] + "..."
    
    return title


def _update_title_from_content(content: str) -> str:
    """Update title based on content (first line or preview)."""
    if not content.strip():
        return "Untitled Note"
    
    lines = content.strip().split('\n')
    first_line = lines[0].strip()
    
    if first_line:
        # Use first line as title, truncate if too long
        if len(first_line) > 30:
            title = first_line[:27] + "..."
        else:
            title = first_line
    else:
        title = "Untitled Note"
    
    # Ensure title respects maximum length
    return _validate_title(title)


def update_existing_notes():
    """Update all existing notes with titles based on their content."""
    notes_dir = Path("data/notes")
    if not notes_dir.exists():
        print("No notes directory found.")
        return
    
    updated_count = 0
    total_count = 0
    
    for note_file in notes_dir.glob("*.json"):
        total_count += 1
        data = load_json_file(note_file)
        
        if not data:
            continue
        
        # Check if note already has a title
        current_title = data.get("title", "")
        content = data.get("content", "")
        
        # If title is empty or "Untitled Note", generate a new one
        if not current_title or current_title == "Untitled Note":
            new_title = _update_title_from_content(content)
            data["title"] = new_title
            
            if save_json_file(note_file, data):
                print(f"Updated {note_file.name}: '{new_title}'")
                updated_count += 1
            else:
                print(f"Failed to update {note_file.name}")
        else:
            print(f"Skipped {note_file.name}: already has title '{current_title}'")
    
    print(f"\nSummary: Updated {updated_count} out of {total_count} notes.")


if __name__ == "__main__":
    print("Updating existing notes with titles...")
    update_existing_notes()
    print("Done!")
