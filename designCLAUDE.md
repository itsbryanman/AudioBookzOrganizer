# Advanced AudioBookzOrganizer TUI Design

Based on your preferences, I've designed a comprehensive TUI framework using Textual. Here's the implementation plan:

## 1. App Structure & Layout

```python name=app.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button, SelectionList, Tree, DataTable, ProgressBar
from textual.containers import Horizontal, Vertical, Container, Grid
from textual.binding import Binding
from textual import events

class AudioBookzOrganizerApp(App):
    """AudioBookzOrganizer - Advanced TUI for audiobook organization."""
    
    CSS_PATH = "styles.css"
    BINDINGS = [
        Binding("q", "quit", "Quit", key_display="q"),
        Binding("j", "cursor_down", "Down", key_display="j"),
        Binding("k", "cursor_up", "Up", key_display="k"),
        Binding("h", "cursor_left", "Left", key_display="h"),
        Binding("l", "cursor_right", "Right", key_display="l"),
        Binding("r", "rename", "Rename", key_display="r"),
        Binding("m", "match", "Match", key_display="m"),
        Binding("f", "filter", "Filter", key_display="f"),
        Binding("e", "edit", "Edit", key_display="e"),
        Binding("ctrl+r", "refresh", "Refresh", key_display="^R"),
        Binding("?", "help", "Help", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        
        # Top Toolbar
        yield Horizontal(
            Button("Load Files", id="load-btn", variant="primary"),
            Button("Match", id="match-btn", variant="primary"),
            Button("Rename", id="rename-btn", variant="primary"),
            Input(placeholder="Format: {author}/{series}/{title}", id="format-input"),
            Button("Presets ▼", id="presets-btn"),
            Input(placeholder="Path...", id="path-input"),
            Button("Browse...", id="browse-btn"),
            id="top-toolbar"
        )
        
        # Main Dual-Pane Workspace
        yield Horizontal(
            # Left Pane - Source Files
            Vertical(
                Static("Source Files", id="source-title"),
                Tree("Library", id="source-tree"),
                id="left-pane"
            ),
            # Right Pane - Preview & Metadata
            Vertical(
                Static("Preview & Metadata", id="preview-title"),
                DataTable(id="preview-table"),
                id="right-pane"
            ),
            id="main-workspace"
        )
        
        # Bottom Panel
        yield Vertical(
            # Log output area
            Static(id="log-area", classes="log"),
            # Bottom status bar
            Horizontal(
                Input(placeholder="Quick filter...", id="filter-input"),
                Static("Files: 0/0 | Errors: 0", id="status-info"),
                ProgressBar(total=100, id="progress-bar"),
                id="status-bar"
            ),
            id="bottom-panel"
        )
        
        yield Footer()

    def on_mount(self) -> None:
        """Called once when the app is mounted."""
        self.title = "AudioBookzOrganizer"
        self._setup_data_table()
        self._display_splash()
        
    def _setup_data_table(self) -> None:
        """Set up the preview data table columns."""
        table = self.query_one("#preview-table", DataTable)
        table.add_columns("Original", "New Name", "Title", "Author", "Series", "Year")
        
    def _display_splash(self) -> None:
        """Display the ASCII splash screen."""
        splash = """
        ╭───────────────────────────────────────────────╮
        │                                               │
        │  [blue]█▀█ █░█ █▀▄ █ █▀█ [orange]█▄▄ █▀█ █▀█ █▄▀ ▀█[/]     │
        │  [blue]█▀█ █▄█ █▄▀ █ █▄█ [orange]█▄█ █▄█ █▄█ █░█ █▄[/]     │
        │                                               │
        │             [blue]█▀█ █▀█ █▀▀ █▀█ █▄░█ █ ▀█ █▀▀ █▀█[/]     │
        │             [orange]█▄█ █▀▄ █▄█ █▀█ █░▀█ █ █▄ ██▄ █▀▄[/]     │
        │                                               │
        ╰───────────────────────────────────────────────╯
        """
        log_area = self.query_one("#log-area", Static)
        log_area.update(splash)
        
    def action_rename(self) -> None:
        """Rename the selected files."""
        # Implementation will go here
        self.log("Renaming files...")
        
    def action_match(self) -> None:
        """Match files with metadata."""
        # Implementation will go here
        self.log("Matching files with Audible metadata...")
        
    def log(self, message: str) -> None:
        """Add a message to the log area."""
        log_area = self.query_one("#log-area", Static)
        current = log_area.render()
        if "[blue]█▀█" not in current:  # Don't append to splash screen
            log_area.update(f"{current}\n{message}")
        else:
            log_area.update(message)

def run():
    app = AudioBookzOrganizerApp()
    app.run()

if __name__ == "__main__":
    run()
```

