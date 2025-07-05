"""Logging and error reporting for audiobook organization."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional, TextIO
from datetime import datetime
import colorama
from colorama import Fore, Style


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages."""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA,
    }
    
    def format(self, record):
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


class AudioBookLogger:
    """Logger for audiobook organization operations."""
    
    def __init__(self, log_file: Optional[Path] = None, enable_colors: bool = True):
        """Initialize the logger.
        
        Parameters
        ----------
        log_file: Path | None
            Path to log file, if None only console logging is enabled
        enable_colors: bool
            Whether to enable colored console output
        """
        self.log_file = log_file
        self.enable_colors = enable_colors
        self.logger = logging.getLogger('audiobookz_organizer')
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Initialize colorama for Windows support
        if enable_colors:
            colorama.init()
        
        # Setup console handler
        self._setup_console_handler()
        
        # Setup file handler if log file is specified
        if log_file:
            self._setup_file_handler()
    
    def _setup_console_handler(self):
        """Setup console logging handler."""
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.WARNING)
        
        if self.enable_colors:
            formatter = ColoredFormatter(
                '%(levelname)s: %(message)s'
            )
        else:
            formatter = logging.Formatter(
                '%(levelname)s: %(message)s'
            )
        
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self):
        """Setup file logging handler."""
        if not self.log_file:
            return
        
        # Create log directory if it doesn't exist
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def log_operation_start(self, input_dir: Path, output_dir: Path, dry_run: bool):
        """Log the start of an organization operation."""
        mode = "DRY-RUN" if dry_run else "COMMIT"
        self.logger.info(f"Starting audiobook organization [{mode}]")
        self.logger.info(f"Input directory: {input_dir}")
        self.logger.info(f"Output directory: {output_dir}")
        self.logger.info("-" * 60)
    
    def log_operation_end(self, processed_count: int, dry_run: bool):
        """Log the end of an organization operation."""
        mode = "Dry run" if dry_run else "Operation"
        self.logger.info("-" * 60)
        self.logger.info(f"{mode} complete. {processed_count} folders processed.")
    
    def log_folder_processed(self, folder_path: Path, result: str):
        """Log a folder processing result."""
        if "ERROR" in result:
            self.logger.error(f"{folder_path.name}: {result}")
        elif "SKIPPED" in result:
            self.logger.warning(f"{folder_path.name}: {result}")
        elif "MOVED" in result or "DRY-RUN" in result:
            self.logger.info(f"{folder_path.name}: {result}")
        else:
            self.logger.debug(f"{folder_path.name}: {result}")
    
    def log_metadata_fetched(self, title: str, author: str, success: bool):
        """Log metadata fetching results."""
        if success:
            self.logger.debug(f"Metadata fetched for '{title}' by {author}")
        else:
            self.logger.warning(f"Failed to fetch metadata for '{title}' by {author}")
    
    def log_cache_hit(self, title: str, author: str):
        """Log cache hit."""
        self.logger.debug(f"Cache hit for '{title}' by {author}")
    
    def log_tag_update(self, file_path: Path, success: bool):
        """Log tag update results."""
        if success:
            self.logger.debug(f"Tags updated for {file_path.name}")
        else:
            self.logger.warning(f"Failed to update tags for {file_path.name}")
    
    def log_multipart_detection(self, folder_path: Path, is_multipart: bool):
        """Log multi-part audiobook detection."""
        status = "detected" if is_multipart else "not detected"
        self.logger.debug(f"Multi-part audiobook {status} in {folder_path.name}")
    
    def log_genre_inference(self, title: str, author: str, inferred_genre: str):
        """Log genre inference results."""
        if inferred_genre != "Unknown Genre":
            self.logger.debug(f"Inferred genre '{inferred_genre}' for '{title}' by {author}")
    
    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log an error message."""
        if exception:
            self.logger.error(f"{message}: {str(exception)}")
        else:
            self.logger.error(message)
    
    def log_warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
    
    def log_info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def log_debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)


# Global logger instance
_logger_instance: Optional[AudioBookLogger] = None


def get_logger() -> AudioBookLogger:
    """Get the global logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = AudioBookLogger()
    return _logger_instance


def setup_logger(log_file: Optional[Path] = None, enable_colors: bool = True):
    """Setup the global logger.
    
    Parameters
    ----------
    log_file: Path | None
        Path to log file
    enable_colors: bool
        Whether to enable colored console output
    """
    global _logger_instance
    _logger_instance = AudioBookLogger(log_file, enable_colors)