"""
Template buttons component for the dashboard.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from src.core.template import TemplateManager
from src.utils.constants import TEMPLATES


class TemplateButtons(QWidget):
    """Template buttons for quick note creation."""
    
    template_selected = pyqtSignal(str)  # template_id
    
    def __init__(self, parent=None):
        """Initialize template buttons."""
        super().__init__(parent)
        self.template_manager = TemplateManager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Title
        title_label = QLabel("Templates")
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Template buttons
        self.create_template_buttons(layout)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_template_buttons(self, layout: QVBoxLayout):
        """Create template buttons."""
        templates = self.template_manager.get_all_templates()
        
        for template_id, template in templates.items():
            button = QPushButton(template.name)
            button.setToolTip(f"Create {template.name} note")
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {template.color};
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 8px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {self._lighten_color(template.color)};
                    border: 1px solid #999;
                }}
                QPushButton:pressed {{
                    background-color: {self._darken_color(template.color)};
                }}
            """)
            
            # Connect signal with template_id as parameter
            button.clicked.connect(
                lambda checked, tid=template_id: self.on_template_clicked(tid)
            )
            
            layout.addWidget(button)
    
    def on_template_clicked(self, template_id: str):
        """Handle template button click."""
        self.template_selected.emit(template_id)
    
    def _lighten_color(self, hex_color: str, factor: float = 0.2) -> str:
        """Lighten a hex color."""
        return self._adjust_color_brightness(hex_color, 1 + factor)
    
    def _darken_color(self, hex_color: str, factor: float = 0.2) -> str:
        """Darken a hex color."""
        return self._adjust_color_brightness(hex_color, 1 - factor)
    
    def _adjust_color_brightness(self, hex_color: str, factor: float) -> str:
        """Adjust color brightness by factor."""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Adjust brightness
        r = min(255, max(0, int(r * factor)))
        g = min(255, max(0, int(g * factor)))
        b = min(255, max(0, int(b * factor)))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def get_template_count(self) -> int:
        """Get number of available templates."""
        return len(self.template_manager.get_all_templates())