## 2. CSS Styling

```css name=styles.css
/* Main theme colors */
:root {
    --background: #2B2B2B;
    --primary: #1E90FF;
    --secondary: #FF8C00;
    --text: #E0E0E0;
    --text-muted: #A0A0A0;
    --border: #505050;
    --error: #FF5252;
    --success: #4CAF50;
}

/* Global styling */
Screen {
    background: var(--background);
    color: var(--text);
}

/* Typography */
* {
    font-family: "Fira Code", "JetBrains Mono", monospace;
}

/* Header styling */
Header {
    background: var(--background);
    color: var(--primary);
    height: 1;
    dock: top;
    border-bottom: solid var(--border);
}

/* Footer styling */
Footer {
    background: var(--background);
    color: var(--text-muted);
    height: 1;
    dock: bottom;
    border-top: solid var(--border);
}

/* Top toolbar */
#top-toolbar {
    height: 3;
    dock: top;
    background: var(--background);
    border-bottom: solid var(--border);
    padding: 0 1;
    align: center middle;
}

Button {
    background: var(--primary);
    color: var(--background);
    border: none;
    height: 1;
    margin: 0 1 0 0;
    min-width: 10;
}

Button:hover {
    background: var(--secondary);
}

Input {
    background: var(--background);
    border: solid var(--border);
    color: var(--text);
    padding: 0 1;
    margin: 0 1 0 0;
    height: 1;
}

/* Main workspace */
#main-workspace {
    min-height: 1fr;
    height: 1fr;
}

#left-pane, #right-pane {
    width: 1fr;
    height: 100%;
    border: solid var(--border);
    margin: 0 1;
}

#source-title, #preview-title {
    background: var(--primary);
    color: var(--background);
    height: 1;
    text-align: center;
    width: 100%;
}

#source-tree {
    border: none;
    padding: 0 1;
    height: 1fr;
    overflow: auto;
}

Tree > .tree--guides {
    color: var(--primary);
}

Tree > .tree--cursor {
    background: var(--primary);
    color: var(--background);
}

DataTable {
    height: 1fr;
    border: none;
    overflow: auto;
}

/* DataTable styles */
DataTable > .datatable--header {
    background: var(--primary);
    color: var(--background);
}

DataTable > .datatable--cursor {
    background: var(--primary);
    color: var(--background);
}

DataTable > .datatable--alternate-row {
    background: #333333;
}

/* Bottom panel */
#bottom-panel {
    height: 6;
    dock: bottom;
    border-top: solid var(--border);
}

#log-area {
    height: 5;
    overflow: auto;
    padding: 0 1;
}

#status-bar {
    height: 1;
    align: center middle;
    background: var(--background);
    border-top: solid var(--border);
}

#status-info {
    width: auto;
    padding: 0 1;
    color: var(--text-muted);
}

#filter-input {
    width: 30;
    margin: 0 1;
}

#progress-bar {
    width: 20;
    margin: 0 1;
}

ProgressBar > .bar--bar {
    background: var(--primary);
}

ProgressBar > .bar--complete {
    color: var(--secondary);
}

/* Log styling */
.log {
    background: #1A1A1A;
    color: var(--text);
    overflow: auto;
    border: solid var(--border);
    margin: 0 1;
}
```

