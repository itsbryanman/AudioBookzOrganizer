"""Terminal User Interface for audiobook organization."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import threading

from .models import Audiobook


class Status(Enum):
    """Status of an audiobook processing operation."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


@dataclass
class AudiobookEntry:
    """Represents an audiobook entry in the TUI."""
    audiobook: Audiobook
    status: Status = Status.PENDING
    message: str = ""
    target_path: Optional[Path] = None
    file_count: int = 0
    is_multipart: bool = False
    processing_time: float = 0.0


class SortBy(Enum):
    """Sorting options for the TUI."""
    FILENAME = "filename"
    STATUS = "status"
    AUTHOR = "author"
    TITLE = "title"
    GENRE = "genre"


class AudiobookTUI:
    """Advanced Terminal User Interface for audiobook organization."""
    
    def __init__(self, entries: List[AudiobookEntry], dry_run: bool = True):
        """Initialize the TUI.
        
        Parameters
        ----------
        entries: List[AudiobookEntry]
            List of audiobook entries to display
        dry_run: bool
            Whether this is a dry run or commit mode
        """
        self.entries = entries
        self.dry_run = dry_run
        self.sort_by = SortBy.FILENAME
        self.sort_reverse = False
        self.current_selection = 0
        self.scroll_offset = 0
        self.collapsed_groups: Dict[str, bool] = {}
        self.show_details = False
        self.terminal_height = self._get_terminal_height()
        self.terminal_width = self._get_terminal_width()
        self.start_time = time.time()
        self.processing_lock = threading.Lock()
        
    def _get_terminal_height(self) -> int:
        """Get terminal height."""
        try:
            return os.get_terminal_size().lines
        except OSError:
            return 24
    
    def _get_terminal_width(self) -> int:
        """Get terminal width."""
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80
    
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def _move_cursor_to(self, line: int, col: int):
        """Move cursor to specific position."""
        print(f"\033[{line};{col}H", end="")
    
    def _hide_cursor(self):
        """Hide terminal cursor."""
        print("\033[?25l", end="")
    
    def _show_cursor(self):
        """Show terminal cursor."""
        print("\033[?25h", end="")
    
    def _get_status_symbol(self, status: Status) -> str:
        """Get symbol for status."""
        symbols = {
            Status.PENDING: "⏳",
            Status.PROCESSING: "🔄",
            Status.COMPLETED: "✅",
            Status.SKIPPED: "⚠️",
            Status.ERROR: "❌"
        }
        return symbols.get(status, "❓")
    
    def _get_status_color(self, status: Status) -> str:
        """Get ANSI color code for status."""
        colors = {
            Status.PENDING: "\033[37m",      # White
            Status.PROCESSING: "\033[33m",   # Yellow
            Status.COMPLETED: "\033[32m",    # Green
            Status.SKIPPED: "\033[93m",      # Bright Yellow
            Status.ERROR: "\033[31m"         # Red
        }
        return colors.get(status, "\033[37m")
    
    def _reset_color(self) -> str:
        """Get ANSI reset color code."""
        return "\033[0m"
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to fit within max_length."""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _sort_entries(self):
        """Sort entries based on current sort criteria."""
        if self.sort_by == SortBy.FILENAME:
            self.entries.sort(key=lambda e: e.audiobook.source_path.name, reverse=self.sort_reverse)
        elif self.sort_by == SortBy.STATUS:
            self.entries.sort(key=lambda e: e.status.value, reverse=self.sort_reverse)
        elif self.sort_by == SortBy.AUTHOR:
            self.entries.sort(key=lambda e: e.audiobook.author, reverse=self.sort_reverse)
        elif self.sort_by == SortBy.TITLE:
            self.entries.sort(key=lambda e: e.audiobook.title, reverse=self.sort_reverse)
        elif self.sort_by == SortBy.GENRE:
            self.entries.sort(key=lambda e: e.audiobook.genre, reverse=self.sort_reverse)
    
    def _render_header(self):
        """Render the header section."""
        mode = "PREVIEW" if self.dry_run else "COMMIT"
        title = f"📚 AudioBookCleanr [{mode}]"
        print("┌" + "─" * (self.terminal_width - 2) + "┐")
        print(f"│{title:^{self.terminal_width - 2}}│")
        print("├" + "─" * (self.terminal_width - 2) + "┤")
        
        # Status counts
        status_counts = {}
        for entry in self.entries:
            status_counts[entry.status] = status_counts.get(entry.status, 0) + 1
        
        total = len(self.entries)
        completed = status_counts.get(Status.COMPLETED, 0)
        skipped = status_counts.get(Status.SKIPPED, 0)
        errors = status_counts.get(Status.ERROR, 0)
        
        status_line = f"Total: {total} | Completed: {completed} | Skipped: {skipped} | Errors: {errors}"
        print(f"│ {status_line:<{self.terminal_width - 3}}│")
        
        # Runtime
        runtime = time.time() - self.start_time
        runtime_str = f"Runtime: {runtime:.1f}s"
        sort_str = f"Sort: {self.sort_by.value} {'↓' if self.sort_reverse else '↑'}"
        info_line = f"{runtime_str} | {sort_str}"
        print(f"│ {info_line:<{self.terminal_width - 3}}│")
        
        print("├" + "─" * (self.terminal_width - 2) + "┤")
    
    def _render_table_header(self):
        """Render the table header."""
        header = "│ STATUS │ SOURCE PATH                    │ DESTINATION PATH                    │"
        print(header[:self.terminal_width - 1] + "│")
        print("├" + "─" * (self.terminal_width - 2) + "┤")
    
    def _render_entry(self, entry: AudiobookEntry, is_selected: bool = False):
        """Render a single entry."""
        status_symbol = self._get_status_symbol(entry.status)
        status_color = self._get_status_color(entry.status)
        reset_color = self._reset_color()
        
        # Truncate paths to fit
        source_path = self._truncate_text(str(entry.audiobook.source_path.name), 30)
        if entry.target_path:
            dest_path = self._truncate_text(str(entry.target_path), 35)
        else:
            dest_path = "(calculating...)"
        
        # Selection indicator
        selection_mark = "►" if is_selected else " "
        
        # Multi-part indicator
        multipart_indicator = "📁" if entry.is_multipart else "📄"
        
        line = f"│{selection_mark}{status_color}{status_symbol}{reset_color} {multipart_indicator} │ {source_path:<28} │ {dest_path:<33} │"
        print(line[:self.terminal_width - 1] + "│")
    
    def _render_entries(self):
        """Render all visible entries."""
        visible_height = self.terminal_height - 10  # Account for header, footer, etc.
        
        for i in range(visible_height):
            entry_index = self.scroll_offset + i
            if entry_index >= len(self.entries):
                break
                
            entry = self.entries[entry_index]
            is_selected = entry_index == self.current_selection
            self._render_entry(entry, is_selected)
    
    def _render_footer(self):
        """Render the footer with controls."""
        print("└" + "─" * (self.terminal_width - 2) + "┘")
        
        controls = [
            "[↑/↓] Navigate",
            "[S] Sort",
            "[SPACE] Select",
            "[ENTER] Details",
            "[C] Commit" if self.dry_run else "[A] Abort",
            "[Q] Quit"
        ]
        
        controls_line = " | ".join(controls)
        print(f" {controls_line}")
    
    def _render_details(self, entry: AudiobookEntry):
        """Render detailed view of an entry."""
        self._clear_screen()
        
        print("┌" + "─" * (self.terminal_width - 2) + "┐")
        print(f"│{'📚 Audiobook Details':^{self.terminal_width - 2}}│")
        print("├" + "─" * (self.terminal_width - 2) + "┤")
        
        details = [
            f"Title: {entry.audiobook.title}",
            f"Author: {entry.audiobook.author}",
            f"Genre: {entry.audiobook.genre}",
            f"Year: {entry.audiobook.year}",
            f"Source: {entry.audiobook.source_path}",
            f"Target: {entry.target_path or 'Not calculated'}",
            f"Status: {entry.status.value}",
            f"Multi-part: {'Yes' if entry.is_multipart else 'No'}",
            f"File count: {entry.file_count}",
            f"Processing time: {entry.processing_time:.2f}s",
            f"Message: {entry.message}"
        ]
        
        for detail in details:
            print(f"│ {detail:<{self.terminal_width - 3}}│")
        
        print("└" + "─" * (self.terminal_width - 2) + "┘")
        print("\nPress any key to return...")
        
        # Wait for key press
        try:
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.cbreak(fd)
            sys.stdin.read(1)
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except ImportError:
            input()  # Fallback for Windows
    
    def render(self):
        """Render the entire TUI."""
        self._clear_screen()
        self._hide_cursor()
        
        try:
            self._sort_entries()
            self._render_header()
            self._render_table_header()
            self._render_entries()
            self._render_footer()
        finally:
            self._show_cursor()
    
    def handle_input(self) -> str:
        """Handle user input and return action."""
        try:
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.cbreak(fd)
            
            while True:
                ch = sys.stdin.read(1)
                
                if ch == '\x1b':  # ESC sequence
                    next_ch = sys.stdin.read(1)
                    if next_ch == '[':
                        arrow_key = sys.stdin.read(1)
                        if arrow_key == 'A':  # Up arrow
                            self.current_selection = max(0, self.current_selection - 1)
                            self._adjust_scroll()
                        elif arrow_key == 'B':  # Down arrow
                            self.current_selection = min(len(self.entries) - 1, self.current_selection + 1)
                            self._adjust_scroll()
                elif ch.lower() == 'q':
                    return 'quit'
                elif ch.lower() == 'c':
                    return 'commit'
                elif ch.lower() == 'a':
                    return 'abort'
                elif ch.lower() == 's':
                    self._cycle_sort()
                elif ch == ' ':
                    return 'select'
                elif ch == '\r' or ch == '\n':
                    if self.current_selection < len(self.entries):
                        self._render_details(self.entries[self.current_selection])
                    
                self.render()
                
        except ImportError:
            # Fallback for Windows
            return input("Enter command (q/c/a): ").strip().lower()
        finally:
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass
    
    def _adjust_scroll(self):
        """Adjust scroll offset based on current selection."""
        visible_height = self.terminal_height - 10
        
        if self.current_selection < self.scroll_offset:
            self.scroll_offset = self.current_selection
        elif self.current_selection >= self.scroll_offset + visible_height:
            self.scroll_offset = self.current_selection - visible_height + 1
    
    def _cycle_sort(self):
        """Cycle through sort options."""
        sort_options = list(SortBy)
        current_index = sort_options.index(self.sort_by)
        
        if current_index == len(sort_options) - 1:
            self.sort_by = sort_options[0]
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_by = sort_options[current_index + 1]
    
    def update_entry(self, index: int, status: Status, message: str = "", target_path: Optional[Path] = None):
        """Update an entry's status and message."""
        with self.processing_lock:
            if 0 <= index < len(self.entries):
                self.entries[index].status = status
                self.entries[index].message = message
                if target_path:
                    self.entries[index].target_path = target_path
    
    def run(self) -> str:
        """Run the TUI and return the user's final choice."""
        self.render()
        
        while True:
            action = self.handle_input()
            
            if action == 'quit':
                return 'quit'
            elif action == 'commit':
                return 'commit'
            elif action == 'abort':
                return 'abort'


def create_audiobook_entries(audiobooks: List[Audiobook]) -> List[AudiobookEntry]:
    """Create TUI entries from audiobook list."""
    entries = []
    
    for audiobook in audiobooks:
        # Count files in the audiobook folder
        file_count = 0
        is_multipart = False
        
        try:
            for item in audiobook.source_path.rglob("*"):
                if item.is_file():
                    file_count += 1
                    if file_count > 1:
                        is_multipart = True
        except:
            file_count = 0
        
        entry = AudiobookEntry(
            audiobook=audiobook,
            file_count=file_count,
            is_multipart=is_multipart
        )
        entries.append(entry)
    
    return entries