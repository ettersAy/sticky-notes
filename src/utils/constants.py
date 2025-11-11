"""
Application constants and configuration.
"""

# Window and UI constants
DASHBOARD_WINDOW_SIZE = (1000, 700)
STICKY_NOTE_DEFAULT_SIZE = (300, 350)
STICKY_NOTE_MIN_SIZE = (200, 200)
STICKY_NOTE_MAX_SIZE = (800, 600)

# Font sizes
FONT_SIZES = [8, 10, 12, 14, 16, 18, 24]
DEFAULT_FONT_SIZE = 12

# Colors
DEFAULT_NOTE_COLOR = "#FFF9C4"
COLOR_PALETTE = [
    "#FFF9C4",  # Yellow
    "#C8E6C9",  # Green
    "#BBDEFB",  # Blue
    "#E1BEE7",  # Purple
    "#FFCDD2",  # Red
    "#F5F5F5",  # White
    "#FFCCBC",  # Orange
    "#DCEDC8",  # Light Green
]

# Template colors
TEMPLATE_COLORS = {
    "todo": "#C8E6C9",
    "meeting": "#BBDEFB",
    "code": "#E1BEE7",
    "shopping": "#FFCDD2",
    "ideas": "#FFF9C4"
}

# File paths
NOTES_DIR = "data/notes"
TEMPLATES_DIR = "data/templates"

# Template definitions
TEMPLATES = {
    "todo": {
        "name": "To-Do List",
        "color": TEMPLATE_COLORS["todo"],
        "content": "📋 To-Do List\n\n✅ Task 1\n□ Task 2\n□ Task 3\n\n📅 Due: \n\n💡 Notes:"
    },
    "meeting": {
        "name": "Meeting Notes",
        "color": TEMPLATE_COLORS["meeting"],
        "content": "📋 Meeting Notes\n\n📅 Date: \n⏰ Time: \n📍 Location: \n\n👥 Attendees:\n• \n• \n• \n\n📝 Agenda:\n• \n• \n• \n\n✅ Action Items:\n• \n• \n•"
    },
    "code": {
        "name": "Code Snippet",
        "color": TEMPLATE_COLORS["code"],
        "content": "💻 Code Snippet\n\n📁 File: \n🔧 Language: \n\n📝 Description:\n\n```\n// Your code here\n```\n\n💡 Notes:"
    },
    "shopping": {
        "name": "Shopping List",
        "color": TEMPLATE_COLORS["shopping"],
        "content": "🛒 Shopping List\n\n🏪 Store: \n\n📋 Items:\n□ \n□ \n□ \n□ \n\n💰 Budget: \n\n📅 Date:"
    },
    "ideas": {
        "name": "Ideas & Brainstorming",
        "color": TEMPLATE_COLORS["ideas"],
        "content": "💡 Ideas & Brainstorming\n\n🎯 Topic: \n\n💭 Ideas:\n• \n• \n• \n\n🔍 Research:\n• \n• \n\n✅ Next Steps:\n• \n•"
    }
}

# UI Text
APP_TITLE = "Sticky Notes Dashboard"
NEW_NOTE_BUTTON_TEXT = "➕"
SEARCH_BUTTON_TEXT = "🔍"
DELETE_BUTTON_TEXT = "🗑️"
COPY_BUTTON_TEXT = "📋"
COLOR_BUTTON_TEXT = "🎨"
CLOSE_BUTTON_TEXT = "×"

# Search
SEARCH_PLACEHOLDER = "Search notes..."
MAX_SEARCH_RESULTS = 50

# Note display
MAX_PREVIEW_LENGTH = 50
NOTE_LIST_ITEM_HEIGHT = 40