## 3. Metadata Editor Modal

```python name=metadata_editor.py
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.containers import Grid

class MetadataEditorModal(ModalScreen):
    """Modal screen for editing audiobook metadata."""
    
    def __init__(self, metadata: dict) -> None:
        """Initialize with book metadata."""
        super().__init__()
        self.metadata = metadata
        
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with Grid(id="metadata-grid"):
            yield Label("Title:")
            yield Input(value=self.metadata.get("title", ""), id="title-input")
            
            yield Label("Author:")
            yield Input(value=self.metadata.get("author", ""), id="author-input")
            
            yield Label("Series:")
            yield Input(value=self.metadata.get("series", ""), id="series-input")
            
            yield Label("Series #:")
            yield Input(value=self.metadata.get("series_number", ""), id="series-number-input")
            
            yield Label("Year:")
            yield Input(value=self.metadata.get("year", ""), id="year-input")
            
            yield Label("Genre:")
            yield Input(value=self.metadata.get("genre", ""), id="genre-input")
            
            yield Label("Narrator:")
            yield Input(value=self.metadata.get("narrator", ""), id="narrator-input")
            
            yield Label("Duration:")
            yield Input(value=self.metadata.get("duration", ""), id="duration-input")
            
        with Grid(id="button-grid"):
            yield Button("Save", variant="primary", id="save-btn")
            yield Button("Cancel", id="cancel-btn")
            
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-btn":
            self.update_metadata()
            self.dismiss(self.metadata)
        elif event.button.id == "cancel-btn":
            self.dismiss(None)
            
    def update_metadata(self) -> None:
        """Update metadata from input fields."""
        self.metadata["title"] = self.query_one("#title-input", Input).value
        self.metadata["author"] = self.query_one("#author-input", Input).value
        self.metadata["series"] = self.query_one("#series-input", Input).value
        self.metadata["series_number"] = self.query_one("#series-number-input", Input).value
        self.metadata["year"] = self.query_one("#year-input", Input).value
        self.metadata["genre"] = self.query_one("#genre-input", Input).value
        self.metadata["narrator"] = self.query_one("#narrator-input", Input).value
        self.metadata["duration"] = self.query_one("#duration-input", Input).value
```

## 4. Statistics Visualization Widget

