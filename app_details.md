# Sticky Notes App Documentation

## Overview

The Sticky Notes App is a feature-rich desktop application built with PyQt6 that provides a modern, intuitive interface for creating, managing, and organizing digital sticky notes. The application offers both a dashboard view for note management and individual floating sticky notes for quick access.

## Interface Components

### Main Dashboard Window

The main dashboard serves as the central hub for note management with a clean, organized layout:

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                    Sticky Notes Dashboard                       │
├─────────────────┬───────────────────────────────────────────────┤
│                 │                                               │
│   Left Panel    │              Right Panel                      │
│                 │                                               │
│  ┌─────────────┐│  ┌─────────────────────────────────────────┐ │
│  │[➕]         |│  │                                         │ │
│  │─────────────││  │                                         │ │
│  │[📝] To-Do   ││  │                                         │ │
│  │[📅] Meeting ││  │          Note Preview/Editor            │ │
│  │[💻] Code    ││  │                                         │ │
│  │[🛒] Shopping││  │                                         │ │
│  │[💡] Ideas   ││  │                                         │ │
│  │─────────────││  │                                         │ │
│  │[Search...][🔍]│││                                         │ │
│  │─────────────││  │                                         │ │
│  │• Note 1     ││  │                                         │ │
│  │• Note 2     ││  │                                         │ │
│  │• Note 3     ││  │                                         │ │
│  │─────────────││  │                                         │ │
│  │[🗑️]         ││  │                                         │ │
│  └─────────────┘│  └─────────────────────────────────────────┘ │
│                 │                                               │
└─────────────────┴───────────────────────────────────────────────┘
```

- **Left Panel**: Note list with template buttons and search functionality
- **Right Panel**: Note preview and editor
- **Resizable Splitter**: Allows users to adjust panel sizes according to their preference

#### Left Panel Components
1. **Template Buttons**: Quick-access buttons for creating notes from predefined templates
2. **Search Field**: Hidden by default, appears when search button is clicked
3. **Note List**: Displays all notes with truncated content preview
4. **Action Buttons**: 
   - ➕ New Note button
   - 🔍 Search toggle button
   - 🗑️ Delete note button (enabled when a note is selected)

#### Right Panel Components
- **Note Preview/Editor**: Full-featured text editor for viewing and editing note content
- Real-time content synchronization with open note windows

### Individual Sticky Note Windows

Each sticky note appears as a floating window with advanced features:

#### Window Layout
```
┌─────────────────────────────────────────────────────────┐
│ Note 1762878163: Meeting notes with...                  │
├─────────────────────────────────────────────────────────┤
│ [📋] [🎨] [12] [×]                                     │
├─────────────────────────────────────────────────────────┤
│ 1 │ Meeting Notes                                      │
│ 2 │                                                    │
│ 3 │ 📋 Agenda:                                         │
│ 4 │ • Project planning                                │
│ 5 │ • Timeline review                                 │
│ 6 │ • Resource allocation                             │
│ 7 │                                                    │
│ 8 │ 👥 Attendees:                                      │
│ 9 │ • John Smith                                       │
│10 │ • Sarah Johnson                                    │
│11 │ • Mike Brown                                       │
│12 │                                                    │
│13 │ 📝 Notes:                                          │
│14 │ • Project scope finalized                         │
│15 │ • Timeline approved                               │
│16 │ • Resources allocated                             │
│17 │                                                    │
│18 │ ✅ Action Items:                                   │
│19 │ • Create project charter                          │
│20 │ • Schedule kickoff meeting                        │
│21 │ • Assign team roles                               │
│22 │                                                    │
├─────────────────────────────────────────────────────────┤
│ Characters: 485 | Lines: 22                            │
└─────────────────────────────────────────────────────────┘
```

#### Window Features
- **Always on Top**: Notes stay visible above other applications
- **Frameless Design**: Clean, modern appearance
- **Draggable**: Click and drag the top bar to move notes
- **Resizable**: Drag the bottom-right corner to resize
- **Auto-save**: Position, size, and content are automatically saved

#### Control Bar (Top)
- **📋 Copy Button**: Copies note content to clipboard with visual feedback
- **🎨 Color Button**: Opens color picker to change note background color
- **Font Size Combo**: Dropdown to select font size (8, 10, 12, 14, 16, 18, 24)
- **× Close Button**: Closes the note window

#### Text Editor
- **Line Numbers**: Shows line numbers for better text navigation
- **Real-time Statistics**: Character and line count displayed in info bar
- **Auto-save**: Content saved automatically as you type
- **Dynamic Title**: Window title updates to show note content preview

## Features

### Core Note Management

1. **Create Notes**
   - Create blank notes from the dashboard
   - Create notes from templates (To-Do, Meeting, Code, Shopping, Ideas)
   - Auto-generated unique IDs with timestamps

2. **Edit Notes**
   - Rich text editing in both dashboard preview and individual windows
   - Real-time content synchronization across all views
   - Font size customization (8-24pt)
   - Background color customization

3. **Delete Notes**
   - Confirmation dialog before deletion
   - Automatic cleanup of associated files
   - Close associated note windows when deleted

4. **Search & Filter**
   - Real-time search across all note content
   - Search suggestions based on content
   - Highlight matching text in results
   - Toggle search field visibility

### Template System

#### Predefined Templates
- **To-Do List**: Structured checklist format with completion indicators
- **Meeting Notes**: Organized sections for agenda, attendees, notes, and action items
- **Code Snippet**: Format for code documentation with language and purpose fields
- **Shopping List**: Categorized shopping items with checkboxes
- **Ideas & Brainstorming**: Structured format for idea organization

#### Template Features
- Custom background colors for different template types
- Pre-formatted content with placeholders
- Ability to create custom templates
- Default templates cannot be deleted

### Advanced Features

1. **Multi-Window Support**
   - Open multiple notes in separate floating windows
   - Independent positioning and sizing for each note
   - Always-on-top functionality for quick reference
   - Automatic window management when notes are deleted

2. **Data Persistence**
   - JSON-based storage for notes and templates
   - Automatic saving of position, size, and content
   - Backup and restore capabilities
   - Timestamp tracking (created_at, updated_at)

3. **User Experience**
   - Resizable interface panels
   - Visual feedback for actions (copy confirmation)
   - Character and line count statistics
   - Intuitive drag-and-drop positioning

### Technical Features

1. **Line Numbering**
   - Automatic line number calculation and display
   - Dynamic width adjustment based on line count
   - Professional code-editor style interface

2. **Real-time Updates**
   - Content changes synchronized across all views
   - Search results update instantly
   - Note list refreshes automatically

3. **Error Handling**
   - Graceful handling of file operations
   - Template loading error recovery
   - Note corruption protection

## File Structure

```
data/
├── notes/           # Individual note files (note_<timestamp>.json)
└── templates/       # Template definition files
```

### Note Data Format
```json
{
  "id": "note_id",
  "title": "Note Title",
  "content": "Note content",
  "color": "#HEXCOLOR",
  "font_size": 12,
  "x": 200,
  "y": 200,
  "w": 300,
  "h": 350,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Usage Workflows

### Creating and Managing Notes
1. Use the dashboard to create new notes or templates
2. Double-click notes to open in floating windows
3. Use search to quickly find specific notes
4. Customize appearance with colors and font sizes

### Quick Reference Workflow
1. Keep frequently used notes open as floating windows
2. Use "Always on Top" feature for constant visibility
3. Position notes around screen edges for organization
4. Use templates for consistent formatting

### Organization Workflow
1. Use different colors to categorize notes
2. Utilize templates for specific use cases
3. Search functionality for quick access
4. Delete old notes to maintain organization

## System Requirements

- **Python 3.8+**
- **PyQt6** for GUI framework
- **File system access** for data persistence
- **Modern desktop environment** with window management

## Keyboard and Mouse Interactions

- **Click**: Select note in list
- **Double-click**: Open note in floating window
- **Drag**: Move floating notes
- **Resize**: Drag bottom-right corner of floating notes
- **Search**: Type in search field for instant filtering

This application provides a comprehensive solution for digital note-taking with the flexibility of traditional sticky notes combined with modern organizational features.
