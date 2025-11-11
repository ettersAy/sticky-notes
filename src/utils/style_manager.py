"""
Style manager for handling application stylesheets.
"""
import os
from typing import Dict, Optional
from PyQt6.QtWidgets import QApplication


class StyleManager:
    """Manages application stylesheets and themes."""
    
    def __init__(self):
        """Initialize style manager."""
        self.styles: Dict[str, str] = {}
        self.current_theme = "light"
        self.themes = {
            "light": "styles/themes/light.css",
            "dark": "styles/themes/dark.css"
        }
        self.load_all_styles()
    
    def load_all_styles(self):
        """Load all available styles into memory."""
        style_files = {
            "global": "styles/global.css",
            "buttons": "styles/widgets/buttons.css",
            "sticky_note": "styles/widgets/sticky_note.css",
            "light_theme": "styles/themes/light.css",
            "dark_theme": "styles/themes/dark.css"
        }
        
        for name, path in style_files.items():
            self.styles[name] = self.safe_load_stylesheet(path)
    
    def safe_load_stylesheet(self, file_path: str) -> str:
        """Safely load a stylesheet with error handling."""
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                print(f"Stylesheet not found: {file_path}")
                return ""
        except Exception as e:
            print(f"Error loading stylesheet {file_path}: {e}")
            return ""
    
    def get_style(self, style_name: str) -> str:
        """Get a specific style by name."""
        return self.styles.get(style_name, "")
    
    def apply_style(self, widget, style_name: str):
        """Apply a style to a specific widget."""
        widget.setStyleSheet(self.get_style(style_name))
    
    def apply_global_styles(self, app: QApplication):
        """Apply global application styles."""
        global_style = self.get_style("global")
        theme_style = self.get_style(f"{self.current_theme}_theme")
        
        combined_style = global_style + "\n" + theme_style
        app.setStyleSheet(combined_style)
    
    def apply_theme(self, app: QApplication, theme_name: str):
        """Apply a specific theme to the application."""
        if theme_name in self.themes:
            theme_style = self.safe_load_stylesheet(self.themes[theme_name])
            global_style = self.get_style("global")
            
            combined_style = global_style + "\n" + theme_style
            app.setStyleSheet(combined_style)
            self.current_theme = theme_name
    
    def toggle_theme(self, app: QApplication):
        """Toggle between light and dark themes."""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(app, new_theme)
    
    def get_current_theme(self) -> str:
        """Get the current theme name."""
        return self.current_theme
    
    def validate_stylesheet(self, css_content: str) -> bool:
        """Basic validation of CSS content."""
        # Simple validation - check for balanced braces
        open_braces = css_content.count('{')
        close_braces = css_content.count('}')
        return open_braces == close_braces


class StyleConstants:
    """Constants for style names."""
    PRIMARY_BUTTON = "primary_button"
    SECONDARY_BUTTON = "secondary_button"
    STICKY_NOTE = "sticky_note"
    GLOBAL = "global"
    LIGHT_THEME = "light_theme"
    DARK_THEME = "dark_theme"