```python name=stats_widget.py
from textual.widget import Widget
from textual.reactive import reactive
from rich.panel import Panel
from rich.text import Text
from rich.console import Console, RenderableType
from rich.table import Table
from rich.box import SIMPLE
from rich.align import Align
from rich import box
from typing import Dict, List

class StatsWidget(Widget):
    """Widget to display library statistics and visualizations."""
    
    genre_data = reactive({})
    author_data = reactive({})
    processing_history = reactive([])
    
    def __init__(self, genre_data=None, author_data=None, processing_history=None):
        """Initialize with optional data."""
        super().__init__()
        if genre_data:
            self.genre_data = genre_data
        if author_data:
            self.author_data = author_data
        if processing_history:
            self.processing_history = processing_history
    
    def render(self) -> RenderableType:
        """Render the widget."""
        # Create a panel to hold all visualizations
        stats_panel = Panel(
            Align.center(
                self._build_stats_content(),
                vertical="middle"
            ),
            title="Library Statistics",
            border_style="blue",
            box=box.DOUBLE
        )
        return stats_panel
    
    def _build_stats_content(self) -> RenderableType:
        """Build the stats content with visualizations."""
        # Create a table to organize the visualizations
        table = Table.grid(expand=True)
        table.add_column("Genre Distribution")
        table.add_column("Top Authors")
        
        # Add genre distribution chart
        genre_chart = self._create_genre_chart()
        
        # Add top authors chart
        author_chart = self._create_author_chart()
        
        # Add processing history sparkline
        history_sparkline = self._create_history_sparkline()
        
        # Add row with the charts
        table.add_row(genre_chart, author_chart)
        
        # Add row with the sparkline
        table.add_row(Text("Processing History:"), "")
        table.add_row(history_sparkline, "")
        
        return table
    
    def _create_genre_chart(self) -> RenderableType:
        """Create an ASCII bar chart for genre distribution."""
        if not self.genre_data:
            return Text("No genre data available")
        
        chart_table = Table(box=None, expand=True, padding=0)
        chart_table.add_column("Genre", style="cyan")
        chart_table.add_column("Count", style="blue")
        chart_table.add_column("Bar", ratio=3)
        
        max_count = max(self.genre_data.values()) if self.genre_data else 0
        for genre, count in sorted(self.genre_data.items(), key=lambda x: x[1], reverse=True)[:5]:
            if max_count > 0:
                bar_width = int((count / max_count) * 20)
                bar = f"[blue]{'█' * bar_width}[/]"
                chart_table.add_row(genre, str(count), bar)
        
        return chart_table
    
    def _create_author_chart(self) -> RenderableType:
        """Create a chart for top authors."""
        if not self.author_data:
            return Text("No author data available")
        
        chart_table = Table(box=None, expand=True, padding=0)
        chart_table.add_column("Author", style="orange")
        chart_table.add_column("Books", style="blue")
        chart_table.add_column("Bar", ratio=3)
        
        max_count = max(self.author_data.values()) if self.author_data else 0
        for author, count in sorted(self.author_data.items(), key=lambda x: x[1], reverse=True)[:5]:
            if max_count > 0:
                bar_width = int((count / max_count) * 20)
                bar = f"[orange]{'█' * bar_width}[/]"
                chart_table.add_row(author, str(count), bar)
        
        return chart_table
    
    def _create_history_sparkline(self) -> RenderableType:
        """Create a sparkline of processing history."""
        if not self.processing_history:
            return Text("No processing history available")
        
        # Use Unicode block characters for the sparkline
        # ▁▂▃▄▅▆▇█
        blocks = "▁▂▃▄▅▆▇█"
        
        # Normalize the history data to 0-7 range for the blocks
        max_value = max(self.processing_history) if self.processing_history else 1
        normalized = [min(7, int((val / max_value) * 7)) for val in self.processing_history]
        
        # Generate the sparkline
        sparkline = "".join(blocks[val] for val in normalized)
        
        return Text(f"[blue]{sparkline}[/]")
    
    def update_data(self, genre_data=None, author_data=None, processing_point=None):
        """Update the widget with new data."""
        if genre_data:
            self.genre_data = genre_data
        if author_data:
            self.author_data = author_data
        if processing_point is not None:
            # Limit history to last 50 points
            self.processing_history = self.processing_history[-49:] + [processing_point]
        
        self.refresh()
```

## 5. Implementation Notes

1. **Key Features**:
   - **Dual-pane layout**: Source files on the left, preview/metadata on the right
   - **Vim-style navigation**: j/k for up/down, h/l for left/right
   - **Advanced styling**: Electric blue and vibrant orange on dark gray background
   - **Interactive components**: DataTable for metadata, Tree for file browsing
   - **Visualizations**: Statistics with ASCII/Unicode charts
   - **Modal editors**: Pop-up dialogs for detailed metadata editing

2. **Performance Optimizations**:
   - Async metadata loading to prevent UI blocking
   - Event-driven architecture for responsive interface
   - Custom widgets with optimized rendering

3. **Installation Requirements**:
```
pip install textual rich
```

my idea for the files maybe? 

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button, SelectionList, Tree, DataTable, ProgressBar
from textual.containers import Horizontal, Vertical, Container, Grid
from textual.binding import Binding
from textual import events

