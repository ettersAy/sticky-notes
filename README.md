# Sticky Notes App

A feature-rich desktop application built with PyQt6 for creating, managing, and organizing digital sticky notes.

## Features

- **Dashboard Interface**: Central hub for note management with search and templates
- **Floating Sticky Notes**: Individual windows with always-on-top functionality
- **Template System**: Predefined templates for different use cases
- **Real-time Search**: Instant filtering across all note content
- **Customizable Appearance**: Font sizes and background colors
- **Auto-save**: Automatic persistence of position, size, and content
- **Multi-window Support**: Open multiple notes simultaneously

## Installation

1. Ensure you have Python 3.8+ installed
2. Run the installation script:
```bash
./install.sh
```

## Usage

Run the application:
```bash
./run.sh
```

## Project Structure

```
sticky_notes_app/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── note.py
│   │   ├── template.py
│   │   └── data_manager.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── sticky_note.py
│   │   ├── note_editor.py
│   │   └── components/
│   │       ├── __init__.py
│   │       ├── search_widget.py
│   │       ├── note_list.py
│   │       └── template_buttons.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── helpers.py
│   └── main.py
├── data/
│   ├── notes/
│   └── templates/
├── install.sh
├── run.sh
└── requirements.txt
```

## Architecture Principles

- Maximum code simplicity
- Single responsibility per class
- Maximum 150 lines per class
- Modular file structure