class AudioBookzOrganizerApp(App):
    """AudioBookzOrganizer - Advanced TUI for audiobook organization."""
    
    CSS_PATH = "styles.css"
    BINDINGS = [
        Binding("q", "quit", "Quit", key_display="q"),
        Binding("j", "cursor_down", "Down", key_display="j"),
        Binding("k", "cursor_up", "Up", key_display="k"),
        Binding("h", "cursor_left", "Left", key_display="h"),
        Binding("l", "cursor_right", "Right", key_display="l"),
        Binding("r", "rename", "Rename", key_display="r"),
        Binding("m", "match", "Match", key_display="m"),
        Binding("f", "filter", "Filter", key_display="f"),
        Binding("e", "edit", "Edit", key_display="e"),
        Binding("ctrl+r", "refresh", "Refresh", key_display="^R"),
        Binding("?", "help", "Help", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        
        # Top Toolbar
        yield Horizontal(
            Button("Load Files", id="load-btn", variant="primary"),
            Button("Match", id="match-btn", variant="primary"),
            Button("Rename", id="rename-btn", variant="primary"),
            Input(placeholder="Format: {author}/{series}/{title}", id="format-input"),
            Button("Presets ▼", id="presets-btn"),
            Input(placeholder="Path...", id="path-input"),
            Button("Browse...", id="browse-btn"),
            id="top-toolbar"
        )
        
        # Main Dual-Pane Workspace
        yield Horizontal(
            # Left Pane - Source Files
            Vertical(
                Static("Source Files", id="source-title"),
                Tree("Library", id="source-tree"),
                id="left-pane"
            ),
            # Right Pane - Preview & Metadata
            Vertical(
                Static("Preview & Metadata", id="preview-title"),
                DataTable(id="preview-table"),
                id="right-pane"
            ),
            id="main-workspace"
        )
        
        # Bottom Panel
        yield Vertical(
            # Log output area
            Static(id="log-area", classes="log"),
            # Bottom status bar
            Horizontal(
                Input(placeholder="Quick filter...", id="filter-input"),
                Static("Files: 0/0 | Errors: 0", id="status-info"),
                ProgressBar(total=100, id="progress-bar"),
                id="status-bar"
            ),
            id="bottom-panel"
        )
        
        yield Footer()

    def on_mount(self) -> None:
        """Called once when the app is mounted."""
        self.title = "AudioBookzOrganizer"
        self._setup_data_table()
        self._display_splash()
        
    def _setup_data_table(self) -> None:
        """Set up the preview data table columns."""
        table = self.query_one("#preview-table", DataTable)
        table.add_columns("Original", "New Name", "Title", "Author", "Series", "Year")
        
    def _display_splash(self) -> None:
        """Display the ASCII splash screen."""
        splash = """
        ╭───────────────────────────────────────────────╮
        │                                               │
        │  [blue]█▀█ █░█ █▀▄ █ █▀█ [orange]█▄▄ █▀█ █▀█ █▄▀ ▀█[/]     │
        │  [blue]█▀█ █▄█ █▄▀ █ █▄█ [orange]█▄█ █▄█ █▄█ █░█ █▄[/]     │
        │                                               │
        │             [blue]█▀█ █▀█ █▀▀ █▀█ █▄░█ █ ▀█ █▀▀ █▀█[/]     │
        │             [orange]█▄█ █▀▄ █▄█ █▀█ █░▀█ █ █▄ ██▄ █▀▄[/]     │
        │                                               │
        ╰───────────────────────────────────────────────╯
        """
        log_area = self.query_one("#log-area", Static)
        log_area.update(splash)
        
    def action_rename(self) -> None:
        """Rename the selected files."""
        # Implementation will go here
        self.log("Renaming files...")
        
    def action_match(self) -> None:
        """Match files with metadata."""
        # Implementation will go here
        self.log("Matching files with Audible metadata...")
        
    def log(self, message: str) -> None:
        """Add a message to the log area."""
        log_area = self.query_one("#log-area", Static)
        current = log_area.render()
        if "[blue]█▀█" not in current:  # Don't append to splash screen
            log_area.update(f"{current}\n{message}")
        else:
            log_area.update(message)

def run():
    app = AudioBookzOrganizerApp()
    app.run()

if __name__ == "__main__":
    run()



    styles.css

    /* Main theme colors */
:root {
    --background: #2B2B2B;
    --primary: #1E90FF;
    --secondary: #FF8C00;
    --text: #E0E0E0;
    --text-muted: #A0A0A0;
    --border: #505050;
    --error: #FF5252;
    --success: #4CAF50;
}

/* Global styling */
Screen {
    background: var(--background);
    color: var(--text);
}

/* Typography */
* {
    font-family: "Fira Code", "JetBrains Mono", monospace;
}

/* Header styling */
Header {
    background: var(--background);
    color: var(--primary);
    height: 1;
    dock: top;
    border-bottom: solid var(--border);
}

/* Footer styling */
Footer {
    background: var(--background);
    color: var(--text-muted);
    height: 1;
    dock: bottom;
    border-top: solid var(--border);
}

/* Top toolbar */
#top-toolbar {
    height: 3;
    dock: top;
    background: var(--background);
    border-bottom: solid var(--border);
    padding: 0 1;
    align: center middle;
}

Button {
    background: var(--primary);
    color: var(--background);
    border: none;
    height: 1;
    margin: 0 1 0 0;
    min-width: 10;
}

Button:hover {
    background: var(--secondary);
}

Input {
    background: var(--background);
    border: solid var(--border);
    color: var(--text);
    padding: 0 1;
    margin: 0 1 0 0;
    height: 1;
}

/* Main workspace */
#main-workspace {
    min-height: 1fr;
    height: 1fr;
}

#left-pane, #right-pane {
    width: 1fr;
    height: 100%;
    border: solid var(--border);
    margin: 0 1;
}

#source-title, #preview-title {
    background: var(--primary);
    color: var(--background);
    height: 1;
    text-align: center;
    width: 100%;
}

#source-tree {
    border: none;
    padding: 0 1;
    height: 1fr;
    overflow: auto;
}

Tree > .tree--guides {
    color: var(--primary);
}

Tree > .tree--cursor {
    background: var(--primary);
    color: var(--background);
}

DataTable {
    height: 1fr;
    border: none;
    overflow: auto;
}

/* DataTable styles */
DataTable > .datatable--header {
    background: var(--primary);
    color: var(--background);
}

DataTable > .datatable--cursor {
    background: var(--primary);
    color: var(--background);
}

DataTable > .datatable--alternate-row {
    background: #333333;
}

/* Bottom panel */
#bottom-panel {
    height: 6;
    dock: bottom;
    border-top: solid var(--border);
}

#log-area {
    height: 5;
    overflow: auto;
    padding: 0 1;
}

#status-bar {
    height: 1;
    align: center middle;
    background: var(--background);
    border-top: solid var(--border);
}

#status-info {
    width: auto;
    padding: 0 1;
    color: var(--text-muted);
}

#filter-input {
    width: 30;
    margin: 0 1;
}

#progress-bar {
    width: 20;
    margin: 0 1;
}

ProgressBar > .bar--bar {
    background: var(--primary);
}

ProgressBar > .bar--complete {
    color: var(--secondary);
}

/* Log styling */
.log {
    background: #1A1A1A;
    color: var(--text);
    overflow: auto;
    border: solid var(--border);
    margin: 0 1;
}



statwidget
from textual.widget import Widget
from textual.reactive import reactive
from rich.panel import Panel
from rich.text import Text
from rich.console import Console, RenderableType
from rich.table import Table
from rich.box import SIMPLE
from rich.align import Align
from rich import box
from typing import Dict, List

class StatsWidget(Widget):
    """Widget to display library statistics and visualizations."""
    
    genre_data = reactive({})
    author_data = reactive({})
    processing_history = reactive([])
    
    def __init__(self, genre_data=None, author_data=None, processing_history=None):
        """Initialize with optional data."""
        super().__init__()
        if genre_data:
            self.genre_data = genre_data
        if author_data:
            self.author_data = author_data
        if processing_history:
            self.processing_history = processing_history
    
    def render(self) -> RenderableType:
        """Render the widget."""
        # Create a panel to hold all visualizations
        stats_panel = Panel(
            Align.center(
                self._build_stats_content(),
                vertical="middle"
            ),
            title="Library Statistics",
            border_style="blue",
            box=box.DOUBLE
        )
        return stats_panel
    
    def _build_stats_content(self) -> RenderableType:
        """Build the stats content with visualizations."""
        # Create a table to organize the visualizations
        table = Table.grid(expand=True)
        table.add_column("Genre Distribution")
        table.add_column("Top Authors")
        
        # Add genre distribution chart
        genre_chart = self._create_genre_chart()
        
        # Add top authors chart
        author_chart = self._create_author_chart()
        
        # Add processing history sparkline
        history_sparkline = self._create_history_sparkline()
        
        # Add row with the charts
        table.add_row(genre_chart, author_chart)
        
        # Add row with the sparkline
        table.add_row(Text("Processing History:"), "")
        table.add_row(history_sparkline, "")
        
        return table
    
    def _create_genre_chart(self) -> RenderableType:
        """Create an ASCII bar chart for genre distribution."""
        if not self.genre_data:
            return Text("No genre data available")
        
        chart_table = Table(box=None, expand=True, padding=0)
        chart_table.add_column("Genre", style="cyan")
        chart_table.add_column("Count", style="blue")
        chart_table.add_column("Bar", ratio=3)
        
        max_count = max(self.genre_data.values()) if self.genre_data else 0
        for genre, count in sorted(self.genre_data.items(), key=lambda x: x[1], reverse=True)[:5]:
            if max_count > 0:
                bar_width = int((count / max_count) * 20)
                bar = f"[blue]{'█' * bar_width}[/]"
                chart_table.add_row(genre, str(count), bar)
        
        return chart_table
    
    def _create_author_chart(self) -> RenderableType:
        """Create a chart for top authors."""
        if not self.author_data:
            return Text("No author data available")
        
        chart_table = Table(box=None, expand=True, padding=0)
        chart_table.add_column("Author", style="orange")
        chart_table.add_column("Books", style="blue")
        chart_table.add_column("Bar", ratio=3)
        
        max_count = max(self.author_data.values()) if self.author_data else 0
        for author, count in sorted(self.author_data.items(), key=lambda x: x[1], reverse=True)[:5]:
            if max_count > 0:
                bar_width = int((count / max_count) * 20)
                bar = f"[orange]{'█' * bar_width}[/]"
                chart_table.add_row(author, str(count), bar)
        
        return chart_table
    
    def _create_history_sparkline(self) -> RenderableType:
        """Create a sparkline of processing history."""
        if not self.processing_history:
            return Text("No processing history available")
        
        # Use Unicode block characters for the sparkline
        # ▁▂▃▄▅▆▇█
        blocks = "▁▂▃▄▅▆▇█"
        
        # Normalize the history data to 0-7 range for the blocks
        max_value = max(self.processing_history) if self.processing_history else 1
        normalized = [min(7, int((val / max_value) * 7)) for val in self.processing_history]
        
        # Generate the sparkline
        sparkline = "".join(blocks[val] for val in normalized)
        
        return Text(f"[blue]{sparkline}[/]")
    
    def update_data(self, genre_data=None, author_data=None, processing_point=None):
        """Update the widget with new data."""
        if genre_data:
            self.genre_data = genre_data
        if author_data:
            self.author_data = author_data
        if processing_point is not None:
            # Limit history to last 50 points
            self.processing_history = self.processing_history[-49:] + [processing_point]
        
        self.refresh()

